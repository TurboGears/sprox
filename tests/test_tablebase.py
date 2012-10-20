from sprox.tablebase import TableBase
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example
from sprox.test.model import User
from sprox.sa.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid
from sprox.widgets import TextField

session = None
engine  = None
connection = None
def setup():
    global session, engine, metadata
    session, engine, metadata = setup_database()
    user = setup_records(session)

def teardown():
    session.rollback()

class UserTable(TableBase):
    __entity__ = User

class UserTableWithWidget(TableBase):
    __entity__ = User
    __omit_fields__ = ['__actions__']
    __limit_fields__ = ['user_id', 'display_name']
    __field_widget_types__ = {'user_id': TextField}

class TestTableBase(SproxTest):
    def setup(self):
        super(TestTableBase, self).setup()
        self.base = UserTable(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.base()

        fields = ["actions", "_password", "user_id", "user_name",
                  "email_address", "display_name", "created",
                  "town_id", "town", "password", "groups"]

        for f in fields:
            assert f in rendered

    def test_using_widgets(self):
        table = UserTableWithWidget()
        t = table(value=[{'user_id':'5', 'display_name':'Test'}])
        assert 'input' in t
