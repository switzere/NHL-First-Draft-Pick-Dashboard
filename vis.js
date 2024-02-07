function drawViz(data) {
    //looker studio nhl goal heatmap

    //get data from data source
    var data = data.tables.DEFAULT;

    //get data from data source
    var data = data.tables.DEFAULT;
}

// Subscribe to data and style changes. Use the table format for data.
dscc.subscribeToData(drawViz, { transform: dscc.tableTransform });