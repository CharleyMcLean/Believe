$(document).ready(function () {
  function initMap() {

  // Center the map on the US.
  var myLatLng = {lat: 39.5, lng: -98.35};

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map($('#map'), {
    center: myLatLng,
    scrollwheel: false,
    zoom: 3,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
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



  // Retrieving the information with AJAX
  $.get('/events.json', function (events) {
      // Create an array of lat/long points from returned JSON
      
      // Create an empty array to hold the map point data
      var heatMapData = [];

      // Defined a function to create a new map point from each report 
      // This is then pushed to the JS array we created.
      function getPoints() {
        for (var key in events) {
          report = events[key];

          heatMapData.push(new google.maps.latLng(report.latitude, report.longitude));
        }
        console.log(report.latitude);
        console.log(report.longitude);

        return heatMapData;
      }
    });
  

google.maps.event.addDomListener(window, 'load', initMap);
});