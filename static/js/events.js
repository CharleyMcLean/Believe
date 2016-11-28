var UGLYRED = ['rgba(180, 100, 50, 0)',
               'rgba(180, 100, 50, 0.5)',
               'rgba(195, 100, 50, 0.5)',
               'rgba(210, 100, 50, 0.5)',
               'rgba(225, 100, 50, 0.5)',
               'rgba(240, 100, 50, 0.5)',
               'rgba(240, 100, 44, 0.5)',
               'rgba(240, 100, 37, 0.5)',
               'rgba(240, 100, 31, 0.5)',
               'rgba(240, 100, 25, 0.5)',
               'rgba(282, 100, 18, 0.5)',
               'rgba(330, 100, 25, 0.5)',
               'rgba(350, 100, 37, 0.5)',
               'rgba(0, 100, 50, 0.5)'
                ]; //end var UGLYRED

var AQUA = ['rgba(0, 255, 255, 0)',
            'rgba(0, 255, 255, 0.5)',
            'rgba(0, 191, 255, 0.5)',
            'rgba(0, 127, 255, 0.5)',
            'rgba(0, 63, 255, 0.5)',
            'rgba(0, 0, 255, 0.5)',
            'rgba(0, 0, 223, 0.5)',
            'rgba(0, 0, 191, 0.5)',
            'rgba(0, 0, 159, 0.5)',
            'rgba(0, 0, 127, 0.5)',
            'rgba(63, 0, 91, 0.5)',
            'rgba(127, 0, 63, 0.5)',
            'rgba(191, 0, 31, 0.5)',
            'rgba(255, 0, 0, 0.5)'
            ]; //end var AQUA


$(document).ready(function () {
  
    var map, heatmap, popHeatmap;

    function initMap() {

        // Center the map on the US.
        var myLatLng = {lat: 39.5, lng: -98.35};

        // Create a map object and specify the DOM element for display.
        map = new google.maps.Map(document.getElementById('map'), {
          center: myLatLng,
          zoom: 4,
          zoomControl: true,
          styles: MAPSTYLES,
          mapTypeId: google.maps.MapTypeId.TERRAIN
        }); //end new map
        console.log("map exists");
        getPoints();
        getPopPoints();
    } //end initMap

///////////////////////////////////////////////////////////////////////////

    function toggleHeatmap() {
        heatmap.setMap(heatmap.getMap() ? null : map);
    } //end toggleHeatmap

    function changeGradient() {
        var gradient = AQUA; //end var gradient
        
        heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
    } //end changeGradient

    function changeRadius() {
        heatmap.set('radius', heatmap.get('radius') ? null : 20);
    } //end changeRadius

    function changeOpacity() {
        heatmap.set('opacity', heatmap.get('opacity') ? null : 2);
    } //end changeOpacity

  
    function getPoints() {
    // Retrieving the information with AJAX
        $.get('/events.json', function (events) {
            // Create an array of lat/long points from returned JSON
            
            // Create an empty array to hold the map point data
            var heatMapData = [];
      
            // Defined a function to create a new map point from each report 
            // This is then pushed to the JS array we created.
            
            for (var key in events) {
                var report = events[key];
                // console.log(report);
                if (!(report.latitude == 48 & report.longitude == -122)) {
                heatMapData.push(new google.maps.LatLng(report.latitude, report.longitude));
                } //end if statement
                else {
                console.log("skipped");
                } //end else statement
                // console.log(report.latitude);
                // console.log(report.longitude);
            } //end for loop

            console.log(heatMapData);
            console.log(typeof(heatMapData));
            console.log($.isArray(heatMapData));
            // return heatMapData;

            console.log("about to add heatmap");
            heatmap = new google.maps.visualization.HeatmapLayer({
                data: heatMapData,
                map: map,
                radius: 20
            }); //end new heatmap
            console.log("just added heatmap");
        }); //end $.get
    } //end getPoints()

    // JQuery toggles for UFO heatmap
    $("#toggle-heatmap").click(function() {
        toggleHeatmap();
    });
    $("#change-gradient").click(function() {
        changeGradient();
    });
    $("#change-radius").click(function() {
        changeRadius();
    });
    $("#change-opacity").click(function() {
        changeOpacity();
    });

    $("#toggle-heatmap").click(function(){
        $(this).toggleClass('purple');
    });

    $("#change-gradient").click(function(){
        $(this).toggleClass('blue');
    });

    $("#change-radius").click(function(){
        $(this).toggleClass('blue');
    });

    $("#change-opacity").click(function(){
        $(this).toggleClass('blue');
    });


///////////////////////////////////////////////////////////////////////////
    // Toggle the population heatmap on and off.
    function togglePopHeatmap() {
        popHeatmap.setMap(popHeatmap.getMap() ? null : map);
    } //end togglePopHeatmap

    // Toggle between AQUA and UGLYRED gradients
    function changePopGradient() {
        
        var currentGradient = popHeatmap.get('gradient');

        if (currentGradient === AQUA) {
            popHeatmap.set('gradient', UGLYRED);
        }

        if (currentGradient === UGLYRED) {
            popHeatmap.set('gradient', AQUA);
        }
        
    } //end changePopGradient


    // Toggle between a larger and smaller radius.
    function changePopRadius() {
        popHeatmap.set('radius', popHeatmap.get('radius') ? null : 20);
    } //end changePopRadius


    // Toggle the opacity.
    function changePopOpacity() {
        popHeatmap.set('opacity', popHeatmap.get('opacity') ? null : 2);
    } //end changePopOpacity


    // Compile the data for the population heatmap layer.
    function getPopPoints() {
        // Retrieving the information with AJAX
        $.get('/population.json', function (city_pops) {
            // Create an array of lat/long points from returned JSON
            
            // Create an empty array to hold the map point data
            var heatMapPopData = [];
      
            // Defined a function to create a new map point from each report 
            // This is then pushed to the JS array we created.
            
            for (var key in city_pops) {
                var city = city_pops[key];
                heatMapPopData.push({location: new google.maps.LatLng(city.latitude, city.longitude), weight: city.population});
            } //end for loop


            console.log("about to add pop heatmap");
            popHeatmap = new google.maps.visualization.HeatmapLayer({
                data: heatMapPopData,
                map: map,
                radius: 20,
                gradient: AQUA
            }); //end new heatmap
            console.log("just added pop heatmap");
        }); //end $.get
    } //end getPoints()


    // Jquery for button clicks.
    $("#toggle-pop-heatmap").click(function() {
        togglePopHeatmap();
    });

    $("#change-pop-gradient").click(function() {
        console.log("About to change gradient");
        changePopGradient();
        console.log("Changed gradient");
    });

    $("#change-pop-radius").click(function() {
        changePopRadius();
    });

    $("#change-pop-opacity").click(function() {
        changePopOpacity();
    });

    $("#toggle-pop-heatmap").click(function(){
        $(this).toggleClass('purple');
    });

    $("#change-pop-gradient").click(function(){
        $(this).toggleClass('blue');
    });

    $("#change-pop-radius").click(function(){
        $(this).toggleClass('blue');
    });

    $("#change-pop-opacity").click(function(){
        $(this).toggleClass('blue');
    });


    google.maps.event.addDomListener(window, 'load', initMap);
    
}); //end $(document).ready