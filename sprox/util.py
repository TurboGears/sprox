"""
util Module

this contains the class which allows dbsprockets to interface with sqlalchemy.

Classes:
Name                               Description
MultiDict                          A class that allows dicts with multiple keys of the same value

Exceptions:
None

Functions:
None


Copyright (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""

from copy import deepcopy, copy

class MultiDict(dict):
    def __setitem__(self, key, value):
        self.setdefault(key, []).append(value)

    def iteritems(self):
        for key in self:
            values = dict.__getitem__(self, key)
            for value in values:
                yield (key, value)
