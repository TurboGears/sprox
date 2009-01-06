from sprox.dojo.sprockets import DojoSprocketCache
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class TestDojoSprocketCache:
    def setup(self):
        self.cache = DojoSprocketCache(session)

    def test_create(self):
        pass

    def test_get_sprocket(self):
        base = self.cache['listing__User']
        assert base.view is not None
        assert base.filler is not None
