async function apiRequest(method, url, body) {
  const options = { method, headers: {} };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    // detail is a text message, or a list of problems when FastAPI rejects the input.
    const detail = data && data.detail;
    throw new Error(Array.isArray(detail) ? detail.map((d) => d.msg).join("; ") : detail || "Request failed.");
  }
  return data;
}

const apiGet = (url) => apiRequest("GET", url);
const apiPost = (url, body) => apiRequest("POST", url, body);
const apiPut = (url, body) => apiRequest("PUT", url, body);
const apiDelete = (url) => apiRequest("DELETE", url);

// Escapes text before putting it inside HTML. Subject and assessment names
// are typed by students (and copied between classmates), so never insert
// them raw.
function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

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
      <a href="/marks">Marks</a>
      <a href="/grades">Grade Planner</a>
      <a href="/dashboard">Dashboard &amp; Reports</a>
      <select id="trimester-select" title="Active trimester"></select>
      <div class="user-chip">
        <div class="avatar">${escapeHtml(initial)}</div>
        <span class="user-name">${escapeHtml(student.username)}</span>
      </div>
      <button id="logout-btn" class="secondary">Logout</button>
    `;
    document.getElementById("logout-btn").addEventListener("click", async () => {
      await apiPost("/api/logout");
      window.location.href = "/login";
    });
    await setupTrimesterSelect();
  }
  return student;
}

// The trimester dropdown in the nav bar. Every page shows data for the
// active trimester only; switching reloads the page.
async function setupTrimesterSelect() {
  const select = document.getElementById("trimester-select");
  const data = await apiGet("/api/trimesters");
  select.innerHTML =
    data.trimesters.map((t) => `<option value="${escapeHtml(t)}" ${t === data.active ? "selected" : ""}>🗓️ ${escapeHtml(t)}</option>`).join("") +
    `<option value="__new__">➕ Start new trimester…</option>`;

  select.addEventListener("change", async () => {
    let trimester = select.value;
    if (trimester === "__new__") {
      trimester = await askNewTrimester(data.active);
      if (!trimester) {
        select.value = data.active;
        return;
      }
    }
    try {
      await apiPut("/api/trimesters/active", { trimester });
      window.location.reload();
    } catch (err) {
      alert(err.message);
      select.value = data.active;
    }
  });
}

// Asks for an academic year + trimester number, suggesting the one after
// the current trimester (T1 -> T2 -> T3 -> next year's T1).
async function askNewTrimester(current) {
  let year = new Date().getFullYear();
  let term = 1;
  const match = /^(\d{4})\/\d{4} T(\d)$/.exec(current || "");
  if (match) {
    year = Number(match[1]);
    term = Number(match[2]) + 1;
    if (term > 3) {
      term = 1;
      year = year + 1;
    }
  }
  const years = [];
  for (let y = year - 3; y <= year + 1; y++) years.push(`${y}/${y + 1}`);

  const values = await showModal({
    title: "Start a new trimester",
    fields: [
      { label: "Academic year", type: "select", options: years, value: `${year}/${year + 1}` },
      { label: "Trimester", type: "select", options: ["T1", "T2", "T3"], value: `T${term}` },
    ],
    confirmText: "Start trimester",
  });
  if (!values) return null;
  return `${values[0]} ${values[1]}`;
}

// Adds the shared modal markup to pages that don't have their own.
function ensureModal() {
  if (document.getElementById("modal-overlay")) return;
  document.body.insertAdjacentHTML("beforeend", `
    <div id="modal-overlay" class="modal-overlay" hidden>
      <div class="modal-box">
        <h3 id="modal-title"></h3>
        <div id="modal-fields"></div>
        <div class="modal-actions">
          <button id="modal-cancel-btn" class="secondary">Cancel</button>
          <button id="modal-confirm-btn">Save</button>
        </div>
      </div>
    </div>
  `);
}

// A rough emoji per subject, guessed from its name. Purely decorative.
function iconForSubject(name) {
  const lower = name.toLowerCase();
  if (lower.includes("math")) return "🧮";
  if (lower.includes("phys")) return "⚛️";
  if (lower.includes("econ")) return "📈";
  if (lower.includes("statistic")) return "📊";
  if (lower.includes("program") || lower.includes("computer") || lower.includes("cs")) return "💻";
  if (lower.includes("english") || lower.includes("language")) return "📖";
  if (lower.includes("chem")) return "🧪";
  if (lower.includes("bio")) return "🧬";
  if (lower.includes("art") || lower.includes("design")) return "🎨";
  if (lower.includes("history")) return "📜";
  if (lower.includes("business") || lower.includes("management")) return "💼";
  if (lower.includes("account") || lower.includes("finance")) return "💰";
  if (lower.includes("music")) return "🎵";
  if (lower.includes("geograph")) return "🌍";
  if (lower.includes("psych")) return "🧠";
  if (lower.includes("law")) return "⚖️";
  if (lower.includes("engineer")) return "⚙️";
  if (lower.includes("communicat") || lower.includes("media")) return "📡";
  return "📘";
}

// Colors a letter-grade badge: green for A's, blue for B's, orange for
// C/D, red for F.
function badgeColorFor(letter) {
  if (!letter) return "#98a2b3";
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
    ensureModal();
    const overlay = document.getElementById("modal-overlay");
    document.getElementById("modal-title").textContent = title;

    const fieldsEl = document.getElementById("modal-fields");
    fieldsEl.innerHTML = fields.map((f, i) => f.type === "select" ? `
      <label>${escapeHtml(f.label)}</label>
      <select id="modal-field-${i}">
        ${f.options.map((o) => `<option value="${escapeHtml(o)}" ${o === f.value ? "selected" : ""}>${escapeHtml(o)}</option>`).join("")}
      </select>
    ` : `
      <label>${escapeHtml(f.label)}</label>
      <input id="modal-field-${i}" type="${f.type || "text"}"
             value="${escapeHtml(f.value)}"
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