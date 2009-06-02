from tw.api import Widget
from tw.forms import CalendarDatePicker, CalendarDateTimePicker, TableForm, DataGrid
from tw.forms.fields import SingleSelectField, MultipleSelectField, InputField, HiddenField
from formencode.schema import Schema
from formencode.validators import StringBool
from formencode import Invalid
import inspect


class SproxMethodPutHiddenField(HiddenField):
    template="""<input xmlns="http://www.w3.org/1999/xhtml"
       xmlns:py="http://genshi.edgewall.org/"
       type="hidden" name="_method" class="${css_class}" id="${id}"
       value="PUT"
       py:attrs="attrs" />"""

class SproxCalendarDatePicker(CalendarDatePicker):
    date_format = '%Y-%m-%d'

class SproxTimePicker(CalendarDateTimePicker):
    date_format = '%H:%M:%S'

class SproxCalendarDateTimePicker(CalendarDateTimePicker):
    date_format = '%Y-%m-%d %H:%M:%S'

class SproxDataGrid(DataGrid):
    template = "genshi:sprox.widgets.templates.datagrid"
    params = ['pks', 'controller', 'xml_fields']
    xml_fields = ['actions']

class ContainerWidget(Widget):
    template = "genshi:sprox.widgets.templates.container"
    params = ["controller",]

class TableLabelWidget(Widget):
    template = "genshi:sprox.widgets.templates.tableLabel"
    params = ["identifier", "controller"]

class ModelLabelWidget(Widget):
    template = "genshi:sprox.widgets.templates.modelLabel"
    params = ["identifier", "controller"]

class EntityLabelWidget(Widget):
    template = "genshi:sprox.widgets.templates.entityLabel"
    params = ["entity", "controller"]

class RecordViewWidget(Widget):
    template = "genshi:sprox.widgets.templates.recordViewTable"
    params = ["entity"]

class RecordFieldWidget(Widget):
    template = "genshi:sprox.widgets.templates.recordField"
    params = ['field_name']

class TableDefWidget(Widget):
    template = "genshi:sprox.widgets.templates.tableDef"
    params = ["identifier"]

class EntityDefWidget(Widget):
    template = "genshi:sprox.widgets.templates.entityDef"
    params = ["entity"]

class TableWidget(Widget):
    template = "genshi:sprox.widgets.templates.table"

class SproxTableForm(TableForm):
    validator = Schema(ignore_missing_keys=True, allow_extra_fields=True)
    template = "genshi:sprox.widgets.templates.tableForm"

#custom checkbox widget since I am not happy with the behavior of the TW one
class SproxCheckBox(InputField):
    template = "genshi:sprox.widgets.templates.checkbox"
    validator = StringBool
    def update_params(self, d):
        InputField.update_params(self, d)
        try:
            checked = self.validator.to_python(d.value)
        except Invalid:
            checked = False
        d.attrs['checked'] = checked or None

class PropertyMixin(Widget):
    params = ['entity', 'field_name', 'provider', 'dropdown_field_names']

    def _my_update_params(self, d, nullable=False):
        entity = self.entity
        options = self.provider.get_dropdown_options(self.entity, self.field_name, self.dropdown_field_names)
        if nullable:
            options.append([None,"-----------"])
        if len(options) == 0:
            return {}
        d['options']= options

        return d

class PropertySingleSelectField(SingleSelectField, PropertyMixin):
    params=["nullable"]
    nullable=False
    def update_params(self, d):
        self._my_update_params(d,nullable=self.nullable)
        SingleSelectField.update_params(self, d)
        return d

class PropertyMultipleSelectField(MultipleSelectField, PropertyMixin):
    def update_params(self, d):
        self._my_update_params(d)
        MultipleSelectField.update_params(self, d)
        return d

