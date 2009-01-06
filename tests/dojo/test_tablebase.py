from sprox.dojo.tablebase import DojoTableBase
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example
from sprox.test.model import User
from sprox.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid

session = None
engine  = None
connection = None
def setup():
    global session, engine, metadata
    session, engine, metadata = setup_database()
    user = setup_records(session)

def teardown():
    session.rollback()

class UserTable(DojoTableBase):
    __entity__ = User

class TestTableBase:
    def setup(self):
        self.base = UserTable(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<thead>
            <tr>
                <th field="__actions__">actions</th>
                <th field="_password" width="auto">_password
                </th><th field="user_id" width="auto">user_id
                </th><th field="user_name" width="auto">user_name
                """ in rendered, rendered
