from nose.tools import raises
from sprox.validators import UniqueValue
from sprox.test.base import *
from formencode import Invalid
from sprox.sa.provider import SAORMProvider

session = None
engine = None
connection = None
trans = None

def setup():
    global session, engine, connect, trans
    session, engine, connect = setup_database()

def teardown():
    global session, trans

class TestUniqueValue(SproxTest):

    def setup(self):
        super(TestUniqueValue, self).setup()
        self.validator = UniqueValue(SAORMProvider(session), User, 'user_name')

    @raises(Invalid)
    def test_to_python_invalid(self):
        self.validator.to_python(u'asdf', None)

    def test_to_python_valid(self):
        self.validator.to_python(u'asdf1234', None)
