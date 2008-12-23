"""
widgetselecter Module

this contains the class which allows the ViewConfig to select the appropriate widget for the given field

Classes:
Name                               Description
WidgetSelecter                     Parent Class
SAWidgetSelector                   Selecter Based on sqlalchemy field types
DatabaseViewWidgetSelector         Database View always selects the same widget
TableDefWidgetSelector             Table def fields use the same widget

Exceptions:
None

Functions:
None


Copyright (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007Database
Released under MIT license.
"""
from sqlalchemy.schema import Column
from sqlalchemy.types import *
from sqlalchemy.orm import PropertyLoader

from tw.api import Widget
from tw.forms.fields import *

from sprox.widgets import *


class WidgetSelector:
    def select(self, field):
        return Widget

class EntitiesViewWidgetSelector(WidgetSelector):
    def select(self, field):
        return EntityLabelWidget

class EntityDefWidgetSelector(WidgetSelector):
    def select(self, field):
        return EntityDefWidget

class RecordViewWidgetSelector(WidgetSelector):
    def select(self, field):
        return RecordFieldWidget

text_field_limit=100

class SAWidgetSelector(WidgetSelector):

    default_widgets = {
    String:   TextField,
    Integer:  TextField,
    Numeric:  TextField,
    DateTime: SproxCalendarDateTimePicker,
    Date:     SproxCalendarDatePicker,
    Time:     SproxTimePicker,
    Binary:   FileField,
    PickleType: TextField,
    Boolean: SproxCheckBox,
#    NullType: TextField
    }

    default_name_based_widgets = {}

    def _get_select_widget(self, field):
        return ForeignKeySingleSelectField

    def select(self, field):

        if isinstance(field, PropertyLoader):
            if field.secondary:
                return PropertyMultipleSelectField
            return PropertySingleSelectField

        if field.name in self.default_name_based_widgets:
            return self.default_name_based_widgets[field.name]

        if field.name.lower() == 'password':
            return PasswordField

        type_ = String
        for t in self.default_widgets.keys():
            if isinstance(field.type, t):
                type_ = t
                break

        widget = self.default_widgets[type_]
        if widget is TextField and hasattr(field.type, 'length') and (field.type.length is None or field.type.length>text_field_limit):
            widget = TextArea
        return widget