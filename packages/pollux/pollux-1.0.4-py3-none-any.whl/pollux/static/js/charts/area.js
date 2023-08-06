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
// for each subcorpus
for (var i = 0; i < data.length; i++){
  // get the dict of token: freq
    var obj = data[i];
    subNames.push(obj[selections[0]]);
    for (var key in obj) {
        var value = obj[key];
        // if not already there, add the entry
        if (out.hasOwnProperty(key)) {
        } else {
            out[key] = {'key': key, 'values': []};
        }
        if (typeof value != 'undefined') {
            var coord = [i, parseFloat(value)];
            out[key]['values'].push(coord);
        }
    }
}

delete out[selections[0]];
delete out['_state'];
var data = $.map(out, function(value, key) { return value });

// remove words that for whatever reason aren't in columns
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

  /* Set up chart as normal */
  var chart = nv.models.stackedAreaChart()
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] })
                .clipEdge(true)
                //.useInteractiveGuideline(true)
      ;

  chart.xAxis.tickFormat(function(d){
    return subNames[d];
  });
  chart.xAxis.ticks(subNames.length);
  chart.xAxis.rotateLabels(-45);
  chart.height(800);

  d3.select('#area svg')
    .datum(data)
      .transition().duration(500).call(chart);

  nv.utils.windowResize( chart.update );
  return chart;
});
//d3.select('#area-chart svg').update();
