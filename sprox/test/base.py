import os
from sqlalchemy import *
from sqlalchemy.orm import *
from model import *
from cStringIO import StringIO
from cgi import FieldStorage

session = None
engine = None
connect = None

sorted_user_columns = ['_password', 'created', 'display_name', 'email_address',
                       'groups', 'password', 'sprox_id', 'town',
                       'town_id', 'user_id', 'user_name']

database_setup=False
def setup_database():
    global session, engine, database_setup, connect, metadata

    #singletonizes things
    if not database_setup:
        engine = create_engine(os.environ.get('DBURL', 'sqlite://'), strategy="threadlocal")
        connect = engine.connect()
    #    print 'testing on', engine
        metadata.bind = engine
        metadata.drop_all()
        metadata.create_all()

        Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
        session = Session()
        database_setup = True
    return session, engine, metadata

records_setup = None
def setup_records(session):


    session.expunge_all()

    user = User()
    user.user_name = u'asdf'
    user.email_address = u"asdf@asdf.com"
    user.password = u"asdf"
    session.add(user)

    arvada = Town(name=u'Arvada')
    session.add(arvada)
    session.flush()
    user.town = arvada

    session.add(Town(name=u'Denver'))
    session.add(Town(name=u'Golden'))
    session.add(Town(name=u'Boulder'))

    #test_table.insert(values=dict(BLOB=FieldStorage('asdf', StringIO()).value)).execute()
    #user_reference_table.insert(values=dict(user_id=user.user_id)).execute()

#    print user.user_id
    for i in range (5):
        group = Group(group_name=unicode(i))
        session.add(group)

    user.groups.append(group)

    session.flush()
    return user

def teardown_database():
    pass
    #metadata.drop_all()

def _reassign_from_metadata():
    global visits_table, visit_identity_table, groups_table, town_table
    global users_table, permissions_table, user_group_table
    global group_permission_table, test_table

    visits_table = metadata.tables['visit']
    visit_identity_table = metadata.tables['visit_identity']
    groups_table = metadata.tables['tg_group']
    town_table = metadata.tables['town_table']
    users_table = metadata.tables['tg_user']
    permissions_table = metadata.tables['permission']
    user_group_table = metadata.tables['user_group']
    group_permission_table = metadata.tables['group_permission']
    test_table = metadata.tables['test_table']

def setup_reflection():
    #if os.environ.get('AUTOLOAD', False):
    metadata.clear()
    metadata.reflect()
    _reassign_from_metadata()

    clear_mappers()
    tables = metadata.tables
    mapper(Town, tables['town_table'])
    mapper(Example, tables['test_table'])
    mapper(Visit, tables['visit'])
    mapper(VisitIdentity, tables['visit_identity'],
           properties=dict(users=relation(User, backref='visit_identity')))
    mapper(User, tables['tg_user'])
    mapper(Group, tables['tg_group'],
           properties=dict(users=relation(User,
                                          secondary=tables['user_group'],
                                          backref='groups')))
    mapper(Permission, tables['permission'],
           properties=dict(groups=relation(Group,
                                           secondary=tables['group_permission'],
                                           backref='permissions')))


class SproxTest(object):
    def setup(self):
        self.session = session
        self.engine = engine
        try:
            self.user = setup_records(session)
        except:
            self.session.rollback()
    def teardown(self):
        self.session.rollback()

if __name__ == '__main__':
    setupDatabase()
