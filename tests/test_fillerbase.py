from sprox.fillerbase import TableFiller, EditFormFiller, AddFormFiller, FormFiller
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, connection, trans
    session, engine, connection = setup_database()

class UserFiller(TableFiller):
    __entity__ = User

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
