from sprox.test.base import setup_database, sorted_user_columns, SproxTest, User, Example
from nose.tools import raises, eq_

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()


