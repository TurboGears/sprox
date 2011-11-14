from sprox.iprovider import IProvider
from nose.tools import raises, eq_
from sprox.test.base import User

class TestSAORMProvider:
    def setup(self):
        self.provider = IProvider()

    def test_create(self):
        pass

    @raises(NotImplementedError)
    def test_get_entity(self):
        entity = self.provider.get_entity('User')

    @raises(NotImplementedError)
    def test_get_field(self):
        entity = self.provider.get_field(User, 'asdf')

    @raises(NotImplementedError)
    def test_get_entities(self):
        entity = self.provider.get_entities()

    @raises(NotImplementedError)
    def test_get_fields(self):
        entity = self.provider.get_fields(User)

    @raises(NotImplementedError)
    def test_get_primary_fields(self):
        fields = self.provider.get_primary_fields(User)


    @raises(NotImplementedError)
    def test_is_relation(self):
        entity = self.provider.is_relation(User, 'asdf')

    @raises(NotImplementedError)
    def test_is_nullable(self):
        entity = self.provider.is_nullable(User, 'asdf')

    @raises(NotImplementedError)
    def test_get_primary_field_function(self):
        field = self.provider.get_primary_field(lambda: User)

    @raises(NotImplementedError)
    def test_get_view_field_name(self):
        field = self.provider.get_view_field_name(User, ['name'])

    @raises(NotImplementedError)
    def test_get_view_field_name_not_found(self):
        field = self.provider.get_view_field_name(User, [])

    @raises(NotImplementedError)
    def test_get_dropdown_options_fk(self):
        options = self.provider.get_dropdown_options(User, 'town')

    @raises(NotImplementedError)
    def test_get_dropdown_options_join(self):
        options = self.provider.get_dropdown_options(User, 'groups')

    @raises(NotImplementedError)
    def test_get_relations(self):
        relations = self.provider.get_relations(User)

    @raises(NotImplementedError)
    def test_get_obj(self):
        self.provider.get_obj(User, {})

    @raises(NotImplementedError)
    def test_query(self):
        self.provider.query(User)

    @raises(NotImplementedError)
    def test_is_binary(self):
        self.provider.is_binary(User, 'field')

    def test_get_field_widget_args(self):
        r= self.provider.get_field_widget_args(User, 'field', None)
        assert r == {}

    def test_is_unique(self):
        r= self.provider.is_unique(User, 'field', None)
        assert r == True

    def test_is_unique_field(self):
        r= self.provider.is_unique_field(User, 'field')
        assert r == False

    @raises(NotImplementedError)
    def test_relation_fields(self):
        self.provider.relation_fields(User, 'field')

    @raises(NotImplementedError)
    def test_dictify(self):
        self.provider.dictify(User)

#    @raises(NotImplementedError)
#    def test_get_synonyms(self):
#        synonyms = self.provider.get_synonyms(User)

#    @raises(NotImplementedError)
#    def test_dictify(self):
#        d = self.provider.dictify(self.user)

    @raises(NotImplementedError)
    def test_create(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)

    @raises(NotImplementedError)
    def test_update(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.update(User, params)

    @raises(NotImplementedError)
    def test_get_default_values(self):
        assert {} == self.provider.get_default_values(User, {})

    @raises(NotImplementedError)
    def test_get(self):
        user = self.provider.get(User, params={'user_id':1})

    @raises(NotImplementedError)
    def test_delete(self):
        user = self.provider.delete(User, params={'user_id':1})