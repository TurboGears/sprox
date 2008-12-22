from sprox.providerselector import SAORMSelector, ProviderTypeSelector
from base import setup_database
from model import User
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, connection, trans
    session, engine, connection = setup_database()
    import sprox.providerselector as p
    #this un-singleton-izes this module for testing with reflection (sqlsoup)
    p.SAORMSelector = p._SAORMSelector()

class TestSAORMProviderSelector:
    def setup(self):
        self.selector = SAORMSelector

    def test_get_entity(self):
        eq_(User, self.selector.get_entity('User'))

    def test_get_provider(self):
        eq_(engine, self.selector.get_provider(User).engine)

    def test_get_identifier(self):
        eq_('User', self.selector.get_identifier(User))

