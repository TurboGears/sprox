from sprox.formbase import FormBase, AddRecordForm
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example
from sprox.test.model import User
from sprox.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class UserForm(FormBase):
    __entity__ = User

class TestFormBase:
    def setup(self):
        self.base = UserForm(session)

    def test_create(self):
        pass

    def test__fields__(self):
        eq_(sorted_user_columns, sorted(self.base.__fields__))

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<td class="fieldcol">
                <input type="submit" class="submitbutton" value="Submit" />
            </td>""" in rendered, rendered

    def test_require_field(self):
        class RegistrationForm(FormBase):
            __entity__ = User
            __require_fields__ = ['user_name']

        form = RegistrationForm(session)
        eq_(form.__widget__.children['user_name'].validator.not_empty, True)

class TestAddRecordForm(SproxTest):
    def setup(self):
        super(TestAddRecordForm, self).setup()
        #setup_records(session)

        class AddUserForm(AddRecordForm):
            __entity__ = User
            __limit_fields__ = ['user_name']

        self.base = AddUserForm(session)

    @raises(Invalid)
    def test_validate(self):
        self.base.validate(params={'sprox_id':'asdf', 'user_name':'asdf'})

    def test_example_form(self):
        class AddExampleForm(AddRecordForm):
            __entity__ = Example
        example_form = AddExampleForm()
        #print example_form()
        #assert "checkbox" in example_form()
        assert "checkbox" in example_form({'boolean':"asdf"})