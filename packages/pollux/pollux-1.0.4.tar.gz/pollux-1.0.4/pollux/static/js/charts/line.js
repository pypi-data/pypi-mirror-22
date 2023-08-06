var data = $('#table-table').bootstrapTable('getData');
var order = [];
$('#table-table > thead > tr > th').each(function(){
    order.push($(this).text())
})
// 2 gets rid of the checkbox and file ... multiindex will need fixing
order = order.slice(2)
// starts as dictionary, will become array later
var out = {}
var subNames = []
// for each subcorpus, i.e. over each file
for (var i = 0; i < data.length; i++){
  // get the dict of token: freq
    var obj = data[i];
    // in that dict is the subcorpus name, to pop out
    subNames.push(obj[selections[0]]);
    // for each token: frequency pair
    for (var key in obj) {
        var value = obj[key];

        // if not already there, add the entry
        if (out.hasOwnProperty(key)) {
        } else {
            out[key] = {'key': key, 'values': []};
        }
        // if it's good data, make the object for the 'values' value
        if (typeof value != 'undefined') {
            // y is the freq, but we need x as the location on the x axis
            // starting from 0.
            var v = parseFloat(value)
            if (v < 0) {
                v = 0
            }
            var coord = {y: v, x: i, label: obj[selections[0]]};
            out[key]['values'].push(coord);
        }
    }
}
delete out[selections[0]];
delete out['_state'];
var data = $.map(out, function(value, key) { return value });

function inFilter(word) {
    return (!(word.key in order))
}
data = data.filter(inFilter);

data.sort(function(a,b){
    return order.indexOf(a.key) < order.indexOf(b.key) ? -1 : 1;
});
var ntp = $("#num_to_plot").val();

data = data.slice(0, ntp);

nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart();
    chart.brushExtent([0, subNames.length]);
    chart.xAxis.tickFormat(function(d){
      return subNames[d];
    });
    chart.xAxis.rotateLabels(-45);
    chart.x2Axis.tickFormat(function(d){
      return subNames[d];
    });
    chart.x2Axis.rotateLabels(-45);

    // todo: choose float format based on relativeness...
    chart.yTickFormat(d3.format(yAxisFormat));
    chart.useInteractiveGuideline(true);
    d3.select('#line svg')
        .datum(data)
        .call(chart);
    nv.utils.windowResize(chart.update);
    return chart;
});
