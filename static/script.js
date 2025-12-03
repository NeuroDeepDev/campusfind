// Minimal JS: form validation, search filtering, confirm delete
document.addEventListener('DOMContentLoaded', function(){
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
