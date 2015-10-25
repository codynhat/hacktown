/*global google*/
var map, heatmap;

function initMap() {
    "use strict";
    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 38.8833, lng: -102.9833},
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true,
    scrollwheel: false,
    zoomControl: false,
    navigationControl: false,
    mapTypeControl: false,
    scaleControl: false,
    draggable: false,
    disableDoubleClickZoom: true
  });

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map
    });
/*
  happy_heatmap = new google.maps.visualization.HeatmapLayer({
    data: getPoints2(),
    map: map
  });

    heatmap3 = new google.maps.visualization.HeatmapLayer({
        data: test(),
        map: map,
        radius: 100
    }); */
}


function toggleHeatmap() {
  "use strict";
    heatmap.setMap(heatmap.getMap() ? null : map);
}

/*function changeGradient() {
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
}*/

// Heatmap data: 500 Points
function getPoints() {
    return [
        new google.maps.LatLng(37.782551, -122.445368),
        new google.maps.LatLng(37.782745, -122.444586),
        new google.maps.LatLng(37.782842, -122.443688),
        new google.maps.LatLng(37.782919, -122.442815),
        new google.maps.LatLng(37.782992, -122.442112),
        new google.maps.LatLng(37.783100, -122.441461),
        new google.maps.LatLng(37.783206, -122.440829),
        new google.maps.LatLng(37.783273, -122.440324),
        new google.maps.LatLng(37.783316, -122.440023),
        new google.maps.LatLng(37.783357, -122.439794),
        new google.maps.LatLng(37.783371, -122.439687),
        new google.maps.LatLng(37.783368, -122.439666),
        new google.maps.LatLng(37.783383, -122.439594),
        new google.maps.LatLng(37.783508, -122.439525),
        new google.maps.LatLng(37.783842, -122.439591),
        new google.maps.LatLng(37.784147, -122.439668),
        new google.maps.LatLng(37.784206, -122.439686),
        new google.maps.LatLng(37.784386, -122.439790),
        new google.maps.LatLng(37.784701, -122.439902),
        new google.maps.LatLng(37.784965, -122.439938),
        new google.maps.LatLng(37.785010, -122.439947),
        new google.maps.LatLng(37.785360, -122.439952),
        new google.maps.LatLng(37.785715, -122.440030),
    ];
<<<<<<< HEAD

=======
    
    /*
    $SCRIPT_ROOT = {{request.script_root | tojson | safe}};
    var $value = $('#ideas option:selected').text();
    $.ajax({
        url: $SCRIPT_ROOT + '/_tweet_calcs', //TO DO
        type: 'GET',
        dataType: 'json',
        data: {
            'query' : $value
        },
        success: function(json) {
            var array = [];
            $.each(json, function (i, item) {
                var coordinates = new google.maps.LatLng(json.lat, json.lng);
                array.push(new google.maps.visualization.WeightLocation(coordnates, json.wgt + 1.01));
            });
            return array;
        },
        error: function (xhr, desc, err) {
            console.log(xhr);
            console.log("Details: " + desc + "\nError: " + err);
        }
   });*/
>>>>>>> 90c0c5d5ab9ccace21675f962febe402d065fab9
}
