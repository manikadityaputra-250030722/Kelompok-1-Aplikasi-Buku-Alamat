const API_BASE = "http://127.0.0.1:8000";

let token = localStorage.getItem("token") || null;
let username = localStorage.getItem("username") || null;

const authSection = document.getElementById("auth-section");
const userSection = document.getElementById("user-section");
const currentUserSpan = document.getElementById("current-user");

const searchInput = document.getElementById("search-input");
const categorySelect = document.getElementById("category-select");

function updateUI() {
  if (token) {
    authSection.classList.add("hidden");
    userSection.classList.remove("hidden");
    currentUserSpan.textContent = username;
    loadContacts(); // awal: semua kontak
  } else {
    authSection.classList.remove("hidden");
    userSection.classList.add("hidden");
    currentUserSpan.textContent = "";
  }
}

async function apiRequest(path, options = {}) {
  const headers = options.headers || {};
  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }
  if (!headers["Content-Type"] && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(API_BASE + path, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    alert(err.detail || "Terjadi kesalahan");
    throw new Error("Request failed");
  }
  if (res.status === 204) return null;
  return res.json();
}

/* ========== AUTH ========== */

// Registrasi
document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = {
    username: document.getElementById("reg-username").value.trim(),
    email: document.getElementById("reg-email").value.trim(),
    password: document.getElementById("reg-password").value,
  };

  if (!body.username || !body.email || !body.password) {
    alert("Semua field registrasi wajib diisi.");
    return;
  }

  try {
    await apiRequest("/register", {
      method: "POST",
      body: JSON.stringify(body),
    });
    alert("Registrasi berhasil, silakan login.");
    e.target.reset();
  } catch (err) {
    console.error(err);
  }
});

// Login
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const uname = document.getElementById("login-username").value.trim();
  const pwd = document.getElementById("login-password").value;

  if (!uname || !pwd) {
    alert("Username dan password wajib diisi.");
    return;
  }

  const formData = new URLSearchParams();
  formData.append("username", uname);
  formData.append("password", pwd);

  try {
    const res = await fetch(API_BASE + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      alert(err.detail || "Login gagal");
      return;
    }
    const data = await res.json();
    token = data.access_token;
    username = uname;
    localStorage.setItem("token", token);
    localStorage.setItem("username", username);
    alert("Login berhasil");
    updateUI();
  } catch (err) {
    console.error(err);
  }
});

// Logout
document.getElementById("logout-btn").addEventListener("click", () => {
  token = null;
  username = null;
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  updateUI();
});

/* ========== CONTACTS ========== */

// Tambah kontak
document.getElementById("contact-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = {
    name: document.getElementById("c-name").value.trim(),
    phone: document.getElementById("c-phone").value.trim(),
    email: document.getElementById("c-email").value.trim(),
    address: document.getElementById("c-address").value.trim(),
    category: document.getElementById("c-category").value.trim(),
  };

  if (!body.name) {
    alert("Nama kontak wajib diisi.");
    return;
  }

  try {
    await apiRequest("/contacts", {
      method: "POST",
      body: JSON.stringify(body),
    });
    e.target.reset();
    // reload dengan filter yang sedang aktif
    loadContacts();
  } catch (err) {
    console.error(err);
  }
});

// Form filter (search + category)
document.getElementById("filter-form").addEventListener("submit", (e) => {
  e.preventDefault();
  loadContacts();
});

// Tombol reset filter
document
  .getElementById("clear-filter-btn")
  .addEventListener("click", function () {
    searchInput.value = "";
    categorySelect.value = "";
    loadContacts();
  });

// Tombol reload
document.getElementById("reload-btn").addEventListener("click", loadContacts);

// Ambil kontak dari API (pakai query param)
async function loadContacts() {
  try {
    const search = searchInput ? searchInput.value.trim() : "";
    const category = categorySelect ? categorySelect.value : "";

    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (category) params.append("category", category);

    const path = params.toString() ? `/contacts?${params.toString()}` : "/contacts";

    const contacts = await apiRequest(path);
    const tbody = document.getElementById("contacts-body");
    tbody.innerHTML = "";
    contacts.forEach((c) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${c.name}</td>
        <td>${c.phone || ""}</td>
        <td>${c.email || ""}</td>
        <td>${c.address || ""}</td>
        <td>${c.category || ""}</td>
        <td><button data-id="${c.id}" class="delete-btn">Hapus</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
  }
}

// Hapus kontak
document.getElementById("contacts-body").addEventListener("click", async (e) => {
  if (e.target.classList.contains("delete-btn")) {
    const id = e.target.getAttribute("data-id");
    if (confirm("Yakin hapus kontak ini?")) {
      try {
        await apiRequest(`/contacts/${id}`, { method: "DELETE" });
        loadContacts();
      } catch (err) {
        console.error(err);
      }
    }
  }
});

// Inisialisasi UI
updateUI();
