function initMap() {
    var center = new google.maps.LatLng(document.getElementById('latitude').innerHTML, document.getElementById('longitude').innerHTML);
    var map = new google.maps.Map(document.getElementById('map'), {
        center: center,
        zoom: 14,
        mapTypeControl: false,
        zoomControl:true,
        streetViewControl: true,
        scrollwheel: false,
    });

    // Build a default marker template with a blue marker
    default_marker = {
        url: "/static/img/marker.png", // url
        scaledSize: new google.maps.Size(40, 40), // scaled size
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(20,40) // anchor
    };

    var marker=new google.maps.Marker({
        position: center,
        map: map,
        icon: default_marker,
    });
};


$('.lightbox').magnificPopup({
    type: 'image',
    gallery: {
        enabled: true
    },
    image: {
        titleSrc: 'title'
    }
});

// Ajax calls and stars a listing or redirects if not signed in
function star (element, id) {
    var star = $(element);
    $.post( "/star/", { "csrfmiddlewaretoken": CSRF_TOKEN, "listing": id})
        .done(function (starred) {
            if (starred === "True") {
                star.addClass('starred');
            }
            else if (starred === "False") {
                star.removeClass('starred');
            }
            else {
                // Redirect to login page if not signed in
                window.location = starred
            }
        });
};

var slider = $('.slider').unslider({
    speed: 400,
    animation: 'horizontal',
    infinite: false,
    nav: false,
    arrows: {
        prev: '<a class="unslider-arrow prev"><i class="chevron left icon"></i></a>',
        next: '<a class="unslider-arrow next"><i class="chevron right icon"></i></a>',
    }
});

$('.star.icon')
    .popup({
        position : 'bottom center',
        transition: 'fade',
        delay: {
            show: 700,
            hide: 100
        }
    })
;

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