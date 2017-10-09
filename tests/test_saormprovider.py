from __future__ import unicode_literals

from nose import SkipTest
from sprox.sa.provider import SAORMProvider
from sprox.test.base import setup_database, setup_records, SproxTest
from sprox.test.model import *
from sprox.sa.widgetselector import SAWidgetSelector
import sqlalchemy
from sqlalchemy.orm import mapper, lazyload
from sqlalchemy import MetaData, Table, Column, Integer
from sqlalchemy.engine import Engine
from nose.tools import raises, eq_
import datetime

from cgi import FieldStorage

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

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
        session.add(Department(department_id=1, name='Marketing'))
        session.add(Department(department_id=2, name='Accounting'))
        session.add(DocumentCategory(document_category_id=1, department_id=1, name='Brochure'))
        session.add(DocumentCategory(document_category_id=2, department_id=1, name='Flyer'))
        session.add(DocumentCategory(document_category_id=3, department_id=2, name='Balance Sheet'))
        session.add(Document(document_category_id=1, owner=1))
        session.add(Document(document_category_id=2, owner=1))
        session.add(Document(document_category_id=1, owner=2))
        session.add(Permission(permission_name='perm'))
        #session.add(DocumentRating(user_id=1, document_id=1, rating=5))
        self.provider.flush()


    def test_get_fields_with_func(self):
        eq_(self.provider.get_fields(lambda: Town), ['town_id', 'name', 'town_id', 'name', 'residents'])

    def test_isbinary_related(self):
        assert not self.provider.is_binary(User, 'groups')

    def test_isrelation_onproperty(self):
        assert not self.provider.is_relation(User, 'permissions')

    def test_is_query_not_a_query(self):
        assert self.provider.is_query(User, None) == False

    def test_is_query_with_dynamic(self):
        e = session.query(Permission).first()
        assert self.provider.is_query(Permission, e.groups) == True

    def test_isbinary_synonym(self):
        assert not self.provider.is_binary(User, 'password')
        assert self.provider.is_binary(File, 'content')

    def test_isstring(self):
        assert self.provider.is_string(User, 'email_address')
        assert not self.provider.is_string(User, 'groups')

    def test_isstring_synonym(self):
        assert self.provider.is_string(User, 'password')

    def test_binary_create(self):
        fs = FieldStorage()
        fs.file = BytesIO(b'fake_content')

        values = {'data':fs}
        self.provider.create(File, values)

    def test_binary_update(self):
        fs = FieldStorage()
        fs.file = BytesIO(b'fake_content')

        values = {'data':fs}
        entity = self.provider.create(File, values)

        values = {'data':fs, 'file_id':entity.file_id}
        self.provider.update(File, values)

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

    def test_get_primary_fields_multi(self):
        fields = self.provider.get_primary_fields(DocumentCategory)
        eq_(fields, ['document_category_id', 'department_id'])

    def test_get_primary_field_function(self):
        field = self.provider.get_primary_field(lambda: User)
        eq_(field, 'user_id')

    def test_get_view_field_name(self):
        field = self.provider.get_view_field_name(Group, ['name'])
        eq_(field, 'group_name')

    def test_get_view_field_name_with_title(self):
        """
        if it exists, saormprovider should use the 'title' info attribute to
        determine the title column
        """
        field = self.provider.get_view_field_name(User, ['name'])
        eq_(field, 'email_address')

    def test_get_view_field_name_not_found(self):
        field = self.provider.get_view_field_name(Group, [])
        eq_(field, 'group_id')

    def test_get_dropdown_options_fk(self):
        options = self.provider.get_dropdown_options(User, 'town')
        eq_(options, [(1, 'Arvada'), (2, 'Denver'), (3, 'Golden'), (4, 'Boulder')])

    def test_get_dropdown_options_fk_multi(self):
        options = self.provider.get_dropdown_options(Document, 'category')
        eq_(options, [('1/1', 'Brochure'), ('2/1', 'Flyer'), ('3/2', 'Balance Sheet')])

    def test_get_dropdown_options_join(self):
        options = self.provider.get_dropdown_options(User, 'groups')
        eq_(options, [(1, 'Group 0'), (2, 'Group 1'), (3, 'Group 2'), (4, 'Group 3'), (5, 'Group 4')])

    def test_get_dropdown_options_join_2(self):
        options = self.provider.get_dropdown_options(Group, 'users')
        eq_(options, [(1, 'asdf@asdf.com'),])

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

    def test_dictify_limit_fields(self):
        d = self.provider.dictify(self.user, fields=['user_name'])
        eq_(d['user_name'], 'asdf')
        eq_(list(d.keys()), ['user_name'])

    def test_dictify_omit_fields(self):
        d = self.provider.dictify(self.user, omit_fields=['password', '_password'])
        assert 'password' not in list(d.keys())
        assert '_password' not in list(d.keys())
        assert 'user_name' in list(d.keys())

    def test_dictify_dynamic_relation(self):
        e = session.query(Permission).first()
        d = self.provider.dictify(e)
        assert isinstance(d['groups'], list)

    def test_dictify_none(self):
        d = self.provider.dictify(None)
        eq_(d, {})

    def test_create(self):
        params = {'user_name': 'asdf2', 'password': 'asdf2',
                  'email_address': 'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)
        q_user = self.session.query(User).get(2)
        assert q_user == new_user

    def test_create_many_to_one_multi(self):
        params = {'category': '1/1'}
        new_ref = self.provider.create(DocumentCategoryReference, params)
        q_ref = self.session.query(DocumentCategoryReference).get(1)
        assert new_ref == q_ref

    def test_create_many_to_many_multi(self):
        params = {'categories': ['1/1', '1/2']}
        new_ratingref = self.provider.create(DocumentCategoryTag, params)
        q_ratingref = self.session.query(DocumentCategoryTag).get(1)
        assert new_ratingref == q_ratingref

    def test_query(self):
        c, r = self.provider.query(User, limit=20, offset=0)
        eq_(len(r), c)
        eq_(len(r), 1)

    def test_query_order_by(self):
        c, r = self.provider.query(Document, limit=20, offset=0, order_by='category')
        assert c > 1, r
        categories = [x.document_category_id for x in r]
        assert categories == list(sorted(categories))

    def test_query_order_by_desc(self):
        c, r = self.provider.query(Document, limit=20, offset=0, order_by='category', desc=1)
        assert c > 1, r
        categories = [x.document_category_id for x in r]
        assert categories == list(sorted(categories, reverse=True))

    def test_query_order_by_multiple(self):
        c, r = self.provider.query(Document, limit=20, offset=0, order_by=['category', 'owner'])
        assert c > 1, r
        categories = [(x.document_category_id, x.owner) for x in r]
        assert categories == list(sorted(categories))

        c, r = self.provider.query(Document, limit=20, offset=0, order_by=['owner', 'category'])
        categories = [(x.owner, x.document_category_id) for x in r]
        assert categories == list(sorted(categories)), (categories, list(sorted(categories)))

    def test_query_filters(self):
        cnt, r = self.provider.query(Town, filters={'name':'Golden'})
        eq_([t.name for t in r], ['Golden'])

    def test_query_filters_relations(self):
        cnt, r = self.provider.query(User, filters={'town':1})
        assert r[0].town.town_id == 1, r

    def test_query_filters_relations_many(self):
        cnt, r = self.provider.query(User, filters={'groups':[5]})
        assert r[0].groups[0].group_id == 5, r

    def test_query_filters_substring(self):
        cnt, r = self.provider.query(Town, filters={'name':'old'}, substring_filters=['name'])
        eq_([t.name for t in r], ['Golden'])

    def test_query_filters_substring_escaping(self):
        cnt, r = self.provider.query(Town, filters={'name':'o%l%d'}, substring_filters=['name'])
        eq_(r, [])

    def test_query_filters_substring_notstring(self):
        cnt, towns = self.provider.query(Town)
        cnt, r = self.provider.query(Town, filters={'town_id':towns[0].town_id}, substring_filters=['town_id'])
        eq_([t.name for t in r], [towns[0].name]), r
        cnt, r = self.provider.query(Town, filters={'town_id':'not-an-id'}, substring_filters=['town_id'])
        eq_(r, []), r

    def test_query_filters_substring_insensitive(self):
        cnt, r = self.provider.query(Town, filters={'name':'gold'}, substring_filters=['name'])
        eq_([t.name for t in r], ['Golden'])

    def test_query_filters_substring_disabled(self):
        cnt, r = self.provider.query(Town, filters={'name':'old'}, substring_filters=[])
        eq_(r, [])

    def test_query_filters_relations_search_many2one(self):
        cnt, r = self.provider.query(User, filters={'town': 'Arvada'},
                                     search_related=True)
        assert cnt == 1, r
        assert r[0].email_address == 'asdf@asdf.com', r

    def test_query_filters_relations_search_many2many(self):
        cnt, r = self.provider.query(Group, filters={'users': 'asdf@asdf.com'},
                                     search_related=True)
        assert cnt == 1, r
        assert r[0].group_name == 'Group 4', r

    def test_query_filters_relations_search_one2many(self):
        cnt, r = self.provider.query(Town, filters={'residents': 'asdf@asdf.com'},
                                     search_related=True)
        assert cnt == 1, r
        assert r[0].name == 'Arvada', r

    def test_query_filters_relations_substring_search_many2one(self):
        cnt, r = self.provider.query(User, filters={'town': 'Arv'},
                                     search_related=True, substring_filters=['town'])
        assert cnt == 1, r
        assert r[0].email_address == 'asdf@asdf.com', r

    def test_query_filters_relations_substring_search_many2many(self):
        cnt, r = self.provider.query(Group, filters={'users': 'asdf'},
                                     search_related=True, substring_filters=['users'])
        assert cnt == 1, r
        assert r[0].group_name == 'Group 4', r

    def test_query_filters_relations_substring_search_one2many(self):
        cnt, r = self.provider.query(Town, filters={'residents': 'asdf'},
                                     search_related=True, substring_filters=['residents'])
        assert cnt == 1, r
        assert r[0].name == 'Arvada', r

    def test_query_filters_relations_search_nonstring(self):
        cnt, r = self.provider.query(User, filters={'groups': 5},
                                     search_related=True)
        assert cnt == 1, r
        assert r[0].email_address == 'asdf@asdf.com', r

    def test_query_filters_relations_search_empty(self):
        cnt, r = self.provider.query(Town, filters={'residents': ''},
                                     search_related=True)
        assert cnt == 4, r

    def test_update(self):
        params = {'user_name': 'asdf2', 'password': 'asdf2',
                  'email_address': 'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)
        params['email_address'] = 'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['user_id'] = 2
        new_user = self.provider.update(User, params)
        q_user = self.session.query(User).get(2)
        eq_(new_user.email_address, 'asdf@asdf.commy')

    def test_update_omit(self):
        params = {'user_name': 'asdf2', 'password': 'asdf2',
                  'email_address': 'email@addy.com', 'groups':[1,4], 'town':2}
        new_user = self.provider.create(User, params)

        params = {}
        params['email_address'] = 'asdf@asdf.commy'
        params['created'] = '2008-3-30 12:21:21'
        params['user_id'] = 2
        new_user = self.provider.update(User, params, omit_fields=['email_address', 'groups'])
        q_user = self.session.query(User).get(2)

        eq_(q_user.email_address, 'email@addy.com')
        eq_([group.group_id for group in q_user.groups], [1,4])

    def test_get_default_values(self):
        assert {} == self.provider.get_default_values(User, {})

    def test_get_field_default(self):
        field = self.provider.get_field(Group, 'created')
        has_default, default_value = self.provider.get_field_default(field)
        assert has_default == True, default_value
        assert datetime.datetime.now().date() == default_value().date()

    def test_get(self):
        user = self.provider.get(User, params={'user_id':1})
        eq_(user['user_name'], 'asdf')

    def test_delete(self):
        # causes some kind of persistence error in SA 0.7 (rollback not working)
        # everything seems ok with SA 1.1.14, maybe it has been fixed

        sa_version = sqlalchemy.__version__
        if sa_version > '0.6.6' and sa_version < '1.1.14':
            raise SkipTest

        self.provider.delete(User, params={'user_id': 1})
        users = self.session.query(User).all()
        assert len(users) == 0
        # Tests twice for idempotence
        self.provider.delete(User, params={'user_id': 1})
        users = self.session.query(User).all()
        assert len(users) == 0

    def test_modify_params_for_datetimes(self):
        params = self.provider._modify_params_for_dates(Example, {'datetime_': '1978-8-29 12:34:56'})
        eq_(params,  {'datetime_': datetime.datetime(1978, 8, 29, 12, 34, 56)})

    def test_modify_params_for_dates(self):
        params = self.provider._modify_params_for_dates(Example, {'date_': '1978-8-29'})
        eq_(params,  {'date_': datetime.date(1978, 8, 29)})

    def test_modify_params_for_intervals(self):
        params = self.provider._modify_params_for_dates(Example, {'interval': '1 days, 3:20:01'})
        eq_(params,  {'interval': datetime.timedelta(days=1, hours=3, minutes=20, seconds=1)})

    def test_modify_params_for_relationships_params_with_instance_already(self):
        group = self.session.query(Group).get(1)
        params = {'groups':group}
        params = self.provider._modify_params_for_relationships(User, params)
        assert params['groups'] == [group], params

    def test_get_field_widget_args(self):
        a = self.provider.get_field_widget_args(User, 'groups', User.groups)
        eq_(a, {'nullable': False, 'provider': self.provider})

    def test_create_with_unicode_cast_to_int(self):
        self.provider.create(User, dict(user_id='34', user_name='something'))

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
        session.flush()
        user = session.query(User).get(1)
        assert user not in obj.users

    def test_create_relationships_remove_town(self):
        town = session.query(Town).first()

        self.user.town = town
        self.session.flush()

        self.provider.update(User, {'user_id':self.user.user_id, 'town':None})
        assert self.user.town is None
