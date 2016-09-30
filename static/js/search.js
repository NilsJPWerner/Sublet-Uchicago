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
        zoom: 14,
        mapTypeControl: false,
        zoomControl: true,
    });

    // Build a default marker template with a blue marker
    default_marker = {
        url: "/static/img/marker.png",
        scaledSize: new google.maps.Size(40, 40),
        origin: new google.maps.Point(0,0),
        anchor: new google.maps.Point(20,40)
    };

    // Build a highlight marker for hovers with a red marker
    highlight_marker = {
        url: "/static/img/highlight_marker.png",
        scaledSize: new google.maps.Size(40, 40),
        origin: new google.maps.Point(0,0),
        anchor: new google.maps.Point(20,40)
    };

    // If the url contains a query from a previous ajax call, use that instead
    // of the current form data.
    if (window.location.search.length > 1) {
        // search_with_url(window.location.pathname + window.location.search);
        updateForm();
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

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = {};
}




//////////////////////////////
/////    ON LOAD STUFF    ////
//////////////////////////////

var price_slider;
const max_price = 1500;

$(document).ready(function() {
    var low = 0
    var high = max_price
    // If there are prices in the url use them instead
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
        margin: 200,
        range: {
            'min': 0,
            'max': max_price
        },
    });

    // When the slider value changes, update the numbers
    var range_low = document.getElementById('slider_low'),
        range_high = document.getElementById('slider_high');
    price_slider.noUiSlider.on('update', function( values, handle ) {
        if ( handle ) {
            range_high.innerHTML = formatPrice(values[handle]);
        } else {
            range_low.innerHTML = formatPrice(values[handle]);
        }
    });

    // If browser goes back in history search with the url
    window.onpopstate =  function(event) {
        if (window.location.search.length > 1) {
            // search_with_url(window.location.pathname + window.location.search);
            updateForm();
            search();
        }
    };

    // if any of the fields are modified perform ajax search
    $(".filter").on('change', function() { search() });

    // if the price slider is touched perform ajax search
    price_slider.noUiSlider.on('change', function(){
        search();
    });
});




///////////////////////////////
///// RESULT HTML TEMPLATE ////
///////////////////////////////

// I needed to build the cards for the results
// and I didn't want to do it server side as I needed to return
// json data rather than html to get shit to work with the map.
// So I used the javascript templating plugin mustache to build
// the html. Javascript sucks at having multiline strings though
// so in order for this to be legible I had to split it into a
// list of strings to then be joined when used.
// I need to learn react

