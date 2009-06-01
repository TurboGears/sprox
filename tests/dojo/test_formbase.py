from sprox.dojo.formbase import DojoFormBase
from sprox.widgets.dojo import SproxDojoSortedSelectShuttleField
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User, Example
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class UserForm(DojoFormBase):
    __entity__ = User
    groups = SproxDojoSortedSelectShuttleField

class TestFormBase(SproxTest):
    def setup(self):
        super(TestFormBase, self).setup()
        self.base = UserForm(session)

    def test_create(self):
        pass

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<div style="float:left; padding: 5px; width:10em;">
        Available<br />
        <select class="shuttle" id="groups_src" multiple="multiple" name="" size="5">
                <option value="1">0</option><option value="2">1</option><option value="3">2</option><option value="4">3</option><option value="5">4</option>
        </select>
    </div>
    <div style="float:left; padding: 25px 5px 5px 0px;" id="groups_Buttons">
        <button class="shuttle" id="groups_AllRightButton">&gt;&gt;</button><br />
        <button class="shuttle" id="groups_RightButton">&gt;</button><br />
        <button class="shuttle" id="groups_LeftButton">&lt;</button><br />
        <button class="shuttle" id="groups_AllLeftButton">&lt;&lt;</button>
    </div>""" in rendered, rendered