from sprox.widgets.dojo import SproxEditableDojoGrid, SproxDojoGrid
from sprox.tablebase import TableBase
from sprox.metadata import FieldsMetadata

class DojoTableBase(TableBase):
    """This class allows you to credate a table widget.

    :Modifiers:

    see modifiers in :mod:`sprox.tablebase`

    """

    #object overrides
    __base_widget_type__ = SproxDojoGrid
    __url__ = 'data'

    def _do_get_widget_args(self):
        args = super(DojoTableBase, self)._do_get_widget_args()
        args['columns'] = self.__fields__
        args['jsId'] = 'something'
        args['url'] = self.__url__
        return args


class DojoEditableTableBase(TableBase):
    __base_widget_type__ = SproxEditableDojoGrid
    __url__ = 'data'

    def _do_get_widget_args(self):
        args = super(DojoEditableTableBase, self)._do_get_widget_args()
        args['columns'] = self.__fields__
        args['jsId'] = 'something'
        args['url'] = self.__url__
        return args
