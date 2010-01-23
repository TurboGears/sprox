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
        eq_(value['groups'], u'4')
        eq_(value['town'], 'Arvada')

    def test_get_value_with_binary_field(self):
        class ExampleFiller(TableFiller):
            __entity__ = Example
        example = Example(binary='datadatadata')
        session.add(example)

        filler = ExampleFiller(session)
        value = filler.get_value()
        eq_(value[0]['binary'], '&lt;file&gt;')

    def test_get_list_data_value_array_values(self):
        r = self.filler._get_list_data_value(User, ['something', 'something else'])
        assert r == ['something', 'something else'], r

    @raises(ConfigBaseError)
    def test_count_without_get(self):
        self.filler.get_count()

    def test_count(self):
        self.filler.get_value()
        c = self.filler.get_count()
        assert c == 1, c

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


