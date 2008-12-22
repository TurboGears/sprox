"""
iprovider Module

this contains the class which allows dbsprockets to interface with any database.

Classes:
Name             Description
IProvider        provider interface

Exceptions:
None

Functions:
None


Copywrite (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""

class IProvider:
    #table information stuff
    def get_tables(self):
        """()->[list of tablesNames]
        get a list of tables from the database"""
        raise NotImplementedError
    def get_table(self, name):
        """(name) -> sqlalchemy.schema.Table
        get the table definition with the given table name
        """
        raise NotImplementedError
    def get_columns(self, table_name):
        """(name) -> [list of column_names]
        get the column names given the table name
        """
        raise NotImplementedError
    def get_column(self, table_name, name):
        """(table_name, name) -> sqlalchemy.schema.Column
        get the column definition givcen the tablename and column name.
        """
        raise NotImplementedError
    def get_primary_keys(self, table_name):
        raise NotImplementedError
    def get_server_default(self,table_name, key):
        raise NotImplementedError
    #crud stuff
    def select(self, table_name, **kw):
        raise NotImplementedError
    def add(self, table_name=None, **kw):
        raise NotImplementedError
    def edit(self, table_name=None, **kw):
        raise NotImplementedError
    def is_nullable_field(self,field):
        raise NotImplementedError
