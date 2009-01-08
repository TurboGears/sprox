"""Dojo Specific Widgets"""

from tw.dojo import DojoQueryReadStore, DojoBase, grid_css, tundragrid_css
from tw.api import JSSource

class SproxDojoGrid(DojoBase):
    css = [grid_css, tundragrid_css]
    require = ['dojox.grid.DataGrid', 'dojox.data.QueryReadStore']
    dojoType = 'dojox.grid.DataGrid'
    params = ['id', 'attrs', 'columns', 'jsId', 'url',
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
    url='.json'
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
                <th py:for="column in columns" field="${column}" width="auto">$column
                </th>

            </tr>
    </thead>
    <div dojoType="dojox.data.QueryReadStore" jsId="${jsId}_store"  id="${jsId}_store" url="${url}"/>
    </table>
    """

class SproxDojoQueryReadStore(DojoQueryReadStore):
    params = ['jsId']
    template="""<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip="">
    <div dojoType="${dojoType}" jsId="${jsId}"  id="${jsId}" url="${url}"/>
    </span>
    """

class SproxEditableDojoGrid(DojoBase):
    css = [grid_css, tundragrid_css]
    require = ['dojox.grid.DataGrid', 'dojox.data.QueryReadStore']
    dojoType = 'dojox.grid.DataGrid'
    params = ['id', 'attrs', 'columns', 'jsId', 'url',
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
    url='.json'
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
    <div dojoType="dojox.data.QueryReadStore" jsId="${jsId}_store"  id="${jsId}_store" url="${url}"/>
    </table>
    """