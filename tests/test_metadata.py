from nose.tools import raises, eq_

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sprox.metadata import Metadata, MetadataError, FieldsMetadata, FieldMetadata, EntitiesMetadata, NotFoundError
from sprox.sa.provider import SAORMProvider
from sprox.iprovider import IProvider
from sprox.test.base import *

session = None
engine = None
connect = None
trans = None

def setup():
    global session, engine, connect, trans
    session, engine, metadata = setup_database()
#    trans = engine.begin()


class MetadataTest(SproxTest):
    obj = Metadata
    provider = IProvider()

    def setup(self):
        super(MetadataTest, self).setup()
        self.metadata = self.obj(self.provider)

    def test_create(self):
        pass

    @raises(NotImplementedError)
    def test_set_item(self):
        self.metadata['asdf'] = 'asdf'

    @raises(NotImplementedError)
    def test_get_item(self):
        value = self.metadata['asdf']

    @raises(NotImplementedError)
    def test_keys(self):
        value = self.metadata.keys()

class TestMetadata(MetadataTest):pass

class TestFieldsMetadata(MetadataTest):
    def setup(self):
        super(TestFieldsMetadata, self).setup()
        provider = SAORMProvider(engine, metadata=metadata)
        self.metadata = FieldsMetadata(provider, Example)

    def test_get_item(self):
        field = self.metadata['binary']
        eq_(field.name, 'binary')

    @raises(KeyError)
    def test_get_item_key_error(self):
        self.metadata['asdf']

    def test_set_item(self):
        self.metadata['asdf'] = '1234'
        assert self.metadata['asdf'] == '1234'

    @raises(MetadataError)
    def test_set_item_bad(self):
        self.metadata['binary'] = '1234'

    def test_keys(self):
        self.metadata['asdf'] = '1234'
        keys = sorted(self.metadata.keys())
        eq_(keys, ['asdf', 'binary', 'binary', 'blob', 'blob',
                    'boolean', 'boolean', 'cLOB', 'cLOB', 'char',
                    'char', 'created', 'created', 'date', 'date',
                    'dateTime', 'dateTime', 'date_', 'date_', 'datetime_',
                    'datetime_', 'decimal', 'decimal', 'example_id', 'example_id',
                    'float_', 'float_', 'float__', 'float__', 'int_', 'int_', 'integer',
                    'integer', 'interval', 'interval', 'numeric', 'numeric',
                    'password', 'password', 'pickletype',
                    'pickletype', 'smallint', 'smallint', 'smalliunteger', 'smalliunteger',
                    'string', 'string', 'text', 'text', 'time', 'time', 'time_', 'time_',
                    'timestamp', 'timestamp', 'unicode_', 'unicode_', 'varchar', 'varchar'])

class TestEntitiesMetadata:
    def setup(self):
        provider = SAORMProvider(engine, metadata=metadata)
        self.metadata = EntitiesMetadata(provider)

    def test_create(self):
        pass

    def test_get_item(self):
        eq_(User, self.metadata['User'])

    @raises(KeyError)
    def test_get_item_not_found(self):
        self.metadata['no_findy']
