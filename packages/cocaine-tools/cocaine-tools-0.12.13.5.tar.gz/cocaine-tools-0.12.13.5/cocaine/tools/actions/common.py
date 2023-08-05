#
# Copyright (c) 2013+ Anton Tyurin <noxiouz@yandex.ru>
# Copyright (c) 2013+ Evgeny Safronov <division494@gmail.com>
# Copyright (c) 2011-2014 Other contributors as noted in the AUTHORS file.
#
# This file is part of Cocaine-tools.
#
# Cocaine is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cocaine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import division

from collections import defaultdict
import datetime
import json
import fnmatch
import os
import time
import socket

from tornado import gen

from cocaine.decorators import coroutine
from cocaine.tools.error import ToolsError
from . import mql

__author__ = 'Evgeny Safronov <division494@gmail.com>'


def split_by_groups(items, split_by=10):
    return (items[i - split_by:i] for i in xrange(split_by, len(items) + split_by, split_by))


class Node(object):
    def __init__(self, node=None):
        self.node = node

    @coroutine
    def execute(self):
        raise NotImplementedError()


class Locate(object):
    def __init__(self, locator, name):
        self.locator = locator
        if not name:
            raise ValueError("option `name` must be specified")
        self.name = name

    @coroutine
    def execute(self):
        channel = yield self.locator.resolve(self.name)
        endpoints, version, api = yield channel.rx.get()
        result = {
            "endpoints": ["%s:%d" % (addr, port) for addr, port in endpoints],
            "version": version,
            "api": dict((num, method[0]) for num, method in api.items())
        }
        raise gen.Return(result)


class Cluster(object):
    def __init__(self, locator, resolve=True):
        self.locator = locator
        self.resolve = resolve

    @coroutine
    def execute(self):
        channel = yield self.locator.cluster()
        result = yield channel.rx.get()
        if self.resolve:
            raise gen.Return(result)

        converted_result = {}
        for uuid, (addr, port) in result.items():
            try:
                host = socket.gethostbyaddr(addr)[0]
                converted_result[uuid] = [host, port]
            except (socket.gaierror, IOError):
                converted_result[uuid] = [addr, port]

        raise gen.Return(converted_result)


class Routing(object):
    extent = pow(2, 32)

    def __init__(self, locator, name=None):
        self.locator = locator
        self.name = name

    def generate_group(self, body):
        if len(body) == 0:
            return {}
        apps = defaultdict(int)
        # initialize with maximum value
        # from the routing
        prev = body[-1][0] - Routing.extent
        for value, app in body:
            apps[app] += (value - prev)
            prev = value

        output = dict((a, w / Routing.extent) for a, w in apps.items())
        return output

    @coroutine
    def execute(self):
        uid = "tools:%s_%d_%f" % (socket.gethostname(), os.getpid(), time.time())
        channel = yield self.locator.routing(uid, True)
        rings = yield channel.rx.get()
        groups = {}
        if not self.name:
            for name, ring in rings.items():
                groups[name] = self.generate_group(ring)
        elif self.name in rings:
            groups[self.name] = self.generate_group(rings[self.name])
        else:
            raise ToolsError("No such group `%s` in the routing. "
                             "Probably you should refresh the locator" % self.name)

        raise gen.Return(groups)


class RuntimeMetrics(object):
    def __init__(self, ty, query, query_type, metrics):
        self._ty = ty
        if query is not None:
            if query_type == 'ast':
                self._query = json.loads(query)
            else:
                self._query = mql.compile_query(query)
        else:
            self._query = None
        self._metrics = metrics

    @coroutine
    def execute(self):
        channel = yield self._metrics.fetch(self._ty, self._query)
        metrics = yield channel.rx.get()
        raise gen.Return(metrics)


class NodeInfo(Node):
    def __init__(self, node, locator,
                 name=None, flags=0x1,
                 use_wildcard=False,
                 timeout=5):
        super(NodeInfo, self).__init__(node)
        self.locator = locator
        self._name = name
        self._flags = flags
        self._use_wildcard = use_wildcard
        self.timeout = datetime.timedelta(seconds=timeout)
        self.on_timeout_reply = {
            "error": "info was timed out",
            "state": "unresponsive",
            "meta": "the error was generated by tools"
        }

    @coroutine
    def execute(self):
        # name is provided and wildcard is switched off
        # so we use exact match
        if self._name and not self._use_wildcard:
            apps = [self._name]
        else:
            channel = yield self.node.list()
            apps = yield channel.rx.get()
            # wildcard has been already checked
            if self._name:
                apps = fnmatch.filter(apps, self._name)

        result = yield self.info(apps)
        raise gen.Return(result)

    @coroutine
    def info(self, apps):
        infos = {}
        for names in split_by_groups(apps, 25):
            futures = {}
            for app in names:
                res_future = (yield self.node.info(app, self._flags)).rx.get()
                futures[app] = gen.with_timeout(self.timeout, res_future)

            wait_iterator = gen.WaitIterator(**futures)
            while not wait_iterator.done():
                try:
                    info = yield wait_iterator.next()
                    infos[wait_iterator.current_index] = info
                except gen.TimeoutError:
                    infos[wait_iterator.current_index] = self.on_timeout_reply
                except Exception as err:
                    infos[wait_iterator.current_index] = str(err)

        result = {
            'apps': infos,
            'count': len(infos),
        }
        raise gen.Return(result)
