from sprox.formbase import FormBase, AddRecordForm, DisabledForm, EditableForm, Field
from sprox.viewbase import ViewBaseError
from sprox.test.mg.base import setup_database, sorted_user_columns, SproxTest, setup_records, Example, Document, assert_in_xml
from sprox.metadata import FieldsMetadata
from nose.tools import raises, eq_
from formencode import Invalid, Schema
from formencode.validators import FieldsMatch, NotEmpty, OpenId
from tw.forms import PasswordField, TextField, validators as twv
from sprox.widgetselector import WidgetSelector, EntityDefWidget, EntityDefWidgetSelector, RecordFieldWidget, RecordViewWidgetSelector
from sprox.mg.provider import MingProvider
from sprox.mg.widgetselector import MingWidgetSelector
from sprox.mg.validatorselector import MingValidatorSelector
from sprox.tablebase import TableBase
from strainer.operators import assert_in_xhtml

from sprox.test.mg.model import User, Group, Department, DocumentCategory, File, DocumentCategoryTag, DocumentCategoryReference, Town, UnrelatedDocument
from sprox.test.mg.model import Permission, TGMMUser
import formencode.validators as v

from cgi import FieldStorage
from StringIO import StringIO

from bson.objectid import InvalidId

from ming import schema as S
from ming.orm import FieldProperty

from tw.forms.fields import *
from sprox.widgets.widgets import *

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

#   Expected failure; requires many-to-many support
    @raises(AssertionError)
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

#   Expected failure; requires many-to-many support
    @raises(AssertionError)
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

#   Expected failure; requires many-to-many support
    @raises(AssertionError)
    def test_entity_with_dropdown_field_names_title(self):
        class GroupFormFieldNames(FormBase):
            __entity__ = Group
            __dropdown_field_names__ = {'groups':'group_name'}
        form = GroupFormFieldNames(session)
        rendered = form()
        assert_in_xml("""<select name="users" class="propertymultipleselectfield" id="users" multiple="multiple" size="5">
        <option value="1">asdf@asdf.com</option>
</select>""", rendered)

#   Expected failure; requires many-to-many support
    @raises(AssertionError)
    def test_entity_with_dropdown_field_names_title_overridden(self):
        class GroupFormFieldNames(FormBase):
            __entity__ = Group
            __dropdown_field_names__ = {'users':'user_name'}
        form = GroupFormFieldNames(session)
        rendered = form()
        assert_in_xml("""<select name="users" class="propertymultipleselectfield" id="users" multiple="multiple" size="5">
        <option value="1">asdf</option>
</select>""", rendered)

#   Expected failure; requires many-to-many support
    @raises(AssertionError)
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
        r = example_form({'boolean':"asdf"})
        assert "checkbox" in r, r

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

# WidgetSelector tests

class TestWidgetSelector:
    def setup(self):
        self.widgetSelector = WidgetSelector()

    def test_createObj(self):
        pass

    def testSelect(self):
        assert self.widgetSelector.select('lala') == Widget
        

class DummyMingWidgetSelector(MingWidgetSelector):
    default_name_based_widgets = {
        'goodGollyMissMolly':     TextField,
        }

class TestEntityDefWidgetSelector:
    def setup(self):
        self.selector = EntityDefWidgetSelector()

    def test_select(self):
        r = self.selector.select('something')
        eq_(r, EntityDefWidget)

class TestRecordViewWidgetSelector:
    def setup(self):
        self.selector = RecordViewWidgetSelector()

    def test_select(self):
        r = self.selector.select('something')
        eq_(r, RecordFieldWidget)

