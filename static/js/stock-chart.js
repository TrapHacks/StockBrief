var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
var lineChartData = {
    labels : ["January","February","March","April","May","June","July"],
    datasets : [
        {
            label: "My Second dataset",
            fillColor : "#75C5C6",
            strokeColor : "#5b5b5b",
            pointColor : "#75C5C6",
            pointStrokeColor : "#5b5b5b",
            pointHighlightFill : "#fff",
            pointHighlightStroke : "rgba(151,187,205,1)",
            data : [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]
        }
    ]
}

// event handler for when the collapse is shown
$(".collapse").on('shown.bs.collapse', function(){
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx).Line(lineChartData, {
        responsive: true,
        bezierCurve: false,
        scaleShowVerticalLines: false
    });
});