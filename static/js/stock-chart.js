var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
var lineChartData = {}

//on search button click
$("#search").click(function() {
  //post reuqest for chart data------------------------------
  var search_val = $('#stock_name').val();
  var return_data = $.post("/search",search_val,function() {
  })
  .done(function(data) {
    lineChartData= {
        labels : data.dates.slice(data.dates.length-21,data.dates.length-1),
        datasets : [
            {
                label: "Closing Prices",
                fillColor : "#75C5C6",
                strokeColor : "#5b5b5b",
                pointColor : "#75C5C6",
                pointStrokeColor : "#5b5b5b",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(151,187,205,1)",
                data: data.prices.slice(data.prices.length-60,data.prices.length-1)
            }
        ]
    }

    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx).Line(lineChartData, {
        responsive: true,
        bezierCurve: false,
        pointDotRadius: 4,
        scaleShowVerticalLines: false
    });
  });
  //---------------------------------------------------------
  // NY TIMES -----------------------------------------------
  $.post("/nytimes", search_val, function(data) {
    // console.log(data.docs[0])
    for(i = 0; i < 10; ++i){
    var times_var = data.docs[i]
    var main_headline = times_var.headline.main;
    var url = times_var.web_url;
    var par = times_var.lead_paragraph;
    //check for non existen urls
    $('#articles').append("<div class='nytimes'><a class='title' href='" + url + "'>" + main_headline + "</a></div>");
  }
  });
  // --------------------------------------------------------
  // TWITTER ------------------------------------------------
  // $.post("/tweet", search_val, function(data) {
  //   console.log(data);
  //   var sentiment = data.sentiment;
  //   if(sentiment == "Negative"){
  //     console.log("U FAKED UP");
  //   }
  //   else{
  //     console.log("YO");
  //   }
  // });

});

// event handler for when the collapse is shown
// $(".collapse").on('shown.bs.collapse', function(){
// });