class TestMingWidgetSelector:

    testColumns = (
    (S.Binary,    FileField),
    (S.Bool,      SproxCheckBox),
    (S.String,    TextField),
    (S.DateTime,  SproxCalendarDateTimePicker),
    (S.Float,     TextField),
    (S.Int,       TextField),
    (S.OneOf,     PropertySingleSelectField),
    )

    def setup(self):
        self.widgetSelector = MingWidgetSelector()

    def test_createObj(self):
        pass

    def _testSelect(self, column, expected):
        widget = self.widgetSelector.select(column)
        assert widget == expected, "expected: %s\nactual: %s"%(expected, widget)

    def testSelect(self):
        for type, expected in self.testColumns:
            args={}
            c = FieldProperty(type, **args)
            yield self._testSelect, c, expected

    def test_select_with_one_relation(self):
        eq_(self.widgetSelector.select(User.town), PropertySingleSelectField)

    def test_select_with_many_relation(self):
        eq_(self.widgetSelector.select(User.groups), PropertyMultipleSelectField)
    
    def test_select_with_password(self):
        eq_(self.widgetSelector.select(UnrelatedDocument.password), PasswordField)

    def test_name_based_selector(self):
        class NamedSelector(MingWidgetSelector):
            default_name_based_widgets = {'number':SingleSelectField}
        sel = NamedSelector()
        eq_(sel.select(UnrelatedDocument.number), SingleSelectField)

    def test_unknown_field_type(self):
        eq_(self.widgetSelector.select(UnrelatedDocument.something), TextField)

    @raises(TypeError)
    def _select(self, arg1):
        self.widgetSelector.select(arg1)

    def testPasswordField(self):
        c = FieldProperty(S.String)
        c.sprox_meta = {"password": True}
        self._testSelect(c, PasswordField)

    def testTextArea(self):
        c = FieldProperty(S.String)
        c.sprox_meta = {"narrative": True}
        self._testSelect(c, TextArea)

    def testNameBasedWidgetSelect(self):
        c = FieldProperty(S.Int)
        selector = DummyMingWidgetSelector()
        widget = selector.select(c)
        assert widget is TextField


class TestMingValidatorSelector:

    def setup(self):
        self.selector = MingValidatorSelector()

    def test_select_with_one_relation(self):
        eq_(self.selector.select(User.town), twv.UnicodeString)

