var map = L.map('map').setView([46.52, 6.633333], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Initial marker position
var initialLat = 46.534419;
var initialLng = 6.583451;
var marker = L.marker([initialLat, initialLng], {
  title: 'Test'
}).addTo(map).bindPopup('La maison de Paul');

// Slider functionality
document.addEventListener('DOMContentLoaded', function() {
  var slider = document.getElementById('timeSlider');
  var sliderValue = document.getElementById('sliderValue');
  
  // Update the displayed value and marker position when slider changes
  slider.oninput = function() {
    var value = this.value;
    sliderValue.textContent = value;
    console.log('Slider value:', value);
    
    // Calculate new longitude based on slider value
    // This will move the marker to the right by a small amount
    // The multiplier (0.0001) controls how much the marker moves
    var newLng = initialLng + (value - 50) * 0.0001;
    
    // Update marker position
    marker.setLatLng([initialLat, newLng]);
  };
});

let points = []

for (let i = 0; i < 100; i += 1) {
  for (let j = 0; j < 100; j += 1) {
    points.push([initialLat + j * 0.0005, initialLng + i * 0.0005, (0.1 + i/100) / 2]);
  }
}


var heat = L.heatLayer(points, {radius: 25, gradient: {0.4: '#3D52D5', 0.65: '#B4C5E4', 1: '#db5a53'}}).addTo(map);