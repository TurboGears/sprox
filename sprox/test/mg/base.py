from __future__ import unicode_literals

import os, re
from copy import copy
from sprox.test.mg import model_relational
from sprox.test.mg.model_relational import *
from sprox._compat import unicode_text

try:
    from ming import create_datastore
    def create_ming_datastore():
        return create_datastore(os.environ.get('MONGOURL', 'mongodb://127.0.0.1:27017/test_db'))
except ImportError:
    from ming import datastore as DS
    def create_ming_datastore():
        return DS.DataStore(master=os.environ.get('MONGOURL', 'mongodb://127.0.0.1:27017/'), database='test_db')

try:
    from tw import framework
    framework.default_view = 'mako'
except ImportError:
    pass

try:
    import tw2.core.core
    import tw2.core.middleware as tmw

    _request_local = {'middleware':tmw.make_middleware(None)}
    def request_local_tst():
        return _request_local

    tw2.core.core.request_local = request_local_tst
    from tw2.core.core import request_local
except ImportError:
    tmw = None
    request_local = None

#try:
import xml.etree.ElementTree as etree
#except ImportError:
#    import cElementTree as etree

session = None
engine = None
connect = None

sorted_user_columns = ['_password', 'created', 'display_name', 'email_address',
                       'groups', 'password', 'sprox_id', 'town',
                       'user_name']

def remove_whitespace_nodes(node):
    new_node = copy(node)
    new_node._children = []
    if new_node.text and new_node.text.strip() == '':
        new_node.text = ''
    if new_node.tail and new_node.tail.strip() == '':
        new_node.tail = ''
    for child in node.getchildren():
        if child is not None:
            child = remove_whitespace_nodes(child)
        new_node.append(child)
    return new_node

def remove_namespace(doc):
    """Remove namespace in the passed document in place."""
    for elem in doc.getiterator():
        match = re.match('(\{.*\})(.*)', elem.tag)
        if match:
            elem.tag = match.group(2)

def replace_escape_chars(needle):
    needle = needle.replace('&nbsp;', ' ')
    return needle

def fix_xml(needle):
    needle = replace_escape_chars(needle)
    needle_node = etree.fromstring(needle)
    needle_node = remove_whitespace_nodes(needle_node)
    remove_namespace(needle_node)
    needle_s = etree.tostring(needle_node)
    return needle_s

def in_xml(needle, haystack):
    needle_s, haystack_s = map(fix_xml, (needle, haystack))
    return needle_s in haystack_s

def eq_xml(needle, haystack):
    needle_s, haystack_s = map(fix_xml, (needle, haystack))
    return needle_s == haystack_s

def assert_in_xml(needle, haystack):
    assert in_xml(needle, haystack), "%s not found in %s"%(needle, haystack)

def assert_eq_xml(needle, haystack):
    assert eq_xml(needle, haystack), "%s does not equal %s"%(needle, haystack)

database_setup=False
def setup_database():
    global session, datastore, database_setup


    #singletonizes things
    if not database_setup:
        datastore = create_ming_datastore()
        session = model_relational.SproxTestClass.__mongometa__.session
        session.impl.bind = datastore

    #    print 'testing on', datastore
#        MappedClass.compile_all()
        database_setup = True
    return session, datastore, None

records_setup = None
def setup_records(session):

#    import ipdb; ipdb.set_trace()
    # clear test database before repopulating with data
    db = session.impl.db
    for coll in db.collection_names():
        if not coll.startswith("system."):
            db.drop_collection(coll)

    #session.ensure_indexes(User)
        
    user = User()
    user.user_name = 'asdf'
    user.email_address = "asdf@asdf.com"
    user.display_name = "asdf@asdf.com"
    user.password = "asdf"

    arvada = Town(name='Arvada', country='USA')
    session.flush()
    user.town_id = arvada._id

    Town(name='Denver', country='USA')
    Town(name='Golden', country='USA')
    Town(name='Boulder', country='USA')
    Town(name='Torino', country='Italy')

    #test_table.insert(values=dict(BLOB=FieldStorage('asdf', StringIO()).value)).execute()
    #user_reference_table.insert(values=dict(user_id=user.user_id)).execute()

#    print user.user_id
    for i in range (5):
        group = Group(group_name=unicode_text(i))

    user.groups = [group]

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
        if tmw and request_local:
            rl = request_local()
            rl.clear()
            rl['middleware'] = tmw.make_middleware(None)

        self.session = session
        self.engine = engine
        try:
            self.user = setup_records(session)
        except Exception as ex:
            try:
                self.session.close()
            except: pass
            raise ex
    def teardown(self):
        self.session.close()

if __name__ == '__main__':
    setupDatabase()
