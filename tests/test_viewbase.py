from sprox.viewbase import ViewBase
from sprox.test.base import setup_database
from sprox.test.model import User
from sprox.sa.widgetselector import SAWidgetSelector
from nose.tools import raises, eq_

from tw.forms import TextField, HiddenField, Widget

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class DummyWidgetSelector(object):
    def select(self, *args, **kw):
        return TextField

class DummyMetadata(object):

    def __init__(self, provider, entity):
        self.entity = entity
        self.provider = provider

    def keys(self):
        return self.provider.get_fields(self.entity)

    def __getitem__(self, name):
        return self.provider.get_field(self.entity, name)

class DummyWidget(Widget):
    params = ['test_param']


class UserView(ViewBase):
    __entity__ = User
    __metadata_type__ = DummyMetadata
    __widget_selector__ = SAWidgetSelector()

class TestViewBase:
    def setup(self):
        self.base = UserView()

    def test_create(self):
        pass

    def test__fields__(self):
        eq_(['_password', 'created', 'display_name', 'email_address', 'groups', 'password', 'town', 'town_id', 'user_id', 'user_name'],
            sorted(self.base.__fields__))

    def test__widget__(self):
        eq_(None, self.base.__widget__())

    def test_widget_with_attrs(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __field_attrs__ = {'password':{'class':'mypassclass'}}
            __widget_selector_type__ = DummyWidgetSelector

        user_view = UserView()

        widget = user_view.__widget__
        child = widget.children['password']
        eq_(child.attrs, {'class':'mypassclass'})

    def test_hidden_fields(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __hide_fields__ = ['password']

        user_view = UserView()
        widget = user_view.__widget__
        child = widget.children['password']
        assert isinstance(child, HiddenField), child.__class__

    def test_custom_field(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __field_widgets__ = {'password':TextField(id='password')}


        user_view = UserView()
        widget = user_view.__widget__
        child = widget.children['password']
        assert isinstance(child, TextField), child.__class__

    def test_custom_with_none(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __add_fields__ = {'password':None}


        user_view = UserView()
        widget = user_view.__widget__
        child = widget.children['password']
        assert isinstance(child, Widget), str(child.__class__)

    def test_omit_fields(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __omit_fields__ = ['password']


        user_view = UserView()
        widget = user_view.__widget__
        assert 'password' not in widget.children.keys()

    def test_bad_fieldname_in_limit(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __limit_fields__ = ['junk']


        user_view = UserView()
        widget = user_view.__widget__
        assert 'junk' not in widget.children.keys()

    def test_widget_attrs(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __field_widget_args__ = {'password':{'test_param':'crazy_param'}}
            password = DummyWidget

        user_view = UserView()
        widget = user_view.__widget__
        assert widget.children['password'].test_param == 'crazy_param'

    def test_widget_attrs_hidden_field(self):
        class UserView(ViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __field_widget_args__ = {'password':{'css_classes':['crazy_param']}}
            __hide_fields__ = ['password']

        user_view = UserView()
        widget = user_view.__widget__
        assert widget.children['password'].css_classes == ['crazy_param'], widget.children['password'].css_classes

    def _test_enum_field(self):
        class EnumView(ViewBase):
            __entity__ = ModelWithEnum
            __metadata_type__ = DummyMetadata
        
        enum_view = EnumView()
        widget = enum_view.__widget__
        #assert widget.children['password'].css_classes == ['crazy_param'], widget.children['password'].css_classes
