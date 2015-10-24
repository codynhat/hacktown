var map, heatmap;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.775, lng: -122.434},
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });
}
  heatmap1 = new google.maps.visualization.HeatmapLayer({
    data: getPoints1(),
    map: map
  });

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
  heatmap1.set('gradient', heatmap1.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

// Heatmap data: 500 Points
function getPoints1() {
    return
}