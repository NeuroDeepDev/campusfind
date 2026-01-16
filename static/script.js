// Clear all filters and state when CampusFind logo is clicked
function clearAllFilters(e) {
  // Clear localStorage
  localStorage.clear();
  
  // Clear sessionStorage
  sessionStorage.clear();
  
  // Clear URL query parameters by navigating to clean home URL
  e.preventDefault();
  window.location.href = '/';
}

// Hamburger menu toggle for mobile
document.addEventListener('DOMContentLoaded', function(){
  const hamburgerBtn = document.getElementById('hamburger-toggle');
  const mobileNav = document.getElementById('mobile-nav');

  if (hamburgerBtn && mobileNav) {
    hamburgerBtn.addEventListener('click', function() {
      hamburgerBtn.classList.toggle('active');
      mobileNav.classList.toggle('mobile-hidden');
    });

    // Close menu when a nav item is clicked
    document.querySelectorAll('.nav-item').forEach(function(item) {
      item.addEventListener('click', function() {
        hamburgerBtn.classList.remove('active');
        mobileNav.classList.add('mobile-hidden');
      });
    });
  }

  // Confirm delete helpers (if any delete buttons exist)
  document.querySelectorAll('.confirm-delete').forEach(function(btn){
    btn.addEventListener('click', function(e){
      if(!confirm('Are you sure you want to delete this item?')){
        e.preventDefault();
      }
    });
  });

  // Simple client-side search filtering if present
  var searchForm = document.getElementById('search-form');
  if(searchForm){
    searchForm.addEventListener('submit', function(){
      // let the server handle search; this is a placeholder
    });
  }
});
