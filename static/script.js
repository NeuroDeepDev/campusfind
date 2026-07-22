(function () {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
})();

// Clear all filters and state when CampusFind logo is clicked
function clearAllFilters(e) {
  // Clear localStorage except theme
  const currentTheme = localStorage.getItem('theme');
  localStorage.clear();
  if (currentTheme) {
    localStorage.setItem('theme', currentTheme);
  }

  // Clear sessionStorage
  sessionStorage.clear();

  // Clear URL query parameters by navigating to clean home URL
  e.preventDefault();
  window.location.href = '/';
}

function initPage() {
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }

  const hamburgerBtn = document.getElementById('hamburger-toggle');
  const mobileNav = document.getElementById('mobile-nav');

  if (hamburgerBtn && mobileNav) {
    hamburgerBtn.addEventListener('click', function () {
      hamburgerBtn.classList.toggle('active');
      mobileNav.classList.toggle('mobile-hidden');
    });

    // Close menu when a nav item is clicked
    document.querySelectorAll('.nav-item').forEach(function (item) {
      item.addEventListener('click', function () {
        hamburgerBtn.classList.remove('active');
        mobileNav.classList.add('mobile-hidden');
      });
    });
  }

  // Confirm delete helpers (if any delete buttons exist)
  document.querySelectorAll('.confirm-delete').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to delete this item?')) {
        e.preventDefault();
      }
    });
  });

  // Simple client-side search filtering if present
  var searchForm = document.getElementById('search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', function () {
      // let the server handle search; this is a placeholder
    });
  }

  // Password show/hide toggle: buttons with class .password-toggle-btn
  document.querySelectorAll('.password-toggle-btn').forEach(function (btn) {
    // helper to sync button state based on input.type
    function syncState() {
      var wrapper = btn.closest('.password-wrapper');
      if (!wrapper) return;
      var input = wrapper.querySelector('input[type="password"], input[type="text"]');
      if (!input) return;
      var isHidden = input.getAttribute('type') === 'password';
      // aria-pressed true means password is visible
      btn.setAttribute('aria-pressed', isHidden ? 'false' : 'true');
      btn.setAttribute('aria-label', isHidden ? 'Show password' : 'Hide password');
      btn.setAttribute('title', isHidden ? 'Show password' : 'Hide password');
    }

    // initialize state on load
    syncState();

    // click handler toggles input type and updates attributes
    btn.addEventListener('click', function (ev) {
      ev.preventDefault();
      var wrapper = btn.closest('.password-wrapper');
      if (!wrapper) return;
      var input = wrapper.querySelector('input[type="password"], input[type="text"]');
      if (!input) return;
      var isHidden = input.getAttribute('type') === 'password';
      if (isHidden) {
        input.setAttribute('type', 'text');
      } else {
        input.setAttribute('type', 'password');
      }
      // Accessibility + visual sync
      syncState();
      // keep focus on the input after toggling for convenience
      try { input.focus(); } catch (e) {}
    });

    // If the input value or type changes elsewhere, keep button in sync
    var wrapper = btn.closest('.password-wrapper');
    if (wrapper) {
      var inputEl = wrapper.querySelector('input[type="password"], input[type="text"]');
      if (inputEl) {
        inputEl.addEventListener('input', function () { /* noop: placeholder */ });
        // If some script changes type, observe it
        var observer = new MutationObserver(function () { syncState(); });
        observer.observe(inputEl, { attributes: true, attributeFilter: ['type'] });
      }
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPage);
} else {
  initPage();
}
