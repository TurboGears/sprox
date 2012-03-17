from sprox.sprockets import Sprocket, SprocketCache, ConfigCache, FillerCache, ViewCache, ConfigCacheError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User
from nose.tools import raises, eq_
from strainer.operators import assert_in_xhtml

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class TestViewCache(SproxTest):
    def setup(self):
        super(TestViewCache, self).setup()
        self.cache = ViewCache(session)

    def test_create(self):
        pass

    @raises(ConfigCacheError)
    def test_config_not_found(self):
        self.cache['never_find_me']

    def test_get_model_view(self):
        base = self.cache['model_view']
        r = base()

        pieces = ['<a href="Department/">Department</a>',
'<a href="Document/">Document</a>',
'<a href="DocumentCategory/">DocumentCategory</a>',
'<a href="DocumentCategoryReference/">DocumentCategoryReference</a>',
'<a href="DocumentCategoryTag/">DocumentCategoryTag</a>',
'<a href="Example/">Example</a>',
'<a href="File/">File</a>',
'<a href="Group/">Group</a>',
'<a href="Permission/">Permission</a>',
'<a href="Town/">Town</a>',
'<a href="User/">User</a>']

        for p in pieces:
            assert p in r, r

    def test_get_empty(self):
        base = self.cache['listing__User']
        b = base()

        fields = ["actions", "_password", "user_id", "user_name",
                  "email_address", "display_name", "created",
                  "town_id", "town", "password", "groups"]
        for f in fields:
            assert f in b

    @raises(ConfigCacheError)
    def get_not_found(self):
        self.cache['not_find_me']

class TestSprocketCache:
    def setup(self):
        self.cache = SprocketCache(session)

    def test_create(self):
        pass

    def test_get_sprocket(self):
        base = self.cache['listing__User']
        assert base.view is not None
        assert base.filler is not None
