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
        assert """<table xmlns="http://www.w3.org/1999/xhtml" dojoType="dojox.grid.DataGrid" jsId="listing__User" id="" store="listing__User_store" columnReordering="false" rowsPerPage="20" delayScroll="true" class="">
    <thead>
            <tr>
                <th field="__actions__">actions</th>
                <th field="_password">_password
                </th><th field="user_id">user_id
                </th><th field="user_name">user_name
                </th><th field="email_address">email_address
                </th><th field="display_name">display_name
                </th><th field="created">created
                </th><th field="town_id">town_id
                </th><th field="town">town
                </th><th field="password">password
                </th><th field="groups">groups
                </th>
            </tr>
    </thead>""" in rendered, rendered
