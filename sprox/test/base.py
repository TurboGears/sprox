from __future__ import unicode_literals

import os, re
from copy import copy
from sqlalchemy import *
from sqlalchemy.orm import *
from .model import *
from cgi import FieldStorage
from sprox._compat import unicode_text

try:
    from tw import framework
    framework.default_view = 'mako'
except ImportError:
    class DisplayOnlyWidget(object):
        """ToscaWidgets2 DisplayOnlyWidget"""

try:
    import tw2.core.core
    import tw2.core.middleware as tmw
    from tw2.core.widgets import DisplayOnlyWidgetMeta

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
    # Create a copy of the node without children
    new_node = copy(node)

    try:
        new_node._children = []
    except AttributeError:
        # On Python 3.3 it is not possible to change _children anymore
        for child in list(new_node):
            new_node.remove(child)

    if new_node.text and new_node.text.strip() == '':
        new_node.text = ''
    if new_node.tail and new_node.tail.strip() == '':
        new_node.tail = ''
    for child in node:
        if child is not None:
            child = remove_whitespace_nodes(child)
        new_node.append(child)
    return new_node

def remove_namespace(doc):
    """Remove namespace in the passed document in place."""
    for elem in doc:
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
    return needle_s.decode('utf-8')

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

def widget_is_type(widget, wtype):
    if hasattr(widget, 'req'):
        return issubclass(widget, wtype)
    else:
        return isinstance(widget, wtype)

def widget_children(w):
    if hasattr(w, 'req'):
        children = w.children
        if isinstance(w, DisplayOnlyWidgetMeta):
            children = w.child.children
        return dict(((c.key, c) for c in children))
    else:
        return w.children

def form_error_message(e):
    try:
        if e.widget.child.error_msg:
            return e.widget.child.error_msg
        return [c.error_msg for c in e.widget.child.children if c.error_msg is not None][0]
    except:
        return e.msg

database_setup=False
def setup_database():
    global session, engine, database_setup, connect, metadata

    #singletonizes things
    if not database_setup:
        engine = create_engine(os.environ.get('DBURL', 'sqlite://'))
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
    user.user_name = "asdf"
    user.display_name = 'Asd Sdf'
    user.email_address = "asdf@asdf.com"
    user.password = "asdf"
    session.add(user)

    arvada = Town(name='Arvada')
    session.add(arvada)
    session.flush()
    user.town = arvada

    session.add(Town(name='Denver'))
    session.add(Town(name='Golden'))
    session.add(Town(name='Boulder'))

    owner = WithoutNameOwner(data='owner')
    session.add(owner)
    session.add(WithoutName(data='Something', owner=owner))

    # This is for tests that need entities with two digits ids.
    otherowner = WithoutNameOwner(data='otherowner')
    session.add(otherowner)
    for i in range(20):
        owned = WithoutName(data='wno_%s' % i)
        if i >= 15:
            owned.owner = otherowner
        session.add(owned)

    #test_table.insert(values=dict(BLOB=FieldStorage('asdf', StringIO()).value)).execute()
    #user_reference_table.insert(values=dict(user_id=user.user_id)).execute()

#    print user.user_id
    for i in range (5):
        group = Group(group_name=unicode_text('Group %s' % i))
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
        if tmw and request_local:
            rl = request_local()
            rl.clear()
            rl['middleware'] = tmw.make_middleware(None)

        self.session = session
        self.engine = engine
        try:
            self.user = setup_records(session)
        except:
            self.session.rollback()

    def teardown(self):
        self.session.rollback()

    def get_line_in_text(self, line_content, text):
        for line in text.split('\n'):
            if line_content in line:
                return line.strip()
        return ''

if __name__ == '__main__':
    setupDatabase()
