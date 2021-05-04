from nose.tools import raises, eq_
from sprox.validatorselector import ValidatorSelector
from sprox.test.base import *

from sprox.sa.validatorselector import *
from sprox.sa.support import Binary, LargeBinary

from sqlalchemy import Column, Integer, String
from sprox.sa.provider import SAORMProvider
NoneType = type(None)

session = None
engine = None
connection = None
trans = None

def setup():
    global session, engine, connect, trans
    session, engine, connect = setup_database()

def teardown():
    global session, trans

provider = SAORMProvider(metadata=metadata)
class TestValidatorSelector(SproxTest):
    def setup(self):
        self.validatorSelector = ValidatorSelector()
        super(TestValidatorSelector, self).setup()

    def test_createObj(self):
        pass

    def testSelect(self):
        assert issubclass(self.validatorSelector.select('lala'), FEUnicodeString)

class TestSAValidatorSelector(SproxTest):
    testColumns = (
    (BLOB,        FileValidator),
    (BOOLEAN,     NoneType),
    (BINARY,      FileValidator),
    (Binary,      FileValidator),
    (LargeBinary, FileValidator),
    (Boolean,     NoneType),
    (CHAR,        UnicodeString),
    (CLOB,        UnicodeString),
    (DATE,        DateValidator),
    (DATETIME,    DateTimeValidator),
    (DECIMAL,     Number),
    (Date,        DateValidator),
    (DateTime,    DateTimeValidator),
    (FLOAT,       Number),
    (Float,       Number),
    (INT,         Int),
    (Integer,     Int),
    (Numeric,     Number),
    (PickleType,  UnicodeString),
    (SMALLINT,    Int),
    (SmallInteger,Int),
    (String,      UnicodeString),
    (TEXT,        UnicodeString),
    (TIME,        DateTimeValidator),
    (Time,        DateTimeValidator),
    (TIMESTAMP,   DateTimeValidator),
    (Unicode,     UnicodeString),
    (VARCHAR,     UnicodeString),
    )

    def setup(self):
        super(TestSAValidatorSelector, self).setup()
        self.validator_selector = SAValidatorSelector(provider)

    def test_createObj(self):
        pass

    def test_select(self):
        for type, expected in self.testColumns:
            args={}
            if isinstance(type, Text):
                args['size'] = 100
            c = Column('asdf', type, **args)
            yield self._test_select, c, expected

    def _test_select(self, column, expected):
        validator = self.validator_selector.select(column)
        assert isinstance(validator, expected) or issubclass(validator, expected), "got: %s, expected: %s"%(validator, expected)

    def test_name_based_validator_select(self):
        column = Column('email_address', String)
        validator = self.validator_selector.select(column)
        assert issubclass(validator, Email), validator
