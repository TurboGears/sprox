"""
fillerbase Module

Classes to help fill widgets with data

Copyright (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""

from sprox.fillerbase import TableFiller

class DojoTableFiller(TableFiller):

    def get_value(self, value, **kw):
        offset = kw.get('start', None)
        limit  = kw.get('count', None)
        items = super(DojoTableFiller, self).get_value(value, limit=limit, offset=offset)
        count = self.get_count()
        identifier = self.__provider__.get_primary_field(self.__entity__)
        return dict(identifier=identifier, numRows=count, items=items)

