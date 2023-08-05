#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  wsgi.py
#
#  Copyright 2014 James Hulett <james.hulett@cuanswers.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from compysition import Actor
from compysition.errors import InvalidEventDataModification, MalformedEventData, ResourceNotFound
from compysition.event import HttpEvent, JSONHttpEvent, XMLHttpEvent
from gevent import pywsgi
import json
from functools import wraps
from collections import defaultdict
from gevent.queue import Queue
from bottle import *
import re
import time
import mimeparse
from datetime import datetime

BaseRequest.MEMFILE_MAX = 1024 * 1024 # (or whatever you want)


class ContentTypePlugin(object):
    """**Bottle plugin that filters basic content types that are processable by Compysition**"""

    DEFAULT_VALID_TYPES = ("text/xml",
                           "application/xml",
                           "text/plain",
                           "text/html",
                           "application/json",
                           "application/x-www-form-urlencoded")

    name = "ctypes"
    api = 2

    def __init__(self, default_types=None):
        self.default_types = default_types or self.DEFAULT_VALID_TYPES

    def apply(self, callback, route):
        ctype = request.content_type.split(';')[0]
        ignore_ctype = route.config.get('ignore_ctype', False) or request.content_length < 1
        if ignore_ctype or ctype in route.config.get('ctypes', self.default_types):
            return callback
        else:
            raise HTTPError(415, "Unsupported Content-Type '{_type}'".format(_type=ctype))


