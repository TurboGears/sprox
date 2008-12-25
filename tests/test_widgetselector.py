from nose.tools import raises
from tw.forms.fields import *
from tw.api import Widget
from sqlalchemy import Column, Integer
from sqlalchemy.types import *
from sqlalchemy.databases.oracle import *

from sprox.widgetselector import WidgetSelector, SAWidgetSelector
from sprox.widgets.widgets import *
from sprox.saormprovider import SAORMProvider

class TestWidgetSelector:
    def setup(self):
        self.widgetSelector = WidgetSelector()

    def test_createObj(self):
        pass

    def testSelect(self):
        assert self.widgetSelector.select('lala') == Widget

class DummySAWidgetSelector(SAWidgetSelector):
    default_name_based_widgets = {
        'goodGollyMissMolly':     TextField,
        }


class TestSAWidgetSelector:
    testColumns = (
    (BLOB,        FileField),
    (BOOLEAN,     SproxCheckBox),
    (Binary,      FileField),
    (Boolean,     SproxCheckBox),
    (CHAR(100),   TextField),
    (CLOB,        TextArea),
    (DATE,        SproxCalendarDatePicker),
    (DATETIME,    SproxCalendarDateTimePicker),
    (DECIMAL,     TextField),
    (Date,        SproxCalendarDatePicker),
    (DateTime,    SproxCalendarDateTimePicker),
    (FLOAT,       TextField),
    (Float,       TextField),
    (INT,         TextField),
    (Integer,     TextField),
    (Numeric,     TextField),
    (PickleType,  TextArea),
    (SMALLINT,    TextField),
    (SmallInteger,TextField),
    (String(100),TextField),
    (TEXT,        TextArea),
    (TIME,        SproxTimePicker),
    (Time,        SproxTimePicker),
    (TIMESTAMP,   SproxCalendarDateTimePicker),
    (Unicode(100),     TextField),
    (Unicode,     TextArea),
    (VARCHAR(100),     TextField),
    (OracleNumeric,      TextField),
    (OracleDate,         SproxCalendarDatePicker),
    (OracleDateTime,     SproxCalendarDateTimePicker),
    (OracleInteger,      TextField),
    (OracleSmallInteger, TextField),

    )

    def setup(self):
        self.widgetSelector = SAWidgetSelector()

    def test_createObj(self):
        pass

    def _testSelect(self, column, expected):
        widget = self.widgetSelector.select(column)
        assert widget == expected, "expected: %s\nactual: %s"%(expected, widget)

    def testSelect(self):
        for type, expected in self.testColumns:
            args={}
            if isinstance(type, Text):
                args['size'] = 100
            c = Column('asdf', type, args)
            yield self._testSelect, c, expected

    @raises(TypeError)
    def _select(self, arg1):
        self.widgetSelector.select(arg1)

    def testPasswordField(self):
        c = Column('password', String(100))
        self._testSelect(c, PasswordField)

    def testTextArea(self):
        c = Column('long_text', String(1000))
        self._testSelect(c, TextArea)

    def testNameBasedWidgetSelect(self):
        c = Column('goodGollyMissMolly', Integer)
        selector = DummySAWidgetSelector()
        widget = selector.select(c)
        assert widget is TextField
