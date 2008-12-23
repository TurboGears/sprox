"""
matadata Module

this contains the class which definies the generic interface for metadata
that is used in form generation later in the pipeline

Classes:
Name                               Description
Metadata                           general metadata function
DatabaseMetadata                   describes the fields as entries in the dictionary
FieldsMetadata                     describes the columns as entries in the dictionary
FieldMetadata                      generic type this is not used right now.

Exceptions:
MetadataError

Functions:
None

Copyright (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
from sprox.iprovider import IProvider

class MetadataError(Exception):pass
class NotFoundError(Exception):pass

class Metadata(dict):
    """
    """
    def __init__(self, provider, entity=None):
        if not isinstance(provider, IProvider):
            raise TypeError('provider must be of type IProvider not %s'%type(provider))
        self.provider = provider
        self.entity = entity

    def __setitem__(self, key, value):
        self._do_check_set_item(key, value)
        dict.__setitem__(self, key, value)

    def __getitem__(self, item):
        try:
            value = self._do_get_item(item)
            return value
        except NotFoundError:
            return dict.__getitem__(self, item)

    def keys(self):
        r = self._do_keys()
        r.extend(dict.keys(self))
        return r

class EntitiesMetadata(Metadata):
    def _do_get_item(self, name):
        if name in self.provider.get_entities():
            return self.provider.get_entity(name)
        raise NotFoundError

    def _do_keys(self):
        entities = self.provider.get_entities()
        return entities


class FieldsMetadata(Metadata):
    """
    """
    def __init__(self, provider, entity):
        Metadata.__init__(self, provider, entity)

    def _do_check_set_item(self, key, value):
        if key in self.get_fields(self.entity):
            raise MetadataError('%s is already found in table: %s'%(key, self.table))

    def _do_get_item(self, item):
        try:
            return self.provider.get_field(self.entity, item)
        except:
            pass
        raise NotFoundError

    def _do_keys(self):
        return self.provider.get_fields(self.entity)

class FieldMetadata(Metadata):
    """
    """
    pass

