document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".detail-container");
  const locStr = container.dataset.location;
  if (!locStr) return;

  const [latStr, lonStr] = locStr.split(",");
  const lat = parseFloat(latStr.trim());
  const lon = parseFloat(lonStr.trim());
  if (isNaN(lat) || isNaN(lon)) return;

  const map = L.map("detail-map").setView([lat, lon], 15);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(map);
  L.marker([lat, lon]).addTo(map);
});
