from sprox.widgets import DBSprocketsDataGrid
from viewbase import ViewBase
from metadata import FieldsMetadata

class TableBase(ViewBase):
    #object overrides
    __base_widget_type__ = DBSprocketsDataGrid
    __metadata_type__    = FieldsMetadata

    def _do_get_widget_args(self):
        args = super(TableBase, self)._do_get_widget_args()
        args['fields'] = [(field, eval('lambda d: d["'+field+'"]')) for field in self.__fields__]
        args['pks'] = self.__provider__.get_primary_fields(self.__entity__)
        return args