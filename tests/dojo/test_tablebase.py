try:
    from sprox.dojo.tablebase import DojoTableBase, DojoEditableTableBase
    from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example, assert_in_xml
    from sprox.test.model import User
    from sprox.sa.widgetselector import SAWidgetSelector
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
            assert_in_xml("""<table  dojoType="dojox.grid.DataGrid" jsId="listing__User" id="None" store="listing__User_store" columnReordering="false" rowsPerPage="20" model="None" delayScroll="true" autoHeight="false" class="sprox-dojo-grid" escapeHTMLInData="False" >
    <thead>
            <tr>
                    <th formatter="lessThan" width="10em" field="__actions__" >actions</th>
                    <th formatter="lessThan" width="10em" field="_password" >_password</th>
                    <th formatter="lessThan" width="10em" field="user_id" >user_id</th>
                    <th formatter="lessThan" width="10em" field="user_name" >user_name</th>
                    <th formatter="lessThan" width="10em" field="email_address" >email_address</th>
                    <th formatter="lessThan" width="10em" field="display_name" >display_name</th>
                    <th formatter="lessThan" width="10em" field="created" >created</th>
                    <th formatter="lessThan" width="10em" field="town_id" >town_id</th>
                    <th formatter="lessThan" width="10em" field="town" >town</th>
                    <th formatter="lessThan" width="10em" field="password" >password</th>
                    <th formatter="lessThan" width="10em" field="groups" >groups</th>
            </tr>
    </thead>
</table>""",rendered)

    class TestDojoEditableTableBase:
        def setup(self):
            self.base = EditableUserTable(session)

        def test_create(self):
            pass

        def test__widget__(self):
            rendered = self.base.__widget__()
            assert_in_xml("""<table  dojoType="dojox.grid.DataGrid" jsId="None" id="None" store="None_store" columnReordering="false" rowsPerPage="20" model="None" delayScroll="true" autoHeight="None" class="sprox-dojo-grid" escapeHTMLInData="False" >
    <thead>
            <tr>
                    <th formatter="lessThan" width="10em" field="__actions__"                             editable="true">actions</th>
                    <th formatter="lessThan" width="10em" field="_password"                             editable="true">_password</th>
                    <th formatter="lessThan" width="10em" field="user_id"                             editable="true">user_id</th>
                    <th formatter="lessThan" width="10em" field="user_name"                             editable="true">user_name</th>
                    <th formatter="lessThan" width="10em" field="email_address"                             editable="true">email_address</th>
                    <th formatter="lessThan" width="10em" field="display_name"                             editable="true">display_name</th>
                    <th formatter="lessThan" width="10em" field="created"                             editable="true">created</th>
                    <th formatter="lessThan" width="10em" field="town_id"                             editable="true">town_id</th>
                    <th formatter="lessThan" width="10em" field="town"                             editable="true">town</th>
                    <th formatter="lessThan" width="10em" field="password"                             editable="true">password</th>
                    <th formatter="lessThan" width="10em" field="groups"                             editable="true">groups</th>
            </tr>
    </thead>
</table>""", rendered)

except ImportError:
    print 'Dojo Tests disabled with ToscaWidgets2'