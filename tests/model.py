from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
metadata = MetaData()
from sqlalchemy.orm import scoped_session, sessionmaker

# Global session manager.  Session() returns the session object
# appropriate for the current web request.
Session = scoped_session(sessionmaker(autoflush=True, autocommit=False))

# The identity schema.
visits_table = Table('visit', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('created', DateTime, nullable=False, default=datetime.now),
    Column('expiry', DateTime),
    mysql_engine='innodb',

)

visit_identity_table = Table('visit_identity', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('user_id', Integer, ForeignKey('tg_user.user_id'), index=True),
    mysql_engine='innodb',

)

groups_table = Table('tg_group', metadata,
    Column('group_id', Integer, primary_key=True),
    Column('group_name', Unicode(16), unique=True),
    Column('display_name', Unicode(255)),
    Column('created', DateTime, default=datetime.now),
    mysql_engine='innodb',
)

town_table = Table('town_table', metadata,
    Column('town_id', Integer, primary_key=True),
    Column('name', Unicode(255)),
    mysql_engine='innodb',
)

users_table = Table('tg_user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', Unicode(16), unique=True),
    Column('email_address', Unicode(255), unique=True),
    Column('display_name', Unicode(255)),
    Column('password', Unicode(40)),
    Column('town_id', Integer, ForeignKey('town_table.town_id')),
    Column('created', DateTime, default=datetime.now),
    mysql_engine='innodb',

)

permissions_table = Table('permission', metadata,
    Column('permission_id', Integer, primary_key=True),
    Column('permission_name', Unicode(16), unique=True),
    Column('description', Unicode(255)),
    mysql_engine='innodb',

)

user_group_table = Table('user_group', metadata,
    Column('user_id', Integer, ForeignKey('tg_user.user_id')),
    Column('group_id', Integer, ForeignKey('tg_group.group_id')),
    mysql_engine='innodb',
)

group_permission_table = Table('group_permission', metadata,
    Column('group_id', Integer, ForeignKey('tg_group.group_id')),
    Column('permission_id', Integer, ForeignKey('permission.permission_id')),
    mysql_engine='innodb',
)
user_reference_table=Table('user_reference', metadata,
    Column('user_id',Integer,ForeignKey('tg_user.user_id'),primary_key=True),
    mysql_engine='innodb',
)
no_auto_increment_table=Table('no_auto_increment', metadata,
    Column('no_auto_increment_id',Integer,autoincrement=False,primary_key=True),
    mysql_engine='innodb',
)
test_table = Table('test_table', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('created', DateTime, default=datetime.now),
                   Column('BLOB',         BLOB          ),
                   Column('BOOLEAN_',      BOOLEAN       ),
                   Column('Binary',       Binary        ),
                   Column('Boolean',      Boolean       ),
                   Column('CHAR',         CHAR(200)     ),
                   Column('CLOB',         CLOB(200)     ),
                   Column('DATE_',         DATE          ),
                   Column('DATETIME_',     DATETIME      ),
                   Column('DECIMAL',      DECIMAL       ),
                   Column('Date',         Date          ),
                   Column('DateTime',     DateTime      ),
                   Column('FLOAT_',        FLOAT         ),
                   Column('Float',        Float         ),
                   Column('INT',          INT           ),
                   Column('Integer',      Integer, default=10),
        #           Column('NCHAR',        NCHAR         ),
                   Column('Numeric',      Numeric       ),
                   Column('PickleType',   PickleType    ),
                   Column('SMALLINT',     SMALLINT      ),
                   Column('SmallInteger', SmallInteger  ),
                   Column('String',       String(20)    ),
                   Column('TEXT',         TEXT(20)      ),
                   Column('TIME_',        TIME          ),
                   Column('Time',         Time          ),
                   Column('TIMESTAMP',    TIMESTAMP     ),
                   Column('Unicode',      Unicode(200)  ),
                   Column('VARCHAR',      VARCHAR(200)  ),
                   Column('Password',     String(20)    ),
)

class Example(object):
    pass

class Visit(object):
    def lookup_visit(cls, visit_key):
        return Visit.get(visit_key)
    lookup_visit = classmethod(lookup_visit)

class VisitIdentity(object):
    pass

class Group(object):
    """
    An ultra-simple group definition.
    """
    def __init__(self, group_name, display_name=u''):
        self.group_name = group_name
        self.display_name = display_name

class User(object):
    """
    Reasonably basic User definition. Probably would want additional
    attributes.
    """
    #def __init__(self, user_name=None,
    #             password=None,
    #             email=None):
    #    self.user_name = user_name
    #    self.password = password
    #    self.email = email
    @property
    def permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

class Permission(object):
    pass

class Town(object):
    def __init__(self, name):
        self.name = name

mapper( Town, town_table)
mapper( Example, test_table)
mapper( Visit, visits_table)
mapper( VisitIdentity, visit_identity_table,
          properties=dict(users=relation(User, backref='visit_identity')))
mapper( User, users_table, properties=dict(town=relation(Town)))
mapper( Group, groups_table,
          properties=dict(users=relation(User,secondary=user_group_table, backref='groups')))
mapper( Permission, permissions_table,
          properties=dict(groups=relation(Group,secondary=group_permission_table, backref='permissions')))
