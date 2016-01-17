var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
var lineChartData = {}

//on search button click
$("#search").click(function() {
  //post request that gets data 
  var search_val = $('#stock_name').val();
  console.log({"search_val": search_val});
  var return_data = $.post("/search",search_val,function(data) {
    lineChartData= {
        labels : data.dates.slice(0,50).slice(4),
        datasets : [
            {
                label: "My Second dataset",
                fillColor : "#75C5C6",
                strokeColor : "#5b5b5b",
                pointColor : "#75C5C6",
                pointStrokeColor : "#5b5b5b",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(151,187,205,1)",
                data : data.prices.slice(0,50)
            }
        ]
    }

  });
  console.log("return:",return_data);
});

// event handler for when the collapse is shown
$(".collapse").on('shown.bs.collapse', function(){
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx).Line(lineChartData, {
        responsive: true,
        bezierCurve: false,
        scaleShowVerticalLines: false
    });
});