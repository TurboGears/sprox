import inspect
from tw.api import Widget
from tw.forms import HiddenField
from configbase import ConfigBase, ConfigBaseError
from sqlalchemy.orm import PropertyLoader
from widgetselector import WidgetSelector

class ClassViewer(object):
    """class wrapper to expose items of a class.  Needed to pass classes to TW as params"""
    def __init__(self, klass):
        self.__name__ = klass.__name__

class ViewBase(ConfigBase):
    __field_widgets__      = None
    __field_widget_types__ = None
    __cache_widget__       = True

    #object overrides
    __base_widget_type__       = Widget
    __widget_selector_type__   = WidgetSelector
    __widget_selector__        = None


    def _do_init_attrs(self):
        super(ViewBase, self)._do_init_attrs()
        if self.__field_widgets__ is None:
            self.__field_widgets__ = {}
        if self.__field_widget_types__ is None:
            self.__field_widget_types__ = {}
        if self.__widget_selector__ is None:
            self.__widget_selector__ = self.__widget_selector_type__()

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
    def __widget_args__(self):
        return self._do_get_widget_args()

    def _do_get_widget_args(self):
        widget_dict = self._do_get_field_widgets(self.__fields__)

        field_widgets = []
        for key in self.__fields__:
            value = widget_dict[key]
            #sometimes a field will have two widgets associated with it (disabled fields)
            if hasattr(value,'__iter__'):
                field_widgets.extend(value)
                continue
            field_widgets.append(value)

        d = dict(children=field_widgets)
        return d

    def _do_get_disabled_fields(self):
        return self.__disable_fields__

    def _do_get_field_widget_args(self, field_name, field):
        field_attrs = self.__field_attrs__

        # toscawidgets does not like ids that have '.' in them.  This does not
        # work for databases with schemas.
        field_name = field_name.replace('.', '_')
        args = {}

        #this is sort of a hack around TW evaluating _some_ params that are classes.
        entity = field
        if inspect.isclass(field):
            entity = ClassViewer(field)

        args = {'id':field_name, 'identity':self.__entity__.__name__+'_'+field_name, 'entity':entity}

        if field in self.__field_attrs__:
            args['attrs'] = field_attrs.get[field_name]

        if isinstance(field, PropertyLoader):
            args['provider'] = self.__provider__
            args['nullable'] = self.__provider__.is_nullable(self.__entity__, field_name)

        return args

    def __create_hidden_fields(self):
        fields = {}
        fields['sprox_id'] = HiddenField(id='sprox_id')

        for field in self.__hide_fields__:
            if field not in self.__omit_fields__:
                fields[field] = HiddenField(id=field, identifier=field)

        return fields

    def _do_get_field_widgets(self, fields):

        widgets = {}
        for field_name in fields:
            if field_name in self.__field_widgets__:
                widgets[field_name] = self.__field_widgets__[field_name]
                continue
            if field_name in self.__add_fields__:
                widgets[field_name] = self.__add_fields__[field_name]
                continue
            if field_name in self.__omit_fields__:
                continue
            if field_name == 'sprox_id':
                continue
            if field_name in self.__hide_fields__:
                continue

            field = self.__metadata__[field_name]

            if inspect.isclass(field):
                identifier = ClassViewer(field)

            field_widget_type = self.__field_widget_types__.get(field_name,
                                                                self.__widget_selector__.select(field))
            field_widget_args = self._do_get_field_widget_args(field_name, field)

            if field_name in self._do_get_disabled_fields():
                # in this case, we display the current field, disabling it, and also add
                # a hidden field into th emix
                field_widget_args['disabled'] = True
                widgets[field_name] = (HiddenField(id=field_name.replace('.','_'), identifier=field_name), field_widget_type(**field_widget_args))
            else:
                widgets[field_name] = field_widget_type(**field_widget_args)

        widgets.update(self.__create_hidden_fields())
        return widgets
