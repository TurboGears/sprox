from sprox.tablebase import TableBase
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example
from sprox.test.model import User
from sprox.sa.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid
from strainer.operators import assert_in_xhtml

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
