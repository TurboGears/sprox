"""
fillerbase Module

Classes to help fill widgets with data

Copyright (c) 2008-10 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""
from operator import itemgetter

from tw.api import Widget

from sprox.viewbase import ViewBase
from sprox.widgets import SproxDataGrid
from sprox.metadata import FieldsMetadata

class TableBase(ViewBase):
    """This class allows you to create a table widget.

    :Modifiers:
    +-----------------------------------+--------------------------------------------+------------------------------+
    | Name                              | Description                                | Default                      |
    +===================================+============================================+==============================+
    | __base_widget_type__              | Base widget for fields to go into.         | SproxDataGrid                |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __metadata_type__                 | Type the widget is based on.               | FieldsMetadata               |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __headers__                       | A dictionay of field/header pairs.         | {}                           |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __column_widths__                 | A dictionay of field/width(string) pairs.  | {}                           |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __default_column_width__          | Header size to use when not specified in   | '10em'                       |
    |                                   | __column_widths__                          |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __xml_fields__                    | fields whos values should show as html     |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+


    see modifiers in :mod:`sprox.viewbase`

    Here is an example listing of the towns in the test database.


    >>> from sprox.tablebase import TableBase
    >>> class TownTable(TableBase):
    ...    __model__ = Town
    >>> town_table = TownTable(session)
    >>> print town_table()
    <div>
    <table
           id="None" class="grid">
        <thead>
            <tr>
                    <th  class="col_0">actions</th>
                    <th  class="col_1">town_id</th>
                    <th  class="col_2">name</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
          No Records Found.
    </div>

    As you can see, this is none too interesting, because there is no data in the table.
    Here is how we fill the table with data using TableFillerBase

    >>> from sprox.fillerbase import TableFiller
    >>> class TownFiller(TableFiller):
    ...     __model__ = Town
    >>> town_filler = TownFiller(session)
    >>> value = town_filler.get_value()
    >>> print town_table.__widget__(value=value) #doctest: +SKIP
    <div xmlns="http://www.w3.org/1999/xhtml">
    <div>
    <table
           id="None" class="grid">
        <thead>
            <tr>
                    <th class="col_0">town_id</th>
                    <th class="col_1">name</th>
            </tr>
        </thead>
        <tbody>
            <tr class="even">
                <td class="col_0">
                        1
                </td>
                <td class="col_1">
                        Arvada
                </td>
            </tr>
            <tr class="odd">
                <td class="col_0">
                        2
                </td>
                <td class="col_1">
                        Denver
                </td>
            </tr>
            <tr class="even">
                <td class="col_0">
                        3
                </td>
                <td class="col_1">
                        Golden
                </td>
            </tr>
            <tr class="odd">
                <td class="col_0">
                        4
                </td>
                <td class="col_1">
                        Boulder
                </td>
            </tr>
        </tbody>
    </table>
    </div>

    And now you can see the table has some data in it, and some restful links to the data.  But what if you don't want those links?
    You can omit the links by adding '__actions__' to omitted fields as follows:

    >>> class TownTable(TableBase):
    ...     __model__ = Town
    ...     __omit_fields__ = ['__actions__']
    >>> town_table = TownTable(session)
    >>> print town_table.__widget__(value=value)
    <div>
    <table
           id="None" class="grid">
        <thead>
            <tr>
                    <th  class="col_0">town_id</th>
                    <th  class="col_1">name</th>
            </tr>
        </thead>
        <tbody>
            <tr class="even">
                <td class="col_0">
                        1
                </td>
                <td class="col_1">
                        Arvada
                </td>
            </tr>
            <tr class="odd">
                <td class="col_0">
                        2
                </td>
                <td class="col_1">
                        Denver
                </td>
            </tr>
            <tr class="even">
                <td class="col_0">
                        3
                </td>
                <td class="col_1">
                        Golden
                </td>
            </tr>
            <tr class="odd">
                <td class="col_0">
                        4
                </td>
                <td class="col_1">
                        Boulder
                </td>
            </tr>
        </tbody>
    </table>
    </div>
    """

    #object overrides
    __base_widget_type__ = SproxDataGrid
    __metadata_type__    = FieldsMetadata
    __headers__          = None
    __column_widths__    = None
    __xml_fields__       = None
    __default_column_width__ = "10em"

    def _do_get_fields(self):
        fields = super(TableBase, self)._do_get_fields()
        if '__actions__' not in self.__omit_fields__ and '__actions__' not in fields:
            fields.insert(0, '__actions__')
            if '__actions__' not in self.__headers__:
                self.__headers__['__actions__'] = 'actions'
        return fields

    def _do_init_attrs(self):
        super(TableBase, self)._do_init_attrs()
        if self.__headers__ is None:
            self.__headers__ = {}
        if self.__column_widths__ is None:
            self.__column_widths__ = {}
        if self.__xml_fields__ is None:
            self.__xml_fields__ = {}

    def _do_get_widget_args(self):
        args = super(TableBase, self)._do_get_widget_args()
        args['pks'] = None
        args['column_widths'] = self.__column_widths__
        args['default_column_width'] = self.__default_column_width__

        # Okay: the trunk version of Sprox creates its args['fields']
        # very simply, as a list of lambdas that do an item lookup on
        # the field name.  This means that TableBase inherently ignores
        # any attempt to specify widgets for displaying or formatting
        # model values; in fact, the field widget list that the
        # TableBase grows at some point during processing appears to be
        # completely ignored.  (You will see if it you add "print"
        # statements around your code to watch how your tables are
        # behaving.)

        # To make widgets active, we need to put the widgets in place of
        # the lambdas in the the args['fields'] that we build.  There
        # are challenges to building this list, however:

        # 1. The widgets supplied by default are useless.  Instead of
        #    being something that can actually display text, the list of
        #    widgets somehow winds up just being bare Widget instances,
        #    which seem to display absolutely nothing when rendered.
        #    Therefore, when we see a bare Widget supplied for a
        #    particular column, we need to ignore it.

        # 2. Some fields (like '__action__') do not even appear in our
        #    list of fields-plus-widgets called self.__fields__, so we
        #    have to be willing to fall back to a lambda in that case
        #    too.

        # 3. For some reason, the list of field widgets is not always
        #    present, so we have to wastefully re-compute it here by
        #    calling the _do_get_field_widgets() method.  It would be
        #    nice if this were produced once before these computations
        #    started and could be relied upon to be present, but it's
        #    not so far as I could tell.  But, then, I was reading code
        #    late at night.

        # Anyway, with the stanza below, I am able to provide my table
        # classes with a __field_widget_types__ dictionary and have
        # those fields rendered differently.

        field_headers = [ self.__headers__.get(field, field)
                          for field in self.__fields__ ]
        field_widget_dict = self._do_get_field_widgets(self.__fields__)
        field_widgets = []
        for field in self.__fields__:
            widget = field_widget_dict.get(field, None)
            if widget is None or widget.__class__ is Widget: # yuck
                widget = itemgetter(field)
            field_widgets.append(widget)
        args['fields'] = zip(field_headers, field_widgets)

        # And, now back to our regularly-scheduled trunk-derived Sprox.

        if '__actions__' not in self.__omit_fields__:
            args['pks'] = self.__provider__.get_primary_fields(self.__entity__)

        args['xml_fields'] = self.__xml_fields__
        return args