# tablebase tests

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
                   <th  class="col_1">town</th>
                   <th  class="col_2">display_name</th>
                   <th  class="col_3">created</th>
                   <th  class="col_4">user_name</th>
                   <th  class="col_5">town_id</th>
                   <th  class="col_6">groups</th>
                   <th  class="col_7">_password</th>
                   <th  class="col_8">_id</th>
                   <th  class="col_9">email_address</th>
           </tr>
       </thead>""", rendered)

# provider tests

class TestMGORMProvider(SproxTest):
    def setup(self):
        super(TestMGORMProvider, self).setup()
        self.provider = MingProvider(User.__mongometa__.session)
        Department(_id=1, name=u'Marketing')
        Department(_id=2, name=u'Accounting')
        DocumentCategory(_id=1, department_id=1, name=u'Brochure')
        DocumentCategory(_id=2, department_id=1, name=u'Flyer')
        DocumentCategory(_id=3, department_id=2, name=u'Balance Sheet')
        #session.add(DocumentRating(user_id=1, document_id=1, rating=5))
        session.flush_all()
        #session.close_all()
        self.asdf_user_id = self.provider.get_obj(User, {'user_name': 'asdf'})._id

    def test_get_field_widget_args(self):
        eq_(self.provider.get_field_widget_args(User, 'groups', User.groups), {'nullable': True, 'provider':self.provider})

    def test_get_fields_with_func(self):
        eq_(self.provider.get_fields(lambda: Town), ['_id', 'users', 'name'])

    def test_isbinary_related(self):
        assert not self.provider.is_binary(User, 'groups')

    def test_binary_create(self):
        fs = "fake_content"

        values = {'data':fs}
        self.provider.create(File, values)
        session.flush()

    def test_binary_update(self):
        fs = "fake_content"

        values = {'data':fs}
        entity = self.provider.create(File, values)

        session.flush()
        values = {'data':fs, '_id':entity._id}
        self.provider.update(File, values)

    def test_get_entity(self):
        entity = self.provider.get_entity('User')
        assert entity == User, entity

    def test_get_entities(self):
        entities = self.provider.get_entities()
        assert set(entities) == set(['Town', 'GroupPermission', 'Group', 'Permission', 'DocumentCategoryReference',
                'SproxTestClass', 'DocumentCategoryTag', 'DocumentCategoryTagAssignment', 'User', 'File', 'TGMMUser',
                'DocumentCategory', 'Department', 'Document', 'MappedClass', 'Example', 'UserGroup', 'UnrelatedDocument'])

    @raises(KeyError)
    def test_get_entity_non_matching_engine(self):
        entity = self.provider.get_entity('OtherClass')


    def test_get_primary_fields(self):
        fields = self.provider.get_primary_fields(User)
        eq_(fields, ['_id'])

    # expected failure; need compound primary key support
    @raises(AssertionError)
    def test_get_primary_fields_multi(self):
        fields = self.provider.get_primary_fields(DocumentCategory)
        eq_(fields, ['document_category_id', 'department_id'])

    def test_get_primary_field_function(self):
        field = self.provider.get_primary_field(lambda: User)
        eq_(field, '_id')

    def test_get_view_field_name_defaults_substring(self):
        field = self.provider.get_view_field_name(Permission, None)
        eq_(field, 'permission_name')

    def test_get_view_field_name_with_title(self):
        """
        if it exists, orm provider should use the 'title' info attribute to
        determine the title column
        """
        field = self.provider.get_view_field_name(User, ['name'])
        eq_(field, 'display_name')

    def test_get_view_field_name_not_found(self):
        field = self.provider.get_view_field_name(Group, [])
        assert field in self.provider.get_fields(Group)

    def test_get_dropdown_options_oneof(self):
        options = self.provider.get_dropdown_options(Example, 'oneof')
        eq_(set(options), set(set([('three', 'three'), ('one', 'one'), ('two', 'two')])))

    @raises(NotImplementedError)
    def test_get_dropdown_options_bad_fieldtype(self):
        class BadClass(object):
            pass
        bc = BadClass()
        options = self.provider.get_dropdown_options(BadClass, None)

    @raises(NotImplementedError)
    def test_get_dropdown_options_bad_type(self):
        options = self.provider.get_dropdown_options(Example, 'int_')

    @raises(NotImplementedError)
    def test_get_dropdown_options_bad_field(self):
        options = self.provider.get_dropdown_options(User, 'town_id')

    def test_get_dropdown_options_fk(self):
        options = self.provider.get_dropdown_options(User, 'town')
        for _id, name in options:
            town = Town.query.find({'name':name}).first()
            assert str(town._id) == str(_id)

    def test_get_dropdown_options_fk_multi(self):
        options = self.provider.get_dropdown_options(Document, 'category')
        eq_(set(options), set((('1', u'Brochure'), ('2', u'Flyer'), ('3', u'Balance Sheet'))))

    # expected failure; need many-to-many support
    @raises(AssertionError)
    def test_get_dropdown_options_join(self):
        options = self.provider.get_dropdown_options(User, 'groups')
        eq_(options, [('1', u'0'), ('2', u'1'), ('3', u'2'), ('4', u'3'), ('5', u'4')])

    # expected failure; need many-to-many support
    @raises(AssertionError)
    def test_get_dropdown_options_join_2(self):
        options = self.provider.get_dropdown_options(Group, 'users')
        eq_(options, [(1, u'asdf@asdf.com'),])

    def test_get_relations(self):
        relations = self.provider.get_relations(User)
        eq_(relations, ['town', 'groups'])

    def test_dictify(self):
        d = self.provider.dictify(self.user)
        eq_(d['user_name'], 'asdf')

    def test_dictify_limit_fields(self):
        d = self.provider.dictify(self.user, fields=['user_name'])
        eq_(d['user_name'], 'asdf')
        eq_(d.keys(), ['user_name'])

    def test_dictify_omit_fields(self):
        d = self.provider.dictify(self.user, omit_fields=['password', '_password'])
        assert 'password' not in d.keys()
        assert '_password' not in d.keys()
        assert 'user_name' in d.keys()

    def test_dictify_none(self):
        d = self.provider.dictify(None)
        eq_(d, {})

    # expected failure; ming does not yet support writing into RelationProperties
    @raises(TypeError)
    def test_create(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)
        assert q_user == new_user

    def test_create_blank__id(self):
        params = {'user_name':u'asdf3', 'password':u'asdf3', 'email_address':u'email111@addy.com', '_id':''}
        new_user = self.provider.create(User, params)
        q_user = self.provider.get(User, {'user_name':u'asdf3'})
        assert q_user is not None

    # expected failure; needs many-to-many support
    @raises(InvalidId)
    def test_create_many_to_one_multi(self):
        params = {'category': '1/1'}
        new_ref = self.provider.create(DocumentCategoryReference, params)
        q_ref = self.session.query(DocumentCategoryReference).get(1)
        assert new_ref == q_ref

    # expected failure; needs many-to-many support
    @raises(InvalidId)
    def test_create_many_to_many_multi(self):
        params = {'categories': ['1/1', '1/2']}
        new_ratingref = self.provider.create(DocumentCategoryTag, params)
        q_ratingref = self.session.query(DocumentCategoryTag).get(1)
        assert new_ratingref == q_ratingref

    def test_query(self):
        r = self.provider.query(User, limit=20, offset=0)
        eq_(len(r), 2)

    def test_query_offset_None(self):
        r = self.provider.query(User, limit=20, offset=None)
        eq_(len(r), 2)

    def test_query_with_offset(self):
        r = self.provider.query(User, offset=10)
        eq_(len(r), 2)

    def test_query_limit_None(self):
        r = self.provider.query(User, limit=None, offset=None)
        eq_(len(r), 2)

    def test_query_limit(self):
        count, r = self.provider.query(User, limit=1)
        eq_(len(r), 1)

    def test_query_sort_asc(self):
        cnt, r = self.provider.query(Town, order_by="name")
        eq_([t.name for t in r], [u'Arvada', u'Boulder', u'Denver', u'Golden'])

    def test_query_sort_desc(self):
        cnt, r = self.provider.query(Town, order_by="name", desc=True)
        eq_([t.name for t in r], [u'Golden', u'Denver', u'Boulder', u'Arvada'])

    def test_query_filters(self):
        cnt, r = self.provider.query(Town, filters={'name':'Golden'})
        eq_([t.name for t in r], [u'Golden']), r

    # expected failure; needs updatable RelationProperty
    @raises(TypeError)
    def test_update(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['_id'] = new_user._id
        new_user = self.provider.update(User, params)
        q_user = User.query.find({ "_id": new_user._id }).first()
        eq_(new_user.email_address, u'asdf@asdf.commy')
        eq_(q_user.email_address, u'asdf@asdf.commy')

    def test_update_simple(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com'}
        new_user = self.provider.create(User, params)
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['_id'] = new_user._id
        session.flush()
        new_user = self.provider.update(User, params)
        q_user = User.query.find({ "_id": new_user._id }).first()
        eq_(new_user.email_address, u'asdf@asdf.commy')
        eq_(q_user.email_address, u'asdf@asdf.commy')

    def test_update_sprox_id(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'sprox_id': 'xyz'}
        new_user = self.provider.create(User, params)
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['_id'] = new_user._id
        session.flush()
        new_user = self.provider.update(User, params)
        q_user = User.query.find({ "_id": new_user._id }).first()
        eq_(new_user.email_address, u'asdf@asdf.commy')
        eq_(q_user.email_address, u'asdf@asdf.commy')

    def test_update_method(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', '_method': 'xyz'}
        new_user = self.provider.create(User, params)
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['_id'] = new_user._id
        session.flush()
        new_user = self.provider.update(User, params)
        q_user = User.query.find({ "_id": new_user._id }).first()
        eq_(new_user.email_address, u'asdf@asdf.commy')
        eq_(q_user.email_address, u'asdf@asdf.commy')

    def test_update_extra_keys(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'extraneous': 'xyz'}
        new_user = self.provider.create(User, params)
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['_id'] = new_user._id
        session.flush()
        new_user = self.provider.update(User, params)
        q_user = User.query.find({ "_id": new_user._id }).first()
        eq_(new_user.email_address, u'asdf@asdf.commy')
        eq_(q_user.email_address, u'asdf@asdf.commy')

    def test_create_one_to_many_relation(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'extraneous': 'xyz'}
        new_user = self.provider.create(User, params)
        session.flush()

        #One-To-Many relations are not writable in Ming, we ensure that we do not have a crash when one is set
        new_town = self.provider.create(Town, {'users':[new_user._id]})
        assert new_town.users == []

    @raises(TypeError)
    def test_relation_fields_invalid(self):
        self.provider.relation_fields(User, "_id")

    def test_relation_fields_tgmm(self):
        relation_fields = self.provider.relation_fields(TGMMUser, 'groups')
        assert relation_fields == []

    # expected failure; needs updatable RelationProperty
    @raises(TypeError)
    def test_update_omit(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)

        params = {}
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['_id'] = 2
        new_user = self.provider.update(User, params, omit_fields=['email_address', 'groups'])
        q_user = self.session.query(User).get(2)

        eq_(q_user.email_address, u'email@addy.com')
        eq_([group.group_id for group in q_user.groups], [1,4])

    def test_get_default_values(self):
        assert {} == self.provider.get_default_values(User, {})

    def test_get(self):
        user = self.provider.get(User, params={'_id': self.asdf_user_id})
        eq_(user['user_name'], 'asdf')

    def test_delete(self):
        user = self.provider.delete(User, params={'_id': self.asdf_user_id})
        session.flush()
        users = User.query.find().all()
        assert len(users) == 0

    def test_create_with_DateTime(self):
        self.provider.create(Document, dict(edited='2011-03-30 12:21:21'))

    def test_create_with_int(self):
        self.provider.create(UnrelatedDocument, dict(number=5))

    def test_create_with_bool(self):
        self.provider.create(UnrelatedDocument, dict(enabled=True))

    def test_create_with_str_bool(self):
        self.provider.create(UnrelatedDocument, dict(enabled='true'))

    def test_create_relationships_with_wacky_relation(self):
        obj = Group.query.find().first()
        user = User.query.find().first()
        self.provider.update(Group, {'_id':obj._id, 'users':[user._id]})
        assert user._id == obj.users[0].user_id

    def test_create_relationships_remove_groups(self):
        obj = Group.query.find().first()
        self.provider.update(User, {'_id':self.user._id, 'groups':[]})
        assert user not in obj.users

    def test_create_relationships_change_town(self):
        town = Town.query.find({'name':'Arvada'}).first()

        self.user.town = town
        self.session.flush()

        self.provider.update(User, {'_id':self.user._id, 'town':Town.query.find({'name':'Denver'}).first()})
        assert self.user.town.name == 'Denver'

    def test_tgmanymany_create(self):
        count, groups = self.provider.query(Group, limit=1)
        params = {'user_name':u'mmuser', 'groups':[groups[0]]}
        new_user = self.provider.create(TGMMUser, params)

        assert new_user.groups[0].group_name == groups[0].group_name
        assert new_user._groups[0] == groups[0].group_name

    def test_tgmanymany_update(self):
        params = {'user_name':u'mmuser', 'groups':[]}
        new_user = self.provider.create(TGMMUser, params)

        assert len(new_user.groups) == 0
        count, groups = self.provider.query(Group, limit=1)
        self.provider.update(TGMMUser, {'_id':new_user._id, 'groups':[groups[0]]})

        new_user = self.provider.get_obj(TGMMUser, {'_id':new_user._id})
        assert len(new_user.groups) == 1
        assert new_user.groups[0].group_name == groups[0].group_name
        assert new_user._groups[0] == groups[0].group_name


#dojo tests
from sprox.dojo.formbase import DojoAddRecordForm, DojoEditableForm, DojoFormBase

# tablebase tests

class DojoUserForm(DojoFormBase):
    __entity__ = User

class DojoUserEditableForm(DojoEditableForm):
    __entity__ = User

class DojoUserAddRecordForm(DojoAddRecordForm):
    __entity__ = User

class TestDojoForms:
    def setup(self):
        pass 

    def test_formbase(self):
        base = DojoUserForm(session)
        rendered = base.__widget__()
        assert_in_xhtml("""<tr class="odd" id="email_address.container" title="" >
               <td class="labelcol">
                   <label id="email_address.label" for="email_address" class="fieldlabel">Email Address</label>
               </td>
               <td class="fieldcol" >
                   <input type="text" id="email_address" class="textfield" name="email_address" value="" />
               </td>
           </tr>""", rendered)

    def test_addrecord(self):
        base = DojoUserAddRecordForm(session)
        rendered = base.__widget__()
        assert_in_xhtml("""<tr class="odd" id="email_address.container" title="" >
               <td class="labelcol">
                   <label id="email_address.label" for="email_address" class="fieldlabel">Email Address</label>
               </td>
               <td class="fieldcol" >
                   <input type="text" id="email_address" class="textfield" name="email_address" value="" />
               </td>
           </tr>""", rendered)

    def test_editableform(self):
        base = DojoUserEditableForm(session)
        rendered = base.__widget__()
        assert_in_xhtml("""<tr class="odd" id="email_address.container" title="" >
               <td class="labelcol">
                   <label id="email_address.label" for="email_address" class="fieldlabel">Email Address</label>
               </td>
               <td class="fieldcol" >
                   <input type="text" id="email_address" class="textfield" name="email_address" value="" />
               </td>
           </tr>""", rendered)

