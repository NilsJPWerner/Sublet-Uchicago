var map;
var markers = {};

var template = [
    '<div id="listing-{{id}}"" class="ui fluid card" data-marker="{{id}}">',
        '<div class="slider image">',
            '<ul>',
                '{{#photos}}',
                    '<li><img class="slider-image" src="{{.}}"></li>',
                '{{/photos}}',
            '</ul>',
        '</div>',
        '<div class="content">',
            '<a class="header">{{name}}</a>',
            '<div class="meta">',
                '<span class="date"></span>',
            '</div>',
            '<div class="description">',
                'Kristy is an art director living in New York.',
            '</div>',
        '</div>',
        '<div class="extra content">',
            '<a>',
                '<i class="user icon"></i>',
                'Listed by {{}}',
            '</a>',
        '</div>',
    '</div>'
].join('\n');

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i in markers) {
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
  markers = {};
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
        data: { bedsize: q_bedsize, bathroom : q_bathroom, fall : q_fall,
            winter : q_winter, spring : q_spring, summer : q_summer,
            price_low : Math.round(slider_vals[0]), price_high : Math.round(slider_vals[1])} ,
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            deleteMarkers();
            var html = ''
            var default_marker = {
                url: "/static/img/marker.png", // url
                scaledSize: new google.maps.Size(40, 40), // scaled size
                origin: new google.maps.Point(0,0), // origin
                anchor: new google.maps.Point(20,40) // anchor
            };
            var highlight_marker = {
                url: "/static/img/highlight_marker.png", // url
                scaledSize: new google.maps.Size(40, 40), // scaled size
                origin: new google.maps.Point(0,0), // origin
                anchor: new google.maps.Point(20,40) // anchor
            };
            for (var i = 0; i < response.length; i++) {
                var data = response[i];
                var output = Mustache.render(template, data);
                html += output

                latlng = new google.maps.LatLng(data.latitude, data.longitude);
                var marker = new google.maps.Marker({
                    position: latlng,
                    map: map,
                    icon: default_marker,
                    title: data.name,
                    data_id: data.id,
                    data_name: data.name
                });
                markers[data.id] = marker;

                marker.addListener("click", function() {
                    infoWindow.setContent(this['data_name']);
                    infoWindow.open(map, markers[this['data_id']]);
                });

                $("#results").on({
                    'mouseenter': function () {
                        var id = $(this).data("marker");
                        markers[id].setIcon(highlight_marker);
                    },
                    'mouseleave': function () {
                        var id = $(this).data("marker");
                        markers[id].setIcon(default_marker);
                    },
                }, '#listing-' + data.id);
            };
            document.getElementById('results').innerHTML = html;
            var infoWindow = new google.maps.InfoWindow({
                content:"Poopie mcgoopie"
            });
            google.maps.event.addListener(map, "click", function(event) {
                infoWindow.close();
            });
            $('.slider').unslider({
                speed: 400,
                infinite: true,
                nav: false,
                arrows: {
                    prev: '<a class="unslider-arrow prev"><i class="chevron large left icon"></i></a>',
                    next: '<a class="unslider-arrow next"><i class="chevron large right icon"></i></a>',
                }
            });
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
