from sprox.viewbase import ViewBase
from sprox.test.base import setup_database
from sprox.test.model import User
from sprox.widgetselector import SAWidgetSelector
from nose.tools import raises, eq_


session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, connection, trans
    session, engine, connection = setup_database()

class DummyMetadata(object):

    def __init__(self, provider, entity):
        self.entity = entity
        self.provider = provider

    def keys(self):
        return self.provider.get_fields(self.entity)

    def __getitem__(self, name):
        return self.provider.get_field(self.entity, name)


class UserView(ViewBase):
    __entity__ = User
    __metadata_type__ = DummyMetadata
    __widget_selector__ = SAWidgetSelector()

class TestViewBase:
    def setup(self):
        self.base = UserView()

    def test_create(self):
        pass

    def test__fields__(self):
        eq_(['_password', 'created', 'display_name', 'email_address', 'groups', 'password', 'town', 'town_id', 'user_id', 'user_name'],
            sorted(self.base.__fields__))

    def test__widget__(self):
        eq_(None, self.base.__widget__())