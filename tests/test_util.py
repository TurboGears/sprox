from sprox.util import MultiDict
from nose.tools import eq_


class TestMultiDict:

    def setup(self):
        self.m = MultiDict()
        self.m['a'] = 1
        self.m['b'] = 2
        self.m['a'] = 3

    def test_create(self):
        pass

    def TestIteritems(self):
        actual = [(key, value) for key, value in self.m.iteritems()]
        eq_(actual, [('a', 1), ('a', 3), ('b', 2)])