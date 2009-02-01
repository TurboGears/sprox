from sprox.formbase import FormBase, AddRecordForm, DisabledForm, EditableForm
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example, Document
from sprox.test.model import User, Group
from sprox.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid, Schema
from formencode.validators import FieldsMatch
from tw.forms import PasswordField, TextField

session = None
engine  = None
connection = None
user = None
def setup():
    global session, engine, metadata, user
    session, engine, metadata = setup_database()
    user = setup_records(session)

class UserForm(FormBase):
    __entity__ = User

class TestsEmptyDropdownWorks:
    def setup(self):
        self.base = UserForm(session)
        
    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<td class="fieldcol">
                <input type="submit" class="submitbutton" value="Submit" />
            </td>""" in rendered, rendered
    


class TestFormBase(SproxTest):
    def setup(self):
        super(TestFormBase, self).setup()
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

    def test_entity_with_synonym(self):
        class DocumentForm(FormBase):
            __entity__ = Document
        form = DocumentForm(session)
        rendered = form()
        assert """<tr id="address.container" class="odd" title="">
            <td class="labelcol">
                <label id="address.label" for="address" class="fieldlabel">Address</label>
            </td>
            <td class="fieldcol">
                <input type="text" name="address" class="textfield" id="address" value="" />
            </td>
        </tr>""" in rendered, rendered

    def test_entity_with_dropdown_field_names(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = ['group_name']
        form = UserFormFieldNames(session)
        rendered = form()
        assert """<select name="groups" class="propertymultipleselectfield" id="groups" multiple="multiple" size="5">
        <option value="1">0</option><option value="2">1</option><option value="3">2</option><option value="4">3</option><option value="5">4</option>
</select>""" in rendered, rendered
        
    def test_entity_with_dropdown_field_names_dict(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = {'groups':['group_name']}
        form = UserFormFieldNames(session)
        rendered = form()
        assert """<select name="groups" class="propertymultipleselectfield" id="groups" multiple="multiple" size="5">
        <option value="1">0</option><option value="2">1</option><option value="3">2</option><option value="4">3</option><option value="5">4</option>
</select>""" in rendered, rendered
        
        
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

    def test_form_with_base_validator(self):
        form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                                'verify_password',
                                                                messages={'invalidNoMatch':
                                                                'Passwords do not match'}),))
        class RegistrationForm(AddRecordForm):
            __model__ = User
            __require_fields__     = ['password', 'user_name', 'email_address']
            __omit_fields__        = ['_password', 'groups', 'created', 'user_id', 'town']
            __field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
            __base_validator__     = form_validator
            email_address          = TextField
            display_name           = TextField
            verify_password        = PasswordField('verify_password')
        registration_form = RegistrationForm()
        try:
            registration_form.validate(params={'password':'blah', 'verify_password':'not_blah'})
        except Invalid, exc:
            assert 'Passwords do not match' in exc.message

class TestEditableForm(SproxTest):
    def setup(self):
        super(TestEditableForm, self).setup()
        #setup_records(session)

        class UserForm(EditableForm):
            __entity__ = User
            __limit_fields__ = ['user_name']

        self.base = UserForm(session)

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<tr id="user_name.container" class="even" title="">
            <td class="labelcol">
                <label id="user_name.label" for="user_name" class="fieldlabel">User Name</label>
            </td>
            <td class="fieldcol">
                <input type="text" name="user_name" class="textfield has_error" id="user_name" value="asdf" />
                <span class="fielderror">That value already exists</span>
            </td>
        </tr>""" in rendered, rendered
        
class TestDisabledForm(SproxTest):
    def setup(self):
        super(TestDisabledForm, self).setup()
        #setup_records(session)

        class UserForm(DisabledForm):
            __entity__ = User
            __limit_fields__ = ['user_name']

        self.base = UserForm(session)

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert """<td class="fieldcol">
                <input type="text" name="user_name" class="textfield has_error" id="user_name" value="asdf" disabled="disabled" />
                <span class="fielderror">That value already exists</span>
            </td>""" in rendered, rendered