class HTTPServer(Actor, Bottle):
    """**Receive events over HTTP.**

    Actor runs a pywsgi gevent webserver, using an optional routes json file for complex routing using Bottle

    Parameters:
        name (str):
            | The instance name.
        address(Optional[str]):
            | The address to bind to.
            | Default: 0.0.0.0
        port(Optional[int]):
            | The port to bind to.
            | Default: 8080
        keyfile(Optional([str]):
            | In case of SSL the location of the keyfile to use.
            | Default: None
        certfile(Optional[str]):
            | In case of SSL the location of the certfile to use.
            | Default: None
        routes_config(Optional[dict]):
            | This is a JSON object that contains a list of Bottle route config kwargs
            | Default: {"routes": [{"path: "/<queue>", "method": ["POST"]}]}
            | Field values correspond to values used in bottle.Route class
            | Special values:
            |    id(Optional[str]): Used to identify this route in the json object
            |    base_path(Optional[str]): Used to identify a route that this route extends, using the referenced id

    Examples:
        Default:
            http://localhost:8080/foo is mapped to 'foo' queue
            http://localhost:8080/bar is mapped to 'bar' queue
        routes_config:
            routes_config {"routes": [{"path: "/my/url/<queue>", "method": ["POST"]}]}
                http://localhost:8080/my/url/goodtimes is mapped to 'goodtimes' queue


    """

    DEFAULT_ROUTE = {
        "routes":
            [
                {
                    "id": "base",
                    "path": "/<queue>",
                    "method": [
                        "POST"
                    ]
                }
            ]
    }

    input = HttpEvent
    output = HttpEvent

    QUEUE_REGEX = re.compile("<queue:re:[a-zA-Z_0-9]+?>")

    # Order matters, as this is used to resolve the returned content type preserved in the accept header, in order of increasing preference.
    _TYPES_MAP = [('application/xml+schema', XMLHttpEvent),
                  ('application/json+schema', JSONHttpEvent),
                  ('*/*', HttpEvent),
                  ('text/plain', HttpEvent),
                  ('text/html', XMLHttpEvent),
                  ('text/xml', XMLHttpEvent),
                  ('application/xml', XMLHttpEvent),
                  ('application/json', JSONHttpEvent)]
    CONTENT_TYPES = [_type[0] for _type in _TYPES_MAP]
    CONTENT_TYPE_MAP = defaultdict(lambda: JSONHttpEvent,
                                   _TYPES_MAP)

    X_WWW_FORM_URLENCODED_KEY_MAP = defaultdict(lambda: HttpEvent, {"XML": XMLHttpEvent, "JSON": JSONHttpEvent})
    X_WWW_FORM_URLENCODED = "application/x-www-form-urlencoded"

    def combine_base_paths(self, route, named_routes):
        base_path_id = route.get('base_path', None)
        if base_path_id:
            base_path = named_routes.get(base_path_id, None)
            if base_path:
                return HTTPServer._normalize_queue_definition(self.combine_base_paths(base_path, named_routes) + route['path'])
            else:
                raise KeyError("Base path '{base_path}' doesn't reference a defined path ID".format(base_path=base_path_id))
        else:
            return route.get('path')


    @staticmethod
    def _parse_queue_variables(path):
        return HTTPServer.QUEUE_REGEX.findall(path)

    @staticmethod
    def _parse_queue_names(path):
        path_variables = HTTPServer._parse_queue_variables(path)
        path_names = [s.replace("<queue:re:", '')[:-1] for s in path_variables]

        return path_names

    @staticmethod
    def _normalize_queue_definition(path):
        """
        This method is used to filter the queue variable in a path, to support the idea of base paths with multiple queue
        definitions. In effect, the <queue> variable in a path is provided at the HIGHEST level of definition. AKA: A higher
        level route containing a <queue:re:foo> will override the definition of <queue:re:bar> in a base_path.

        e.g. /<queue:re:foo>/<queue:re:bar> -> /foo/<queue:re:bar>

        This ONLY works for SIMPLE regex cases, which should be the case anyway for the queue name.
        """

        path_variables = HTTPServer._parse_queue_variables(path)
        path_names = HTTPServer._parse_queue_names(path)

        for path_variable in path_variables[:-1]:
            path = path.replace(path_variable, path_names.pop(0))

        return path

    def __init__(self, name, address="0.0.0.0", port=8080, keyfile=None, certfile=None, routes_config=None, *args, **kwargs):
        Actor.__init__(self, name, *args, **kwargs)
        Bottle.__init__(self)
        self.blockdiag_config["shape"] = "cloud"
        self.address = address
        self.port = port
        self.keyfile = keyfile
        self.certfile = certfile
        self.responders = {}
        routes_config = routes_config or self.DEFAULT_ROUTE

        if isinstance(routes_config, str):
            routes_config = json.loads(routes_config)

        if isinstance(routes_config, dict):
            named_routes = {route['id']:{'path': route['path'], 'base_path': route.get('base_path', None)} for route in routes_config.get('routes') if route.get('id', None)}
            for route in routes_config.get('routes'):
                callback = getattr(self, route.get('callback', 'callback'))
                if route.get('base_path', None):
                    route['path'] = self.combine_base_paths(route, named_routes)

                if not route.get('method', None):
                    route['method'] = []

                self.logger.debug("Configured route '{path}' with methods '{methods}'".format(path=route['path'], methods=route['method']))
                self.route(callback=callback, **route)

        self.wsgi_app = self
        self.wsgi_app.install(self.log_to_logger)
        self.wsgi_app.install(ContentTypePlugin())

    def log_to_logger(self, fn):
        '''
        Wrap a Bottle request so that a log line is emitted after it's handled.
        '''
        @wraps(fn)
        def _log_to_logger(*args, **kwargs):
            self.logger.info('[{address}] {method} {url}'.format(address=request.remote_addr,
                                            method=request.method,
                                            url=request.url))
            actual_response = fn(*args, **kwargs)
            return actual_response
        return _log_to_logger

    def __call__(self, e, h):
        """**Override Bottle.__call__ to strip trailing slash from incoming requests**"""

        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return Bottle.__call__(self, e, h)

    def format_response_data(self, event):
        """
        Meant to return a json response nested under a data tag if it isn't already done so, or return formatted
        errors under the "errors" tag.
        """
        if event.error:
            if isinstance(event, JSONHttpEvent):
                response_data = json.dumps({"errors": event.format_error()})
            else:
                response_data = event.error_string()
        else:
            if not isinstance(event.data, (list, dict, str)) or \
                    (isinstance(event.data, dict) and len(event.data) == 1 and event.data.get("data", None)):
                response_data = event.data_string()
            else:
                response_data = json.dumps({"data": event.data})

        return response_data

    def consume(self, event, *args, **kwargs):
        # There is an error that results in responding with an empty list that will cause an internal server error

        original_event_class, response_queue = self.responders.pop(event.event_id, None)

        if response_queue:

            accept = event.get('accept', original_event_class.content_type)

            if not isinstance(event, self.CONTENT_TYPE_MAP[accept]):
                self.logger.warning(
                    "Incoming event did did not match the clients Accept format. Converting '{current}' to '{new}'".format(
                        current=type(event), new=original_event_class.__name__))
                event = event.convert(self.CONTENT_TYPE_MAP[accept])

            local_response = HTTPResponse()
            status, status_message = event.status
            local_response.status = "{code} {message}".format(code=status, message=status_message)

            for header in event.headers.keys():
                local_response.set_header(header, event.headers[header])

            local_response.set_header("Content-Type", event.content_type)

            if int(status) == 204:
                response_data = ""
            else:
                response_data = self.format_response_data(event)

            local_response.body = response_data

            response_queue.put(local_response)
            response_queue.put(StopIteration)
            self.logger.info("[{status}] Returned in {time} ms".format(status=local_response.status, time=(datetime.now()-event.created).microseconds / 1000), event=event)
        else:
            self.logger.warning("Received event response for an unknown event ID. The request might have already received a response", event=event)

    def _format_bottle_env(self, environ):
        """**Filters incoming bottle environment of non-serializable objects, and adds useful shortcuts**"""

        query_string_data = {}
        for key in environ["bottle.request"].query.iterkeys():
            query_string_data[key] = environ["bottle.request"].query.get(key)

        environ = {key: environ[key] for key in environ.keys() if isinstance(environ[key], (str, tuple, bool, dict))}
        environ['QUERY_STRING_DATA'] = query_string_data

        return environ

    def callback(self, queue=None, *args, **kwargs):
        queue_name = queue or self.name
        queue = self.pool.outbound.get(queue_name, None)
        ctype = request.content_type.split(';')[0]

        accept_header = request.headers.get("Accept", "*/*")
        try:
            accept = mimeparse.best_match(self.CONTENT_TYPES, accept_header)
        except ValueError:
            accept = "*/*"
            self.logger.warning("Invalid mimetype defined in client Accepts header. '{accept}' is not a valid mime type".format(accept=accept_header))

        if request.method in ["GET", "OPTIONS", "HEAD", "DELETE"]:
            for accept_type in accept_header:
                if accept_type in self.CONTENT_TYPE_MAP.keys():
                    pass

        if ctype == '':
            ctype = None

        try:
            event_class = None
            data = None
            environment = self._format_bottle_env(request.environ)

            if not queue:
                self.logger.error("Received {method} request with URL '{url}'. Queue name '{queue_name}' was not found".format(method=request.method,
                                                                                                                           url=request.path,
                                                                                                                           queue_name=queue_name))
                raise ResourceNotFound("Service '{0}' not found".format(queue_name))

            if ctype == self.X_WWW_FORM_URLENCODED:
                if len(request.forms.items()) < 1:
                    raise MalformedEventData("Mismatched content type")
                else:
                    for item in request.forms.items():
                        event_class, data = self.X_WWW_FORM_URLENCODED_KEY_MAP[item[0]], item[1]
                        break
            else:
                event_class = self.CONTENT_TYPE_MAP[ctype]
                try:
                    data = request.body.read()
                except:
                    # A body is not required
                    data = None

            if data == '':
                data = None

            event = event_class(environment=environment, service=queue_name, data=data, accept=accept, **kwargs)

        except (ResourceNotFound, InvalidEventDataModification, MalformedEventData) as err:
            event_class = event_class or JSONHttpEvent
            event = event_class(environment=environment, service=queue_name, accept=accept, **kwargs)
            event.error = err
            queue = self.pool.inbound[self.pool.inbound.keys()[0]]

        response_queue = Queue()
        self.responders.update({event.event_id: (event_class, response_queue)})
        local_response = response_queue
        self.logger.info("Received {0} request for service {1}".format(request.method, queue_name), event=event)
        self.send_event(event, queues=[queue])

        return local_response

    def post_hook(self):
        self.__server.stop()
        self.logger.info("Stopped serving")

    def __serve(self):
        if self.keyfile is not None and self.certfile is not None:
            self.__server = pywsgi.WSGIServer((self.address, self.port), self, keyfile=self.keyfile, certfile=self.certfile)
        else:
            self.__server = pywsgi.WSGIServer((self.address, self.port), self, log=None)
        self.logger.info("Serving on {address}:{port}".format(address=self.address, port=self.port))
        self.__server.start()

    def pre_hook(self):
        self.__serve()