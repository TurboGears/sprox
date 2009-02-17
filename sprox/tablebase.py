from sprox.widgets import SproxDataGrid
from viewbase import ViewBase
from metadata import FieldsMetadata

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


    see modifiers in :mod:`sprox.viewbase`

    Here is an example listing of the towns in the test database.

    
    >>> from sprox.tablebase import TableBase
    >>> class TownTable(TableBase):
    ...    __model__ = Town
    >>> town_table = TownTable(session)
    >>> print town_table()
    <div xmlns="http://www.w3.org/1999/xhtml">
    <table class="grid">
        <thead>
            <tr>
                <th></th>
                <th class="col_0">
                town_id
                </th><th class="col_1">
                name
                </th>
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
    <table class="grid">
        <thead>
            <tr>
                <th></th>
                <th class="col_0">
                town_id
                </th><th class="col_1">
                name
                </th>
            </tr>
        </thead>
        <tbody>
            <tr class="even">
                <td>
                <a href="1/edit">edit</a> |
                <a href="1/delete">delete</a>
                </td>
                <td>1</td><td>Arvada</td>
            </tr><tr class="odd">
                <td>
                <a href="2/edit">edit</a> |
                <a href="2/delete">delete</a>
                </td>
                <td>2</td><td>Denver</td>
            </tr><tr class="even">
                <td>
                <a href="3/edit">edit</a> |
                <a href="3/delete">delete</a>
                </td>
                <td>3</td><td>Golden</td>
            </tr><tr class="odd">
                <td>
                <a href="4/edit">edit</a> |
                <a href="4/delete">delete</a>
                </td>
                <td>4</td><td>Boulder</td>
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
    <div xmlns="http://www.w3.org/1999/xhtml">
    <table class="grid">
        <thead>
            <tr>
                <th class="col_0">
                town_id
                </th><th class="col_1">
                name
                </th>
            </tr>
        </thead>
        <tbody>
            <tr class="even">
                <td>1</td><td>Arvada</td>
            </tr><tr class="odd">
                <td>2</td><td>Denver</td>
            </tr><tr class="even">
                <td>3</td><td>Golden</td>
            </tr><tr class="odd">
                <td>4</td><td>Boulder</td>
            </tr>
        </tbody>
    </table>
    </div>

    """

    #object overrides
    __base_widget_type__ = SproxDataGrid
    __metadata_type__    = FieldsMetadata
    __headers__          = None
    
    def _do_init_attrs(self):
        super(TableBase, self)._do_init_attrs()
        if self.__headers__ is None:
            self.__headers__ = {}
    
    def _do_get_widget_args(self):
        args = super(TableBase, self)._do_get_widget_args()
        args['fields'] = [(self.__headers__.get(field, field), eval('lambda d: d["'+field+'"]')) for field in self.__fields__]
        args['pks'] = None
        if '__actions__' not in self.__omit_fields__:
            args['pks'] = self.__provider__.get_primary_fields(self.__entity__)

        return args