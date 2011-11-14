"""
formbase Module

Classes to create form widgets.

Copyright (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""
import inspect
from tw.api import Widget
from tw.forms import HiddenField, TableForm
from viewbase import ViewBase, ViewBaseError
from formencode import Schema, All
from formencode import Validator
from formencode.validators import UnicodeString, String

from sprox.validators import UniqueValue
from sprox.metadata import FieldsMetadata
from sprox.widgets.widgets import SproxMethodPutHiddenField
from sprox.viewbase import ViewBase, ViewBaseError

class FilteringSchema(Schema):
    """This makes formencode work for most forms, because some wsgi apps append extra values to the parameter list."""
    filter_extra_fields = True
    allow_extra_fields = True

class Field(object):
    """Used to handle the case where you want to override both a validator and a widget for a given field"""
    def __init__(self, widget=None, validator=None):
        self.widget = widget
        self.validator = validator

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
    | __dropdown_field_names__          | list or dict of names to use for discovery | None                         |
    |                                   | of field names for dropdowns (None uses    |                              |
    |                                   | sprox default names.)                      |                              |
    |                                   | a dict provides field-level granularity    |                              |
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


    :Example Usage:

    One of the more useful things sprox does for you is to fill in the arguments to a drop down automatically.
    Here is the userform, limited to just the town field, which gets populated with the towns.

    >>> from sprox.formbase import FormBase
    >>> class UserOnlyTownForm(FormBase):
    ...    __model__ = User
    ...    __limit_fields__ = ['town']
    >>>
    >>> town_form = UserOnlyTownForm(session)
    >>>
    >>> print town_form() # doctest: +XML
    <form action="" method="post" class="required tableform">
        <div>
                <input type="hidden" id="sprox_id" class="hiddenfield" name="sprox_id" value="" />
        </div>
        <table border="0" cellspacing="0" cellpadding="2" >
            <tr class="even" id="town.container" title="" >
                <td class="labelcol">
                    <label id="town.label" for="town" class="fieldlabel">Town</label>
                </td>
                <td class="fieldcol" >
                    <select name="town" class="propertysingleselectfield" id="town">
            <option value="1">Arvada</option>
            <option value="2">Denver</option>
            <option value="3">Golden</option>
            <option value="4">Boulder</option>
            <option value="" selected="selected">-----------</option>
    </select>
                </td>
            </tr>
            <tr class="odd" id="submit.container" title="" >
                <td class="labelcol">
                    <label id="submit.label" for="submit" class="fieldlabel"></label>
                </td>
                <td class="fieldcol" >
                    <input type="submit" class="submitbutton" value="Submit" />
                </td>
            </tr>
        </table>
    </form>

    Forms created with sprox can be validated as you would any other widget.
    >>> class UserOnlyTownForm(FormBase):
    ...    __model__ = User
    ...    __limit_fields__ = ['town']
    ...    __required_fields__ = ['town']
    >>> town_form = UserOnlyTownForm(session)
    >>> town_form.validate(params={'sprox_id':1})
    Traceback (most recent call last):
    ...
    Invalid: town: Missing value



    """
    __require_fields__     = None
    __check_if_unique__    = False

    #object overrides
    __base_widget_type__       = TableForm

    @property
    def __widget_selector_type__(self):
        return self.__provider__.default_widget_selector_type

    __validator_selector__      = None

    @property
    def __validator_selector_type__(self):
        return self.__provider__.default_validator_selector_type

    __field_validators__       = None
    __field_validator_types__  = None
    __base_validator__         = FilteringSchema

    __metadata_type__ = FieldsMetadata

    __dropdown_field_names__      = None

    def _do_init_attrs(self):
        super(FormBase, self)._do_init_attrs()
        if self.__require_fields__ is None:
            self.__require_fields__ = []
        if self.__field_validators__ is None:
            self.__field_validators__ = {}
        if self.__validator_selector__ is None:
            self.__validator_selector__ = self.__validator_selector_type__(self.__provider__)
        if self.__field_validator_types__ is None:
            self.__field_validator_types__ = {}
        if self.__dropdown_field_names__ is None:
            self.__dropdown_field_names__ = ['name', '_name', 'description', '_description']

        #bring in custom declared validators
        for attr in dir(self):
            if not attr.startswith('__'):
                value = getattr(self, attr)
                if isinstance(value, Field):
                    widget = value.widget
                    if isinstance(widget, Widget):
                        if not getattr(widget, 'id', None):
                            raise ViewBaseError('Widgets must provide an id argument for use as a field within a ViewBase')
                        self.__add_fields__[attr] = widget
                    try:
                        if issubclass(widget, Widget):
                            self.__field_widget_types__[attr] = widget
                    except TypeError:
                        pass
                    validator = value.validator
                    if isinstance(validator, Validator):
                        self.__field_validators__[attr] = validator
                    try:
                        if issubclass(validator, Validator):
                            self.__field_validator_types__[attr] = validator
                    except TypeError:
                        pass
                if isinstance(value, Validator):
                    self.__field_validators__[attr] = value
                    continue
                try:
                    if issubclass(value, Validator):
                        self.__field_validator_types__[attr] = value
                except TypeError:
                    pass

    def validate(self, params, state=None, use_request_local=True):
        """A pass-thru to the widget's validate function."""
        return self.__widget__.validate(params, state, use_request_local=use_request_local)

    def _do_get_widget_args(self):
        """Override this method to define how the class get's the
           arguments for the main widget
        """
        d = super(FormBase, self)._do_get_widget_args()
        if self.__base_validator__ is not None:
            d['validator'] = self.__base_validator__
        return d

    def _do_get_field_widget_args(self, field_name, field):
        """Override this method do define how this class gets the field
        widget arguemnts
        """
        args = super(FormBase, self)._do_get_field_widget_args( field_name, field)
        v = self.__field_validators__.get(field_name, self._do_get_field_validator(field_name, field))
        if self.__provider__.is_relation(self.__entity__, field_name):
            args['entity'] = self.__entity__
            args['field_name'] = field_name
            if isinstance(self.__dropdown_field_names__, dict) and field_name in self.__dropdown_field_names__:
                view_names = self.__dropdown_field_names__[field_name]
                if not isinstance(view_names, list):
                    view_names = [view_names]
                args['dropdown_field_names'] = view_names
            elif isinstance(self.__dropdown_field_names__, list):
                args['dropdown_field_names'] = self.__dropdown_field_names__
        if v:
            args['validator'] = v
        return args

    def _do_get_fields(self):
        """Override this function to define what fields are available to the widget.
        """
        fields = super(FormBase, self)._do_get_fields()
        provider = self.__provider__
        field_order = self.__field_order__ or []
        for relation in provider.get_relations(self.__entity__):
            # do not remove field if it is listed in field_order
            for rel in provider.relation_fields(self.__entity__, relation):
                if rel not in field_order and rel in fields:
                    fields.remove(rel)
        if 'sprox_id' not in fields:
            fields.append('sprox_id')
        return fields

    def _do_get_field_widgets(self, fields):
        widgets = super(FormBase, self)._do_get_field_widgets(fields)
        widgets['sprox_id'] = HiddenField('sprox_id', validator=String(if_missing=None))
        return widgets

    def _do_get_field_validator(self, field_name, field):
        """Override this function to define how a field validator is chosen for a given field.
        """
        v_type = self.__field_validator_types__.get(field_name, self.__validator_selector__[field])
        if field_name in self.__require_fields__ and v_type is None:
            v_type = String
        if v_type is None:
            return
        args = self._do_get_validator_args(field_name, field, v_type)
        v = v_type(**args)
        if self.__check_if_unique__ and self.__provider__.is_unique_field(self.__entity__, field_name):
            v = All(UniqueValue(self.__provider__, self.__entity__, field_name), v)
        return v

    def _do_get_validator_args(self, field_name, field, validator_type):
        """Override this function to define how to get the validator arguments for the field's validator.
        """
        args = {}
        args['not_empty'] = (not self.__provider__.is_nullable(self.__entity__, field_name)) or \
                             field_name in self.__require_fields__

        if hasattr(field, 'type') and hasattr(field.type, 'length') and\
           issubclass(validator_type, String):
            args['max'] = field.type.length

        return args

