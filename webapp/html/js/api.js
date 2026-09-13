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

// Renders the shared nav bar into #nav, redirecting to /login if not
// authenticated. Returns the current user, or null (and redirects) if
// nobody is logged in.
async function requireAuth() {
  let user;
  try {
    user = await apiGet("/api/me");
  } catch (err) {
    window.location.href = "/login";
    return null;
  }

  const nav = document.getElementById("nav");
  if (nav) {
    nav.innerHTML = `
      <div>
        <a href="/dashboard">Dashboard &amp; Reports</a>
      </div>
      <div>
        Logged in as ${user.username}
        <button id="logout-btn">Logout</button>
      </div>
    `;
    document.getElementById("logout-btn").addEventListener("click", async () => {
      await apiPost("/api/logout");
      window.location.href = "/login";
    });
  }

  return user;
}
