from sprox.fillerbase import EditFormFiller
from sprox.formbase import FormBase, AddRecordForm, DisabledForm, EditableForm, Field
from sprox.viewbase import ViewBaseError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, setup_records, \
    Example, Document, assert_in_xml, widget_children, widget_is_type, form_error_message
from sprox.test.model import User, Group, WithoutName, WithoutNameOwner, CompoundPrimaryKey
from sprox.sa.widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid, Schema
from formencode.validators import FieldsMatch, NotEmpty, OpenId, Int as IntValidator

try:
    from tw2.forms import PasswordField, TextField
except:
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
        rendered = self.base()
        assert 'selected="selected"' in rendered
        assert '-----------</option>' in rendered


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
            widget.validate({'user_name':'something', 'created':''})
        except Invalid as e:
            msg = form_error_message(e)
            assert '"something" is not a valid OpenId (it is neither an URL nor an XRI)' in msg, msg

    def test_formbase_with_validator_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = OpenId()
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something', 'created':''})
        except Invalid as e:
            msg = form_error_message(e)
            assert '"something" is not a valid OpenId (it is neither an URL nor an XRI)' in msg, msg

    def test_formbase_with_field_validator_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(validator=OpenId())
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something', 'created':''})
        except Invalid as e:
            msg = form_error_message(e)
            assert '"something" is not a valid OpenId (it is neither an URL nor an XRI)' in msg, msg

    def test_formbase_with_field_validator_class(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(validator=OpenId())
        user_form = UserForm(session)
        widget = user_form.__widget__
        try:
            widget.validate({'user_name':'something', 'created':''})
        except Invalid as e:
            msg = form_error_message(e)
            assert '"something" is not a valid OpenId (it is neither an URL nor an XRI)' in msg, msg

    def test_formbase_with_field_validator_many2many(self):
        class UserForm(FormBase):
            __entity__ = User
            groups = Field(validator=IntValidator())
        user_form = UserForm(session)
        widget = user_form.__widget__

        data = widget.validate({'groups': ['1', '2']})
        assert data['groups'] == [1, 2], data

        data = widget.validate({'groups': ['a', 'b']})
        assert data['groups'] == [], data

    def test_formbase_with_field_widget_class(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField)
        user_form = UserForm(session)
        widget = user_form.__widget__

        assert widget_is_type(widget_children(widget)['user_name'], MyTextField)

    def test_formbase_with_field_widget_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField('user_name'))
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert widget_is_type(widget_children(widget)['user_name'], MyTextField)

    @raises(ViewBaseError)
    def test_formbase_with_field_widget_instance_no_id(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField())
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert widget_is_type(widget_children(widget)['user_name'], MyTextField)

    def test_formbase_with_field_widget_and_validator_instance(self):
        class UserForm(FormBase):
            __entity__ = User
            user_name = Field(MyTextField, OpenId)
        user_form = UserForm(session)
        widget = user_form.__widget__
        assert widget_is_type(widget_children(widget)['user_name'], MyTextField)
        try:
            widget.validate({'user_name':'something', 'created':''})
        except Invalid as e:
            msg = form_error_message(e)
            assert '"something" is not a valid OpenId (it is neither an URL nor an XRI)' in msg, msg

    def test__fields__(self):
        eq_(sorted_user_columns, sorted(self.base.__fields__))

    def test__widget__(self):
        rendered = self.base()
        assert 'type="submit"' in rendered

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
        assert 'name="address"' in rendered, rendered

    def test_entity_with_dropdown_field_names(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = ['group_name']
        form = UserFormFieldNames(session)
        rendered = form()

        entries = ['<option value="1">Group 0</option>', '<option value="2">Group 1</option>',
                   '<option value="3">Group 2</option>',
                   '<option value="4">Group 3</option>', '<option value="5">Group 4</option>']

        for e in entries:
            assert e in rendered

    def test_entity_with_dropdown_field_names2(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = {'groups':'group_name'}
        form = UserFormFieldNames(session)
        rendered = form()

        entries = ['<option value="1">Group 0</option>', '<option value="2">Group 1</option>',
                   '<option value="3">Group 2</option>',
                   '<option value="4">Group 3</option>', '<option value="5">Group 4</option>']

        for e in entries:
            assert e in rendered

    def test_entity_with_dropdown_field_on_entity(self):
        class OwnerFormFieldNames(FormBase):
            __entity__ = WithoutName
        form = OwnerFormFieldNames(session)
        rendered = form()

        entries = ['<option value="1">owner</option>']

        for e in entries:
            assert e in rendered, rendered

    def test_entity_with_dropdown_field_names_title(self):
        class GroupFormFieldNames(FormBase):
            __entity__ = Group
            __dropdown_field_names__ = {'groups':'group_name'}
        form = GroupFormFieldNames(session)
        rendered = form()

        assert '<option value="1">asdf@asdf.com</option>' in rendered

    def test_entity_with_dropdown_field_names_title_overridden(self):
        class GroupFormFieldNames(FormBase):
            __entity__ = Group
            __dropdown_field_names__ = {'users':'user_name'}
        form = GroupFormFieldNames(session)
        rendered = form()

        assert '<option value="1">asdf</option>' in rendered

    def test_entity_with_dropdown_field_names_dict(self):
        class UserFormFieldNames(FormBase):
            __entity__ = User
            __dropdown_field_names__ = {'groups':['group_name']}
        form = UserFormFieldNames(session)
        rendered = form()

        entries = ['<option value="1">Group 0</option>', '<option value="2">Group 1</option>',
                   '<option value="3">Group 2</option>',
                   '<option value="4">Group 3</option>', '<option value="5">Group 4</option>']

        for e in entries:
            assert e in rendered

    def test_require_field(self):
        class RegistrationForm(FormBase):
            __entity__ = User
            __require_fields__ = ['user_name']

        form = RegistrationForm(session)
        eq_(widget_children(form.__widget__)['user_name'].validator.not_empty, True)

    def test_validator_for_hidden_fields(self):
        class RegistrationForm(FormBase):
            __entity__ = Group
            __hide_fields__ = ['group_name']

        form = RegistrationForm(session)
        assert widget_children(form.__widget__)['group_name'].validator is not None


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

    def test_primary_key_is_omitted_with_omit_fields_specified(self):
        class AddUserForm(AddRecordForm):
            __entity__ = User
            __omit_fields__ = ['user_name']
        test_form = AddUserForm()

        assert 'user_id' in test_form.__omit_fields__, test_form.__omit_fields__

    def test_example_form(self):
        class AddExampleForm(AddRecordForm):
            __entity__ = Example
        example_form = AddExampleForm()
        #print example_form()
        #assert "checkbox" in example_form()
        assert "checkbox" in example_form({'boolean':"asdf"})

    def test_form_with_base_validator(self):
        if hasattr(TextField, 'req'):
            form_validator = FieldsMatch('password', 'verify_password',
                messages={'invalidNoMatch': 'Passwords do not match'})
        else:
            form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                                'verify_password',
                                                                messages={'invalidNoMatch':
                                                                'Passwords do not match'}),))
        class RegistrationForm(AddRecordForm):
            __model__ = User
            __require_fields__     = ['password', 'user_name', 'email_address']
            __omit_fields__        = ['_password', 'groups', 'created', 'user_id', 'town']
            __field_order__        = ['password', 'verify_password', 'user_name', 'email_address', 'display_name']
            __base_validator__     = form_validator
            email_address          = TextField
            display_name           = TextField
            verify_password        = PasswordField('verify_password')
        registration_form = RegistrationForm()
        try:
            registration_form.validate(params={'password':'blah', 'verify_password':'not_blah'})
        except Invalid as e:
            msg = form_error_message(e)
            assert 'Passwords do not match' in msg, msg

    def test_default_value(self):
        class AddGroupForm(AddRecordForm):
            __entity__ = Group
        example_form = AddGroupForm()
        rendered = example_form()
        assert 'default group name' in rendered

    def test_autoincrement_single_primary_key(self):
        class AddUserForm(AddRecordForm):
            __entity__ = User

        test_form = AddUserForm()
        html = test_form.display()

        uid_input = self.get_line_in_text('name="user_id"', html)
        assert not uid_input, uid_input

    def test_required_single_primary_key(self):
        class AddUserForm(AddRecordForm):
            __entity__ = User
            __require_fields__ = ['user_id']

        test_form = AddUserForm()
        html = test_form.display()

        uid_input = self.get_line_in_text('name="user_id"', html)
        assert 'type="text"' in uid_input, html
        assert 'disabled' not in uid_input, html

    def test_compound_primary_key(self):
        class AddCompoundPrimaryKey(AddRecordForm):
            __entity__ = CompoundPrimaryKey

        test_form = AddCompoundPrimaryKey()
        html = test_form.display()

        name_input = self.get_line_in_text('name="name"', html)
        surname_input = self.get_line_in_text('name="surname"', html)
        assert 'type="text"' in name_input, name_input
        assert 'disabled' not in name_input, name_input
        assert 'type="text"' in surname_input, surname_input
        assert 'disabled' not in surname_input, surname_input

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
        rendered = self.base()
        assert 'name="user_name"' in rendered
        assert 'User Name' in rendered

    def test_required_validator_select_field(self):
        o = session.query(WithoutNameOwner).filter_by(data='otherowner').first()
        assert o, 'Something wrong in tests setup'

        class OwnerFiller(EditFormFiller):
            __entity__ = WithoutNameOwner
        owner_filler = OwnerFiller(session)
        value = owner_filler.get_value({'uid': o.uid})

        class OwnerForm(EditableForm):
            __entity__ = WithoutNameOwner
            __require_fields__ = ['owned']
        owner_form = OwnerForm(session)

        form_html = owner_form.display(value=value)
        selected = [row for row in form_html.split('\n') if 'selected="selected"' in row]
        assert len(selected) == len(value['owned'])

        selected_html = '\n'.join(selected)
        for entry in value['owned']:
            assert str(entry) in selected_html, (entry, selected_html)

    def test_autoincrement_single_primary_key(self):
        class EditUserForm(EditableForm):
            __entity__ = User

        test_form = EditUserForm()
        html = test_form.display()

        uid_input = self.get_line_in_text('name="user_id"', html)
        assert 'type="text"' in uid_input, html
        assert 'disabled' in uid_input, html

    def test_required_single_primary_key(self):
        class EditUserForm(EditableForm):
            __entity__ = User
            __require_fields__ = ['user_id']

        test_form = EditUserForm()
        html = test_form.display()

        uid_input = self.get_line_in_text('name="user_id"', html)
        assert 'type="text"' in uid_input, html
        assert 'disabled' in uid_input, html

    def test_compound_primary_key(self):
        class EditCompoundPrimaryKey(EditableForm):
            __entity__ = CompoundPrimaryKey

        test_form = EditCompoundPrimaryKey()
        html = test_form.display()

        name_input = self.get_line_in_text('name="name"', html)
        surname_input = self.get_line_in_text('name="surname"', html)
        assert 'type="text"' in name_input, name_input
        assert 'disabled' in name_input, name_input
        assert 'type="text"' in surname_input, surname_input
        assert 'disabled' in surname_input, surname_input


class TestDisabledForm(SproxTest):
    def setup(self):
        super(TestDisabledForm, self).setup()
        #setup_records(session)

        class UserForm(DisabledForm):
            __entity__ = User
            __limit_fields__ = ['user_name']

        self.base = UserForm(session)

    def test__widget__(self):
        rendered = self.base()
        assert 'name="user_name"' in rendered
        assert 'User Name' in rendered