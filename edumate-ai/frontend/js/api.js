// ============================================================
//  Edumate AI — API Helper  (FIXED VERSION)
//  Har request mein X-User-Id header bhejna hai
//  Taake session problem na ho file:// ya Live Server pe
// ============================================================

const BASE_URL = "http://127.0.0.1:5000/api";

const api = {

  // User ID localStorage se lo
  _uid() {
    const u = JSON.parse(localStorage.getItem("user") || "null");
    return u ? String(u.id) : "";
  },

  // Common headers
  _headers() {
    return {
      "Content-Type": "application/json",
      "X-User-Id": this._uid(),
    };
  },

  async get(endpoint) {
    try {
      const res = await fetch(BASE_URL + endpoint, {
        method: "GET",
        credentials: "include",
        headers: this._headers(),
      });
      return await res.json();
    } catch (e) {
      console.error("GET error:", e);
      return { error: "Server se connect nahi ho saka. Flask chal raha hai? (python app.py)" };
    }
  },

  async post(endpoint, body) {
    try {
      const res = await fetch(BASE_URL + endpoint, {
        method: "POST",
        credentials: "include",
        headers: this._headers(),
        body: JSON.stringify(body),
      });
      return await res.json();
    } catch (e) {
      console.error("POST error:", e);
      return { error: "Server se connect nahi ho saka. Flask chal raha hai? (python app.py)" };
    }
  },
};

// Protected page guard — login nahi hai toh login.html bhejo
function requireLogin() {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  if (!user || !user.id) {
    window.location.href = "login.html";
    return null;
  }
  return user;
}

// Date nicely format karo
function formatDate(str) {
  if (!str) return "";
  const d = new Date(str);
  return d.toLocaleString("en-PK", {
    weekday: "short", month: "short", day: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

// Bootstrap toast notification
function showToast(msg, type = "success") {
  const existing = document.getElementById("global-toast");
  if (existing) existing.remove();
  const icons = {
    success: "check-circle-fill",
    danger: "x-circle-fill",
    warning: "exclamation-triangle-fill",
    info: "info-circle-fill"
  };
  const div = document.createElement("div");
  div.id = "global-toast";
  div.style.cssText = "position:fixed;top:20px;right:20px;z-index:9999;min-width:260px;";
  div.innerHTML = `
    <div class="alert alert-${type} alert-dismissible shadow d-flex align-items-center gap-2" role="alert">
      <i class="bi bi-${icons[type] || "info-circle-fill"}"></i> ${msg}
      <button type="button" class="btn-close ms-auto"
        onclick="this.closest('#global-toast').remove()"></button>
    </div>`;
  document.body.appendChild(div);
  setTimeout(() => { if (div.parentNode) div.remove(); }, 4000);
}
