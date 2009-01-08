import inspect
from sprox.widgets import ContainerWidget, TableWidget
from viewbase import ViewBase
from widgetselector import EntitiesViewWidgetSelector, EntityDefWidgetSelector
from sprox.metadata import EntitiesMetadata, FieldsMetadata

class EntityDefBase(ViewBase):
    """This view can display all of the entities for a given provider.

    :Modifiers:
     see :mod:`sprox.viewbase.ViewBase`

    :Usage:
    >>> from sprox.test.base import setup_database, User
    >>> session, engine, metadata = setup_database()
    >>> class UserEntityDef(EntityDefBase):
    ...     __entity__ = User
    >>> base = UserEntityDef(session)
    >>> print base()
    <table xmlns="http://www.w3.org/1999/xhtml" class="tablewidget">
    <tr><th>Name</th><th>Definition</th></tr>
    <tr class="odd">
        <td>
            password
        </td>
        <td>
            Unicode(length=40)
        </td>
    </tr>
    <tr class="even">
        <td>
            user_id
        </td>
        <td>
            Integer()
        </td>
    </tr>
    <tr class="odd">
        <td>
            user_name
        </td>
        <td>
            Unicode(length=16)
        </td>
    </tr>
    <tr class="even">
        <td>
            email_address
        </td>
        <td>
            Unicode(length=255)
        </td>
    </tr>
    <tr class="odd">
        <td>
            display_name
        </td>
        <td>
            Unicode(length=255)
        </td>
    </tr>
    <tr class="even">
        <td>
            created
        </td>
        <td>
            DateTime(timezone=False)
        </td>
    </tr>
    <tr class="odd">
        <td>
            town_id
        </td>
        <td>
            Integer()
        </td>
    </tr>
    <tr class="even">
        <td>
            town
        </td>
        <td>
            relation
        </td>
    </tr>
    <tr class="odd">
        <td>
            password
        </td>
        <td>
            relation
        </td>
    </tr>
    <tr class="even">
        <td>
            groups
        </td>
        <td>
            relation
        </td>
    </tr>
    </table>
    >>> session.rollback()
    """

    __base_widget_type__       = TableWidget
    __widget_selector_type__   = EntityDefWidgetSelector
    __metadata_type__          = FieldsMetadata


class DummyEntity(object):
    pass

class EntitiesBase(ViewBase):
    """This view can display all of the entities for a given provider.

    :Modifiers:
     see :mod:`sprox.viewbase.ViewBase`

    :Usage:
    >>> from sprox.test.base import setup_database, User
    >>> session, engine, metadata = setup_database()
    >>> class EntitiesBaseTest(EntitiesBase):
    ...     __entity__ = User
    >>> base = EntitiesBaseTest(session, metadata=metadata)
    >>> print base()
    <div xmlns="http://www.w3.org/1999/xhtml" class="containerwidget">
    <div class="entitylabelwidget">
    <a href="Document/">Document</a>
    </div>
    <div class="entitylabelwidget">
    <a href="Example/">Example</a>
    </div>
    <div class="entitylabelwidget">
    <a href="Group/">Group</a>
    </div>
    <div class="entitylabelwidget">
    <a href="Permission/">Permission</a>
    </div>
    <div class="entitylabelwidget">
    <a href="Town/">Town</a>
    </div>
    <div class="entitylabelwidget">
    <a href="User/">User</a>
    </div>
    </div>
    >>> session.rollback()
    """
    __entity__ = DummyEntity
    __base_widget_type__       = ContainerWidget
    __widget_selector_type__   = EntitiesViewWidgetSelector
    __metadata_type__          = EntitiesMetadata