class EditableForm(FormBase):
    """A form for editing a record.
    :Modifiers:

    see :class:`sprox.formbase.FormBase`

    """
    def _do_get_disabled_fields(self):
        fields = self.__disable_fields__[:]
        fields.append(self.__provider__.get_primary_field(self.__entity__))
        return fields

    def _do_get_fields(self):
        """Override this function to define what fields are available to the widget.

        """
        fields = super(EditableForm, self)._do_get_fields()
        primary_field = self.__provider__.get_primary_field(self.__entity__)
        if primary_field not in fields:
            fields.append(primary_field)
        
        if '_method' not in fields:
            fields.append('_method')
            
        return fields

    def _do_get_field_widgets(self, fields):
        widgets = super(EditableForm, self)._do_get_field_widgets(fields)
        widgets['_method'] = SproxMethodPutHiddenField(id='_method', validator=String(if_missing=None))
        return widgets

    __check_if_unique__ = False

class AddRecordForm(FormBase):
    """An editable form who's purpose is record addition.

    :Modifiers:

    see :class:`sprox.formbase.FormBase`

    +-----------------------------------+--------------------------------------------+------------------------------+
    | Name                              | Description                                | Default                      |
    +===================================+============================================+==============================+
    | __check_if_unique__               | Set this to True for "new" forms.  This    | True                         |
    |                                   | causes Sprox to check if there is an       |                              |
    |                                   | existing record in the database which      |                              |
    |                                   | matches the field data.                    |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+

    Here is an example registration form, as generated from the vase User model.

    >>> from sprox.formbase import AddRecordForm
    >>> from formencode import Schema
    >>> from formencode.validators import FieldsMatch
    >>> from tw.forms import PasswordField, TextField
    >>> form_validator =  Schema(chained_validators=(FieldsMatch('password',
    ...                                                         'verify_password',
    ...                                                         messages={'invalidNoMatch':
    ...                                                         'Passwords do not match'}),))
    >>> class RegistrationForm(AddRecordForm):
    ...     __model__ = User
    ...     __require_fields__     = ['password', 'user_name', 'email_address']
    ...     __omit_fields__        = ['_password', 'groups', 'created', 'user_id', 'town']
    ...     __field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    ...     __base_validator__     = form_validator
    ...     email_address          = TextField
    ...     display_name           = TextField
    ...     verify_password        = PasswordField('verify_password')
    >>> registration_form = RegistrationForm()
    >>> print registration_form() # doctest: +XML
    <form action="" method="post" class="required tableform">
        <div>
                <input type="hidden" id="sprox_id" class="hiddenfield" name="sprox_id" value="" />
        </div>
        <table border="0" cellspacing="0" cellpadding="2" >
            <tr class="even" id="user_name.container" title="" >
                <td class="labelcol">
                    <label id="user_name.label" for="user_name" class="fieldlabel required">User Name</label>
                </td>
                <td class="fieldcol" >
                    <input type="text" id="user_name" class="textfield required" name="user_name" value="" />
                </td>
            </tr>
            <tr class="odd" id="email_address.container" title="" >
                <td class="labelcol">
                    <label id="email_address.label" for="email_address" class="fieldlabel required">Email Address</label>
                </td>
                <td class="fieldcol" >
                    <input type="text" id="email_address" class="textfield required" name="email_address" value="" />
                </td>
            </tr>
            <tr class="even" id="display_name.container" title="" >
                <td class="labelcol">
                    <label id="display_name.label" for="display_name" class="fieldlabel">Display Name</label>
                </td>
                <td class="fieldcol" >
                    <input type="text" id="display_name" class="textfield" name="display_name" value="" />
                </td>
            </tr>
            <tr class="odd" id="password.container" title="" >
                <td class="labelcol">
                    <label id="password.label" for="password" class="fieldlabel required">Password</label>
                </td>
                <td class="fieldcol" >
                    <input type="password" id="password" class="required passwordfield" name="password" value="" />
                </td>
            </tr>
            <tr class="even" id="verify_password.container" title="" >
                <td class="labelcol">
                    <label id="verify_password.label" for="verify_password" class="fieldlabel">Verify Password</label>
                </td>
                <td class="fieldcol" >
                    <input type="password" id="verify_password" class="passwordfield" name="verify_password" value="" />
                </td>
            </tr>
            <tr class="odd" id="submit.container" title="" >
                <td class="labelcol">
                    <label id="submit.label" for="submit" class="fieldlabel"></label>
                </td>
                <td class="fieldcol" >
                    <input type="submit" class="submitbutton" value="Submit" />
                </td>
            </tr>
        </table>
    </form>

    What is unique about the AddRecord form, is that if the fields in the database are labeled unique, it will
    automatically vaidate against uniqueness for that field.  Here is a simple user form definition, where the
    user_name in the model is unique:


    >>> class AddUserForm(AddRecordForm):
    ...     __entity__ = User
    ...     __limit_fields__ = ['user_name']
    >>> user_form = AddUserForm(session)
    >>> user_form.validate(params={'sprox_id':'asdf', 'user_name':u'asdf'}) # doctest: +SKIP
    Traceback (most recent call last):
    ...
    Invalid: user_name: That value already exists

    The validation fails because there is already a user with the user_name 'asdf' in the database


    """
    __check_if_unique__ = True

    def _do_get_disabled_fields(self):
        fields = self.__disable_fields__[:]
        fields.append(self.__provider__.get_primary_field(self.__entity__))
        return fields


