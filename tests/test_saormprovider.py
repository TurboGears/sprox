from sprox.saormprovider import SAORMProvider
from sprox.test.base import setup_database, setup_records, SproxTest
from sprox.test.model import *
from sprox.widgetselector import SAWidgetSelector
from sqlalchemy.orm import mapper
from sqlalchemy import MetaData, Table, Column, Integer
from sqlalchemy.engine import Engine
from nose.tools import raises, eq_
import datetime

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()


class DummyEngine(Engine):
    def __init__(self):
        pass
    url = 'dummy!'

other_engine = DummyEngine()

other_metadata = MetaData(bind=other_engine)
class OtherClass(object):pass

other_table = Table('other_table', other_metadata,
                    Column('other_id', Integer, primary_key=True))
mapper(OtherClass, other_table)

class TestSAORMProvider(SproxTest):
    def setup(self):
        super(TestSAORMProvider, self).setup()
        self.provider = SAORMProvider(session)

    def test_get_fields_with_func(self):
        eq_(self.provider.get_fields(lambda: Town), ['town_id', 'name', 'town_id', 'name'])

    def test_create(self):
        pass

    def test_isbinary_related(self):
        assert not self.provider.is_binary(User, 'groups')

    def test_create_with_engine(self):
        provider = SAORMProvider(engine)
        assert provider.engine == engine

    def test_create_with_metadata(self):
        provider = SAORMProvider(metadata)
        assert provider.engine == engine

    def test_create_with_session(self):
        provider = SAORMProvider(session)
        assert provider.engine == engine

    def test_get_entity(self):
        entity = self.provider.get_entity('User')
        assert entity == User

    @raises(KeyError)
    def test_get_entity_non_matching_engine(self):
        entity = self.provider.get_entity('OtherClass')


    def test_get_primary_fields(self):
        fields = self.provider.get_primary_fields(User)
        eq_(fields, ['user_id'])

    def test_get_primary_field_function(self):
        field = self.provider.get_primary_field(lambda: User)
        eq_(field, 'user_id')

    def test_get_view_field_name(self):
        field = self.provider.get_view_field_name(User, ['name'])
        eq_(field, 'user_name')

    def test_get_view_field_name_not_found(self):
        field = self.provider.get_view_field_name(User, [])
        eq_(field, '_password')

    def test_get_dropdown_options_fk(self):
        options = self.provider.get_dropdown_options(User, 'town')
        eq_(options, [(1, u'Arvada'), (2, u'Denver'), (3, u'Golden'), (4, u'Boulder')])

    def test_get_dropdown_options_join(self):
        options = self.provider.get_dropdown_options(User, 'groups')
        eq_(options, [(1, u'0'), (2, u'1'), (3, u'2'), (4, u'3'), (5, u'4')])

    def test_get_dropdown_options_join_2(self):
        options = self.provider.get_dropdown_options(Group, 'users')
        eq_(options, [(1, u'asdf'),])

    def test_dropdown_options_warn(self):
        provider = SAORMProvider(metadata)
        options = provider.get_dropdown_options(User, 'town')
        eq_(options, [])

    def test_get_relations(self):
        relations = self.provider.get_relations(User)
        eq_(relations, ['town', 'groups'])

    def test_get_synonyms(self):
        synonyms = self.provider.get_synonyms(User)
        eq_(synonyms, ['password'])

    def test_dictify(self):
        d = self.provider.dictify(self.user)
        eq_(d['groups'], [5])
        eq_(d['user_name'], 'asdf')

    def test_dictify_none(self):
        d = self.provider.dictify(None)
        eq_(d, {})

    def test_create(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)
        q_user = self.session.query(User).get(2)
        assert q_user == new_user

    def test_query(self):
        r = self.provider.query(User, limit=20, offset=0)
        eq_(len(r), 2)

    def test_update(self):
        params = {'user_name':u'asdf2', 'password':u'asdf2', 'email_address':u'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)
        params['email_address'] = u'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['user_id'] = 2
        new_user = self.provider.update(User, params)
        q_user = self.session.query(User).get(2)
        eq_(new_user.email_address, u'asdf@asdf.commy')

    def test_get_default_values(self):
        assert {} == self.provider.get_default_values(User, {})

    def test_get(self):
        user = self.provider.get(User, params={'user_id':1})
        eq_(user['user_name'], 'asdf')

    def test_delete(self):
        user = self.provider.delete(User, params={'user_id':1})
        users = self.session.query(User).all()
        assert len(users) == 0

    def test_modify_params_for_dates(self):
        params = self.provider._modify_params_for_dates(Example, {'date_': '1978-8-29'})
        eq_(params,  {'date_': datetime.datetime(1978, 8, 29, 0, 0)})

    def test_modify_params_for_relationships_params_with_instance_already(self):
        group = self.session.query(Group).get(1)
        params = {'groups':group}
        params = self.provider._modify_params_for_relationships(User, params)
        assert params['groups'] == [group], params
    
    def test_create_relationships_with_wacky_relation(self):
        obj = session.query(Group).first()
        params = {'group_id':obj.group_id, 'users':1}
        self.provider.update(Group, params)
        user = session.query(User).get(1)
        assert user in obj.users

    def test_create_relationships_remove_groups(self):
        obj = session.query(Group).first()
        obj.users.append(self.user)
        self.provider.update(User, {'user_id':self.user.user_id, 'groups':[]})
        user = session.query(User).get(1)
        assert user not in obj.users
        
    def test_create_relationships_remove_town(self):
        town = session.query(Town).first()
        
        self.user.town = town
        self.session.flush()
        
        self.provider.update(User, {'user_id':self.user.user_id, 'town':None})
        assert self.user.town is None