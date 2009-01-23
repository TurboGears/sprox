from sprox.sprockets import Sprocket, SprocketCache, ConfigCache, FillerCache, ViewCache, ConfigCacheError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User
from nose.tools import raises, eq_

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
        eq_(base(), """<div xmlns="http://www.w3.org/1999/xhtml" class="containerwidget">
<div class="entitylabelwidget">
<a href="Document/">Document</a>
</div>
<div class="entitylabelwidget">
<a href="Example/">Example</a>
</div>
<div class="entitylabelwidget">
<a href="Group/">Group</a>
</div>
<div class="entitylabelwidget">
<a href="Permission/">Permission</a>
</div>
<div class="entitylabelwidget">
<a href="Town/">Town</a>
</div>
<div class="entitylabelwidget">
<a href="User/">User</a>
</div>
</div>""")

    def test_get_empty(self):
        base = self.cache['listing__User']
        eq_(base(), """<div xmlns="http://www.w3.org/1999/xhtml">
<table class="grid">
    <thead>
        <tr>
            <th></th>
            <th class="col_0">
            _password
            </th><th class="col_1">
            user_id
            </th><th class="col_2">
            user_name
            </th><th class="col_3">
            email_address
            </th><th class="col_4">
            display_name
            </th><th class="col_5">
            created
            </th><th class="col_6">
            town_id
            </th><th class="col_7">
            town
            </th><th class="col_8">
            password
            </th><th class="col_9">
            groups
            </th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>
      No Records Found.
</div>""")

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
