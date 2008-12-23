"""
iprovider Module

This contains the class which allows dbsprockets to interface with any database.


Copyright (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""

class IProvider:
    def get_field(self, entity, name):
        raise NotImplementedError
    def get_fields(self, entity):
        raise NotImplementedError
    def get_entity(self, name):
        raise NotImplementedError
    
    def get_entities(self):
        raise NotImplementedError
    
    def get_primary_fields(self, entity):
        raise NotImplementedError
    
    def get_primary_field(self, entity):
        raise NotImplementedError
    
    def get_view_field_name(self, entity, possible_columns):
        raise NotImplementedError
    
    def get_dropdown_options(self, entity, view_names=None):
        raise NotImplementedError
    
    def get_relations(self, entity):
        raise NotImplementedError
    
    def is_relation(self, entity, field_name):
        raise NotImplementedError
    def is_nullable(self, entity, name):
        raise NotImplementedError
    
    def get_default_values(self, entity, params):
        """Get the default values for form filling based on the database schema"""
        raise NotImplementedError
    
    def create(self, entity, params):
        """Create an entry of type entity with the given params"""
        raise NotImplementedError

    def create_relationships(self, obj, params, delete_first=False):
        raise NotImplementedError

    def get(self, entity, params):
        """Get a single entry of type entity which matches the params"""
        raise NotImplementedError
    def update(self, entity, params):
        """Update an entry of type entity which matches the params"""
        raise NotImplementedError
    def delete(self, entity, params):
        """Delete an entry of typeentity which matches the params"""
        raise NotImplementedError
