#most of this file was taken from turbogears default template
from hashlib import sha1
import os
try:
    from hashlib import md5, sha1 as sha
except ImportError:
    import md5
    import sha
from datetime import datetime

from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, synonym_for

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata

# This is the association table for the many-to-many relationship between
# groups and permissions.
group_permission_table = Table('tg_group_permission', metadata,
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('permission_id', Integer, ForeignKey('tg_permission.permission_id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships.
user_group_table = Table('tg_user_group', metadata,
    Column('user_id', Integer, ForeignKey('tg_user.user_id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# auth model

class Group(DeclarativeBase):
    """An ultra-simple group definition.
    """
    __tablename__ = 'tg_group'

    group_id = Column(Integer, autoincrement=True, primary_key=True)
    group_name = Column(Unicode(16), unique=True, default='default group name')
    display_name = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    users = relation('User', secondary=user_group_table, backref='groups')

    def __repr__(self):
        return '<Group: name=%s>' % self.group_name

class Town(DeclarativeBase):
    __tablename__ = 'town'
    town_id = Column(Integer, primary_key=True)
    name = Column(String(32))

class User(DeclarativeBase):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    """
    __tablename__ = 'tg_user'

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(16), unique=True)
    email_address = Column(Unicode(255), unique=True, info={'title':True})
    display_name = Column(Unicode(255))
    _password = Column('password', Unicode(40))
    created = Column(DateTime, default=datetime.now)
    town_id = Column(Integer, ForeignKey('town.town_id'))
    town = relation(Town, backref=backref('residents'))

    def __repr__(self):
        return '<User: email="%s", display name="%s">' % (
                self.email_address, self.display_name)

    @property
    def permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, password):
        """encrypts password on the fly using the encryption
        algo defined in the configuration
        """
        #unfortunately, this causes coverage not to work
        #self._password = self._encrypt_password(algorithm, password)

    def _get_password(self):
        """returns password
        """
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                       _set_password))


class Permission(DeclarativeBase):
    """A relationship that determines what each Group can do
    """
    __tablename__ = 'tg_permission'

    permission_id = Column(Integer, autoincrement=True, primary_key=True)
    permission_name = Column(Unicode(16), unique=True)
    description = Column(Unicode(255))
    groups = relation(Group, secondary=group_permission_table, lazy='dynamic',
                      backref='permissions')

class Example(DeclarativeBase):
    __tablename__  = 'example'

    example_id      = Column(Integer, primary_key=True)
    created         = Column(DateTime, default=datetime.now)
    blob            = Column(BLOB          )
    binary          = Column(Binary        )
    boolean         = Column(Boolean       )
    char            = Column(CHAR(200)     )
    cLOB            = Column(CLOB(200)     )
    date_           = Column( DATE         )
    datetime_       = Column( DATETIME     )
    decimal         = Column(DECIMAL       )
    date            = Column(Date          )
    dateTime        = Column(DateTime      )
    float__         = Column( FLOAT        )
    float_          = Column(Float         )
    int_            = Column(INT           )
    integer         = Column(Integer, default=10)
    interval        = Column(Interval      )
   # (NCHAR =       #Column NCHAR          )
    numeric         = Column(Numeric       )
    pickletype      = Column(PickleType    )
    smallint        = Column(SMALLINT      )
    smalliunteger   = Column(SmallInteger  )
    string          = Column(String(20)    )
    text            = Column(TEXT(20)      )
    time_           = Column(TIME          )
    time            = Column(Time          )
    timestamp       = Column(TIMESTAMP     )
    unicode_        = Column(Unicode(200)  )
    varchar         = Column(VARCHAR(200)  )
    password        = Column(String(20)    )


class Department(DeclarativeBase):
    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))


class DocumentCategory(DeclarativeBase):
    __tablename__ = 'document_category'

    document_category_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.department_id'), primary_key=True)
    name = Column(Unicode(255))

    department = relation(Department, foreign_keys=[department_id])


document_category_tag_association_table = Table(
    'document_category_tag_assignment', metadata,
    Column('document_category_id', None, ForeignKey('document_category.document_category_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('department_id', None, ForeignKey('document_category.department_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('document_category_tag_id', None, ForeignKey('document_category_tag.document_category_tag_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
)


class DocumentCategoryTag(DeclarativeBase):
    __tablename__ = 'document_category_tag'

    document_category_tag_id = Column(Integer, primary_key=True)
    categories = relation(
        DocumentCategory,
        secondary=document_category_tag_association_table,
        primaryjoin=document_category_tag_id == document_category_tag_association_table.c.document_category_tag_id,
        secondaryjoin=and_(
            DocumentCategory.document_category_id == document_category_tag_association_table.c.document_category_id,
            DocumentCategory.department_id == document_category_tag_association_table.c.department_id
            ),
        backref='tags')


class DocumentCategoryReference(DeclarativeBase):
    __tablename__ = 'document_category_ref'
    # removed for sa 0.7 support
    #__table_args__ = (
    #    ForeignKeyConstraint(
    #        ['document_category_id','department_id'], ['document_category.document_category_id', 'document_category.department_id'])
    #)

    id = Column(Integer, primary_key=True)

    document_category_id = Column(Integer, ForeignKey('document_category.document_category_id'))
    department_id = Column(Integer, ForeignKey('document_category.department_id'))

    category = relation(DocumentCategory,
        primaryjoin=and_(
            document_category_id == DocumentCategory.document_category_id,
            department_id == DocumentCategory.department_id
            )
        )


class Document(DeclarativeBase):

    __tablename__ = 'document'
    document_id     = Column(Integer, primary_key=True)
    created         = Column(DateTime, default=datetime.now)
    blob            = Column(BLOB          )
    owner           = Column(Integer, ForeignKey('tg_user.user_id'))
    url             = Column(String(500))
    document_category_id = Column(None, ForeignKey('document_category.document_category_id'))

    def _get_address(self):
        return self.url

    def _set_address(self, value):
        self.url = value

    address = synonym('address', descriptor=property(_get_address,
                                                       _set_address))
    category = relation(DocumentCategory)


class File(DeclarativeBase):
    __tablename__ = 'attachments'

    file_id = Column(Integer, primary_key=True)
    data = Column(Binary)

    @synonym_for('data')
    @property
    def content(self):
        return self.data

class WithoutNameOwner(DeclarativeBase):
    __tablename__ = 'withoutname_owner'

    uid = Column(Integer, primary_key=True)
    data = Column(String(100))

class WithoutName(DeclarativeBase):
    __tablename__ = 'withoutname'

    class __sprox__(object):
        dropdown_field_names = {'owner': ['data']}

    uid = Column(Integer, primary_key=True)
    data = Column(String(100), info={'title': True})

    owner_id = Column(Integer, ForeignKey(WithoutNameOwner.uid))
    owner = relation('WithoutNameOwner', backref=backref('owned'))

class CompoundPrimaryKey(DeclarativeBase):
    __tablename__ = 'withoutname_compound'

    name = Column(String(100), primary_key=True)
    surname = Column(String(100), primary_key=True)
    age = Column(Integer)

#not supporting enums for now.
#ModelWithEnum=None
#if sa.__version__ >='0.6':
#    global ModelWithEnum
#    
#    class _ModelWithEnum(DeclarativeBase):
#        __tablename__ = 'model_with_enum'
        
#        model_with_enum_id = Column(Integer, primary_key=True)

        #taken directly from Mike's blog
#        enum = Enum('part_time', 'full_time', 'contractor', name='employee_types')
#    ModelWithEnum = _ModelWithEnum