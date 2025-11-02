document.addEventListener("DOMContentLoaded", () => {
  console.log("CivicLens loaded!");

  // === MAP SETUP ===
  const map = L.map("map").setView([27.8006, -97.3964], 11); // default: Corpus Christi, TX
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  let marker;

  // Allow user to drop a pin manually
  map.on("click", (e) => {
    const { lat, lng } = e.latlng;
    if (marker) marker.setLatLng(e.latlng);
    else marker = L.marker(e.latlng).addTo(map);
    document.getElementById("location").value = `${lat.toFixed(
      5
    )}, ${lng.toFixed(5)}`;
  });

  // === CURRENT LOCATION BUTTON ===
  const locateBtn = document.getElementById("locateBtn");
  if (locateBtn) {
    locateBtn.addEventListener("click", () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
          const { latitude, longitude } = pos.coords;
          map.setView([latitude, longitude], 16);
          if (marker) marker.setLatLng([latitude, longitude]);
          else marker = L.marker([latitude, longitude]).addTo(map);
          document.getElementById(
            "location"
          ).value = `${latitude.toFixed(5)}, ${longitude.toFixed(5)}`;
        });
      } else {
        alert("Geolocation not supported on this browser.");
      }
    });
  }

  // === IMAGE PREVIEW ===
  const imageInput = document.getElementById("image");
  const preview = document.getElementById("preview");
  if (imageInput && preview) {
    imageInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
        preview.style.height = "1.75in";   // <-- add this line
        preview.style.width = "auto";      // keeps aspect ratio
        preview.style.objectFit = "cover"; // optional for cropping style
      }
    });
  }

  // === PHONE AUTO-FORMAT (US) ===
const phoneInput = document.getElementById("phone");

if (phoneInput) {
  phoneInput.addEventListener("input", (e) => {
    let value = e.target.value.replace(/\D/g, "").substring(0, 10);
    const area = value.substring(0, 3);
    const middle = value.substring(3, 6);
    const last = value.substring(6, 10);

    if (value.length > 6) {
      e.target.value = `(${area}) ${middle}-${last}`;
    } else if (value.length > 3) {
      e.target.value = `(${area}) ${middle}`;
    } else if (value.length > 0) {
      e.target.value = `(${area}`;
    }
  });
}

  // === FORM SUBMISSION TO DJANGO ===
  const form = document.getElementById("reportForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(form);

      try {
        const response = await fetch("/", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          showToast("✅ Report submitted successfully!");
          form.reset();
          preview.src = "";
          if (marker) map.removeLayer(marker);
        } else {
          showToast("⚠️ Submission failed. Please try again.");
        }
      } catch (err) {
        console.error(err);
        showToast("❌ Network error. Check your connection.");
      }
    });
  }

  // === TOAST MESSAGE UTILITY ===
  function showToast(msg) {
    const toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3000);
  }

});

