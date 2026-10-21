/**
 * Activity, Education & Certificate Hub - Interactive Client Application
 * Candidate: Pradeep Kumar Suresh
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initModals();
  initSearchAndFilters();
  initCertificateSearchAndFilters();
  initEducationForm();
  initCertificateForm();
  initActivityForm();
  initProfileForm();
  initCardActionDelegates();
  checkAdminStatus();
});

/* --------------------------------------------------------------------------
   1. Theme Switcher (Dark / Light) with LocalStorage
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  if (!themeToggleBtn || !themeIcon) return;

  const savedTheme = localStorage.getItem('hub_theme') || 'dark';
  applyTheme(savedTheme);

  themeToggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  });

  function applyTheme(theme) {
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
      themeIcon.className = 'fa-solid fa-moon';
    } else {
      document.documentElement.removeAttribute('data-theme');
      themeIcon.className = 'fa-solid fa-sun';
    }
    localStorage.setItem('hub_theme', theme);
  }
}

/* --------------------------------------------------------------------------
   2. Modal Dialog Management & File Dropzone
   -------------------------------------------------------------------------- */
function initModals() {
  // Triggers for Education Modal
  const newEduBtns = [
    document.getElementById('openNewEduModalBtn'),
    document.getElementById('sectionAddEduBtn')
  ];
  newEduBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => {
      resetEducationForm();
      openModal('educationModal');
    });
  });

  // Triggers for Certificate Modal
  const uploadCertBtns = [
    document.getElementById('openUploadCertModalBtn'),
    document.getElementById('sectionUploadCertBtn')
  ];
  uploadCertBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => {
      resetCertificateForm();
      openModal('certificateModal');
    });
  });

  // Triggers for Activity Modal
  const newActBtns = [
    document.getElementById('openNewActivityModalBtn'),
    document.getElementById('sectionNewActBtn')
  ];
  newActBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => {
      resetActivityForm();
      openModal('activityModal');
    });
  });

  // Trigger for Profile Modal
  const editProfBtn = document.getElementById('openEditProfileBtn');
  if (editProfBtn) {
    editProfBtn.addEventListener('click', () => openModal('profileModal'));
  }

  // File dropzone trigger & feedback
  const dropzone = document.getElementById('certDropzone');
  const fileInput = document.getElementById('formCertFile');
  const fileDisplay = document.getElementById('fileSelectedDisplay');
  const fileNameSpan = document.getElementById('fileSelectedName');

  if (dropzone && fileInput) {
    dropzone.addEventListener('click', (e) => {
      if (e.target !== fileInput) fileInput.click();
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        if (fileNameSpan) fileNameSpan.textContent = `${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        if (fileDisplay) fileDisplay.style.display = 'block';
      } else {
        if (fileDisplay) fileDisplay.style.display = 'none';
      }
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      if (e.dataTransfer && e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        const file = fileInput.files[0];
        if (fileNameSpan) fileNameSpan.textContent = `${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        if (fileDisplay) fileDisplay.style.display = 'block';
      }
    });
  }

  // Close triggers
  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modalId = btn.getAttribute('data-close');
      closeModal(modalId);
    });
  });

  // Close on backdrop click
  document.querySelectorAll('.modal-backdrop').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal(modal.id);
    });
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.open').forEach(modal => {
        closeModal(modal.id);
      });
    }
  });
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }
}

/* --------------------------------------------------------------------------
   3. Search & Category Filtering for Activities
   -------------------------------------------------------------------------- */
function initSearchAndFilters() {
  const searchInput = document.getElementById('activitySearchInput');
  const clearBtn = document.getElementById('clearSearchBtn');
  const filterChips = document.querySelectorAll('#activities .filter-chip');

  let activeCategory = 'all';

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.trim().toLowerCase();
      if (clearBtn) clearBtn.style.display = query ? 'block' : 'none';
      filterCards(query, activeCategory);
    });
  }

  if (clearBtn && searchInput) {
    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      clearBtn.style.display = 'none';
      filterCards('', activeCategory);
      searchInput.focus();
    });
  }

  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.getAttribute('data-category') || 'all';
      const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
      filterCards(query, activeCategory);
    });
  });

  function filterCards(query, category) {
    const cards = document.querySelectorAll('#activityFeedList .activity-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const cardCategory = card.getAttribute('data-category') || '';
      const text = card.textContent.toLowerCase();

      const matchesCat = (category === 'all' || cardCategory === category);
      const matchesQuery = (!query || text.includes(query));

      if (matchesCat && matchesQuery) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    const feedList = document.getElementById('activityFeedList');
    let noResultsNotice = document.getElementById('noActivitySearchResults');
    if (visibleCount === 0) {
      if (!noResultsNotice) {
        noResultsNotice = document.createElement('div');
        noResultsNotice.id = 'noActivitySearchResults';
        noResultsNotice.className = 'empty-state';
        noResultsNotice.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i><p>No activity updates match your search or filter.</p>';
        if (feedList) feedList.appendChild(noResultsNotice);
      }
    } else {
      if (noResultsNotice) noResultsNotice.remove();
    }
  }
}

