$(document).ready(function () {
    var ctx_donut = $("#donut-chart").get(0).getContext("2d");
    var ctx = $("#bar-chart").get(0).getContext("2d");
    var options = {
        responsive: true,
        // legendCallback: function(chart){
        //     var labels = chart.data.labels;
        //     var colors = chart.data.datasets[0].backgroundColor;
        //     var legHTML = "";
        //     for (var i=0; i<labels.length; i++){
        //         $('#legend').append("<p id='"+labels[i]+"'>" + labels[i] +"</p>");
        //         $('#'+labels[i]).css('color', colors[i]);
        //     }
        }; //end of var options
    // get the data!
    $.get('/reports-per-capita.json', showDonutChart);
    $.get('/reports-each-day-of-week.json', showBarChart);

    // make a chart
    function showDonutChart(data){
        var donutChart = new Chart(ctx_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: options
                                                }); //end of var donutChart
        // $('#legend').html(donutChart.generateLegend());
    } //end of showCharts function

    function showBarChart(data) {
        var barChart = new Chart(ctx, {
                                        type: 'bar',
                                        data: data,
                                        options: options
                                       }); //end of var barChart
    }

}); //end of document.ready function