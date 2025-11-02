document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".mini-map").forEach((mapDiv) => {
    const coords = mapDiv.dataset.location.split(",");
    if (coords.length < 2) return;

    const lat = parseFloat(coords[0].trim());
    const lng = parseFloat(coords[1].trim());
    if (isNaN(lat) || isNaN(lng)) return;

    const map = L.map(mapDiv.id, {
      zoomControl: false,
      attributionControl: false
    }).setView([lat, lng], 15);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19
    }).addTo(map);

    L.marker([lat, lng]).addTo(map);
  });
});
