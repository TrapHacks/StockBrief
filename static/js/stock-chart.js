var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
var lineChartData = {}

//on search button click
$("#search").click(function() {
  //post request that gets data 
  console.log('hello');
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
});

// event handler for when the collapse is shown
// $(".collapse").on('shown.bs.collapse', function(){
// });