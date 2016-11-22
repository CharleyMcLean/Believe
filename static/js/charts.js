$(document).ready(function () {
    var ctx_donut = $("#donut-chart").get(0).getContext("2d");
    var ctx = $("#bar-chart").get(0).getContext("2d");
    var optionsDonut = {
        responsive: true,
        legend: {
            display: false
        },
        title: {
            display: true,
            text: 'UFO Reports per capita in each state',
            fontSize: 20,
            fontFamily: "'Open Sans', sans-serif",
        },
    }; //end of var optionsDonut

    var optionsBar = {
        responsive: true,
        legend: {
            display: false
        },
        title: {
            display: true,
            text: 'UFO Reports by day of the week',
            fontSize: 20,
        }
    }; //end of var optionsBar


    // get the data!
    $.get('/reports-per-capita.json', showDonutChart);
    $.get('/reports-each-day-of-week.json', showBarChart);

    // make a chart
    function showDonutChart(data){
        var donutChart = new Chart(ctx_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: optionsDonut,
                                                }); //end of var donutChart
        // $('#legend').html(donutChart.generateLegend());
    } //end of showCharts function

    function showBarChart(data) {
        var barChart = new Chart(ctx, {
                                        type: 'bar',
                                        data: data,
                                        options: optionsBar,
                                       }); //end of var barChart
    }

}); //end of document.ready function