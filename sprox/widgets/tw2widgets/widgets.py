from tw2.core import Widget, Param, DisplayOnlyWidget
from tw2.forms import (CalendarDatePicker, CalendarDateTimePicker, TableForm, DataGrid,
                       SingleSelectField, MultipleSelectField, InputField, HiddenField,
                       TextField, FileField, CheckBox, PasswordField, TextArea)

class SproxMethodPutHiddenField(HiddenField):
    template = "genshi:sprox.widgets.tw2widgets.templates.hidden_put"

class ContainerWidget(DisplayOnlyWidget):
    template = "genshi:sprox.widgets.tw2widgets.templates.container"
    controller = Param('controller', attribute=False, default=None)
    css_class = "containerwidget"

class TableLabelWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.tableLabel"
    controller = Param('controller', attribute=False, default=None)
    identifier = Param('identifier', attribute=False)

class ModelLabelWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.modelLabel"
    controller = Param('controller', attribute=False, default=None)
    identifier = Param('identifier', attribute=False)

class EntityLabelWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.entityLabel"
    controller = Param('controller', attribute=False, default=None)
    entity = Param('entity', attribute=False)
    css_class = "entitylabelwidget"

class RecordViewWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.recordViewTable"
    entity = Param('entity', attribute=False)

class RecordFieldWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.recordField"
    field_name = Param('field_name', attribute=False)

class TableDefWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.tableDef"
    identifier = Param('identifier', attribute=False)

class EntityDefWidget(Widget):
    available_engines = ['genshi']
    template = "genshi:sprox.widgets.tw2widgets.templates.entityDef"
    entity = Param('entity', attribute=False)

class TableWidget(Widget):
    available_engines = ['genshi']
    template = "genshi:sprox.widgets.tw2widgets.templates.table"

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
    value = []

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
