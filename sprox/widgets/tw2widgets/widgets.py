from formencode import Invalid
from tw2.core import Widget, Param, DisplayOnlyWidget, ValidationError, RepeatingWidget
from tw2.forms import (CalendarDatePicker, CalendarDateTimePicker, TableForm, DataGrid,
                       SingleSelectField, MultipleSelectField, InputField, HiddenField,
                       TextField, FileField, CheckBox, PasswordField, TextArea, ListLayout,
                       StripBlanks)
from tw2.forms import Label as tw2Label
from tw2.core import validation as tw2v
from sprox._compat import unicode_text


class Label(tw2Label):
    def prepare(self):
        self.text = unicode_text(self.value)
        super(Label, self).prepare()

class SproxMethodPutHiddenField(HiddenField):
    name = '_method'

    def prepare(self):
        self.value = 'PUT'
        super(SproxMethodPutHiddenField, self).prepare()

class ContainerWidget(DisplayOnlyWidget):
    template = "genshi:sprox.widgets.tw2widgets.templates.container"
    controller = Param('controller', attribute=False, default=None)
    css_class = "containerwidget"
    id_suffix = 'container'

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
    entity = Param('entity', attribute=False, default=None)

class RecordFieldWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.recordField"
    field_name = Param('field_name', attribute=False)
    css_class = "recordfieldwidget"

class TableDefWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.tableDef"
    identifier = Param('identifier', attribute=False)

class EntityDefWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.entityDef"
    entity = Param('entity', attribute=False)

class TableWidget(Widget):
    template = "genshi:sprox.widgets.tw2widgets.templates.table"

class SproxCalendarDatePicker(CalendarDatePicker):
    date_format = '%Y-%m-%d'

class SproxTimePicker(CalendarDateTimePicker):
    date_format = '%H:%M:%S'

class SproxCalendarDateTimePicker(CalendarDateTimePicker):
    date_format = '%Y-%m-%d %H:%M:%S'

class SproxDataGrid(DataGrid):
    template = "sprox.widgets.tw2widgets.templates.datagrid"

    pks = Param('pks', attribute=False),
    xml_fields = Param('xml_fields', attribute=False, default=['actions'])
    value = []

class SproxCheckBox(CheckBox):
    def prepare(self):
        super(SproxCheckBox, self).prepare()
        self.attrs['value'] = 'true'


class PropertySingleSelectField(SingleSelectField):
    entity = Param('entity', attribute=False, default=None)
    provider = Param('provider', attribute=False, default=None)
    field_name = Param('field_name', attribute=False, default=None)
    dropdown_field_names = Param('dropdown_field_names', attribute=False, default=None)
    nullable = Param('nullable', attribute=False, default=False)
    disabled = Param('disabled', attribute=False, default=False)
    prompt_text = None

    def prepare(self):
        #This is required for ming
        entity = self.__class__.entity

        options = self.provider.get_dropdown_options(entity, self.field_name, self.dropdown_field_names)
        self.options = [(unicode_text(k), unicode_text(v)) for k,v in options]
        if self.nullable:
            self.options.append(['', "-----------"])

        if not self.value:
            self.value = ''

        self.value = unicode_text(self.value)
        super(PropertySingleSelectField, self).prepare()


class PropertyMultipleSelectField(MultipleSelectField):
    entity = Param('entity', attribute=False, default=None)
    provider = Param('provider', attribute=False, default=None)
    field_name = Param('field_name', attribute=False, default=None)
    dropdown_field_names = Param('dropdown_field_names', attribute=False, default=None)
    nullable = Param('nullable', attribute=False, default=False)
    disabled = Param('disabled', attribute=False, default=False)

    def _safe_from_validate(self, validator, value, state=None):
        try:
            return validator.from_python(value, state=state)
        except Invalid:
            return Invalid

    def _safe_to_validate(self, validator, value, state=None):
        try:
            return validator.to_python(value, state=state)
        except Invalid:
            return Invalid

    def _validate(self, value, state=None):
        # Work around a bug in tw2.core <= 2.2.2 where twc.safe_validate
        # doesn't work with formencode validators.
        value = value or []
        if not isinstance(value, (list, tuple)):
            value = [value]
        if self.validator:
            self.validator.to_python(value, state)
        if self.item_validator:
            value = [self._safe_to_validate(self.item_validator, v) for v in value]
        self.value = [v for v in value if v is not Invalid]
        return self.value

    def prepare(self):
        # This is required for ming
        entity = self.__class__.entity

        options = self.provider.get_dropdown_options(entity, self.field_name, self.dropdown_field_names)
        self.options = [(unicode_text(k), unicode_text(v)) for k,v in options]

        if not self.value:
            self.value = []

        if not hasattr(self, '_validated') and self.item_validator:
            self.value = [self._safe_from_validate(self.item_validator, v) for v in self.value]

        self.value = [unicode_text(v) for v in self.value if v is not Invalid]
        super(PropertyMultipleSelectField, self).prepare()


class SubDocument(ListLayout):
    direct = Param('direct', attribute=False, default=False)
    children_attrs = Param('children_attrs', attribute=False, default={})

    @classmethod
    def post_define(cls):
        if not cls.css_class:
            cls.css_class = ''
        if 'subdocument' not in cls.css_class:
            cls.css_class += ' subdocument'

        for c in getattr(cls, 'children', []):
            # SubDocument always propagates its template to nested subdocuments
            if issubclass(c, SubDocument):
                c.children_attrs = cls.children_attrs
                c.template = cls.template
            elif issubclass(c, SubDocumentsList):
                c.children_attrs = cls.children_attrs
                c.child = c.child(template=cls.template)
            else:
                for name, value in cls.children_attrs.items():
                    setattr(c, name, value)

            if cls.direct:
                # In direct mode we just act as a proxy to the real field
                # so we set the field key equal to our own
                c.compound_key = ':'.join(c.compound_key.split(':')[:-1])

        if not hasattr(cls, 'children'):
            cls.children = []

    @tw2v.catch_errors
    def _validate(self, value, state=None):
        if self.direct:
            # In direct mode we just act as a proxy to the real field
            # so we directly validate the field
            return self.children[0]._validate(value, state)
        else:
            return super(SubDocument, self)._validate(value, state)

    def prepare(self):
        if self.direct:
            # In direct mode we just act as a proxy to the real field
            # so we provide the value to the field and throw away error messages
            # to avoid duplicating them (one for us and one for the field).
            self.children[0].value = self.value
            self.error_msg = ''
        super(SubDocument, self).prepare()


class SubDocumentsList(RepeatingWidget):
    template = 'sprox.widgets.tw2widgets.templates.subdocuments'
    child = SubDocument
    children_attrs = Param('children_attrs', attribute=False, default={})
    direct = Param('direct', attribute=False, default=False)
    extra_reps = 1

    @classmethod
    def post_define(cls):
        if not cls.css_class:
            cls.css_class = ''
        if 'subdocuments' not in cls.css_class:
            cls.css_class += ' subdocuments'

        cls.child.children_attrs = cls.children_attrs
        if cls.direct:
            cls.child.direct = True

    def prepare(self):
        super(SubDocumentsList, self).prepare()
        # Hide the last element, used to add new entries
        self.children[len(self.children)-1].attrs['style'] = 'display: none'

    def _validate(self, value, state=None):
        return super(SubDocumentsList, self)._validate(
            StripBlanks().to_python(value, state), state
        )