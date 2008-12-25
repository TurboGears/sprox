from nose.tools import raises
from sprox.validatorselector import ValidatorSelector, SAValidatorSelector
from sprox.test.base import *
from tw.forms.validators  import *
from formencode.compound import All
from sqlalchemy import Column, Integer
from sqlalchemy.databases.oracle import *
from sprox.saormprovider import SAORMProvider
from types import NoneType

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
        assert self.validatorSelector.select('lala') == UnicodeString

class _TestSAValidatorSelector(SproxTest):
    testColumns = (
    (BLOB,        NoneType),
    (BOOLEAN,     NoneType),
    (Binary,      NoneType),
    (Boolean,     NoneType),
    (CHAR,        UnicodeString),
    (CLOB,        UnicodeString),
    (DATE,        DateValidator),
    (DATETIME,    DateValidator),
    (DECIMAL,     Number),
    (Date,        DateValidator),
    (DateTime,    DateValidator),
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
    (TIME,        DateValidator),
    (Time,        DateValidator),
    (TIMESTAMP,   DateValidator),
    (Unicode,     UnicodeString),
    (VARCHAR,     UnicodeString),
    (OracleNumeric,      Number),
    (OracleDate,         DateValidator),
    (OracleDateTime,     DateValidator),
    (OracleInteger,      Int),
    (OracleSmallInteger, Int),

    )

    def setup(self):
        super(TestSAValidatorSelector, self).setup()
        self.validatorSelector = SAValidatorSelector(provider)

    def test_createObj(self):
        pass

    def test_select(self):
        for type, expected in self.testColumns:
            args={}
            if isinstance(type, Text):
                args['size'] = 100
            c = Column('asdf', type, args)
            yield self._testSelect, c, expected

    def _test_select(self, column, expected):
        validator = self.validatorSelector.select(column)
        assert validator.__class__ == expected, "expected: %s\nactual: type: %s validator: %s"%(expected, column.type, validator.__type__)

    @raises(TypeError)
    def _select(self, arg1):
        self.validatorSelector.select(arg1)

    def test_select_bad(self):
        badInput = ('a', 1, {}, [], (), None, 1.2)
        for input in badInput:
            yield self._select, input

    def test_name_based_validator_select(self):
        c = Column('email_address', String)
        validator = self.validatorSelector.select(c)
        assert isinstance(validator, Email)

    def test_validator_selector_unique_field(self):
        c = Column('nana', String, unique=True)
        validator= self.validatorSelector.select(c, check_if_unique=True)
        assert type(validator) is All


