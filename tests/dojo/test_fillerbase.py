from sprox.dojo.fillerbase import DojoTableFiller
from sprox.configbase import ConfigBaseError
from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User, Example
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()

class UserFiller(DojoTableFiller):
    __entity__ = User

class TestTableFiller(SproxTest):
    def setup(self):
        super(TestTableFiller, self).setup()
        self.filler = UserFiller(session)

    def test_create(self):
        pass

    def test_get_value(self):
        value = self.filler.get_value()
        eq_(len(value), 4)
        value = value['items'][0]
        eq_(value['groups'], u'4')
        eq_(value['town'], 'Arvada')

    def test_get_value_with_binary_field(self):
        class ExampleFiller(DojoTableFiller):
            __entity__ = Example
        example = Example(binary='datadatadata')
        session.add(example)

        filler = ExampleFiller(session)
        value = filler.get_value()
        eq_(value['items'][0]['binary'], '&lt;file&gt;')

    def test_get_value_with_orderby_desc(self):
        class ExampleFiller(DojoTableFiller):
            __entity__ = Example
        example = Example(binary='datadatadata')
        session.add(example)

        filler = ExampleFiller(session)
        value = filler.get_value(sort='-example_id')
        eq_(value['items'][0]['binary'], '&lt;file&gt;')

    @raises(ConfigBaseError)
    def _test_count_without_get(self):
        self.filler.get_count()

    def test_count(self):
        v = self.filler.get_value()
        c = self.filler.get_count()
        assert c == 1, v

