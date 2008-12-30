"""
fillerbase Module

Classes to help fill widgets with data

Copyright (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""

from configbase import ConfigBase, ConfigBaseError
from metadata import FieldsMetadata
from genshi import XML

class FillerBase(ConfigBase):
    """
    :Modifiers:

    see :mod:`sprox.configbase`.

    The base filler class.

        :Arguments:
          values
            pass through of values.  This is typically a set of default values that is updated by the
            filler.  This is useful when updating an existing form.
          kw
            Set of keyword arguments for assisting the fill.  This is for instance information like offset
            and limit for a TableFiller.

        :Usage:

        >>> filler = FillerBase()
        >>> filler.get_value()
        {}
    """

    def get_value(self, values=None, **kw):
        """
        The main function for getting data to fill widgets,
        """
        if values is None:
            values = {}
        return values

class ModelsFiller(FillerBase):
    pass
class ModelDefFiller(FillerBase):
    pass

class FormFiller(FillerBase):
    __metadata_type__ = FieldsMetadata

    def get_value(self, values=None, **kw):
        values = super(FormFiller, self).get_value(values)
        values['sprox_id'] =  self.__sprox_id__
        return values

class TableFiller(FillerBase):
    """
    This is the base class for generating table data for use in table widgets.

    This class will automatically parse relations and choose values for the related items to dispay based
    on the __possible_field_names_modifier__ .

    Here is how we would get the values to fill up a user's table.

    >>> from sprox.test.base import User, setup_database, setup_records
    >>> session, engine, metadata = setup_database()
    >>> user = setup_records(session)
    >>> class UsersFiller(TableFiller):
    ...     __model__ = User
    >>> users_filler = UsersFiller(session)
    >>> value = users_filler.get_value(values={}, limit=20, offset=0)
    >>> value # doctest: +SKIP
    [{'town': u'Arvada', 'user_id': u'1', 'created': u'2008-12-28 17:33:11.078931',
      'user_name': u'asdf', 'town_id': u'1', 'groups': u'4', '_password': '******',
      'password': '******', 'email_address': u'asdf@asdf.com', 'display_name': u'None'}]
    >>> session.rollback()
    """
    __metadata_type__ = FieldsMetadata
    __possible_field_names__ = ['_name', 'name', 'description', 'title']


    def _get_list_data_value(self, field, values):
        l = []
        for value in values:
            name = self.__provider__.get_view_field_name(value.__class__, self.__possible_field_names__)
            l.append(str(getattr(value, name)))
        return ','.join(l)

    def _get_relation_value(self, field, value):
        #this may be needed for catwalk, but I am not sure what conditions cause it to be needed
        #if value is None:
        #    return None
        name = self.__provider__.get_view_field_name(value.__class__, self.__possible_field_names__)
        return getattr(value, name)

    def get_value(self, values=None, **kw):
        """
        Get the values to fill a form widget.

        :Arguments:
         offset
          offset into the records
         limit
          number of records to return

        """
        limit = kw.get('limit', None)
        offset = kw.get('offset', None)
        query = self.__provider__.session.query(self.__entity__)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        objs = query.all()
        rows = []
        for obj in objs:
            row = {}
            for field in self.__fields__:
                value = getattr(obj, field)
                if 'password' in field.lower():
                    row[field] = '******'
                    continue
                if isinstance(value, list):
                    value = self._get_list_data_value(field, value)
                elif self.__provider__.is_relation(self.__entity__, field) and value is not None:
                    value = self._get_relation_value(field, value)
                elif self.__provider__.is_binary(self.__entity__, field) and value is not None:
                    value = '<file>'
                row[field] = unicode(value)
            rows.append(row)
        return rows

class EditFormFiller(FormFiller):
    def get_value(self, values=None, **kw):
        values = super(EditFormFiller, self).get_value(values, **kw)
        values = self.__provider__.get(self.__entity__, params=values)
        return values

class RecordFiller(EditFormFiller):pass


class AddFormFiller(FormFiller):
    def get_value(self, values=None, **kw):
        """xxx: get the server/entity defaults."""
        kw = super(AddFormFiller, self).get_value(values, **kw)
        return self.__provider__.get_default_values(self.__entity__, params=values)