var template = [
    '<div id="listing-{{id}}"" class="ui fluid card" data-marker="{{id}}">',
        '<div class="slider image">',
            '<ul>',
                '<li>',
                    '<div class="slider-photo">',
                        '<img class="slider-image" src="{{cover_photo}}">',
                        '<a class="slider-link middle" href="{{listing_url}}" target="_blank"></a>',
                    '</div>',
                '</li>',
                '{{#photos}}',
                    '<li>',
                        '<div class="loader-container">',
                            '<div class="ui disabled active dimmer">',
                                '<div class="ui active text loader">Loading Image</div>',
                            '</div>',
                        '<div>',
                        '<div class="slider-photo">',
                            '<img class="slider-image" data-src="{{.}}">',
                            '<a class="slider-link middle" href="{{listing_url}}" target="_blank"></a>',
                        '</div>',
                    '</li>',
                '{{/photos}}',
            '</ul>',
        '</div>',
        '<div class="content">',
            // Sneaky use of starred boolean as a css class to mark active state
            '<i class="ui right floated large {{starred}} star icon"',
                'onclick="star(this, {{id}})" data-content="Star this listing"></i>',
            '<a href={{listing_url}} target="_blank" class="header">{{name}}</a>',
            '<div class="meta">',
                '<span class="date"></span>',
            '</div>',
            '<div class="description">',
                'Insert a part of the summary here maybe',
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
    console.log('Search');
    quarter = $("input[name=quarter]:checked").val()
    bedsize = $("#bedsize").val();
    bathroom = $("#bathroom").val();
    roommates = $("#roommates").val();
    slider_vals = slider.noUiSlider.get();
    $.ajax({
        url: '/search/',
        type: 'GET',
        data: {
            quarter: quarter,
            bedsize: bedsize,
            bathroom: bathroom,
            roommates: roommates,
            price_low: Math.round(slider_vals[0]),
            price_high: Math.round(slider_vals[1]), ajax: 1
        },
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            search_success(response, this.url);
            update_history(this.url);
        },
        error: function () {
            search_error();
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
            updateForm();
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
            // Also velocity >>>> Jquery
            marker.addListener("click", function() {
                // infoWindow.setContent(this['data_name']);
                // infoWindow.open(map, markers[this['data_id']]);
                var card_id = "#listing-" + this['data_id'];
                $(card_id).velocity("scroll", {
                    container: $("#data-column"),
                    easing: "easeInOut",
                    duration: 500 });
            });


            // Add mouseover listner to the markers to change icon color
            // on hover.
            google.maps.event.addListener(markers[data.id], 'mouseover', function() {
                this.setIcon(highlight_marker);
                var card_id = "#listing-" + this['data_id'];
                $(".ui.fluid.card:not(" + card_id +")").css({"opacity" : "0.3"});
            });
            google.maps.event.addListener(markers[data.id], 'mouseout', function() {
                this.setIcon(default_marker);
                var card_id = "#listing-" + this['data_id'];
                $(".ui.fluid.card:not(" + card_id +")").css({"opacity" : ""});
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
            prev: '<a class="unslider-arrow prev"><i class="chevron big left icon"></i></a>',
            next: '<a class="unslider-arrow next"><i class="chevron big right icon"></i></a>',
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

    $('.large.star.icon')
        .popup({
            position : 'bottom center',
            transition: 'fade',
            delay: {
                show: 1000,
                hide: 100
            }
        })
    ;

}




//////////////////////////////
/////     SEARCH ERROR    ////
//////////////////////////////

function search_error() {
    $("#error-message").removeClass("hidden");
}


//////////////////////////////
/////  UTILITY FUNCTIONS  ////
//////////////////////////////


// function to get url parameter. Credit: http://stackoverflow.com/questions/901115
function getUrlParam(name, url) {
    if (!url) url = window.location.href;
    url = url.toLowerCase();
    name = name.replace(/[\[\]]/g, "\\$&").toLowerCase();
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}


// Ajax calls and stars a listing or redirects if not signed in
function star (element, id) {
    var star = $(element);
    $.post( "/star/", { "csrfmiddlewaretoken": CSRF_TOKEN, "listing": id})
        .done(function (starred) {
            if (starred === "True") {
                star.addClass('true');
            }
            else if (starred === "False") {
                star.removeClass('true');
            }
            else {
                // Redirect to login page if not signed in
                window.location = starred
            }
        });
};

// updates form with data from url
function updateForm () {
    price_slider.noUiSlider.set([getUrlParam('price_low'), getUrlParam('price_high')]);
    $('#bedsize').dropdown('set selected', getUrlParam('bedsize'));
    $('#bathroom').dropdown('set selected', getUrlParam('bathroom'));
    $('#roommates').dropdown('set selected', getUrlParam('roommates'));
    // Need to set for other parts of form
}


function update_history (url) {
    history.pushState('', 'Search', url);
}

// Remove decimal and then add comma and dollars sign
function formatPrice(number) {
    number = Math.floor(number)
    price = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    price = '$' + price
    if ( number == max_price ) {
        price += '+'
    }
    return price
}

// $(document).ajaxStart( function() {
//     $("#spinner").removeClass('disabled');
// }).ajaxStop( function() {
//     $("#spinner").addClass('disabled')
// });

