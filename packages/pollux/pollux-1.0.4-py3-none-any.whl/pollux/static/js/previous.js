// what to do with the previous panel. it's complicated.

$('#prev-list .list-group-item').on('click', function() {
  var $this = $(this);
  // (1) if disabled, do nothing
  if ($this.attr("class").indexOf("disabled") >= 0) {
    $this.attr('disabled', true);
    console.log("disabled, do nothing");
    return false;
  }
  // if active, do nothing
  if ($this.attr("class").indexOf("active") >= 0) {
    console.log("already active, do nothing");
    return false;
  }
  // remove active from others and make this one active
  $("#prev-list").find('a').removeClass('active');
  $this.addClass('active');

  // if it had a right arrow, it was closed. open it up
  if ($this.children().first().attr("class").indexOf("chevron-right") >= 0) {
    console.log("was right arrow, opening up");
    $this.next().collapse('show');
    $this.children().first().attr("class", "glyphicon glyphicon-chevron-down");
    return false;
  }
  // if not active, and not disabled, we get the result from server
  // show loading
  $(".table").bootstrapTable("showLoading");    

  if ($this.children().first().attr("class").indexOf("globe") >= 0) {
    console.log("corpsu presses, changing buttons");
    $('#conc-tab-button-text').text('Sentences');
    $('.keep-dels').prop('disabled', true);
    $('.keep-dels').selectpicker('refresh');
    $("#query-submit-button").empty();
    $("#query-submit-button").attr("class", "btn btn-primary");
    $("#query-submit-button").append('<span class="glyphicon glyphicon-search"></span>');
    $("#query-submit-button").append(" Search");
  } else {
    console.log("search pressed, changing buttons");
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


//$('#prev-list .list-group-item').on('shown.bs.collapse', function () {
//    var $this = $(this);
//    // (4)
//    if ($this.children().first().attr("class").indexOf("chevron") >= 0) {
//        $this.children().first().attr("class", "glyphicon glyphicon-chevron-down")
//    }
//    // (8a)
//    $(this).find('span').attr("style", "display:none;");
//});
//
//// (8b)
//$('#prev-list .list-group-item').on('hide.bs.collapse', function () {
//    var $this = $(this);
//    $(this).find('span').removeAttr("style");
//    });