import inspect
from sprox.widgets import ContainerWidget, TableWidget
from viewbase import ViewBase
from widgetselector import EntitiesViewWidgetSelector, EntityDefWidgetSelector
from sprox.metadata import EntitiesMetadata, FieldsMetadata

class EntityDefBase(ViewBase):
    __base_widget_type__       = TableWidget
    __widget_selector_type__   = EntityDefWidgetSelector
    __metadata_type__          = FieldsMetadata


class DummyEntity(object):
    pass

class EntitiesBase(ViewBase):
    __entity__ = DummyEntity
    __base_widget_type__       = ContainerWidget
    __widget_selector_type__   = EntitiesViewWidgetSelector
    __metadata_type__          = EntitiesMetadata

