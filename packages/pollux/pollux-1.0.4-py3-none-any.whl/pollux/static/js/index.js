
function LinkFormatter(value, row, index) {
  if (row.parsed == 'False') {
    return "<a href='/parse/"+value+"'>"+value+"</a>";
  } else {return "<a href='/explore/"+value+"'>"+value+"</a>";}
}
