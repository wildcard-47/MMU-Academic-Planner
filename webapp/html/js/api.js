async function apiRequest(method, url, body) {
  const options = { method, headers: {} };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error((data && data.detail) || "Request failed.");
  }
  return data;
}

const apiGet = (url) => apiRequest("GET", url);
const apiPost = (url, body) => apiRequest("POST", url, body);
const apiPut = (url, body) => apiRequest("PUT", url, body);
const apiDelete = (url) => apiRequest("DELETE", url);

// Renders the branded nav bar into #nav, redirecting to /login if not
// authenticated. Returns the current student, or null (and redirects) if
// nobody is logged in.
async function requireAuth() {
  let student;
  try {
    student = await apiGet("/api/me");
  } catch (err) {
    window.location.href = "/login";
    return null;
  }

  const nav = document.getElementById("nav");
  if (nav) {
    const initial = student.username.charAt(0).toUpperCase();
    nav.innerHTML = `
      <a href="/subjects">Subjects</a>
      <a href="/grades">Grade Planner</a>
      <a href="/dashboard">Dashboard &amp; Reports</a>
      <div class="user-chip">
        <div class="avatar">${initial}</div>
        <span class="user-name">${student.username}</span>
      </div>
      <button id="logout-btn" class="secondary">Logout</button>
    `;
    document.getElementById("logout-btn").addEventListener("click", async () => {
      await apiPost("/api/logout");
      window.location.href = "/login";
    });
  }
  return student;
}

// A rough emoji per subject, guessed from its name. Purely decorative.
function iconForSubject(name) {
  const lower = name.toLowerCase();
  if (lower.includes("math")) return "🧮";
  if (lower.includes("phys")) return "⚛️";
  if (lower.includes("program") || lower.includes("computer") || lower.includes("cs")) return "💻";
  if (lower.includes("english") || lower.includes("language")) return "📖";
  if (lower.includes("chem")) return "🧪";
  if (lower.includes("bio")) return "🧬";
  if (lower.includes("art") || lower.includes("design")) return "🎨";
  if (lower.includes("history")) return "📜";
  if (lower.includes("econ")) return "📈";
  if (lower.includes("business") || lower.includes("management")) return "💼";
  if (lower.includes("account") || lower.includes("finance")) return "💰";
  if (lower.includes("music")) return "🎵";
  if (lower.includes("geograph")) return "🌍";
  if (lower.includes("psych")) return "🧠";
  if (lower.includes("law")) return "⚖️";
  if (lower.includes("statistic")) return "📊";
  if (lower.includes("engineer")) return "⚙️";
  if (lower.includes("communicat") || lower.includes("media")) return "📡";
  return "📘";
}

// Colors a letter-grade badge: green for A's, blue for B's, orange for
// C/D, red for F.
function badgeColorFor(letter) {
  if (letter.startsWith("A")) return "#2fa84f";
  if (letter.startsWith("B")) return "#0056b3";
  if (letter.startsWith("C") || letter.startsWith("D")) return "#e0a800";
  return "#da252b";
}

// --- A small reusable modal, replacing window.prompt()/confirm() ---
//
// showModal({ title, fields, confirmText, danger }) resolves with an array
// of the entered field values, or null if the user cancelled.
// showConfirm(message) resolves true/false.

function showModal({ title, fields = [], confirmText = "Save", danger = false }) {
  return new Promise((resolve) => {
    const overlay = document.getElementById("modal-overlay");
    document.getElementById("modal-title").textContent = title;

    const fieldsEl = document.getElementById("modal-fields");
    fieldsEl.innerHTML = fields.map((f, i) => `
      <label>${f.label}</label>
      <input id="modal-field-${i}" type="${f.type || "text"}"
             value="${f.value === null || f.value === undefined ? "" : f.value}"
             ${f.step ? `step="${f.step}"` : ""}>
    `).join("");

    const confirmBtn = document.getElementById("modal-confirm-btn");
    const cancelBtn = document.getElementById("modal-cancel-btn");
    confirmBtn.textContent = confirmText;
    confirmBtn.className = danger ? "danger" : "";

    overlay.hidden = false;
    if (fields.length > 0) document.getElementById("modal-field-0").focus();

    function cleanup() {
      overlay.hidden = true;
      confirmBtn.removeEventListener("click", onConfirm);
      cancelBtn.removeEventListener("click", onCancel);
    }
    function onConfirm() {
      const values = fields.map((f, i) => document.getElementById(`modal-field-${i}`).value);
      cleanup();
      resolve(values);
    }
    function onCancel() {
      cleanup();
      resolve(null);
    }
    confirmBtn.addEventListener("click", onConfirm);
    cancelBtn.addEventListener("click", onCancel);
  });
}

async function showConfirm(message) {
  const result = await showModal({ title: message, fields: [], confirmText: "Delete", danger: true });
  return result !== null;
}