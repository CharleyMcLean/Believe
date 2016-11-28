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
            text: 'UFO Reports per 100,000 People by State',
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
            text: 'UFO Reports by Weekday',
            fontSize: 20,
        }
    }; //end of var optionsBar


    var donutInView = false;
    var barInView = false;

    function isScrolledIntoView(elem) {
        var docViewTop = $(window).scrollTop();
        var docViewBottom = docViewTop + $(window).height();

        var elemTop = $(elem).offset().top;
        var elemBottom = elemTop + $(elem).height();

        return ((elemTop <= docViewBottom) && (elemBottom >= docViewTop));
    }

     // make a chart
    function showDonutChart(data){
        var donutChart = new Chart(ctx_donut, {
                                                  type: 'doughnut',
                                                  data: data,
                                                  options: optionsDonut,
                                                }); //end of var donutChart
    } //end of showCharts function

    function showBarChart(data) {
        var barChart = new Chart(ctx, {
                                        type: 'bar',
                                        data: data,
                                        options: optionsBar,
                                       }); //end of var barChart
    }

    $(window).scroll(function() {
        if (isScrolledIntoView('#donut-chart')) {
            
            // if donut wasnt in view, and now IS
            if (donutInView===false) {
                donutInView = true;
                $.get('/reports-per-capita.json', showDonutChart);
            } //end of if donutInView statement
            
        } else { //end of if isScrolledIntoView and beginning of else statements
            donutInView = false;
        } //end of else statement

        // if (isScrolledIntoView('#bar-chart')) {

        //     if(barInView === false) {
        //         barInView = true;
        //         $.get('/reports-each-day-of-week.json', showBarChart);

        //     } else { //end of if barInView and beginning of else statements
        //         barInView = false;
        //     } //end of else statement
        // }
    });
    
     //end of window.scroll function

    // get the data!
    // $.get('/reports-per-capita.json', showDonutChart);
    $.get('/reports-each-day-of-week.json', showBarChart);

}); //end of document.ready function