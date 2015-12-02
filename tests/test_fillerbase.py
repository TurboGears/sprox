from sprox.fillerbase import FillerBase, TableFiller, EditFormFiller, AddFormFiller, FormFiller, ConfigBaseError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User, Example
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class UserFiller(TableFiller):
    __entity__ = User
    __possible_field_names__ = TableFiller.__possible_field_name_defaults__ + ['group_name']

class TestFillerBase(SproxTest):
    def setup(self):
        super(TestFillerBase, self).setup()
        class UserFiller(FillerBase):
            __entity__ = User

        self.filler = UserFiller(session)

    def test_get_value(self):
        value = self.filler.get_value()
        assert value =={}, value

class TestTableFiller(SproxTest):
    def setup(self):
        super(TestTableFiller, self).setup()
        self.filler = UserFiller(session)

    def test_create(self):
        pass

    def test_get_value(self):
        value = self.filler.get_value()
        eq_(len(value), 1)
        value = value[0]
        eq_(value['groups'], 'Group 4')
        eq_(value['town'], 'Arvada')

    def test_get_value_with_binary_field(self):
        class ExampleFiller(TableFiller):
            __entity__ = Example
        example = Example(binary=b'datadatadata')
        session.add(example)

        filler = ExampleFiller(session)
        value = filler.get_value()
        eq_(value[0]['binary'], '&lt;file&gt;')

    def test_get_list_data_value_array_values(self):
        r = self.filler._get_list_data_value('groups', ['something', 'something else'])
        assert r == 'something, something else', r

    def test_get_list_data_value_related_values(self):
        c, u = self.filler.__provider__.query(User, limit=1)
        u = u[0]
        r = self.filler._get_list_data_value('groups', u.groups)
        assert r == 'Group 4', r

    @raises(ConfigBaseError)
    def test_count_without_get(self):
        self.filler.get_count()

    def test_count(self):
        self.filler.get_value()
        c = self.filler.get_count()
        assert c == 1, c

    def test_possible_field_name_dict(self):
        class UserFiller(TableFiller):
            __entity__ = User
            __possible_field_names__ = {'groups': 'group_name'}
        filler = UserFiller(session)
        value = filler.get_value()
        eq_(value[0]['groups'], 'Group 4')

    def test_possible_field_name_list(self):
        class UserFiller(TableFiller):
            __entity__ = User
            __possible_field_names__ = ['_name']
        filler = UserFiller(session)
        value = filler.get_value()
        eq_(value[0]['groups'], 'Group 4')

    def test_possible_field_name_default(self):
        class UserFiller(TableFiller):
            __entity__ = User
            __possible_field_names__ = {}
        filler = UserFiller(session)
        value = filler.get_value()
        eq_(value[0]['groups'], 'Group 4')

    def test_get_value_multiargs_method(self):
        class FillerWithMethod(TableFiller):
            __entity__ = User
            def town(self, obj, town):
                return 'City of ' + town
        filler = FillerWithMethod(session)
        value = filler.get_value(values={'user_id':1}, town='Arvada')
        assert value[0]['town'] == 'City of Arvada', value[0]

class TestEditFormFiller(SproxTest):
    def setup(self):
        super(TestEditFormFiller, self).setup()
        self.filler = EditFormFiller(session)
        self.filler.__entity__ = User

    def test_create(self):
        pass

    def test_get_value(self):
        value = self.filler.get_value(values={'user_id':1})
        eq_(value['groups'], [5])
        eq_(value['town'], 1)

    def test_get_value_method(self):
        class FillerWithMethod(EditFormFiller):
            __entity__ = User
            def town(self, obj):
                return 'Unionville'
        filler = FillerWithMethod(session)
        value = filler.get_value(values={'user_id':1})
        assert value['town']== 'Unionville', value['town']

    def test_get_value_multiargs_method(self):
        class FillerWithMethod(EditFormFiller):
            __entity__ = User
            def town(self, obj, city):
                return city
        filler = FillerWithMethod(session)
        value = filler.get_value(values={'user_id':1}, city='Rome')
        assert value['town'] == 'Rome', value['town']


class TestAddFormFiller(SproxTest):
    def setup(self):
        super(TestAddFormFiller, self).setup()
        self.filler = AddFormFiller(session)
        self.filler.__entity__ = User

    def test_create(self):
        pass

    def test_get_value(self):
        value = self.filler.get_value(values={'user_id':1})
        eq_(value['user_id'], 1)


