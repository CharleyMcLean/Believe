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
    });

    
  }


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
          }
          else {
            console.log("skipped");
          }
          console.log(report.latitude);
          console.log(report.longitude);
        }

        console.log(heatMapData);
        console.log(typeof(heatMapData));
        console.log($.isArray(heatMapData));
        // return heatMapData;

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: heatMapData,
          map: map
    });

      });
  } //end getPoints()
  

google.maps.event.addDomListener(window, 'load', initMap);
getPoints();
});