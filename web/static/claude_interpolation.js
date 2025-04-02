// Assuming you have wealth data for different time periods
const wealthData = {
    0: [/* wealth data points at time 0 */],
    25: [/* wealth data points at time 25 */],
    50: [/* wealth data points at time 50 */],
    75: [/* wealth data points at time 75 */],
    100: [/* wealth data points at time 100 */]
  };
  
  // Create heatmap layer
  let heatLayer = L.heatLayer(wealthData[50], {
    radius: 25,
    blur: 15,
    maxZoom: 17,
    gradient: {0.4: 'blue', 0.65: 'lime', 0.85: 'yellow', 1.0: 'red'}
  }).addTo(map);
  
  // Handle slider change with transition
  slider.oninput = function() {
    const value = parseInt(this.value);
    sliderValue.textContent = value;
    
    // Find the closest data points we have
    const lowerKey = Math.max(...Object.keys(wealthData)
                      .map(Number)
                      .filter(k => k <= value));
    const upperKey = Math.min(...Object.keys(wealthData)
                      .map(Number)
                      .filter(k => k >= value));
    
    // If we have an exact match, just update directly
    if (lowerKey === upperKey) {
      heatLayer.setLatLngs(wealthData[lowerKey]);
      return;
    }
    
    // Otherwise, interpolate between the two closest data points
    const ratio = (value - lowerKey) / (upperKey - lowerKey);
    const interpolatedData = interpolateHeatmapData(
      wealthData[lowerKey], 
      wealthData[upperKey], 
      ratio
    );
    
    heatLayer.setLatLngs(interpolatedData);
  };
  
  // Helper function to interpolate between two sets of heatmap data
  function interpolateHeatmapData(dataA, dataB, ratio) {
    // If the data points don't align 1:1, this gets more complex
    // This is a simplified version assuming matching points
    return dataA.map((pointA, i) => {
      const pointB = dataB[i];
      return [
        pointA[0], // Latitude stays the same
        pointA[1], // Longitude stays the same
        pointA[2] * (1 - ratio) + pointB[2] * ratio // Interpolate intensity
      ];
    });
  }