from sprox.configbase import ConfigBase, ConfigBaseError
from sprox.test.base import setup_database
from sprox.test.model import User
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

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
