from configbase import ConfigBase, ConfigBaseError
from metadata import FieldsMetadata
from genshi import XML

class FillerBase(ConfigBase):
    def get_value(self, values=None, offset=None, limit=None):
        if values is None:
            values = {}
        return values

class ModelsFiller(FillerBase):
    pass
class ModelDefFiller(FillerBase):
    pass

class FormFiller(FillerBase):
    __metadata_type__ = FieldsMetadata

    def get_value(self, values=None, offset=None, limit=None):
        values = super(FormFiller, self).get_value(values, offset, limit)
        values['sprox_id'] =  self.__id__
        return values

class TableFiller(FillerBase):
    __metadata_type__ = FieldsMetadata
    __possible_field_names__ = ['_name', 'name', 'description', 'title']

    def _get_list_data_value(self, field, values):
        l = []
        for value in values:
            name = self.__provider__.get_view_column_name(value.__class__, self.__possible_field_names__)
            l.append(str(getattr(value, name)))
        return ','.join(l)

    def _get_relation_value(self, field, value):
        if value is None:
            return None
        name = self.__provider__.get_view_column_name(value.__class__, self.__possible_field_names__)
        return getattr(value, name)

    def get_value(self, values=None, offset=None, limit=None):
        query = self.__provider__.session.query(self.__entity__)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit()
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
                elif self.__provider__.is_relation(self.__entity__, field):
                    value = self._get_relation_value(field, value)
                row[field] = unicode(value)
            rows.append(row)
        return rows

class EditFormFiller(FormFiller):
    def get_value(self, values=None, offset=None, limit=None):
        values = super(EditFormFiller, self).get_value(values, offset, limit)
        values = self.__provider__.get(self.__entity__, params=values)
        return values

class AddFormFiller(FormFiller):
    def get_value(self, values=None, offset=None, limit=None):
        kw = super(AddFormFiller, self).get_value(values, offset, limit)
        return self.__provider__.get_default_values(self.__entity__, params=values)
