$(document).ready(function () {
  
  var map, heatmap;

  function initMap() {


    // Center the map on the US.
    var myLatLng = {lat: 39.5, lng: -98.35};

    // Create a map object and specify the DOM element for display.
    map = new google.maps.Map(document.getElementById('map'), {
      center: myLatLng,
      zoom: 3,
      zoomControl: true,
      styles: MAPSTYLES,
      mapTypeId: google.maps.MapTypeId.TERRAIN
    }); //end new map
    console.log("map exists");
    getPoints();
  } //end initMap


  // --------------------------------------------------------------//
  // --------------------------------------------------------------//
  // If you want to create a StyledMapType to make a map type control
  // create it like this:

  // Create a new StyledMapType object, passing it the array of styles,
  // as well as the name to be displayed on the map type control.
  // var styledMap = new google.maps.StyledMapType(
  //     MAPSTYLES,
  //     {name: "Custom Style"}
  // );
  // You would then set 'styles' in the mapoptions to 'styledMap'

  // Associate the styled map with the MapTypeId and set it to display.
  // map.mapTypes.set('map_style', styledMap);
  // map.setMapTypeId('map_style');
  // --------------------------------------------------------------//
  // --------------------------------------------------------------//

  function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
  }

  function changeGradient() {
    var gradient = [
      'rgba(0, 255, 255, 0)',
      'rgba(0, 255, 255, 1)',
      'rgba(0, 191, 255, 1)',
      'rgba(0, 127, 255, 1)',
      'rgba(0, 63, 255, 1)',
      'rgba(0, 0, 255, 1)',
      'rgba(0, 0, 223, 1)',
      'rgba(0, 0, 191, 1)',
      'rgba(0, 0, 159, 1)',
      'rgba(0, 0, 127, 1)',
      'rgba(63, 0, 91, 1)',
      'rgba(127, 0, 63, 1)',
      'rgba(191, 0, 31, 1)',
      'rgba(255, 0, 0, 1)'
    ]; //end var gradient
      heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
    } //end changeGradient

  function changeRadius() {
    heatmap.set('radius', heatmap.get('radius') ? null : 20);
  } //end changeRadius

  function changeOpacity() {
    heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
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
          console.log(report.latitude);
          console.log(report.longitude);
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


google.maps.event.addDomListener(window, 'load', initMap);
}); //end $(document).ready