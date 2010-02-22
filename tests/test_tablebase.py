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

class TestTableBase:
    def setup(self):
        self.base = UserTable(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert_in_xhtml("""<thead>
        <tr>
                <th  class="col_0">actions</th>
                <th  class="col_1">_password</th>
                <th  class="col_2">user_id</th>
                <th  class="col_3">user_name</th>
                <th  class="col_4">email_address</th>
                <th  class="col_5">display_name</th>
                <th  class="col_6">created</th>
                <th  class="col_7">town_id</th>
                <th  class="col_8">town</th>
                <th  class="col_9">password</th>
                <th  class="col_10">groups</th>
        </tr>
    </thead>""", rendered)