/* --------------------------------------------------------------------------
   4. Search & Category Filtering for Certificates
   -------------------------------------------------------------------------- */
function initCertificateSearchAndFilters() {
  const searchInput = document.getElementById('certSearchInput');
  const clearBtn = document.getElementById('clearCertSearchBtn');
  const filterChips = document.querySelectorAll('.cert-filter-chip');

  let activeCategory = 'all';

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.trim().toLowerCase();
      if (clearBtn) clearBtn.style.display = query ? 'block' : 'none';
      filterCertCards(query, activeCategory);
    });
  }

  if (clearBtn && searchInput) {
    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      clearBtn.style.display = 'none';
      filterCertCards('', activeCategory);
      searchInput.focus();
    });
  }

  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.getAttribute('data-category') || 'all';
      const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
      filterCertCards(query, activeCategory);
    });
  });

  function filterCertCards(query, category) {
    const cards = document.querySelectorAll('#certificateGridList .certificate-card');
    let visibleCount = 0;

    cards.forEach(card => {
      const cardCategory = card.getAttribute('data-category') || '';
      const text = card.textContent.toLowerCase();

      const matchesCat = (category === 'all' || cardCategory === category);
      const matchesQuery = (!query || text.includes(query));

      if (matchesCat && matchesQuery) {
        card.style.display = 'flex';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    const gridList = document.getElementById('certificateGridList');
    let noResultsNotice = document.getElementById('noCertSearchResults');
    if (visibleCount === 0) {
      if (!noResultsNotice) {
        noResultsNotice = document.createElement('div');
        noResultsNotice.id = 'noCertSearchResults';
        noResultsNotice.className = 'empty-state';
        noResultsNotice.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i><p>No certificates match your search or filter.</p>';
        if (gridList) gridList.appendChild(noResultsNotice);
      }
    } else {
      if (noResultsNotice) noResultsNotice.remove();
    }
  }
}

/* --------------------------------------------------------------------------
   5. Education Form Submission (Add & Edit)
   -------------------------------------------------------------------------- */
function initEducationForm() {
  const form = document.getElementById('educationForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('saveEducationBtn');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

    const eduId = document.getElementById('formEduId')?.value.trim();
    const payload = {
      id: eduId || undefined,
      level: document.getElementById('formEduLevel')?.value.trim(),
      degree: document.getElementById('formEduDegree')?.value.trim(),
      major: document.getElementById('formEduMajor')?.value.trim(),
      institution: document.getElementById('formEduInstitution')?.value.trim(),
      board: document.getElementById('formEduBoard')?.value.trim(),
      timeline: document.getElementById('formEduTimeline')?.value.trim(),
      cgpa: document.getElementById('formEduCgpa')?.value.trim(),
      status: document.getElementById('formEduStatus')?.value.trim(),
      coursework: document.getElementById('formEduCoursework')?.value.trim(),
      description: document.getElementById('formEduDesc')?.value.trim(),
      admin_pin: document.getElementById('formEduAdminPin')?.value.trim()
    };

    try {
      const res = await fetch('/api/education', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (res.ok && data.success) {
        showToast(data.message || 'Education record saved successfully!', 'success');
        setAdminUnlocked();
        renderEducationListDOM(data.education_list);
        updateStatsDOM(data.stats);
        if (data.primary_education) {
          updateHeroEducationDOM(data.primary_education);
        }
        closeModal('educationModal');
        form.reset();
      } else {
        showToast(data.message || 'Error updating education record.', 'error');
      }
    } catch (err) {
      console.error(err);
      showToast('Network error while saving education.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });
}

function resetEducationForm() {
  const form = document.getElementById('educationForm');
  if (form) form.reset();
  const formId = document.getElementById('formEduId');
  if (formId) formId.value = '';
  const title = document.getElementById('eduModalTitle');
  if (title) title.innerHTML = '<i class="fa-solid fa-graduation-cap"></i> Add Academic Milestone';
}

function openEditEducationModal(eduId) {
  fetch(`/api/education/${eduId}`)
    .then(res => res.json())
    .then(edu => {
      if (edu && !edu.error) {
        document.getElementById('formEduId').value = edu.id;
        document.getElementById('formEduLevel').value = edu.level || 'College / Degree';
        document.getElementById('formEduDegree').value = edu.degree || '';
        document.getElementById('formEduMajor').value = edu.major || '';
        document.getElementById('formEduInstitution').value = edu.institution || '';
        document.getElementById('formEduBoard').value = edu.board || '';
        document.getElementById('formEduTimeline').value = edu.timeline || '';
        document.getElementById('formEduCgpa').value = edu.cgpa || '';
        document.getElementById('formEduStatus').value = edu.status || 'Completed';
        document.getElementById('formEduCoursework').value = edu.coursework || '';
        document.getElementById('formEduDesc').value = edu.description || '';

        const title = document.getElementById('eduModalTitle');
        if (title) title.innerHTML = `<i class="fa-solid fa-graduation-cap"></i> Edit: ${escapeHtml(edu.degree || edu.level)}`;

        openModal('educationModal');
      } else {
        showToast('Could not load education record details.', 'error');
      }
    })
    .catch(() => showToast('Error fetching education details.', 'error'));
}

function renderEducationListDOM(eduList) {
  const container = document.getElementById('educationTimelineList');
  if (!container || !eduList) return;

  container.innerHTML = '';
  eduList.forEach(edu => {
    let levelBadgeClass = 'edu-level-college';
    let levelIcon = 'fa-graduation-cap';
    const lvl = (edu.level || '').toLowerCase();
    if (lvl.includes('12th') || lvl.includes('higher')) {
      levelBadgeClass = 'edu-level-12th';
      levelIcon = 'fa-school';
    } else if (lvl.includes('10th') || lvl.includes('secondary')) {
      levelBadgeClass = 'edu-level-10th';
      levelIcon = 'fa-book-open';
    }

    const card = document.createElement('div');
    card.className = 'education-card';
    card.id = `edu-card-${edu.id}`;

    let courseworkHtml = '';
    if (edu.coursework_list && edu.coursework_list.length > 0) {
      const chips = edu.coursework_list.map(c => `<span class="course-chip">${escapeHtml(c)}</span>`).join('');
      courseworkHtml = `
        <div class="edu-coursework-section">
          <span class="coursework-label"><i class="fa-solid fa-book-bookmark"></i> Key Subjects / Coursework:</span>
          <div class="coursework-chips">${chips}</div>
        </div>
      `;
    }

    let boardHtml = edu.board ? `<p class="edu-board-title"><i class="fa-solid fa-landmark"></i> Affiliation / Board: ${escapeHtml(edu.board)}</p>` : '';
    let cgpaHtml = edu.cgpa ? `<span class="edu-cgpa-pill"><i class="fa-solid fa-medal"></i> Score: ${escapeHtml(edu.cgpa)}</span>` : '';
    let descHtml = edu.description ? `<p class="edu-description">${escapeHtml(edu.description)}</p>` : '';

    card.innerHTML = `
      <div class="edu-card-top">
        <div class="edu-institution-info">
          <span class="edu-level-badge ${levelBadgeClass}"><i class="fa-solid ${levelIcon}"></i> ${escapeHtml(edu.level)}</span>
          <h3 class="edu-institution-name">${escapeHtml(edu.institution)}</h3>
          ${boardHtml}
          <h4 class="edu-major-title">${escapeHtml(edu.degree)} ${edu.major ? '• ' + escapeHtml(edu.major) : ''}</h4>
        </div>

        <div class="edu-badges-col">
          <span class="edu-timeline-pill"><i class="fa-regular fa-calendar-check"></i> ${escapeHtml(edu.timeline)}</span>
          ${cgpaHtml}
          <span class="edu-status-pill">${escapeHtml(edu.status)}</span>
        </div>
      </div>

      ${descHtml}
      ${courseworkHtml}

      <div class="edu-card-actions">
        <button class="btn btn-sm btn-outline edit-edu-btn" data-id="${edu.id}" title="Edit education record">
          <i class="fa-solid fa-pen-to-square"></i> Edit
        </button>
        <button class="btn btn-sm btn-outline delete-edu-btn admin-only-actions" data-id="${edu.id}" title="Delete record" style="color: #EF4444; border-color: rgba(239, 68, 68, 0.3);">
          <i class="fa-solid fa-trash-can"></i> Delete
        </button>
      </div>
    `;

    container.appendChild(card);
  });

  // Re-apply admin visibility
  if (isAdminSessionActive()) {
    document.querySelectorAll('.admin-only-actions').forEach(el => el.classList.add('visible'));
  }
}

function updateHeroEducationDOM(primaryEdu) {
  if (!primaryEdu) return;
  const instHero = document.getElementById('displayHeroEduInst');
  const cgpaMetric = document.getElementById('displayEduCgpa');
  if (instHero && primaryEdu.institution) instHero.textContent = primaryEdu.institution;
  if (cgpaMetric && primaryEdu.cgpa) cgpaMetric.textContent = primaryEdu.cgpa;
}

/* --------------------------------------------------------------------------
   6. Certificate Form Submission (File Upload / Online Badge)
   -------------------------------------------------------------------------- */
function initCertificateForm() {
  const form = document.getElementById('certificateForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('saveCertBtn');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading & Saving...';

    const formData = new FormData(form);

    try {
      const res = await fetch('/api/certificates', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      if (res.ok && data.success) {
        showToast(data.message || 'Certificate uploaded & saved!', 'success');
        setAdminUnlocked();
        closeModal('certificateModal');
        form.reset();

        const fileDisplay = document.getElementById('fileSelectedDisplay');
        if (fileDisplay) fileDisplay.style.display = 'none';

        // Refresh certificates list dynamically
        refreshCertificatesGrid();
        updateStatsDOM(data.stats);
      } else {
        showToast(data.message || 'Error uploading certificate.', 'error');
      }
    } catch (err) {
      console.error(err);
      showToast('Network error while uploading certificate.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });
}

function resetCertificateForm() {
  const form = document.getElementById('certificateForm');
  if (form) form.reset();
  const certId = document.getElementById('formCertId');
  if (certId) certId.value = '';
  const fileDisplay = document.getElementById('fileSelectedDisplay');
  if (fileDisplay) fileDisplay.style.display = 'none';
  const title = document.getElementById('certModalTitle');
  if (title) title.innerHTML = '<i class="fa-solid fa-file-arrow-up"></i> Upload / Add Certificate';
}

function openEditCertificateModal(certId) {
  fetch(`/api/certificates/${certId}`)
    .then(res => res.json())
    .then(cert => {
      if (cert && !cert.error) {
        document.getElementById('formCertId').value = cert.id;
        document.getElementById('formCertTitle').value = cert.title || '';
        document.getElementById('formCertIssuer').value = cert.issuer || '';
        document.getElementById('formCertDate').value = cert.issue_date || '';
        document.getElementById('formCertCategory').value = cert.category || 'Technical Certification';
        document.getElementById('formCertCredId').value = cert.credential_id || '';
        document.getElementById('formCertUrl').value = cert.credential_url || '';
        document.getElementById('formCertDesc').value = cert.description || '';

        const fileDisplay = document.getElementById('fileSelectedDisplay');
        const fileNameSpan = document.getElementById('fileSelectedName');
        if (cert.file_path && fileDisplay && fileNameSpan) {
          fileNameSpan.textContent = `Current File: ${cert.file_name || 'Uploaded Document'}`;
          fileDisplay.style.display = 'block';
        }

        const title = document.getElementById('certModalTitle');
        if (title) title.innerHTML = `<i class="fa-solid fa-pen-to-square"></i> Edit: ${escapeHtml(cert.title)}`;

        openModal('certificateModal');
      } else {
        showToast('Could not load certificate details.', 'error');
      }
    })
    .catch(() => showToast('Error fetching certificate details.', 'error'));
}

async function refreshCertificatesGrid() {
  try {
    const res = await fetch('/api/certificates');
    const certificates = await res.json();
    renderCertificatesGridDOM(certificates);
  } catch (e) {
    console.error(e);
  }
}

function renderCertificatesGridDOM(certificates) {
  const grid = document.getElementById('certificateGridList');
  if (!grid || !certificates) return;

  grid.innerHTML = '';
  if (certificates.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <i class="fa-solid fa-certificate"></i>
        <p>No certificates uploaded yet. Click "Upload Certificate" to add your 10th/12th marksheet or course credentials!</p>
      </div>
    `;
    return;
  }

  certificates.forEach(cert => {
    let iconClass = 'file-link';
    let iconEl = '<i class="fa-solid fa-certificate"></i>';
    if (cert.file_path && cert.file_path.toLowerCase().endsWith('.pdf')) {
      iconClass = 'file-pdf';
      iconEl = '<i class="fa-solid fa-file-pdf"></i>';
    } else if (cert.file_path) {
      iconClass = 'file-img';
      iconEl = '<i class="fa-solid fa-file-image"></i>';
    }

    let credIdHtml = cert.credential_id ? `<span class="cert-cred-id"><i class="fa-solid fa-hashtag"></i> ID: ${escapeHtml(cert.credential_id)}</span>` : '';
    let descHtml = cert.description ? `<p class="cert-desc">${escapeHtml(cert.description)}</p>` : '';

    let actionBtnHtml = '';
    if (cert.file_path) {
      actionBtnHtml = `
        <a href="${cert.file_path}" target="_blank" rel="noopener noreferrer" class="cert-action-btn" title="View or Download Certificate">
          <i class="fa-solid fa-arrow-down-to-bracket"></i>
          <span>View / Download</span>
        </a>
      `;
    } else if (cert.credential_url) {
      actionBtnHtml = `
        <a href="${cert.credential_url}" target="_blank" rel="noopener noreferrer" class="cert-action-btn" title="Verify Online">
          <i class="fa-solid fa-arrow-up-right-from-square"></i>
          <span>Verify Online</span>
        </a>
      `;
    } else {
      actionBtnHtml = `
        <span class="cert-action-btn" style="opacity: 0.6; cursor: default;">
          <i class="fa-solid fa-circle-check"></i>
          <span>Verified</span>
        </span>
      `;
    }

    const card = document.createElement('article');
    card.className = 'certificate-card';
    card.id = `cert-card-${cert.id}`;
    card.setAttribute('data-category', cert.category_slug);

    card.innerHTML = `
      <div class="cert-card-header">
        <div class="cert-icon-wrapper ${iconClass}">
          ${iconEl}
        </div>
        <div class="cert-meta-col">
          <span class="cert-category-tag category-${cert.category_slug}">${escapeHtml(cert.category)}</span>
          <span class="cert-date"><i class="fa-regular fa-calendar"></i> ${escapeHtml(cert.issue_date)}</span>
        </div>
      </div>

      <h3 class="cert-title">${escapeHtml(cert.title)}</h3>
      <p class="cert-issuer"><i class="fa-solid fa-building-columns"></i> ${escapeHtml(cert.issuer)}</p>

      ${descHtml}
      ${credIdHtml}

      <div class="cert-footer">
        ${actionBtnHtml}

        <div class="activity-actions admin-only-actions">
          <button class="icon-action-btn edit-cert-btn" data-id="${cert.id}" title="Edit Certificate">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="icon-action-btn delete-cert-btn" data-id="${cert.id}" title="Delete Certificate">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  if (isAdminSessionActive()) {
    document.querySelectorAll('.admin-only-actions').forEach(el => el.classList.add('visible'));
  }
}

/* --------------------------------------------------------------------------
   7. Card Action Event Delegation (Edit & Delete for Edu, Certs, Activities)
   -------------------------------------------------------------------------- */
function initCardActionDelegates() {
  document.addEventListener('click', async (e) => {
    // 1. Edit Education Record
    const editEduBtn = e.target.closest('.edit-edu-btn');
    if (editEduBtn) {
      const eduId = editEduBtn.getAttribute('data-id');
      if (eduId) openEditEducationModal(eduId);
      return;
    }

    // 2. Delete Education Record
    const deleteEduBtn = e.target.closest('.delete-edu-btn');
    if (deleteEduBtn) {
      const eduId = deleteEduBtn.getAttribute('data-id');
      if (!eduId) return;

      if (!confirm('Are you sure you want to delete this education milestone?')) return;

      let pin = '';
      if (!isAdminSessionActive()) {
        pin = prompt('Enter Admin PIN to confirm delete:');
        if (!pin) return;
      }

      try {
        const res = await fetch(`/api/education/${eduId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Admin-PIN': pin
          },
          body: JSON.stringify({ admin_pin: pin })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast('Education record deleted.', 'info');
          const card = document.getElementById(`edu-card-${eduId}`);
          if (card) card.remove();
          updateStatsDOM(data.stats);
          if (data.primary_education) updateHeroEducationDOM(data.primary_education);
        } else {
          showToast(data.message || 'Error deleting education record.', 'error');
        }
      } catch (err) {
        showToast('Network error while deleting.', 'error');
      }
      return;
    }

    // 3. Edit Certificate
    const editCertBtn = e.target.closest('.edit-cert-btn');
    if (editCertBtn) {
      const certId = editCertBtn.getAttribute('data-id');
      if (certId) openEditCertificateModal(certId);
      return;
    }

    // 4. Delete Certificate
    const deleteCertBtn = e.target.closest('.delete-cert-btn');
    if (deleteCertBtn) {
      const certId = deleteCertBtn.getAttribute('data-id');
      if (!certId) return;

      if (!confirm('Are you sure you want to delete this certificate?')) return;

      let pin = '';
      if (!isAdminSessionActive()) {
        pin = prompt('Enter Admin PIN to confirm delete:');
        if (!pin) return;
      }

      try {
        const res = await fetch(`/api/certificates/${certId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Admin-PIN': pin
          },
          body: JSON.stringify({ admin_pin: pin })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast('Certificate deleted.', 'info');
          const card = document.getElementById(`cert-card-${certId}`);
          if (card) card.remove();
          updateStatsDOM(data.stats);
        } else {
          showToast(data.message || 'Error deleting certificate.', 'error');
        }
      } catch (err) {
        showToast('Network error while deleting.', 'error');
      }
      return;
    }

    // 5. Edit Activity
    const editActBtn = e.target.closest('.edit-act-btn');
    if (editActBtn) {
      const actId = editActBtn.getAttribute('data-id');
      if (actId) openEditActivityModal(actId);
      return;
    }

    // 6. Delete Activity
    const deleteActBtn = e.target.closest('.delete-act-btn');
    if (deleteActBtn) {
      const actId = deleteActBtn.getAttribute('data-id');
      if (!actId) return;

      if (!confirm('Are you sure you want to delete this activity entry?')) return;

      let pin = '';
      if (!isAdminSessionActive()) {
        pin = prompt('Enter Admin PIN to confirm delete:');
        if (!pin) return;
      }

      try {
        const res = await fetch(`/api/activities/${actId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-Admin-PIN': pin
          },
          body: JSON.stringify({ admin_pin: pin })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast('Activity deleted.', 'info');
          const card = document.getElementById(`card-${actId}`);
          if (card) card.remove();
          updateStatsDOM(data.stats);
        } else {
          showToast(data.message || 'Error deleting activity.', 'error');
        }
      } catch (err) {
        showToast('Network error while deleting activity.', 'error');
      }
      return;
    }
  });
}

/* --------------------------------------------------------------------------
   8. Activity Form (New & Edit)
   -------------------------------------------------------------------------- */
function initActivityForm() {
  const form = document.getElementById('activityForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('saveActivityBtn');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Publishing...';

    const actId = document.getElementById('formActId')?.value.trim();
    const isEdit = Boolean(actId);

    const payload = {
      title: document.getElementById('formActTitle')?.value.trim(),
      category: document.getElementById('formActCategory')?.value.trim(),
      date: document.getElementById('formActDate')?.value.trim(),
      badge: document.getElementById('formActBadge')?.value.trim(),
      description: document.getElementById('formActDesc')?.value.trim(),
      link: document.getElementById('formActLink')?.value.trim(),
      link_text: document.getElementById('formActLinkText')?.value.trim(),
      admin_pin: document.getElementById('formActAdminPin')?.value.trim()
    };

    const url = isEdit ? `/api/activities/${actId}` : '/api/activities';
    const method = isEdit ? 'PUT' : 'POST';

    try {
      const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (res.ok && data.success) {
        showToast(isEdit ? 'Activity updated successfully!' : 'Live activity published!', 'success');
        setAdminUnlocked();

        if (isEdit) {
          updateActivityCardDOM(data.activity);
        } else {
          prependActivityCardDOM(data.activity);
        }

        updateStatsDOM(data.stats);
        closeModal('activityModal');
        form.reset();
      } else {
        showToast(data.message || 'Error saving activity.', 'error');
      }
    } catch (err) {
      console.error(err);
      showToast('Network error while saving activity.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });

  function prependActivityCardDOM(act) {
    const list = document.getElementById('activityFeedList');
    if (!list) return;

    const emptyState = list.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    const card = document.createElement('article');
    card.className = 'activity-card';
    card.id = `card-${act.id}`;
    card.setAttribute('data-category', act.category_slug);

    let linkHtml = '';
    if (act.link) {
      linkHtml = `
        <a href="${escapeHtml(act.link)}" target="_blank" rel="noopener noreferrer" class="activity-link">
          <span>${escapeHtml(act.link_text || 'Explore Link')}</span>
          <i class="fa-solid fa-arrow-up-right-from-square"></i>
        </a>
      `;
    }

    let badgeHtml = act.badge ? `<span class="activity-tech-badge"><i class="fa-solid fa-tag"></i> ${escapeHtml(act.badge)}</span>` : '';

    card.innerHTML = `
      <div class="activity-card-header">
        <span class="activity-category-tag category-${act.category_slug}">${escapeHtml(act.category)}</span>
        <span class="activity-date"><i class="fa-regular fa-clock"></i> ${escapeHtml(act.date)}</span>
      </div>
      <h3 class="activity-title">${escapeHtml(act.title)}</h3>
      <p class="activity-desc">${escapeHtml(act.description)}</p>
      <div class="activity-footer">
        ${badgeHtml}
        ${linkHtml}
        <div class="activity-actions admin-only-actions visible">
          <button class="icon-action-btn edit-act-btn" data-id="${act.id}" title="Edit Activity">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="icon-action-btn delete-act-btn" data-id="${act.id}" title="Delete Activity">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>
    `;

    list.prepend(card);
  }

  function updateActivityCardDOM(act) {
    const card = document.getElementById(`card-${act.id}`);
    if (!card) return;

    card.setAttribute('data-category', act.category_slug);
    const catTag = card.querySelector('.activity-category-tag');
    if (catTag) {
      catTag.className = `activity-category-tag category-${act.category_slug}`;
      catTag.textContent = act.category;
    }

    const titleEl = card.querySelector('.activity-title');
    if (titleEl) titleEl.textContent = act.title;

    const descEl = card.querySelector('.activity-desc');
    if (descEl) descEl.textContent = act.description;

    const dateEl = card.querySelector('.activity-date');
    if (dateEl) dateEl.innerHTML = `<i class="fa-regular fa-clock"></i> ${escapeHtml(act.date)}`;
  }
}

function resetActivityForm() {
  const form = document.getElementById('activityForm');
  if (form) form.reset();
  const formId = document.getElementById('formActId');
  if (formId) formId.value = '';
  const title = document.getElementById('actModalTitle');
  if (title) title.innerHTML = '<i class="fa-solid fa-plus-circle"></i> Post Live Activity';
}

function openEditActivityModal(activityId) {
  fetch(`/api/activities/${activityId}`)
    .then(res => res.json())
    .then(act => {
      if (act && !act.error) {
        document.getElementById('formActId').value = act.id;
        document.getElementById('formActTitle').value = act.title || '';
        document.getElementById('formActCategory').value = act.category || 'Project Milestone';
        document.getElementById('formActDate').value = act.date || '';
        document.getElementById('formActBadge').value = act.badge || '';
        document.getElementById('formActDesc').value = act.description || '';
        document.getElementById('formActLink').value = act.link || '';
        document.getElementById('formActLinkText').value = act.link_text || 'View Repository';

        const title = document.getElementById('actModalTitle');
        if (title) title.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Edit Activity Entry';

        openModal('activityModal');
      } else {
        showToast('Could not load activity details.', 'error');
      }
    })
    .catch(() => showToast('Error fetching activity details.', 'error'));
}

/* --------------------------------------------------------------------------
   9. Profile Form Submission
   -------------------------------------------------------------------------- */
function initProfileForm() {
  const form = document.getElementById('profileForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('formProfName')?.value.trim(),
      title: document.getElementById('formProfTitle')?.value.trim(),
      email: document.getElementById('formProfEmail')?.value.trim(),
      phone: document.getElementById('formProfPhone')?.value.trim(),
      location: document.getElementById('formProfLocation')?.value.trim(),
      github: document.getElementById('formProfGithub')?.value.trim(),
      linkedin: document.getElementById('formProfLinkedin')?.value.trim(),
      twitter: document.getElementById('formProfTwitter')?.value.trim(),
      tagline: document.getElementById('formProfTagline')?.value.trim(),
      bio: document.getElementById('formProfBio')?.value.trim(),
      admin_pin: document.getElementById('formProfAdminPin')?.value.trim()
    };

    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok && data.success) {
        showToast('Profile updated!', 'success');
        setAdminUnlocked();
        document.getElementById('displayProfileName').textContent = payload.name;
        document.getElementById('displayProfileTitle').textContent = payload.title;
        document.getElementById('displayProfileTagline').textContent = `"${payload.tagline}"`;
        document.getElementById('displayContactEmail').textContent = payload.email;
        document.getElementById('displayContactLocation').textContent = payload.location;
        closeModal('profileModal');
      } else {
        showToast(data.message || 'Error updating profile.', 'error');
      }
    } catch (err) {
      showToast('Network error while saving profile.', 'error');
    }
  });
}

/* --------------------------------------------------------------------------
   10. Admin PIN State Management
   -------------------------------------------------------------------------- */
async function checkAdminStatus() {
  try {
    const res = await fetch('/api/auth/status');
    const data = await res.json();
    if (data.authenticated) {
      setAdminUnlocked();
    }
  } catch (e) {}

  const btn = document.getElementById('adminStatusBtn');
  const footerBtn = document.getElementById('footerAdminToggleBtn');

  [btn, footerBtn].forEach(b => {
    if (b) {
      b.addEventListener('click', () => {
        promptAdminUnlock();
      });
    }
  });
}

function isAdminSessionActive() {
  const btn = document.getElementById('adminStatusBtn');
  return btn && btn.classList.contains('unlocked');
}

function promptAdminUnlock() {
  const pin = prompt('Enter Admin PIN to unlock instant in-browser editing:');
  if (!pin) return;

  fetch('/api/auth/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pin: pin })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showToast('Admin edit mode unlocked!', 'success');
      setAdminUnlocked();
    } else {
      showToast(data.message || 'Invalid PIN.', 'error');
    }
  })
  .catch(() => showToast('Error verifying PIN.', 'error'));
}

function setAdminUnlocked() {
  const btn = document.getElementById('adminStatusBtn');
  if (btn) {
    btn.classList.add('unlocked');
    btn.innerHTML = '<i class="fa-solid fa-lock-open"></i>';
    btn.title = 'Admin Edit Mode: Active';
  }

  // Show inline edit/delete buttons
  document.querySelectorAll('.admin-only-actions').forEach(el => {
    el.classList.add('visible');
  });

  // Hide PIN inputs inside modals once authenticated
  document.querySelectorAll('.admin-pin-input-group').forEach(el => {
    el.style.display = 'none';
  });
}

function updateStatsDOM(stats) {
  if (!stats) return;
  const totalActEl = document.getElementById('displayStatTotalAct');
  const certsEl = document.getElementById('displayStatCertificates');
  const eduStagesEl = document.getElementById('displayStatEduStages');

  if (totalActEl && stats.total_activities !== undefined) totalActEl.textContent = stats.total_activities;
  if (certsEl && stats.total_certificates !== undefined) certsEl.textContent = stats.total_certificates;
  if (eduStagesEl && stats.total_education_stages !== undefined) eduStagesEl.textContent = stats.total_education_stages;
}

/* --------------------------------------------------------------------------
   11. Toast Utility
   -------------------------------------------------------------------------- */
function showToast(message, type = 'info') {
  const stack = document.getElementById('toastStack');
  if (!stack) return;

  const iconMap = {
    success: 'fa-solid fa-circle-check',
    error: 'fa-solid fa-circle-xmark',
    info: 'fa-solid fa-circle-info'
  };

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<i class="${iconMap[type] || iconMap.info}"></i> <span>${escapeHtml(message)}</span>`;

  stack.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(25px)';
    toast.style.transition = 'all 0.25s ease-out';
    setTimeout(() => toast.remove(), 250);
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
