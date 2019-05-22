$(function(){
    function logEvent(eventName) {
        var logList = $("#events ul"),
            newItem = $("<li>", { text: eventName });

        logList.prepend(newItem);
    }

    $("#gridContainer").dxDataGrid({
        dataSource: employees,
        keyExpr: "id",
        showBorders: true,
        paging: {
            enabled: false
        },
        editing: {
            mode: "row",
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },
        columns: [
            {
                dataField: "username",
                caption: "Title"
            },
            {
                dataField: "password",
                caption: "Password"
            }
        ],
        onEditingStart: function(e) {
            logEvent("EditingStart");
        },
        onInitNewRow: function(e) {
            logEvent("InitNewRow");
        },
        onRowInserting: function(e) {
            logEvent("RowInserting");
        },
        onRowInserted: function(e) {
            logEvent("RowInserted");
        },
        onRowUpdating: function(e) {
            logEvent("RowUpdating");
        },
        onRowUpdated: function(e) {
            logEvent("RowUpdated");
        },
        onRowRemoving: function(e) {
            logEvent("RowRemoving");
        },
        onRowRemoved: function(e) {
            logEvent("RowRemoved");
        }
    });


    $("#clear").dxButton({
        text: "Clear",
        onClick: function() {
            $("#events ul").empty();
        }
    });
});