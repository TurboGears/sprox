"""Dojo Specific Widgets"""

from tw.dojo import DojoQueryReadStore, DojoBase, grid_css, tundragrid_css
from tw.dojo.selectshuttle import DojoSelectShuttleField
from tw.api import JSSource
from sprox.widgets import PropertyMixin

class SproxDojoGrid(DojoBase):
    css = [grid_css, tundragrid_css]
    require = ['dojox.grid.DataGrid', 'dojox.data.QueryReadStore']
    dojoType = 'dojox.grid.DataGrid'
    params = ['id', 'attrs', 'columns', 'jsId', 'action',
              'rowsPerPage', 'model', 'delayScroll', 'cssclass', 'actions',
              'columnResizing', 'columnReordering', 'headers'
              ]
    delayScroll = "true"
    cssclass="sprox-dojo-grid"
    rowsPerPage = 20
    columns = []
    columnReordering = "false"
    columnResizing="false"
    include_dynamic_js_calls = True
    action='.json'
    model = None
    actions = True
    template = "genshi:sprox.widgets.templates.dojogrid"

class SproxEditableDojoGrid(DojoBase):
    css = [grid_css, tundragrid_css]
    require = ['dojox.grid.DataGrid', 'dojox.data.QueryReadStore']
    dojoType = 'dojox.grid.DataGrid'
    params = ['id', 'attrs', 'columns', 'jsId', 'action',
              'rowsPerPage', 'model', 'delayScroll', 'cssclass', 'actions',
              'columnResizing', 'columnReordering'
              ]
    delayScroll = "true"
    cssclass=""
    rowsPerPage = 20
    columns = []
    columnReordering = "true"
    columnResizing="false"
    include_dynamic_js_calls = True
    action='.json'
    model = None
    actions = True
    template = """<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/"
                         dojoType="$dojoType"
                         jsId="${jsId}"
                         id="${id}"
                         store="${jsId}_store"
                         columnReordering="${columnReordering}"
                         rowsPerPage="${rowsPerPage}"
                         model="${model}"
                         delayScroll="${delayScroll}"
                         class="${cssclass}"
                         >
    <thead>
            <tr>
                <th py:if="actions" field='__actions__'>actions</th>
                <th py:for="column in columns" field="${column}" width="auto" editor="dojox.grid.editors.Input">$column
                </th>

            </tr>
    </thead>
    <div dojoType="dojox.data.QueryReadStore" jsId="${jsId}_store"  id="${jsId}_store" url="${action}"/>
    </table>
    """
    
class SproxDojoSelectShuttleField(DojoSelectShuttleField, PropertyMixin):
    def update_params(self, d):
        self._my_update_params(d)
        super(SproxDojoSelectShuttleField, self).update_params(d)

