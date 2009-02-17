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

    def _do_get_widget_args(self):
        args = super(DojoTableBase, self)._do_get_widget_args()
        args['columns'] = self.__fields__
        args['headers'] = self.__headers__
        args['jsId'] = self.__sprox_id__
        return args

"""
Experimental for next version.  Will not be included in 0.5

class DojoEditableTableBase(TableBase):
    __base_widget_type__ = SproxEditableDojoGrid

    def _do_get_widget_args(self):
        args = super(DojoEditableTableBase, self)._do_get_widget_args()
        args['columns'] = self.__fields__
        args['jsId'] = self.__sprox_id__
        return args
"""