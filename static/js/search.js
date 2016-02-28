var map;
var markers = [];

function initMap() {
    var myCenter = new google.maps.LatLng(41.795113,-87.594300);
    map = new google.maps.Map(document.getElementById('map'), {
        center: myCenter,
        zoom: 15,
        mapTypeControl: false,
        zoomControl: true,
    });
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Shows any markers currently in the array.
function showMarkers() {
  setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}

// Searches database for
function search() {
    q_bedsize = $("#bedsize").val();
    q_bathroom = $("#bathroom").val();
    q_fall = $("#fall").is(':checked');
    q_winter = $("#winter").is(':checked');
    q_spring = $("#spring").is(':checked');
    q_summer = $("#summer").is(':checked');
    slider_vals = slider.noUiSlider.get();
    $.ajax({
        url: '/search_data/',
        type: 'GET',
        data: { bedsize: q_bedsize, bathroom : q_bathroom, fall : q_fall, winter : q_winter, spring : q_spring, summer : q_summer, price_low : Math.round(slider_vals[0]), price_high : Math.round(slider_vals[1])} ,
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            $("#results").html(response);
        },
        error: function () {
            alert("error");
        }
    });
    $.ajax({
        url: '/search_coordinates/',
        type: 'GET',
        data: {},
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            deleteMarkers();
            for (var i = 0; i < response.length; i++) {
                var data = response[i];
                latlng = new google.maps.LatLng(data.fields.latitude, data.fields.longitude);
                var marker = new google.maps.Marker({
                    position: latlng,
                    map: map,
                    title: "poop"
                });
                markers.push(marker);
            }
        },
        error: function () {
            alert("error");
        }
    });
}





$(document).ajaxStart( function() {
    $("#spinner").removeClass('disabled');
}).ajaxStop( function() {
    $("#spinner").addClass('disabled')
});


$(document).ready(function() {

    var slider = document.getElementById('slider');
    noUiSlider.create(slider, {
        start: [300, 700],
        connect: true,
        range: {
            'min': 0,
            'max': 1000
        }
    });

    $(".filter").change(function() {
        search();
    });

    slider.noUiSlider.on('change', function(){
        search();
    });

    search();
});
