import inspect

try:
    from sqlalchemy.orm import PropertyLoader
except ImportError:
    # Compatibility with SQLA0.9
    from sqlalchemy.orm import RelationshipProperty as PropertyLoader

try:
    from sqlalchemy.ext.declarative.clsregistry import _class_resolver
except ImportError as e:
    _class_resolver = None


def resolve_entity(entity):
    if inspect.isfunction(entity):
        entity = entity()
    if _class_resolver is not None and isinstance(entity, _class_resolver):
        entity = entity()
    return entity

