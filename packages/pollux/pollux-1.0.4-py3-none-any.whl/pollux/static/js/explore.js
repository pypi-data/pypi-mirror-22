
// everything we need to do after a search/filter is performed
function updateChart(kind) {

    var loc = "{{ url_for('static',filename='js/charts/bar.js') }}"
    loc = loc.replace('bar', kind);
    $("#area, #line, #bar, #pie").css("display", "none");
    $("#" + kind).css("display", "");
    $.getScript(loc);
}

function updateViews(data) {

  var updates = data.needupdate;
  $('.keep-dels').prop('disabled', false);
  $('.keep-dels').selectpicker('refresh');

  if (updates.includes('conc')) {
    $('#conc-table').bootstrapTable('refreshOptions', data.conc);
  }

  if (updates.includes('pivot')) {
    $("#pivot-space").pivotUI(data.pivot, {rows: ["file"],
                                             cols: ["word"]});
  }
  if (updates.includes('table')) {
    $('#table-table').bootstrapTable('refreshOptions', data.table);
    var charttype = $("#chart-type option:selected").val().toLowerCase();
    if (!charttype) {
      charttype = 'bar';
    }
    updateChart(charttype);
  }

  if (updates.includes('table_extra')) {
    var ht = $.parseHTML(data.table_extra);
    $('#viewer-relative').selectpicker('destroy');
    $('#viewer-relative').replaceWith(ht);
    $('#viewer-relative').selectpicker('refresh');    
  }

  if (updates.includes('tree')) {
    var attrs = ["lemma", "pos"];
    var abbvs = {"lemma": "Lemma"};
    $('#diagram-div').empty();
    arcDiagram(data.tree, attrs, abbvs, false);
    //treeDiagram(data.cons, attrs, abbvs, false);
    //var Zoomer = svgPanZoom('#tree', opt);
    $("#sent-text").attr("data-num", "0");
    $("#sent-text").text(data.sent); 
  }

  if (updates.includes('previous')) {
    var htm = $.parseHTML(data.previous);
    $('#prev-list').replaceWith(htm);
    $('#conc-tab-button-text').text('Concordance');
    $("#query-submit-button").empty();
    $("#query-submit-button").attr("class", "btn btn-warning");
    $("#query-submit-button").append('<span class="glyphicon glyphicon-filter"></span>');
    $("#query-submit-button").append(" Filter");
  }

  $(".table").bootstrapTable("hideLoading");
}

var opt = {panEnabled: true,
           center: false,
           controlIconsEnabled: true,
           preventMouseEventsDefault: true}


function LinkFormatter(value, row, index) {
  return "<a href='/explore/"+value+"'>"+value+"</a>";
}

// add in all data when the page is loaded
$(document).ready( function() {
  var derivers = $.pivotUtilities.derivers;
  var renderers = $.extend($.pivotUtilities.renderers, $.pivotUtilities.c3_renderers, $.pivotUtilities.d3_renderers);
  $(".table").bootstrapTable("showLoading");
  $('#table-table').bootstrapTable({{ initial_data.table|tojson }});
  $('#conc-table').bootstrapTable({{ initial_data.conc|tojson }});
  $("#pivot-space").pivotUI({{ initial_data.pivot|tojson }},
                            {rows: ["file"],
                             cols: ["word"],
                             renderers: renderers});
  $(".table").bootstrapTable("hideLoading");
  $("#extra-toolbar-table").removeAttr('style');
  $("#extra-toolbar-conc").removeAttr('style');
  var attrs = ["lemma", "pos"]
  var abbvs = {"lemma": "Lemma"}
  $('#diagram-div').empty();
  arcDiagram({{ initial_data.tree|tojson }}, attrs, abbvs, false);
  var Zoomer = svgPanZoom('#arc', opt);
  //var Zoomer = svgPanZoom('#arc', opt);
  //treeDiagram({{ initial_data.cons|tojson }}, attrs, abbvs, false);
  //var Zoomer = svgPanZoom('#tree', opt);
  $('#sent-text').text( {{ initial_data.sent|tojson }} );
});

