/**
 * Halaman Experience: memuat data lewat AJAX, pencarian dengan debouncing,
 * tambah data lewat modal + Fetch API, star, dan notifikasi toast.
 *
 * Membutuhkan: utils.js (getCookie, escapeHtml, notify) dan toast.js (showToast),
 * serta objek window.EXPERIENCE_CONFIG yang diisi oleh experience.html.
 */
(function () {
  'use strict';

  const CFG = window.EXPERIENCE_CONFIG;
  const DUMMY_ID = '00000000-0000-0000-0000-000000000000';
  const SEARCH_DEBOUNCE_DELAY = 300; // ms

  // ================= ELEMEN HTML =================
  const loadingState = document.getElementById('loading');
  const errorState = document.getElementById('error');
  const emptyState = document.getElementById('empty');
  const emptyText = document.getElementById('empty-text');
  const gridContainer = document.getElementById('grid');
  const searchForm = document.getElementById('experience-search-form');
  const searchInput = document.getElementById('search-input');
  // Elemen di bawah ini hanya dirender untuk superuser/editor -> bisa null
  const experienceForm = document.getElementById('experience-form');
  const addModal = document.getElementById('add-experience-modal');
  const deleteModal = document.getElementById('delete-experience-modal');
  const deleteForm = document.getElementById('delete-experience-form');
  const deleteTitle = document.getElementById('delete-experience-title');

  let searchDebounceTimer;
  let experienceAbortController;

  // ================= TAMPILAN STATE =================
  // Tampilkan SATU bagian saja: loading / error / kosong / daftar
  function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
    loadingState.classList.toggle('hide', !showLoading);
    errorState.classList.toggle('hide', !showError);
    emptyState.classList.toggle('hide', !showEmpty);
    gridContainer.classList.toggle('hide', !showGrid);
  }

  // ================= BIKIN KARTU =================
  function starLabel(fields) {
    return fields.is_starred ? 'Unstar' : 'Star';
  }

  function starTitle(fields) {
    return fields.star_count > 0
      ? `Dibintangi oleh ${fields.starred_by_names.join(', ')}`
      : 'Jadilah yang pertama memberi star';
  }

  function buildStarButtonHtml(item) {
    const f = item.fields;
    return `
      <button type="button"
              class="button button-star js-star${f.is_starred ? ' is-starred' : ''}"
              data-id="${escapeHtml(item.pk)}"
              title="${escapeHtml(starTitle(f))}">
        <span aria-hidden="true">★</span>
        <span class="star-label">${starLabel(f)}</span>
        <span class="star-count">${Number(f.star_count)}</span>
      </button>`;
  }

  function buildExperienceCardElement(item, index) {
    const f = item.fields;
    const id = item.pk;
    const color = index % 2 === 0 ? 'coral' : 'teal';
    const tilt = index % 2 === 0 ? 'left' : 'right';
    // "2025-03-01" -> "250301" + nomor urut (sama seperti versi template)
    const barcode = (f.started_at ? f.started_at.replace(/-/g, '').slice(2) : '000000') + (index + 1);

    const orgHtml = f.organization
      ? `<p class="ticket-org">${escapeHtml(f.organization)}</p>`
      : '';

    const endHtml = f.is_current
      ? '<span class="status-ongoing">Ongoing</span>'
      : escapeHtml(f.ended_label || '');

    let manageHtml = '';
    if (CFG.canManage) {
      const editUrl = CFG.editUrlTemplate.replace(DUMMY_ID, id);
      manageHtml = `
        <a href="${escapeHtml(editUrl)}" class="button button-secondary">Edit</a>
        <button type="button" class="button button-danger js-delete"
                data-id="${escapeHtml(id)}"
                data-title="${escapeHtml(f.title)}">Hapus</button>`;
    }

    const article = document.createElement('article');
    article.className = `ticket ticket-${color} tilt-${tilt}`;
    article.innerHTML = `
      <div class="ticket-header"><span>${escapeHtml(f.category_display)}</span></div>
      <div class="ticket-body">
        <div class="ticket-barcode" aria-hidden="true"><span>${escapeHtml(barcode)}</span></div>
        <div class="ticket-info">
          <h2 class="ticket-role">${escapeHtml(f.title)}</h2>
          ${orgHtml}
          <p class="ticket-desc">${escapeHtml(f.description)}</p>
          <p class="ticket-period">${escapeHtml(f.started_label)} – ${endHtml}</p>
          <div class="ticket-actions">
            ${buildStarButtonHtml(item)}
            ${manageHtml}
          </div>
        </div>
        <svg class="ticket-plane" viewBox="0 0 24 24" fill="currentColor">
          <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>
        </svg>
      </div>`;
    return article;
  }

  // ================= AMBIL DATA DARI SERVER =================
  async function fetchExperiences(searchQuery = '') {
    // Batalkan request lama supaya hasil lama tidak menimpa hasil baru
    if (experienceAbortController) experienceAbortController.abort();
    experienceAbortController = new AbortController();

    try {
      displayPageSection({ showLoading: true });

      const url = searchQuery
        ? `${CFG.listUrl}?q=${encodeURIComponent(searchQuery)}`
        : CFG.listUrl;

      const response = await fetch(url, {
        headers: { 'Accept': 'application/json' },
        signal: experienceAbortController.signal,
      });
      if (!response.ok) throw new Error(`Failed to fetch data (${response.status})`);

      const data = await response.json();

      if (data.length === 0) {
        emptyText.textContent = searchQuery
          ? 'Tidak ada pengalaman yang cocok dengan pencarianmu.'
          : 'Belum ada pengalaman yang ditambahkan.';
        displayPageSection({ showEmpty: true });
      } else {
        gridContainer.innerHTML = '';
        data.forEach((item, index) =>
          gridContainer.appendChild(buildExperienceCardElement(item, index))
        );
        displayPageSection({ showGrid: true });
      }
    } catch (error) {
      if (error.name === 'AbortError') return; // request dibatalkan, bukan error
      console.error('Error loading experiences:', error);
      displayPageSection({ showError: true });
    }
  }

  // ================= PENCARIAN (DEBOUNCING) =================
  // Request baru dikirim hanya setelah user berhenti mengetik selama 300 ms
  function searchExperiences() {
    fetchExperiences(searchInput.value.trim());
  }

  searchInput.addEventListener('input', function () {
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(searchExperiences, SEARCH_DEBOUNCE_DELAY);
  });

  searchForm.addEventListener('submit', function (event) {
    event.preventDefault();
    clearTimeout(searchDebounceTimer);
    searchExperiences();
  });

  document.getElementById('retry-button').addEventListener('click', searchExperiences);

  // ================= TAMBAH DATA (MODAL + AJAX) =================
  function clearFormErrors() {
    experienceForm.querySelectorAll('[data-error-for]').forEach(el => { el.textContent = ''; });
  }

  function fieldLabel(name) {
    const label = experienceForm.querySelector(`label[for="id_${name}"]`);
    return label ? label.textContent.trim() : '';
  }

  // Tampilkan error validasi dari server: di bawah field + dikembalikan sebagai array pesan toast
  function showFieldErrors(errors) {
    const messages = [];
    Object.entries(errors).forEach(([field, list]) => {
      const text = list.map(e => e.message).join(' ');
      const slot = experienceForm.querySelector(`[data-error-for="${field}"]`);
      if (slot) slot.textContent = text; // textContent -> aman dari XSS
      const label = field === '__all__' ? '' : fieldLabel(field);
      messages.push(label ? `${label}: ${text}` : text);
    });
    return messages;
  }

  async function addExperience(event) {
    event.preventDefault();
    clearFormErrors();

    const submitButton = experienceForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
      const response = await fetch(CFG.createUrl, {
        method: 'POST',
        // Token CSRF: juga ikut terkirim sebagai csrfmiddlewaretoken di dalam FormData
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: new FormData(experienceForm),
      });
      const result = await response.json().catch(() => ({}));

      if (response.status === 201) {
        experienceForm.reset();
        if (addModal) addModal.hidePopover();
        notify('Berhasil', 'Pengalaman baru berhasil ditambahkan!', 'success');
        fetchExperiences(searchInput.value.trim()); // perbarui daftar tanpa reload
      } else if (response.status === 400 && result.errors) {
        notify('Gagal menambahkan pengalaman', showFieldErrors(result.errors).join(' • '), 'error');
      } else {
        notify(
          'Gagal menambahkan pengalaman',
          result.message || `Terjadi kesalahan (status ${response.status}).`,
          'error'
        );
      }
    } catch (error) {
      console.error('Error adding experience:', error);
      notify('Gagal menambahkan pengalaman', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
    } finally {
      submitButton.disabled = false;
    }
  }

  // experienceForm bernilai null untuk pengunjung/user biasa -> cek dulu
  if (experienceForm) {
    experienceForm.addEventListener('submit', addExperience);
  }

  // ================= STAR (AJAX) =================
  async function toggleStar(button) {
    if (!CFG.isAuthenticated) {
      notify('Login diperlukan', 'Silakan login untuk memberi star.', 'error');
      return;
    }
    button.disabled = true;
    try {
      const url = CFG.starUrlTemplate.replace(DUMMY_ID, button.dataset.id);
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Accept': 'application/json' },
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        notify('Gagal memberi star', result.message || `Terjadi kesalahan (status ${response.status}).`, 'error');
        return;
      }
      const f = result.fields;
      button.classList.toggle('is-starred', f.is_starred);
      button.title = starTitle(f);
      button.querySelector('.star-label').textContent = starLabel(f);
      button.querySelector('.star-count').textContent = f.star_count;
    } catch (error) {
      console.error('Error toggling star:', error);
      notify('Gagal memberi star', 'Tidak dapat terhubung ke server.', 'error');
    } finally {
      button.disabled = false;
    }
  }

  // ================= HAPUS (dialog konfirmasi bersama) =================
  function openDeleteModal(id, title) {
    if (!deleteModal || !deleteForm) return;
    deleteForm.action = CFG.deleteUrlTemplate.replace(DUMMY_ID, id);
    deleteTitle.textContent = title; // textContent -> aman dari XSS
    deleteModal.showModal();
  }

  if (deleteModal) {
    deleteModal.querySelectorAll('[data-close-delete]').forEach(el =>
      el.addEventListener('click', () => deleteModal.close())
    );
  }

  // Event delegation: kartu dibuat ulang tiap fetch, jadi listener dipasang di grid
  gridContainer.addEventListener('click', function (event) {
    const starBtn = event.target.closest('.js-star');
    if (starBtn) return toggleStar(starBtn);
    const deleteBtn = event.target.closest('.js-delete');
    if (deleteBtn) openDeleteModal(deleteBtn.dataset.id, deleteBtn.dataset.title);
  });

  // ================= MULAI =================
  fetchExperiences(searchInput.value.trim());
})();
