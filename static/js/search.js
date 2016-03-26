//////////////////////////////
/////   GOOGLE MAP STUFF  ////
//////////////////////////////

var map;
var markers = {};
var infoWindow;
var default_marker;
var highlight_marker;

// This is the callback function from google maps
// Will run after google maps has loaded
function initMap() {
    // Initialize a map centered on Hyde Park
    var myCenter = new google.maps.LatLng(41.795113,-87.594300);
    map = new google.maps.Map(document.getElementById('map'), {
        center: myCenter,
        zoom: 15,
        mapTypeControl: false,
        zoomControl: true,
    });

    // Create an info window to later be shared by the listing markers
    infoWindow = new google.maps.InfoWindow({
        content:"Poopie mcgoopie"
    });

    // Add an event to close the infowindow if you click outisde of it
    google.maps.event.addListener(map, "click", function(event) {
        infoWindow.close();
    });

    // Build a default marker template with a blue marker
    default_marker = {
        url: "/static/img/marker.png", // url
        scaledSize: new google.maps.Size(40, 40), // scaled size
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(20,40) // anchor
    };

    // Build a highlight marker for hovers with a red marker
    highlight_marker = {
        url: "/static/img/highlight_marker.png", // url
        scaledSize: new google.maps.Size(40, 40), // scaled size
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(20,40) // anchor
    };

    // If the url contains a query from a previous ajax call, use that instead
    // of the current form data. This is so that you can share or save the url
    // of a search and come back to it later.
    if (window.location.search.length > 1) {
        search_with_url(window.location.pathname + window.location.search);
        price_slider.noUiSlider.set([getParameterByName('price_low'),
            getParameterByName('price_high')]);
    }
    // Otherwise just search normally
    else {
        search();
    }
};

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




//////////////////////////////
/////    ON LOAD STUFF    ////
//////////////////////////////

var price_slider;

$(document).ready(function() {
    var low = 300
    var high = 700
    // If there are prices in the url use them instead
    // This is to return to prev state if page is loaded anew
    if (getUrlParam('price_low') || getUrlParam('price_high')) {
        low = getUrlParam('price_low')
        high = getUrlParam('price_high')
    }

    // Activate the price slider
    price_slider = document.getElementById('slider');
    noUiSlider.create(price_slider, {
        start: [low, high],
        connect: true,
        step: 1,
        range: {
            'min': 0,
            'max': 1000
        },
    });

    // When the slider value changes, update the numbers
    var range_low = document.getElementById('slider_low'),
        range_high = document.getElementById('slider_high');
    price_slider.noUiSlider.on('update', function( values, handle ) {
        if ( handle ) {
            range_high.innerHTML = '$' + values[handle];
        } else {
            range_low.innerHTML = '$' + values[handle];
        }
    });

    // if any of the fields are modified perform ajax search
    $(".filter").change(function() {
        search();
    });

    // if the price slider is touched perform ajax search
    price_slider.noUiSlider.on('change', function(){
        search();
    });
});




///////////////////////////////
///// RESULT HTML TEMPLATE ////
///////////////////////////////

// Explanation/rant for this shit.
// Fuck this thing. I needed to build the cards for the results
// and I didn't want to do it server side as I needed to return
// json data rather than html to get shit to work with the map.
// So I used the javascript templating plugin mustache to build
// the html. Javascript sucks at having multiline strings though
// so in order for this to be legible I had to split it into a
// list of strings to then be joined when used.

var template = [
    '<div id="listing-{{id}}"" class="ui fluid card" data-marker="{{id}}">',
        '<div class="slider image">',
            '<ul>',
                '<li><img class="slider-image" src="{{cover_photo}}"></li>',
                '{{#photos}}',
                    '<li>',
                        '<div class="loader-container">',
                            '<div class="ui disabled active dimmer">',
                                '<div class="ui active text loader">Loading Image</div>',
                            '</div>',
                        '<div>',
                        '<img class="slider-image" data-src="{{.}}">',
                    '</li>',
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
            '<a href={{user_url}}>',
                '<i class="user icon"></i>',
                'Listed by {{username}}',
            '</a>',
        '</div>',
    '</div>'
].join('\n');



