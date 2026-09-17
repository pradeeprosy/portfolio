/**
 * Personal Career Portfolio - Client-side Interactive Script
 * Pradeep Kumar | Computer Science Engineering Student
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initMobileNavigation();
  initScrollSpy();
  initScrollTop();
  initProjectModals();
  initContactForm();
});

/* --------------------------------------------------------------------------
   1. Theme Toggle (Dark / Light Mode) with LocalStorage
   -------------------------------------------------------------------------- */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  if (!themeToggleBtn || !themeIcon) return;

  // Retrieve saved preference or default to dark
  const savedTheme = localStorage.getItem('theme') || 'dark';
  applyTheme(savedTheme);

  themeToggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  });

  function applyTheme(theme) {
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
      themeIcon.className = 'fa-solid fa-moon';
      themeToggleBtn.setAttribute('aria-label', 'Switch to dark mode');
    } else {
      document.documentElement.removeAttribute('data-theme');
      themeIcon.className = 'fa-solid fa-sun';
      themeToggleBtn.setAttribute('aria-label', 'Switch to light mode');
    }
    localStorage.setItem('theme', theme);
  }
}

/* --------------------------------------------------------------------------
   2. Mobile Navigation Drawer
   -------------------------------------------------------------------------- */
function initMobileNavigation() {
  const mobileToggleBtn = document.getElementById('mobileToggleBtn');
  const navMenu = document.getElementById('navMenu');
  if (!mobileToggleBtn || !navMenu) return;

  mobileToggleBtn.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    mobileToggleBtn.setAttribute('aria-expanded', isOpen);
    mobileToggleBtn.innerHTML = isOpen 
      ? '<i class="fa-solid fa-xmark"></i>' 
      : '<i class="fa-solid fa-bars"></i>';
  });

  // Close nav drawer upon clicking any link
  navMenu.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      mobileToggleBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
    });
  });

  // Close when clicking outside header
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.site-header') && navMenu.classList.contains('open')) {
      navMenu.classList.remove('open');
      mobileToggleBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
    }
  });
}

/* --------------------------------------------------------------------------
   3. Scroll Spy for Active Navigation Links
   -------------------------------------------------------------------------- */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  if (!sections.length || !navLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const activeId = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${activeId}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach(section => observer.observe(section));
}

/* --------------------------------------------------------------------------
   4. Scroll To Top Button
   -------------------------------------------------------------------------- */
function initScrollTop() {
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  if (!scrollTopBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 350) {
      scrollTopBtn.classList.add('visible');
    } else {
      scrollTopBtn.classList.remove('visible');
    }
  });

  scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/* --------------------------------------------------------------------------
   5. Interactive Project Modal
   -------------------------------------------------------------------------- */
function initProjectModals() {
  const modalBackdrop = document.getElementById('projectModalBackdrop');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const detailButtons = document.querySelectorAll('.view-project-details');
  if (!modalBackdrop) return;

  const modalTitle = document.getElementById('modalTitle');
  const modalCategory = document.getElementById('modalCategory');
  const modalImage = document.getElementById('modalImage');
  const modalProblem = document.getElementById('modalProblem');
  const modalSolution = document.getElementById('modalSolution');
  const modalTechList = document.getElementById('modalTechList');
  const modalFeatureList = document.getElementById('modalFeatureList');
  const modalGithubLink = document.getElementById('modalGithubLink');
  const modalDemoLink = document.getElementById('modalDemoLink');

  detailButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const slug = btn.getAttribute('data-slug');
      if (!slug) return;

      // Fetch dynamic project JSON from Flask API
      fetch(`/api/projects/${slug}`)
        .then(res => {
          if (!res.ok) throw new Error('Network error loading project');
          return res.json();
        })
        .then(project => {
          populateModal(project);
          openModal();
        })
        .catch(err => {
          console.error(err);
        });
    });
  });

  function populateModal(project) {
    if (modalTitle) modalTitle.textContent = project.title || '';
    if (modalCategory) modalCategory.textContent = project.category || '';
    if (modalImage) {
      modalImage.src = project.image || '/static/images/chatbot-preview.svg';
      modalImage.alt = project.title || 'Project Preview';
    }
    if (modalProblem) modalProblem.textContent = project.problem || '';
    if (modalSolution) modalSolution.textContent = project.solution || '';

    // Populate Technologies
    if (modalTechList) {
      modalTechList.innerHTML = '';
      (project.technologies || []).forEach(tech => {
        const span = document.createElement('span');
        span.className = 'tech-tag';
        span.textContent = tech;
        modalTechList.appendChild(span);
      });
    }

    // Populate Features
    if (modalFeatureList) {
      modalFeatureList.innerHTML = '';
      (project.features || []).forEach(feat => {
        const li = document.createElement('li');
        li.innerHTML = `<i class="fa-solid fa-circle-check"></i> <span>${feat}</span>`;
        modalFeatureList.appendChild(li);
      });
    }

    // Links
    if (modalGithubLink) {
      modalGithubLink.href = project.github || '#';
    }
    if (modalDemoLink) {
      modalDemoLink.href = project.demo || '#';
    }
  }

  function openModal() {
    modalBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modalBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) {
      closeModal();
    }
  });
}

/* --------------------------------------------------------------------------
   6. Contact Form Validation & Asynchronous Dispatch
   -------------------------------------------------------------------------- */
function initContactForm() {
  const contactForm = document.getElementById('contactForm');
  const feedbackBox = document.getElementById('formFeedback');
  const submitBtn = document.getElementById('contactSubmitBtn');
  if (!contactForm || !feedbackBox || !submitBtn) return;

  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nameInput = document.getElementById('formName');
    const emailInput = document.getElementById('formEmail');
    const messageInput = document.getElementById('formMessage');
    const honeypotInput = document.getElementById('formWebsite');

    const name = nameInput ? nameInput.value.trim() : '';
    const email = emailInput ? emailInput.value.trim() : '';
    const message = messageInput ? messageInput.value.trim() : '';
    const honeypot = honeypotInput ? honeypotInput.value.trim() : '';

    // Frontend validation
    if (!name || name.length < 2) {
      showFeedback('Please provide your name (at least 2 characters).', 'error');
      nameInput.focus();
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      showFeedback('Please provide a valid email address.', 'error');
      emailInput.focus();
      return;
    }

    if (!message || message.length < 10) {
      showFeedback('Please write a message with at least 10 characters.', 'error');
      messageInput.focus();
      return;
    }

    // Loading State
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending message...';
    hideFeedback();

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
          name: name,
          email: email,
          message: message,
          website: honeypot
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showFeedback(data.message || 'Thank you! Your message has been sent successfully.', 'success');
        contactForm.reset();
      } else {
        showFeedback(data.message || 'An error occurred while sending your message. Please try again.', 'error');
      }
    } catch (err) {
      console.error(err);
      showFeedback('Network error. Please check your connection or contact directly via email.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });

  function showFeedback(text, type) {
    feedbackBox.className = `form-feedback ${type}`;
    feedbackBox.textContent = text;
    feedbackBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function hideFeedback() {
    feedbackBox.className = 'form-feedback';
    feedbackBox.textContent = '';
  }
}
