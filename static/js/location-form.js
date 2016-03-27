$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

function initMap() {
  var center = new google.maps.LatLng(document.getElementById('id_latitude').value, document.getElementById('id_longitude').value);
  var map = new google.maps.Map(document.getElementById('map'), {
    center: center,
    zoom: 15,
    mapTypeControl: false,
    zoomControl:true,
    streetViewControl: false,
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
      draggable: true,
      map: map,
      icon: default_marker,
    });

    google.maps.event.addListener(marker, 'dragend', function (evt) {
      map.panTo(this.getPosition());
      document.getElementById('id_latitude').value = evt.latLng.lat().toFixed(6);
      document.getElementById('id_longitude').value = evt.latLng.lng().toFixed(6);
    });

  // Autocomplete stuff

  var input, placeSearch, autocomplete;
  var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    postal_code: 'short_name'
  };


  input = document.getElementById('id_street_address');
  autocomplete = new google.maps.places.Autocomplete(input, {types: ['geocode']});
  autocomplete.addListener('place_changed', function(event) {
    fillInAddress();
    var place = autocomplete.getPlace();
    var location = place.geometry.location;
    var position = new google.maps.LatLng(location.lat(), location.lng());
    map.panTo(position);
    marker.setPosition(position);
    document.getElementById('id_latitude').value = location.lat().toFixed(6);
    document.getElementById('id_longitude').value = location.lng().toFixed(6);
  });

  function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    var streetnum, road

    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
      var addressType = place.address_components[i].types[0];
      if (componentForm[addressType]) {
        var val = place.address_components[i][componentForm[addressType]];
        if (addressType == 'locality') {
          document.getElementById('id_city').value = val;
        }
        else if (addressType == 'administrative_area_level_1') {
          document.getElementById('id_state').value = val;
        }
        else if (addressType == 'postal_code') {
          document.getElementById('id_zip_code').value = val;
        }
        else if (addressType == 'street_number') {
          streetnum = val;
        }
        else if (addressType == 'route') {
          road = val;
        }
      }
    }
    document.getElementById('id_street_address').value = streetnum+ " " + road

  }

}

// google.maps.event.addListener(myMarker, 'dragstart', function (evt) {
//     document.getElementById('current').innerHTML = '<p>Currently dragging marker...</p>';
// });