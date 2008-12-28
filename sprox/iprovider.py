"""
iprovider Module

This contains the class which allows dbsprockets to interface with any database.


Copyright &copy 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""

class IProvider:
    def get_field(self, entity, name):
        """Get a field with the given field name."""
        raise NotImplementedError

    def get_fields(self, entity):
        """Get all of the fields for a given entity."""
        raise NotImplementedError

    def get_entity(self, name):
        """Get an entity with the given name."""
        raise NotImplementedError

    def get_entities(self):
        """Get all entities available for this provider."""
        raise NotImplementedError

    def get_primary_fields(self, entity):
        """Get the fields in the entity which uniquely identifies a record."""
        raise NotImplementedError

    def get_primary_field(self, entity):
        """Get the single primary field for an entity"""
        raise NotImplementedError

    def get_view_field_name(self, entity, possible_names):
        """Get the name of the field which first matches the possible colums

        :Arguments:
          entity
            the entity where the field is located
          possible_names
            a list of names which define what the view field may contain.  This allows the first
            field that has a name in the list of names will be returned as the view field.
        """
        raise NotImplementedError

    def get_dropdown_options(self, entity, field_name, view_names=None):
        """Get all dropdown options for a given entity field.

        :Arguments:
          entity
            the entity where the field is located
          field_name
            name of the field in the entity
          view_names
            a list of names which define what the view field may contain.  This allows the first
            field that has a name in the list of names will be returned as the view field.

        :Returns:
        A list of tuples with (id, view_value) as items.

        """
        raise NotImplementedError

    def get_relations(self, entity):
        """Get all of the field names in an enity which are related to other entities."""
        raise NotImplementedError

    def is_relation(self, entity, field_name):
        """Determine if a field is related to a field in another entity."""
        raise NotImplementedError

    def is_nullable(self, entity, field_name):
        """Determine if a field is nullable."""
        raise NotImplementedError

    def get_default_values(self, entity, params):
        """Get the default values for form filling based on the database schema."""
        raise NotImplementedError

    def create(self, entity, params):
        """Create an entry of type entity with the given params."""
        raise NotImplementedError

    def get(self, entity, params):
        """Get a single entry of type entity which matches the params."""
        raise NotImplementedError
    def update(self, entity, params):
        """Update an entry of type entity which matches the params."""
        raise NotImplementedError
    def delete(self, entity, params):
        """Delete an entry of typeentity which matches the params."""
        raise NotImplementedError
