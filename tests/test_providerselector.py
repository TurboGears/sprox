from sprox.providerselector import SAORMSelector, ProviderTypeSelector, ProviderSelector, ProviderTypeSelectorError
from sprox.test.base import setup_database
from sprox.test.model import User
from nose.tools import raises, eq_
from sprox.dummyentity import DummyEntity

session = None
engine  = None
connection = None
trans = None
metadata = None
def setup():
    global session, engine, metadata, trans, metadata
    session, engine, metadata = setup_database()
    from sprox.test.base import metadata as meta
    metadata = meta
    import sprox.providerselector as p
    #this un-singleton-izes this module for testing with reflection (sqlsoup)
    p.SAORMSelector = p._SAORMSelector()

class TestProviderSelector:
    def setup(self):
        self.selector = ProviderSelector()

    def test_create(self):
        pass

    @raises(NotImplementedError)
    def test_get_entity(self):
        self.selector.get_entity('User')

    @raises(NotImplementedError)
    def test_get_provider(self):
        self.selector.get_provider(User)

    @raises(NotImplementedError)
    def test_get_identifier(self):
        self.selector.get_identifier(User)

class TestSAORMProviderSelector:
    def setup(self):
        self.selector = SAORMSelector

    def test_get_entity(self):
        eq_(User, self.selector.get_entity('User'))

    def test_get_entity_engine_not_none(self):
        eq_(User, self.selector.get_entity('User', hint=engine))

    def test_get_provider(self):
        eq_(engine, self.selector.get_provider(User).engine)

    def test_get_identifier(self):
        eq_('User', self.selector.get_identifier(User))

    def test_get_provider_with_metadata(self):
        eq_(engine, self.selector.get_provider(User, hint=metadata).engine)

    @raises(NameError)
    def test_entity_not_found(self):
        self.selector.get_entity('Dummy')

    def test_get_provider_engine_none(self):
        self.selector.get_provider()

    #xxx: this is not super clean, and I think it should be removed.
    def test_get_provider_with_cleared_providers(self):
        self.selector._providers = {}
        self.selector.get_provider(hint=engine)

class TestProviderTypeSelector:
    def setup(self):
        self.type_selector = ProviderTypeSelector()

    def test_create(self):
        pass

    @raises(ProviderTypeSelectorError)
    def test_no_provider_type(self):
        self.type_selector.get_selector('asdf')
    
    def test_dummy_provider_type(self):
        self.type_selector.get_selector(DummyEntity)