import inspect

try:
    from sqlalchemy.orm import PropertyLoader
except ImportError:
    # Compatibility with SQLA0.9
    from sqlalchemy.orm import RelationshipProperty as PropertyLoader

try:
    from sqlalchemy.ext.declarative.clsregistry import _class_resolver
except ImportError as e:  # pragma: no cover
    # Compatibility with SQLA < 0.9
    _class_resolver = None

try:
    # Not available in some SQLA versions
    from sqlalchemy.types import LargeBinary
except ImportError:  # pragma: no cover
    class LargeBinary:
        pass

try:
    # Future proof as it will probably be removed as deprecated
    from sqlalchemy.types import Binary
except ImportError:  # pragma: no cover
    class Binary(LargeBinary):
        pass

from sqlalchemy.orm import mapperlib
def _all_registries():
    try:
        return mapperlib._all_registries()
    except AttributeError:
        class RegistryCompat:
            def __init__(self, mr):
                self.mappers = mr
        return [RegistryCompat(mapperlib._mapper_registry)]


def mapped_classes(engine):
    classes = []
    for registry in _all_registries():
        for mapper in registry.mappers:
            mapped_engine = mapper.tables[0].bind
            if engine is None:
                classes.append(mapper.class_)
            if mapped_engine is not None and mapped_engine != engine:
                continue
            classes.append(mapper.class_)
    return classes


def mapped_class(engine, class_name):
    for _class in mapped_classes(engine):
        if _class.__name__ == class_name:
            return _class
    raise KeyError('could not find model by the name %s (in %s)' % (class_name, [c.__name__ for c in mapped_classes(engine)]))


def resolve_entity(entity):
    if inspect.isfunction(entity) or inspect.ismethod(entity):
        entity = entity()
    if _class_resolver is not None and isinstance(entity, _class_resolver):
        entity = entity()
    return entity


