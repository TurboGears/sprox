//alert('here');
dojo.require("dojo.parser");
dojo.require("dojox.data.QueryReadStore");
dojo.require("dojox.grid.DataGrid");
dojo.require("dojo._base.xhr");
dojo.addOnLoad(
    function(){
        dojo.__XhrArgs = {preventCache:true}
        dojo.parser.parse();
    });

