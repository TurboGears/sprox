from sprox.formbase import FormBase, AddRecordForm, DisabledForm, EditableForm, Field
from sprox.viewbase import ViewBaseError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example, Document, assert_in_xml
from sprox.test.model import User, Group
from sprox.sa.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid, Schema
from formencode.validators import FieldsMatch, NotEmpty, OpenId
from tw.forms import PasswordField, TextField

class MyTextField(TextField):pass

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

class TestField:

    def setup(self):
        self.field = Field(TextField, NotEmpty)

    def test_create(self):
        assert self.field.widget == TextField
        assert self.field.validator == NotEmpty

class TestsEmptyDropdownWorks:
    def setup(self):
        self.base = UserForm(session)

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert_in_xml("""<td class="fieldcol" >
                <select name="town" class="propertysingleselectfield" id="town">
        <option value="" selected="selected">-----------</option>
</select>
            </td>""", rendered)

class TestFormBase(SproxTest):
    def setup(self):
        super(TestFormBase, self).setup()
        self.base = UserForm(session)

    def test_create(self):
        pass

    def test_formbase_with_validator_class(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = OpenId
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something'})
        except Invalid, e:
            assert u'"something" is not a valid OpenId (it is neither an URL nor an XRI)' in e.msg, e.msg

    def test_formbase_with_validator_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = OpenId()
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something'})
        except Invalid, e:
            assert u'"something" is not a valid OpenId (it is neither an URL nor an XRI)' in e.msg, e.msg

    def test_formbase_with_field_validator_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(validator=OpenId())
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something'})
        except Invalid, e:
            assert u'"something" is not a valid OpenId (it is neither an URL nor an XRI)' in e.msg, e.msg

    def test_formbase_with_field_validator_class(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(validator=OpenId())
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something'})
        except Invalid, e:
            assert u'"something" is not a valid OpenId (it is neither an URL nor an XRI)' in e.msg, e.msg

    def test_formbase_with_field_widget_class(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField)
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert isinstance(widget.children['user_name'], MyTextField)

    def test_formbase_with_field_widget_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField('user_name'))
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert isinstance(widget.children['user_name'], MyTextField)

    @raises(ViewBaseError)
    def test_formbase_with_field_widget_instance_no_id(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField())
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert isinstance(widget.children['user_name'], MyTextField)


    def test_formbase_with_field_widget_and_validator_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField, OpenId)
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert isinstance(widget.children['user_name'], MyTextField)
        try:
            widget.validate({'user_name':'something'})
        except Invalid, e:
            assert u'"something" is not a valid OpenId (it is neither an URL nor an XRI)' in e.msg, e.msg

    def test__fields__(self):
        eq_(sorted_user_columns, sorted(self.base.__fields__))

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert_in_xml("""<tr class="even" id="submit.container" title="" >
            <td class="labelcol">
                <label id="submit.label" for="submit" class="fieldlabel"></label>
            </td>
            <td class="fieldcol" >
                <input type="submit" class="submitbutton" value="Submit" />
            </td>
        </tr>""", rendered)

    @raises(ViewBaseError)
    def test_form_field_with_no_id(self):
        class BogusUserForm(FormBase):
            __entity__ = User
            field = TextField()
        bogus = BogusUserForm(session)

    def test_entity_with_synonym(self):
        class DocumentForm(FormBase):
            __entity__ = Document
        form = DocumentForm(session)
        rendered = form()
        assert_in_xml("""<tr class="odd" id="address.container" title="" >
            <td class="labelcol">
                <label id="address.label" for="address" class="fieldlabel">Address</label>
            </td>
            <td class="fieldcol" >
                <input type="text" id="address" class="textfield" name="address" value="" />
            </td>
        </tr>""", rendered)

    def test_entity_with_dropdown_field_names(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = ['group_name']
        form = UserFormFieldNames(session)
        rendered = form()
        assert_in_xml("""<td class="fieldcol" >
                <select name="groups" class="propertymultipleselectfield" id="groups" multiple="multiple" size="5">
        <option value="1">0</option>
        <option value="2">1</option>
        <option value="3">2</option>
        <option value="4">3</option>
        <option value="5">4</option>
</select>
            </td>""", rendered)

    def test_entity_with_dropdown_field_names2(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = {'groups':'group_name'}
        form = UserFormFieldNames(session)
        rendered = form()
        assert_in_xml("""<td class="fieldcol" >
                <select name="groups" class="propertymultipleselectfield" id="groups" multiple="multiple" size="5">
        <option value="1">0</option>
        <option value="2">1</option>
        <option value="3">2</option>
        <option value="4">3</option>
        <option value="5">4</option>
</select>
            </td>""", rendered)

    def test_entity_with_dropdown_field_names_title(self):
        class GroupFormFieldNames(FormBase):
            __entity__ = Group
            __dropdown_field_names__ = {'groups':'group_name'}
        form = GroupFormFieldNames(session)
        rendered = form()
        assert_in_xml("""<select name="users" class="propertymultipleselectfield" id="users" multiple="multiple" size="5">
        <option value="1">asdf@asdf.com</option>
</select>""", rendered)

    def test_entity_with_dropdown_field_names_title_overridden(self):
        class GroupFormFieldNames(FormBase):
            __entity__ = Group
            __dropdown_field_names__ = {'users':'user_name'}
        form = GroupFormFieldNames(session)
        rendered = form()
        assert_in_xml("""<select name="users" class="propertymultipleselectfield" id="users" multiple="multiple" size="5">
        <option value="1">asdf</option>
</select>""", rendered)

    def test_entity_with_dropdown_field_names_dict(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = {'groups':['group_name']}
        form = UserFormFieldNames(session)
        rendered = form()
        assert_in_xml( """<td class="fieldcol" >
                <select name="groups" class="propertymultipleselectfield" id="groups" multiple="multiple" size="5">
        <option value="1">0</option>
        <option value="2">1</option>
        <option value="3">2</option>
        <option value="4">3</option>
        <option value="5">4</option>
</select>
            </td>""", rendered)


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
            assert 'Passwords do not match' in exc.msg

class TestEditableForm(SproxTest):
    def setup(self):
        super(TestEditableForm, self).setup()
        #setup_records(session)

        class UserForm(EditableForm):
            __entity__ = User
            __limit_fields__ = ['user_name']

        self.base = UserForm(session)

    def test__fields__(self):
        form_fields = sorted(self.base.__fields__)
        expected_form_fields = sorted(['user_name', 'sprox_id', 'user_id', '_method'])
        eq_(expected_form_fields, form_fields)

    def test__widget__(self):
        rendered = self.base.__widget__()
        assert_in_xml("""<tr class="even" id="user_name.container" title="" >
            <td class="labelcol">
                <label id="user_name.label" for="user_name" class="fieldlabel">User Name</label>
            </td>
            <td class="fieldcol" >
                <input type="text" id="user_name" class="textfield" name="user_name" value="" />
            </td>
        </tr>""", rendered)

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
        assert_in_xml( """<tr class="even" id="user_name.container" title="" >
            <td class="labelcol">
                <label id="user_name.label" for="user_name" class="fieldlabel">User Name</label>
            </td>
            <td class="fieldcol" >
                <input type="text" id="user_name" class="textfield" name="user_name" value="" disabled="disabled" />
            </td>
        </tr>""", rendered)
