function initMap() {
    $.get("/marker_map_api/" + window.location.hash.replace("#", ""), function(data){

        data = JSON.parse(data);

        console.log(data);
        var settings = {
            zoom: 5,
            center: {
                lat: 65.5274,
                lng: 27.1588
            }
        };
        if(data.settings) {
            settings = data.settings;
        }

        var map = new google.maps.Map(document.getElementById('marker_map'), settings);

        data.markers.forEach(function(marker_data) {

            marker_data.map = map;
            var marker = new google.maps.Marker(marker_data);

            if(marker_data.show_infowindow == true) {

                var infowindow = new google.maps.InfoWindow({
                    content: marker_data.infowindow_text
                });

                marker.addListener('click', function() {
                    infowindow.open(map, marker);
                });

                if(marker_data.infowindow_open_start == true) {
                    infowindow.open(map, marker);
                }
            }
        });
    });
}

$(window).hashchange(initMap);

$( document ).ready(function() {
    initMap();
});




