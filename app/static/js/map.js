// Render the markers for cab locations on Google Maps
var SF = new google.maps.LatLng(37.7577, -122.4376);
var markers = [];
var map;
var userMarker;
var updateProcess;

function initialize() {
    var mapOptions = {
        zoom: 13,
        center: SF
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    google.maps.event.addListener(map, 'click', function (e) {
        placeMarker(e.latLng);
    })
}

function placeMarker(position) {
    clearTimeout(updateProcess);
    clearUserMarker();
    userMarker = new google.maps.Marker({
        position: position,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 10
        },
        map: map
    });
    map.panTo(position);
    update_values(position);
}

function update_values(position) {
    $.getJSON('/realtime/' + position.A + '/' + position.F,
        function (data) {
            cabs = data.cabs
            console.log(cabs)
            clearMarkers();
            for (var i = 0; i < cabs.length; i = i + 1) {
                addMarker(new google.maps.LatLng(cabs[i].lat, cabs[i].lng));
            }
        });

    updateProcess = window.setTimeout(function(){
        update_values(position)
    }, 2000);
}

//update_values();
function drop(lat, lng) {
    point = new google.maps.LatLng(lat, lng);
    clearMarkers();
    addMarker(point);
}

function addMarker(position) {
    markers.push(new google.maps.Marker({
        position: position,
        //icon: 'templates/images/taxi.png',
        map: map,
    }));
}

function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

function clearUserMarker() {
    if (userMarker != null) {
        userMarker.setMap(null);
    }
}

google.maps.event.addDomListener(window, 'load', initialize);
