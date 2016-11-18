$(document).ready(function () {
    var ctx_donut = $("#donut-chart").get(0).getContext("2d");
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
            };
        // get the data!
        $.get('/reports-per-capita.json', showCharts);
        // make a chart
        function showCharts(data){
            var donutChart = new Chart(ctx_donut, {
                                                      type: 'doughnut',
                                                      data: data,
                                                      options: options
                                                    });
            // $('#legend').html(donutChart.generateLegend());
        }
});