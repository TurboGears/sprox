"""
saprovider Module

this contains the class which allows dbsprockets to interface with sqlalchemy.

Classes:
Name                               Description
SAProvider                         sqlalchemy metadata/crud provider

Exceptions:
None

Functions:
None


Copyright (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
import inspect
from sqlalchemy import and_, or_, select, DateTime, Date, Binary, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.orm import class_mapper, Mapper, PropertyLoader, _mapper_registry, SynonymProperty
from sqlalchemy.orm.exc import UnmappedClassError
from sprox.iprovider import IProvider
from cgi import FieldStorage
from datetime import datetime
from warnings import warn

class SAORMProviderError(Exception):pass

class SAORMProvider(IProvider):
    def __init__(self, hint=None, **hints):
        """
        initialize me with a engine, bound metadata or bound session object
        or a combination of the above.
        """
        #if hint is None and len(hints) == 0:
        #    raise SAORMProviderError('You must provide a hint to this provider')
        self.engine, self.session, self.metadata = self._get_engine(hint, hints)

    def _get_engine(self, hint, hints):
        metadata = hints.get('metadata', None)
        engine   = hints.get('engine', None)
        session  = hints.get('session', None)

        if isinstance(hint, Engine):
            engine=hint

        if isinstance(hint, MetaData):
            metadata=hint

        if isinstance(hint, (Session, ScopedSession)):
            session = hint

        if session is not None and engine is None:
            engine = session.bind

        if metadata is not None and engine is None:
            engine = metadata.bind

        return engine, session, metadata

    def get_fields(self, entity):
        mapper = class_mapper(entity)
        field_names = mapper.c.keys()
        for prop in mapper.iterate_properties:
            try:
                getattr(mapper.c, prop.key)
                field_names.append(prop.key)
            except AttributeError:
                mapper.get_property(prop.key)
                field_names.append(prop.key)

        return field_names

    def get_entity(self, name):
        for mapper in _mapper_registry:
            if mapper.class_.__name__ == name:
                engine = mapper.tables[0].bind
                if engine is not None and mapper.tables[0].bind != self.engine:
                    continue
                if self.metadata is not None and self.mapper.tables.metadata != self.metadata:
                    continue
                return mapper.class_
        raise KeyError('could not find model by the name %s in %s'%(model_name, metadata))

    def get_entities(self):
        entities = []
        for mapper in _mapper_registry:
            engine = mapper.tables[0].bind
            if engine is not None and mapper.tables[0].bind != self.engine:
                continue
            if self.metadata is not None and self.mapper.tables.metadata != self.metadata:
                continue
            entities.append(mapper.class_.__name__)
        return entities

    def get_field(self, entity, name):
        mapper = class_mapper(entity)
        try:
            return getattr(mapper.c, name)
        except AttributeError:
            return mapper.get_property(name)

    def is_nullable(self, entity, name):
        field = self.get_field(entity, name)
        if isinstance(field, PropertyLoader):
            return field.local_side[0].nullable
        return field.nullable

    def get_primary_fields(self, entity):
        #for now we are only supporting entities with a single primary field
        return [self.get_primary_field(entity)]

    def get_primary_field(self, entity):
        if inspect.isfunction(entity):
            entity = entity()
        mapper = class_mapper(entity)
        for field_name in self.get_fields(entity):
            value = getattr(mapper.c, field_name)
            if value.primary_key:
                return value.name

    def get_view_field_name(self, entity, possible_columns):
        fields = self.get_fields(entity)
        view_field = None
        for column_name in possible_columns:
            for actual_name in fields:
                if column_name in actual_name:
                    view_field = actual_name
                    break
            if view_field:
                break;
        if view_field is None:
            view_field = fields[0]
        return view_field

    def get_dropdown_options(self, entity, view_names=['_name', 'name', 'description', 'title']):
        if self.session is None:
            warn('No dropdown options will be shown for %s.  '
                 'Try passing the session into the initialization'
                 'of your form base object so that this sprocket'
                 'can have values in the drop downs'%entity)
            return []

        if isinstance(entity, PropertyLoader):
            target_entity = entity.argument
        else:
            target_entity = entity

        #some kind of join tablesd
        if isinstance(target_entity, Mapper):
            target_entity = entity.class_

        pk_name = self.get_primary_field(target_entity)
        view_name = self.get_view_field_name(target_entity, view_names)

        rows = self.session.query(target_entity).all()
        return [(getattr(row, pk_name), getattr(row, view_name)) for row in rows]

    def get_relations(self, entity):
        mapper = class_mapper(entity)
        return [prop.key for prop in mapper.iterate_properties if isinstance(prop, PropertyLoader)]

    def is_relation(self, entity, field_name):
        if entity is None:
            return None
        try:
            mapper = class_mapper(entity)
        except UnmappedClassError:
            return None
        if isinstance(mapper.get_property(field_name), PropertyLoader):
            return True


    def get_synonyms(self, entity):
        mapper = class_mapper(entity)
        return [prop.key for prop in mapper.iterate_properties if isinstance(prop, SynonymProperty)]

    def create_relationships(self, obj, params, delete_first=False):
        entity = obj.__class__
        mapper = class_mapper(entity)
        for relation in self.get_relations(obj.__class__):
            if delete_first:
                related_items = getattr(obj, relation)
                if related_items is not None:
                    if hasattr(related_items, '__iter__'):
                        for item in getattr(obj, relation):
                            getattr(obj, relation).remove(item)
                        self.session.flush()
                    else:
                        setattr(obj, relation, None)

            if relation in params:
                prop = mapper.get_property(relation)
                target = prop.argument
                if not isinstance(params[relation], list):
                    params[relation] = [params[relation]]
                for value in params[relation]:
                    if value is not None:
                        target_obj = self.session.query(target).get(value)
                        if target_obj is not None:
                            if prop.uselist:
                                getattr(obj, relation).append(target_obj)
                            else:
                                setattr(obj, relation, target_obj)

    def create(self, entity, params):
        params = self._modify_params_for_dates(entity, params)
        obj = entity()
        relations = self.get_relations(entity)
        for key, value in params.iteritems():
            if key not in relations and value is not None:
                setattr(obj, key, value)
        self.session.add(obj)
        self.create_relationships(obj, params)
        self.session.flush()
        return obj

    def dictify(self, obj):
        r = {}
        mapper = class_mapper(obj.__class__)
        for prop in mapper.iterate_properties:
            value = getattr(obj, prop.key)
            if value is not None:
                if isinstance(prop, PropertyLoader):
                    klass = prop.argument
                    if isinstance(klass, Mapper):
                        klass = klass.class_
                    pk_name = self.get_primary_field(klass)
                    if isinstance(value, list):
                        #joins
                        value = [getattr(value, pk_name) for value in value]
                    else:
                        #fks
                        value = getattr(value, pk_name)
            r[prop.key] = value
        return r

    def get_default_values(self, entity, params):
        return params

    def get(self, entity, params):
        pk_name = self.get_primary_field(entity)
        obj = self.session.query(entity).get(params[pk_name])
        return self.dictify(obj)

    def _modify_params_for_dates(self, entity, params):
        mapper = class_mapper(entity)
        for key, value in params.iteritems():
            if key in mapper.c and value is not None:
                field = mapper.c[key]
                if hasattr(field, 'type') and isinstance(field.type, DateTime) and not isinstance(value, datetime):
                    dt = datetime.strptime(value[:19], '%Y-%m-%d %H:%M:%S')
                    params[key] = dt
                if hasattr(field, 'type') and isinstance(field.type, Date) and not isinstance(value, datetime):
                    dt = datetime.strptime(value, '%Y-%m-%d')
                    params[key] = dt
        return params


    def update(self, entity, params):
        params = self._modify_params_for_dates(entity, params)
        pk_name = self.get_primary_field(entity)
        obj = self.session.query(entity).get(params[pk_name])
        relations = self.get_relations(entity)
        for key, value in params.iteritems():
            if key not in relations:
                setattr(obj, key, value)
        self.create_relationships(obj, params, delete_first=True)
        self.session.flush()

    def delete(self, entity, params):
        pk_name = self.get_primary_field(entity)
        obj = self.session.query(entity).get(params[pk_name])
        self.session.delete(obj)
        return obj
