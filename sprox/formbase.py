import inspect
from tw.api import Widget
from tw.forms import HiddenField, TableForm
from viewbase import ViewBase
from formencode import Schema
from formencode.validators import UnicodeString
from widgetselector import SAWidgetSelector
from sprox.metadata import FieldsMetadata
from validatorselector import SAValidatorSelector

class FilteringSchema(Schema):
    """This makes formencode work for most forms, because some wsgi apps append extra"""
    filter_extra_fields = True
    allow_extra_fields = True

class FormBase(ViewBase):
    __field_validators__   = None
    __base_validator__     = None
    __require_fields__    = None
    __check_if_unique__    = False

    #object overrides
    __base_widget_type__       = TableForm
    __widget_selector_type__   = None
    __field_metadata_type__    = None

    __widget_selector_type__   = SAWidgetSelector

    __validator_selector__      = None
    __validator_selector_type__ = SAValidatorSelector


    __field_validators__       = None
    __field_validator_types__    = None
    __base_validator__         = None

    __metadata_type__ = FieldsMetadata

    __dropdown_view_names__      = None

    def _do_init_attrs(self):
        super(FormBase, self)._do_init_attrs()
        if self.__require_fields__ is None:
            self.__require_fields__ = []
        if self.__field_validators__ is None:
            self.__field_validators__ = {}
        if self.__validator_selector__ is None:
            self.__validator_selector__ = self.__validator_selector_type__(self.__provider__)
        if self.__field_validators__ is None:
            self.__field_validators__ = {}
        if self.__field_validator_types__ is None:
            self.__field_validator_types__ = {}

    @property
    def __widget__(self):
        if (not self.__cache_widget__) or not hasattr(self, '___widget__'):
            self.___widget__ = self.__base_widget_type__(**self.__widget_args__)
        return self.___widget__

    #try to act like a widget as much as possible
    @property
    def __call__(self, *args, **kw):
        return self.__widget__(*args, **kw)

    @property
    def validate(self, params):
        return self.__widget__.validate(params)

    def _do_get_widget_args(self):
        d = super(FormBase, self)._do_get_widget_args()
        return d

    def _do_get_field_widget_args(self, field_name, field):
        args = super(FormBase, self)._do_get_field_widget_args( field_name, field)
        v = self.__field_validators__.get(field_name, self._do_get_field_validator(field_name, field))
        if self.__provider__.is_relation(self.__entity__, field_name):
            args['entity'] = field.argument
        if v:
            args['validator'] = v
        return args

    def _do_get_fields(self):
        fields = super(FormBase, self)._do_get_fields()
        if 'sprox_id' not in fields:
            fields.append('sprox_id')
        return fields

    def _do_get_field_widgets(self, fields):
        widgets = super(FormBase, self)._do_get_field_widgets(fields)
        widgets['sprox_id'] = HiddenField('sprox_id')
        return widgets

    def _do_get_field_validator(self, field_name, field):
        v_type = self.__field_validator_types__.get(field_name, self.__validator_selector__.select(field))
        if v_type is None:
            return
        args = self._do_get_validator_args(field_name, field, v_type)
        v = v_type(**args)
        if hasattr(field, 'unique') and field.unique and self.__check_if_unique__:
            v = All(UniqueValue(self.__provider__, field), v)
        return v

    def _do_get_validator_args(self, field_name, field, validator_type):
        args = {}
        args['not_empty'] = (not self.__provider__.is_nullable(self.__entity__, field_name)) or \
                             field_name in self.__require_fields__

        if hasattr(field, 'type') and hasattr(field.type, 'length') and\
           validator_type is UnicodeString:
            args['max'] = field.type.length

        return args

class EditableForm(FormBase):
    def _do_get_disabled_fields(self):
        fields = self.__disable_fields__[:]
        fields.append(self.__provider__.get_primary_field(self.__entity__))
        return fields

class AddRecordForm(EditableForm):
    __check_for_unique__ = True

class DisabledForm(FormBase):
    def _do_get_disabled_fields(self):
        return self.__fields__