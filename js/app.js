var map, heatmap;

function initMap() {
  "use strict";
    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.775, lng: -122.434},
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: getPoints(),
    map: map
  });
    
  /*heatmap2 = new google.maps.visualization.HeatmapLayer({
    data: getPoints2(),
    map: map
  });
    
    heatmap3 = new google.maps.visualization.HeatmapLayer({
        data: test(),
        map: map,
        radius: 100
    })*/
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 255, 255, 0)', //Transparent
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(0, 0, 191, 1)',
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

// Heatmap data: 500 Points
function getPoints() {
    $.ajax({
        url: 'flask/getpoint.py', //TO DO
        type: 'GET',
        dataType: 'json',
        data: {
            'query' : $('input[name=query]')
        },
        success: function(json) {
            var array = [];
            $.each(json, function (i, item) {
                array.push(new google.maps.visualization.WeightLocation(google.maps.LatLng(json.lat, json.long), json.weight + 1.01));
            });
            return array;
        },
        error: function (xhr, desc, err) {
            console.log(xhr);
            console.log("Details: " + desc + "\nError: " + err);
        }
   });
}
