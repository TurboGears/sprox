from sprox.configbase import ConfigBase, ConfigBaseError
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

class TestConfigBase:
    def setup(self):
        self.base = ConfigBase()

    def test_create(self):
        pass

    @raises(ConfigBaseError)
    def test__metadata__bad(self):
        self.base.__metadata__

    @raises(ConfigBaseError)
    def test__provider__bad(self):
        self.base.__provider__
