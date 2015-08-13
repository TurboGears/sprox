from nose.tools import eq_, raises
import datetime as d
import sprox.util as u

        
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
