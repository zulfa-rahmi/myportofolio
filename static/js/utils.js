/**
 * Fungsi bantuan yang dipakai bersama oleh beberapa halaman.
 * (Dipindah dari <script> inline di projects.html supaya bisa dipakai ulang.)
 */

// Ambil nilai cookie berdasarkan nama (dipakai untuk token CSRF: "csrftoken")
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Escape teks agar aman disisipkan ke innerHTML (pencegahan XSS)
function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value ?? '';
  return div.innerHTML;
}

// Tampilkan toast; fallback ke alert kalau showToast belum dimuat
function notify(title, message, type) {
  if (typeof showToast === 'function') {
    showToast(title, message, type);
  } else {
    alert(title + ': ' + message);
  }
}
