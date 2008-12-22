from tw.api import Widget
from tw.forms import CalendarDatePicker, CalendarDateTimePicker, TableForm, DataGrid
from tw.forms.fields import SingleSelectField, MultipleSelectField, InputField
from formencode.schema import Schema
from formencode.validators import StringBool
from formencode import Invalid
import inspect


class DBSprocketsCalendarDatePicker(CalendarDatePicker):
    date_format = '%Y-%m-%d'

class DBSprocketsTimePicker(CalendarDateTimePicker):
    date_format = '%H:%M:%S'

class DBSprocketsCalendarDateTimePicker(CalendarDateTimePicker):
    date_format = '%Y-%m-%d %H:%M:%S'

class DBSprocketsDataGrid(DataGrid):
    template = "genshi:sprox.widgets.templates.datagrid"
    params = ['pks', 'controller']

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
    params = ["identifier"]

class RecordFieldWidget(Widget):
    template = "genshi:sprox.widgets.templates.recordField"
    params = ['identifier', 'controller']

class TableDefWidget(Widget):
    template = "genshi:sprox.widgets.templates.tableDef"
    params = ["identifier"]

class EntityDefWidget(Widget):
    template = "genshi:sprox.widgets.templates.entityDef"
    params = ["entity"]

class TableWidget(Widget):
    template = "genshi:sprox.widgets.templates.table"

class DBSprocketsTableForm(TableForm):
    validator = Schema(ignore_missing_keys=True, allow_extra_fields=True)
    template = "genshi:sprox.widgets.templates.tableForm"

    def update_params(self, d):
        super(DBSprocketsTableForm, self).update_params(d)

#custom checkbox widget since I am not happy with the behavior of the TW one
class DBSprocketsCheckBox(InputField):
    template = "genshi:sprox.widgets.templates.checkbox"
    validator = StringBool
    def update_params(self, d):
        InputField.update_params(self, d)
        try:
            checked = self.validator.to_python(d.value)
        except Invalid:
            checked = False
        d.attrs['checked'] = checked or None

class ForeignKeyMixin(Widget):
    params = ["table_name", "provider"]
    def _my_update_params(self, d,nullable=False):
        view_column = self.provider.get_view_column_name(self.table_name)
        id_column = self.provider.get_id_column_name(self.table_name)
        rows = self.provider.select(self.table_name, columns_limit=[id_column, view_column])
        rows= [(row[id_column], row[view_column]) for row in rows]
        if nullable:
            rows.append([None,"-----------"])
        if len(rows) == 0:
            return {}
        d['options']= rows

        return d

class ForeignKeySingleSelectField(SingleSelectField, ForeignKeyMixin):
    params=["nullable"]
    nullable=False
    def update_params(self, d):
        self._my_update_params(d,nullable=self.nullable)
        SingleSelectField.update_params(self, d)
        return d

class ForeignKeyMultipleSelectField(MultipleSelectField, ForeignKeyMixin):
    def update_params(self, d):
        self._my_update_params(d)
        MultipleSelectField.update_params(self, d)
        return d

class PropertyMixin(Widget):
    params = ['entity', 'provider']

    def _my_update_params(self, d, nullable=False):
        entity = self.entity
        if inspect.isfunction(self.entity):
            entity = self.entity()
        options = self.provider.get_dropdown_options(entity)
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