class DisabledForm(FormBase):
    """A form who's set of fields is disabled.


    :Modifiers:

    see :class:`sprox.formbase.FormBase`

    Here is an example disabled form with only the user_name and email fields.

    >>> from sprox.test.model import User
    >>> from sprox.formbase import DisabledForm
    >>> class DisabledUserForm(DisabledForm):
    ...     __model__ = User
    ...     __limit_fields__ = ['user_name', 'email_address']
    >>> disabled_user_form = DisabledUserForm()
    >>> print disabled_user_form(values=dict(user_name='percious', email='chris@percious.com'))  # doctest: +XML
    <form action="" method="post" class="required tableform">
        <div>
                <input type="hidden" id="user_name" class="hiddenfield" name="user_name" value="" />
                <input type="hidden" id="email_address" class="hiddenfield" name="email_address" value="" />
                <input type="hidden" id="sprox_id" class="hiddenfield" name="sprox_id" value="" />
        </div>
        <table border="0" cellspacing="0" cellpadding="2" >
            <tr class="even" id="user_name.container" title="" >
                <td class="labelcol">
                    <label id="user_name.label" for="user_name" class="fieldlabel">User Name</label>
                </td>
                <td class="fieldcol" >
                    <input type="text" id="user_name" class="textfield" name="user_name" value="" disabled="disabled" />
                </td>
            </tr>
            <tr class="odd" id="email_address.container" title="" >
                <td class="labelcol">
                    <label id="email_address.label" for="email_address" class="fieldlabel">Email Address</label>
                </td>
                <td class="fieldcol" >
                    <textarea id="email_address" name="email_address" class="textarea" disabled="disabled" rows="7" cols="50"></textarea>
                </td>
            </tr>
            <tr class="even" id="submit.container" title="" >
                <td class="labelcol">
                    <label id="submit.label" for="submit" class="fieldlabel"></label>
                </td>
                <td class="fieldcol" >
                    <input type="submit" class="submitbutton" value="Submit" />
                </td>
            </tr>
        </table>
    </form>

    You may notice in the above example that disabled fields pass in a hidden value for each disabled field.

    """


    def _do_get_disabled_fields(self):
        return self.__fields__
