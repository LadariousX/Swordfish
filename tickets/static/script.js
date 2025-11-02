// Initialize map
const map = L.map("map").setView([27.8006, -97.3964], 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19 }).addTo(map);

let marker = L.marker([27.8006, -97.3964], { draggable: true }).addTo(map);
const locationInput = document.getElementById("location");
const suggestionsList = document.getElementById("suggestions");

// Reverse geocode
function updateLocation(lat, lng) {
  fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
    .then(res => res.json())
    .then(data => {
      locationInput.value = data.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    });
}
marker.on("dragend", () => {
  const { lat, lng } = marker.getLatLng();
  updateLocation(lat, lng);
});

// Auto-suggest for typed address
let typingTimer;
locationInput.addEventListener("input", () => {
  clearTimeout(typingTimer);
  const query = locationInput.value.trim();
  if (query.length < 3) {
    suggestionsList.style.display = "none";
    return;
  }
  typingTimer = setTimeout(() => fetchSuggestions(query), 400);
});

function fetchSuggestions(query) {
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=5`)
    .then(res => res.json())
    .then(data => {
      suggestionsList.innerHTML = "";
      if (data.length === 0) {
        suggestionsList.style.display = "none";
        return;
      }
      data.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.display_name;
        li.addEventListener("click", () => {
          locationInput.value = item.display_name;
          map.setView([item.lat, item.lon], 15);
          marker.setLatLng([item.lat, item.lon]);
          suggestionsList.style.display = "none";
        });
        suggestionsList.appendChild(li);
      });
      suggestionsList.style.display = "block";
    });
}

// Hide suggestions if clicked outside
document.addEventListener("click", (e) => {
  if (!locationInput.contains(e.target) && !suggestionsList.contains(e.target)) {
    suggestionsList.style.display = "none";
  }
});

// Use current location
document.getElementById("locateBtn").addEventListener("click", () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
      const { latitude, longitude } = pos.coords;
      map.setView([latitude, longitude], 15);
      marker.setLatLng([latitude, longitude]);
      updateLocation(latitude, longitude);
    });
  } else alert("Geolocation not supported.");
});

// Image preview
document.getElementById("image").addEventListener("change", e => {
  const file = e.target.files[0];
  const preview = document.getElementById("preview");
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      preview.src = reader.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else preview.style.display = "none";
});

// Form submission
document.getElementById("reportForm").addEventListener("submit", e => {
  e.preventDefault();
  const image = document.getElementById("image").files[0];
  const comment = document.getElementById("comment").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const location = document.getElementById("location").value.trim();

  if (!image || !comment || !phone || !location) {
    showToast("⚠️ Please fill all required fields including an image.", true);
    return;
  }

  const ticketID = "TK" + Math.floor(1000 + Math.random() * 9000);
  showToast(`✅ Ticket Created! ID: ${ticketID}`);
  e.target.reset();
  document.getElementById("preview").style.display = "none";
});

function showToast(msg, isError = false) {
  const toast = document.getElementById("toast");
  toast.style.color = isError ? "red" : "#1cc88a";
  toast.textContent = msg;
  setTimeout(() => (toast.textContent = ""), 4000);
}
