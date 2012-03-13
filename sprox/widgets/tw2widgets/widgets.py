from tw2.core import Widget, Param
from tw2.forms import (CalendarDatePicker, CalendarDateTimePicker, TableForm, DataGrid,
                       SingleSelectField, MultipleSelectField, InputField, HiddenField,
                       TextField, FileField, CheckBox, PasswordField, TextArea)

class SproxMethodPutHiddenField(HiddenField):
    template = "genshi:sprox.widgets.tw2widgets.templates.hidden_put"

class SproxCalendarDatePicker(CalendarDatePicker):
    date_format = '%Y-%m-%d'

class SproxTimePicker(CalendarDateTimePicker):
    date_format = '%H:%M:%S'

class SproxCalendarDateTimePicker(CalendarDateTimePicker):
    date_format = '%Y-%m-%d %H:%M:%S'

class SproxDataGrid(DataGrid):
    template = "genshi:sprox.widgets.tw2widgets.templates.datagrid"

    pks = Param('pks', attribute=False),
    controller = Param('controller', attribute=False)
    xml_fields = Param('xml_fields', attribute=False, default=['actions'])

class SproxCheckBox(CheckBox):
    pass

class PropertySingleSelectField(SingleSelectField):
    def prepare(self):
        entity = self.entity
        options = self.provider.get_dropdown_options(self.entity, self.field_name, self.dropdown_field_names)
        self.options = options

        super(PropertySingleSelectField, self).prepare()

class PropertyMultipleSelectField(MultipleSelectField):
    def prepare(self):
        entity = self.entity
        options = self.provider.get_dropdown_options(self.entity, self.field_name, self.dropdown_field_names)
        self.options = options

        super(PropertyMultipleSelectField, self).prepare()