//////////////////////////////
/////   SEARCH FUNCTIONS  ////
//////////////////////////////

// Searches database for inputed requirements
function search() {
    // Gets all the field data from the filters
    q_bedsize = $("#bedsize").val();
    q_bathroom = $("#bathroom").val();
    q_fall = $("#fall").is(':checked');
    q_winter = $("#winter").is(':checked');
    q_spring = $("#spring").is(':checked');
    q_summer = $("#summer").is(':checked');
    slider_vals = slider.noUiSlider.get();
    $.ajax({
        url: '/search/',
        type: 'GET',
        data: {ajax: 1, bedsize: q_bedsize, bathroom : q_bathroom, fall : q_fall,
            winter : q_winter, spring : q_spring, summer : q_summer,
            price_low : Math.round(slider_vals[0]), price_high : Math.round(slider_vals[1])} ,
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            search_success(response, this.url);
        },
        error: function () {

        }
    });
}

// Use the current url to do the search
function search_with_url(url) {
    $.ajax({
        url: url,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            search_success(response, this.url);
        },
        error: function () {
            search_error();
        }
    });
}




//////////////////////////////
/////   SEARCH RESULTS    ////
//////////////////////////////

function search_success(response, url) {
    var html = '';

    // Get the ids of the markers to keep
    var markers2keep = [];
    for (var i = 0; i < response.length; i++) {
        if (response[i].id in markers) {
            markers2keep.push(response[i].id.toString());
        }
    };

    // Remove markers that are not going to be shown
    for (var i in markers) {
        if (markers2keep.indexOf(i) === -1) {
            markers[i].setMap(null);
            delete markers[i];
        }
    };


    for (var i = 0; i < response.length; i++) {
        var data = response[i];

        // Render the cards and add to html string
        var output = Mustache.render(template, data);
        html += output

        // If the marker is not already present
        if (!(data.id in markers)) {
            // Add a marker to the map
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

            // Add a listener to the marker
            // I should really remove the event listener on marker delete but eh
            marker.addListener("click", function() {
                infoWindow.setContent(this['data_name']);
                infoWindow.open(map, markers[this['data_id']]);
            });

            // Add a mouseover listener to change the marker color on hover
            // I'm limiting the scope to only the result wrapper to avoid
            // unescesary mouse position checking, and because the actual
            // html cards haven't been added to the dom yet.
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
    };

    // Insert all the result cards into the dom
    document.getElementById('results').innerHTML = html;

    // Acrivate all the sliders in all the result cards
    var slider = $('.slider').unslider({
        speed: 400,
        animation: 'horizontal',
        infinite: false,
        nav: false,
        arrows: {
            prev: '<a class="unslider-arrow prev"><i class="chevron large left icon"></i></a>',
            next: '<a class="unslider-arrow next"><i class="chevron large right icon"></i></a>',
        }
    });

    // Lazy loading images in slider
    slider.on('unslider.change', function(event, index, slide) {
        var img = slide.find("img");
        if (img.attr("src") === undefined) {
            var dimmer = slide.find("div.ui.active.disabled.dimmer");
            dimmer.removeClass('disabled');
            var src = img.attr("data-src");
            img.attr("src", src).removeAttr('data-src');
            img.on('load', function() {
                // hide/remove the loading image
                dimmer.fadeOut(400, function() {
                    $(this).remove();
                });
            });
        };
    });

    // Update url to the ajax request
    history.pushState('', 'Search', url);
}




//////////////////////////////
/////     SEARCH ERROR    ////
//////////////////////////////

function search_error() {
    alert("error");
}


//////////////////////////////
/////  UTILITY FUNCTIONS  ////
//////////////////////////////


// function to get url parameter. Credit: http://stackoverflow.com/questions/901115
function getUrlParam(name, url) {
    if (!url) url = window.location.href;
    url = url.toLowerCase(); // This is just to avoid case sensitiveness
    name = name.replace(/[\[\]]/g, "\\$&").toLowerCase();// This is just to avoid case sensitiveness for query parameter name
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}


$(document).ajaxStart( function() {
    $("#spinner").removeClass('disabled');
}).ajaxStop( function() {
    $("#spinner").addClass('disabled')
});

