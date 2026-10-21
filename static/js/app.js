/**
 * Activity & Academic Hub - Interactive Client Application
 * Candidate: Pradeep Kumar Suresh
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initModals();
  initSearchAndFilters();
  initEducationForm();
  initActivityForm();
  initProfileForm();
  initActivityActions();
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
   2. Modal Dialog Management
   -------------------------------------------------------------------------- */
function initModals() {
  // Triggers for Education Modal
  const editEduBtns = [
    document.getElementById('openEditEducationModalBtn'),
    document.getElementById('sectionEditEduBtn')
  ];
  editEduBtns.forEach(btn => {
    if (btn) btn.addEventListener('click', () => openModal('educationModal'));
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
   3. Search and Category Filtering
   -------------------------------------------------------------------------- */
function initSearchAndFilters() {
  const searchInput = document.getElementById('activitySearchInput');
  const clearBtn = document.getElementById('clearSearchBtn');
  const filterChips = document.querySelectorAll('.filter-chip');

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
    const cards = document.querySelectorAll('.activity-card');
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

    // Handle empty search feedback
    const feedList = document.getElementById('activityFeedList');
    let noResultsNotice = document.getElementById('noSearchResults');
    if (visibleCount === 0) {
      if (!noResultsNotice) {
        noResultsNotice = document.createElement('div');
        noResultsNotice.id = 'noSearchResults';
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
   4. Education Form Submission (AJAX)
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

    const payload = {
      institution: document.getElementById('formEduInstitution')?.value.trim(),
      degree: document.getElementById('formEduDegree')?.value.trim(),
      major: document.getElementById('formEduMajor')?.value.trim(),
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
        showToast(data.message || 'Education details saved!', 'success');
        updateEducationDOM(data.education);
        setAdminUnlocked();
        closeModal('educationModal');
      } else {
        showToast(data.message || 'Error updating education.', 'error');
      }
    } catch (err) {
      console.error(err);
      showToast('Network error while saving education.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });

  function updateEducationDOM(edu) {
    if (!edu) return;
    const instEl = document.getElementById('displayEduInstitution');
    const majorEl = document.getElementById('displayEduMajor');
    const timelineEl = document.getElementById('displayEduTimeline');
    const cgpaPill = document.getElementById('displayEduCgpaBadge');
    const cgpaMetric = document.getElementById('displayEduCgpa');
    const statusEl = document.getElementById('displayEduStatus');
    const descEl = document.getElementById('displayEduDesc');
    const chipsEl = document.getElementById('displayCourseworkChips');

    if (instEl) instEl.textContent = edu.institution;
    if (majorEl) majorEl.textContent = edu.major;
    if (timelineEl) timelineEl.innerHTML = `<i class="fa-regular fa-calendar-check"></i> ${escapeHtml(edu.timeline)}`;
    if (cgpaPill) cgpaPill.innerHTML = `<i class="fa-solid fa-medal"></i> CGPA: ${escapeHtml(edu.cgpa || 'N/A')}`;
    if (cgpaMetric) cgpaMetric.textContent = edu.cgpa || 'N/A';
    if (statusEl) statusEl.textContent = edu.status;
    if (descEl) descEl.textContent = edu.description;

    if (chipsEl && edu.coursework_list) {
      chipsEl.innerHTML = '';
      edu.coursework_list.forEach(course => {
        const chip = document.createElement('span');
        chip.className = 'course-chip';
        chip.textContent = course;
        chipsEl.appendChild(chip);
      });
    }
  }
}

/* --------------------------------------------------------------------------
   5. Activity Form Submission (New & Edit)
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

    // Remove empty state
    const emptyState = list.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    const card = document.createElement('article');
    card.className = 'activity-card';
    card.id = `card-${act.id}`;
    card.setAttribute('data-category', act.category_slug);
    card.innerHTML = buildActivityCardHTML(act);

    list.prepend(card);
    attachCardActions(card);
  }

  function updateActivityCardDOM(act) {
    const card = document.getElementById(`card-${act.id}`);
    if (card) {
      card.setAttribute('data-category', act.category_slug);
      card.innerHTML = buildActivityCardHTML(act);
      attachCardActions(card);
    }
  }
}

function resetActivityForm() {
  const form = document.getElementById('activityForm');
  if (form) form.reset();
  const actIdInput = document.getElementById('formActId');
  if (actIdInput) actIdInput.value = '';
  const titleEl = document.getElementById('actModalTitle');
  if (titleEl) titleEl.innerHTML = '<i class="fa-solid fa-plus-circle"></i> Post Live Activity';
  const submitBtn = document.getElementById('saveActivityBtn');
  if (submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Publish Activity';
}

function buildActivityCardHTML(act) {
  return `
    <div class="activity-card-header">
      <span class="activity-category-tag category-${escapeHtml(act.category_slug)}">${escapeHtml(act.category)}</span>
      <span class="activity-date"><i class="fa-regular fa-clock"></i> ${escapeHtml(act.date)}</span>
    </div>
    <h3 class="activity-title">${escapeHtml(act.title)}</h3>
    <p class="activity-desc">${escapeHtml(act.description)}</p>
    <div class="activity-footer">
      ${act.badge ? `<span class="activity-tech-badge"><i class="fa-solid fa-tag"></i> ${escapeHtml(act.badge)}</span>` : ''}
      ${act.link ? `<a href="${escapeHtml(act.link)}" target="_blank" rel="noopener noreferrer" class="activity-link"><span>${escapeHtml(act.link_text || 'Explore')}</span><i class="fa-solid fa-arrow-up-right-from-square"></i></a>` : ''}
      <div class="activity-actions admin-only-actions visible">
        <button class="icon-action-btn edit-act-btn" data-id="${act.id}" title="Edit Activity"><i class="fa-solid fa-pen"></i></button>
        <button class="icon-action-btn delete-act-btn" data-id="${act.id}" title="Delete Activity"><i class="fa-solid fa-trash-can"></i></button>
      </div>
    </div>
  `;
}

/* --------------------------------------------------------------------------
   6. Activity Card Actions (Edit & Delete)
   -------------------------------------------------------------------------- */
function initActivityActions() {
  document.querySelectorAll('.activity-card').forEach(card => {
    attachCardActions(card);
  });
}

function attachCardActions(card) {
  const editBtn = card.querySelector('.edit-act-btn');
  const delBtn = card.querySelector('.delete-act-btn');

  if (editBtn) {
    editBtn.addEventListener('click', async () => {
      const id = editBtn.getAttribute('data-id');
      try {
        const res = await fetch(`/api/activities/${id}`);
        const act = await res.json();
        if (res.ok && act) {
          document.getElementById('formActId').value = act.id;
          document.getElementById('formActTitle').value = act.title;
          document.getElementById('formActCategory').value = act.category;
          document.getElementById('formActDate').value = act.date;
          document.getElementById('formActBadge').value = act.badge || '';
          document.getElementById('formActDesc').value = act.description;
          document.getElementById('formActLink').value = act.link || '';
          document.getElementById('formActLinkText').value = act.link_text || '';

          document.getElementById('actModalTitle').innerHTML = '<i class="fa-solid fa-pen"></i> Edit Activity';
          document.getElementById('saveActivityBtn').innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Activity Changes';
          openModal('activityModal');
        }
      } catch (err) {
        showToast('Error loading activity data.', 'error');
      }
    });
  }

  if (delBtn) {
    delBtn.addEventListener('click', async () => {
      const id = delBtn.getAttribute('data-id');
      if (!confirm('Are you sure you want to delete this activity update?')) return;

      try {
        const res = await fetch(`/api/activities/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast('Activity deleted.', 'info');
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          card.style.transition = 'all 0.25s ease-out';
          setTimeout(() => {
            card.remove();
            updateStatsDOM(data.stats);
          }, 250);
        } else {
          showToast(data.message || 'Failed to delete activity.', 'error');
        }
      } catch (err) {
        showToast('Network error while deleting.', 'error');
      }
    });
  }
}

/* --------------------------------------------------------------------------
   7. Profile Form (AJAX)
   -------------------------------------------------------------------------- */
function initProfileForm() {
  const form = document.getElementById('profileForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
      name: document.getElementById('formProfName')?.value.trim(),
      title: document.getElementById('formProfTitle')?.value.trim(),
      tagline: document.getElementById('formProfTagline')?.value.trim(),
      bio: document.getElementById('formProfBio')?.value.trim(),
      email: document.getElementById('formProfEmail')?.value.trim(),
      phone: document.getElementById('formProfPhone')?.value.trim(),
      location: document.getElementById('formProfLocation')?.value.trim(),
      github: document.getElementById('formProfGithub')?.value.trim(),
      linkedin: document.getElementById('formProfLinkedin')?.value.trim(),
      twitter: document.getElementById('formProfTwitter')?.value.trim(),
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
      showToast('Network error.', 'error');
    }
  });
}

/* --------------------------------------------------------------------------
   8. Admin PIN State Management
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

  // Show inline edit/delete buttons on activity cards
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
  const totalEl = document.getElementById('displayStatTotalAct');
  const projEl = document.getElementById('displayStatProjects');
  const hackEl = document.getElementById('displayStatHackathons');

  if (totalEl) totalEl.textContent = stats.total_activities;
  if (projEl) projEl.textContent = stats.project_milestones;
  if (hackEl) hackEl.textContent = stats.hackathons;
}

/* --------------------------------------------------------------------------
   Toast Utility
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