// previous queries, which need to collapse etc.
// defined via 'on' because they are deleted and remade
$('#previous-searches').on('click', '.list-group-item', function() {
  var $this = $(this);
  // (1) if disabled, do nothing
  if ($this.attr("class").indexOf("disabled") >= 0) {
    $this.attr('disabled', true);
    return false;
  }
  // if active, and has down arrow, collapse
  if ($this.attr("class").indexOf("active") >= 0) {
    // these two lines don't seem to work
    if ($this.children().first().attr("class").indexOf("chevron-down") >= 0) {
      $this.next().removeClass('in');
      $this.children().first().removeClass("glyphicon-chevron-down");
      $this.children().first().addClass("glyphicon-chevron-right");
    }
    else if ($this.children().first().attr("class").indexOf("chevron-right") >= 0) {
      $this.next().addClass('in');
      $this.children().first().removeClass("glyphicon-chevron-right");
      $this.children().first().addClass("glyphicon-chevron-down");
    }
    // if has no down arrow, do nothing, as it is already selected
    return false;
  }
  if ($this.children().first().attr("class").indexOf("chevron-right") >= 0 && 
     $this.attr('data-edits') != "0") {
    $this.next().collapse('show');
    $this.children().first().attr("class", "glyphicon glyphicon-chevron-down");
    //return false;
  }

  // remove active from others and make this one active
  $("#prev-list").find('a').removeClass('active');
  $this.addClass('active');

  $(".table").bootstrapTable("showLoading");    

  if ($this.children().first().attr("class").indexOf("globe") >= 0) {
    $(this).parent().find('.list-group').removeClass('in');
    // make all chevrons right
    var chevs = $this.parent().find(".glyphicon-chevron-down");
    chevs.removeClass("glyphicon-chevron-down");
    chevs.addClass("glyphicon-chevron-right");

    $('#conc-tab-button-text').text('Sentences');
    $('.keep-dels').prop('disabled', true);
    $('.keep-dels').selectpicker('refresh');
    $("#query-submit-button").empty();
    $("#query-submit-button").attr("class", "btn btn-primary");
    $("#query-submit-button").append('<span class="glyphicon glyphicon-search"></span>');
    $("#query-submit-button").append(" Search");
  } else {
    $('.keep-dels').prop('disabled', false);
    $('.keep-dels').selectpicker('refresh');
    $('#conc-tab-button-text').text('Concordance');
    $("#query-submit-button").empty();
    $("#query-submit-button").attr("class", "btn btn-warning");
    $("#query-submit-button").append('<span class="glyphicon glyphicon-filter"></span>');
    $("#query-submit-button").append(" Filter");
  }
  // get the result and reset the data
  var dpath = $SCRIPT_ROOT + '/view_different_result/' + $this.attr("data-searchnum");
  $.getJSON(dpath, {}, function(data) {
    updateViews(data);
  });
});

// post the data, rather than submit the form. then, we can update views with it
$(function(){
  $('form[name=query-form]').submit(function(){
    $(".table").bootstrapTable("showLoading");
    var corp_id = $("#prev-list a.active").attr("id");
    $(".searchfrom").attr("value", corp_id);
    $.post($(this).attr('action'), $(this).serialize(), function(data) {
      updateViews(data);
    }, 'json');
    return false;
  });
});

$(document).ready( function() {
  var clickEvent = false;
  selections = ["file "];
  $('.carousel-tabs').on('click', '.nav a', function() {
      clickEvent = true;
      $(this).parent().siblings().removeClass('active');
      $(this).parent().addClass('active');    
      //$(window).trigger('resize');
  }).on('slid.bs.carousel', function(e) {
    if(!clickEvent) {
      var count = $('.nav').children().length -1;
      var current = $('.nav li.active');
      current.removeClass('active').next().addClass('active');
      var id = parseInt(current.data('slide-to'));
      if(count == id) {
        $(this).parent().siblings().first().addClass('active');  
      }
    }
    clickEvent = false;
  });
});

// if the user clicks a sentence to view, show it
$(document).on('click', '.view-tree', function () {
  var idx = $("#prev-list a.active").attr("id");
  $("#tree-tab-button-text").click();
  // if we clicked a next/previous button
  if ($(this).hasClass("make-num")) {
    if ($(this).hasClass("start")) {
      var tabId = 0
    } else if ($(this).hasClass("minus")) {
      var tabId = parseInt($('#sent-text').attr("data-num"))-1
    } else if ($(this).hasClass("plus")) {
      var tabId = parseInt($('#sent-text').attr("data-num"))+1
    } else if ($(this).hasClass("end")) {
      var tabId = $('#conc-table').bootstrapTable('getOptions').totalPages
    }

  } else {
    // if we are clicking a conc line, we can get its unique id
    var tabId = parseInt($(this).attr("data-num"));
  }
  $('#sent-text').attr("data-num", tabId);
  var dpath = $SCRIPT_ROOT + '/view_tree/' + idx + '/' + $(this).attr("value");
  $.getJSON(dpath, {}, function(data) {
    var attrs = ["lemma", "pos"];
    var abbvs = {"lemma": "Lemma"};
    //var attrs = [];
    //var abbvs = [];
    $('#diagram-div').empty();
    //arcDiagram(data.tree, attrs, abbvs, false);
    //var Zoomer = svgPanZoom('#arc', opt);
    treeDiagram(data.cons, attrs, abbvs, false);
    var Zoomer = svgPanZoom('#tree', opt);

    $('#sent-text').text(data.text);
  });
});

function makeDataFromTable() {
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
    return {data: data, subNames: subNames}
}

