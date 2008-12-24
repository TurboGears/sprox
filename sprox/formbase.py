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
    """

    :Modifiers:


    Modifiers defined in this class

    +-----------------------------------+--------------------------------------------+------------------------------+
    | Name                              | Description                                | Default                      |
    +===================================+============================================+==============================+
    | __base_widget_type__              | What widget to use for the form.           | TableForm                    |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __widget_selector_type__          | What class to use for widget selection.    | SAWidgetSelector             |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __validator_selector_type__       | What class to use for validator selection. | SAValidatorSelector          |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __require_fields__                | Specifies which fields are required.       | []                           |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __check_if_unique__               | Set this to True for "new" forms.  This    | False                        |
    |                                   | causes Sprox to check if there is an       |                              |
    |                                   | existing record in the database which      |                              |
    |                                   | matches the field data.                    |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __field_validators__              | A dictionary of validators indexed by      | {}                           |
    |                                   | fieldname.                                 |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __field_validator_types__         | Types of validators to use for each field  | {}                           |
    |                                   | (allow sprox to set the attribute of the   |                              |
    |                                   | validators).                               |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __base_validator__                | A validator to attch to the form.          | None                         |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __validator_selector__            | What object to use to select field         | None                         |
    |                                   | validators.                                |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __metadata_type__                 | What metadata type to use to get schema    | FieldsMetadata               |
    |                                   | info on this object                        |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __dropdown_view_names__           | list of names to use for discovery of view | None                         |
    |                                   | fieldnames for dropdowns (None uses the    |                              |
    |                                   | sprox default names.                       |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+

    Modifiers inherited from :class:`sprox.viewbase.ViewBase`

    +-----------------------------------+--------------------------------------------+------------------------------+
    | Name                              | Description                                | Default                      |
    +===================================+============================================+==============================+
    | __field_widgets__                 | A dictionary of widgets to replace the     | {}                           |
    |                                   | ones that would be chosen by the selector  |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __field_widget_types__            | A dictionary of types of widgets, allowing | {}                           |
    |                                   | sprox to determine the widget args         |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __widget_selector__               | an instantiated object to use for widget   | None                         |
    |                                   | selection.                                 |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+

    Modifiers inherited from :class:`sprox.configbase.ConfigBase`
    """
    __require_fields__     = None
    __check_if_unique__    = False

    #object overrides
    __base_widget_type__       = TableForm

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

    def validate(self, params):
        """A pass-thru to the widget's validate function."""
        return self.__widget__.validate(params)

    def _do_get_widget_args(self):
        """Override this method to define how the class get's the
           arguments for the main widget
        """
        d = super(FormBase, self)._do_get_widget_args()
        return d

    def _do_get_field_widget_args(self, field_name, field):
        """Override this method do define how this class gets the field
        widget arguemnts
        """
        args = super(FormBase, self)._do_get_field_widget_args( field_name, field)
        v = self.__field_validators__.get(field_name, self._do_get_field_validator(field_name, field))
        if self.__provider__.is_relation(self.__entity__, field_name):
            args['entity'] = field.argument
        if v:
            args['validator'] = v
        return args

    def _do_get_fields(self):
        """Override this function to define how
        """
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