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

from collections import Iterable

try:
    import simplejson as json
    from simplejson import JSONDecodeError
except ImportError:  # pragma: no cover
    import json
    JSONDecodeError = ValueError


class JSONUnpacker(Iterable):
    def __init__(self):
        self.buff = ""

    def feed(self, data):
        self.buff += data

    def __iter__(self):
        return self

    def next(self):
        js = json.JSONDecoder()
        try:
            res, index = js.raw_decode(self.buff)
            self.buff = self.buff[index:].lstrip('\r\n')
            return res
        except JSONDecodeError:
            raise StopIteration
