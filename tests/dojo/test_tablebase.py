from sprox.dojo.tablebase import DojoTableBase, DojoEditableTableBase
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
    __url__ = './something.json'

class EditableUserTable(DojoEditableTableBase):
    __entity__ = User
    __url__ = './something.json'

class TestDojoTableBase:
    def setup(self):
        self.base = UserTable(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/"
                         dojoType="dojox.grid.DataGrid"
                         jsId="listing__User"
                         id=""
                         store="listing__User_store"
                         columnReordering="false"
                         rowsPerPage="20"
                         model="None"
                         delayScroll="true"
                         class="sprox-dojo-grid"
                         >
    <thead>
            <tr>
                    <th width="10em" name="actions" field="__actions__" >__actions__</th>
                    <th width="10em" name="_password" field="_password" >_password</th>
                    <th width="10em" name="user_id" field="user_id" >user_id</th>
                    <th width="10em" name="user_name" field="user_name" >user_name</th>
                    <th width="10em" name="email_address" field="email_address" >email_address</th>
                    <th width="10em" name="display_name" field="display_name" >display_name</th>
                    <th width="10em" name="created" field="created" >created</th>
                    <th width="10em" name="town_id" field="town_id" >town_id</th>
                    <th width="10em" name="town" field="town" >town</th>
                    <th width="10em" name="password" field="password" >password</th>
                    <th width="10em" name="groups" field="groups" >groups</th>
            </tr>
    </thead>
    <div dojoType="dojox.data.QueryReadStore" jsId="listing__User_store"  id="listing__User_store" url="./something.json"/>
</table>""" in rendered, rendered

class TestDojoEditableTableBase:
    def setup(self):
        self.base = EditableUserTable(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/"
                         dojoType="dojox.grid.DataGrid"
                         jsId="None"
                         id=""
                         store="None_store"
                         columnReordering="false"
                         rowsPerPage="20"
                         model="None"
                         delayScroll="true"
                         class="sprox-dojo-grid"
                         >
    <thead>
            <tr>
                    <th width="10em" name="actions" field="__actions__"                             editable="true">__actions__</th>
                    <th width="10em" name="_password" field="_password"                             editable="true">_password</th>
                    <th width="10em" name="user_id" field="user_id"                             editable="true">user_id</th>
                    <th width="10em" name="user_name" field="user_name"                             editable="true">user_name</th>
                    <th width="10em" name="email_address" field="email_address"                             editable="true">email_address</th>
                    <th width="10em" name="display_name" field="display_name"                             editable="true">display_name</th>
                    <th width="10em" name="created" field="created"                             editable="true">created</th>
                    <th width="10em" name="town_id" field="town_id"                             editable="true">town_id</th>
                    <th width="10em" name="town" field="town"                             editable="true">town</th>
                    <th width="10em" name="password" field="password"                             editable="true">password</th>
                    <th width="10em" name="groups" field="groups"                             editable="true">groups</th>
            </tr>
    </thead>
</table>""" in rendered, rendered

