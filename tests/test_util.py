from sprox.util import MultiDict
from nose.tools import eq_, raises
import datetime as d
import sprox.util as u

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
        
        
@raises(u.ConverterError)
def test_timestamp_bad():
    u.timestamp('bad')
    
def test_timestamp_timestamp():
    r = u.timestamp('2001-02-01 05:05:05.3')
    eq_(r, d.datetime(2001, 2, 1, 5, 5, 5, 300000))
    
def test_timestamp_no_hours():
    r = u.timestamp('2001-02-01')
    eq_(r, d.date(2001, 2, 1))

def test_timestamp_tz_sign():
    r = u.timestamp('2001-02-01 05:05:05.3 -5')
    eq_(r, d.datetime(2001, 2, 1, 10, 5, 5, 300000))
