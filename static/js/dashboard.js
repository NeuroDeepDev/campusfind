async function loadProfile(){
  const token = localStorage.getItem('access_token');
  const el = document.getElementById('user-info');
  if (!token){
    window.location = '/login/';
    return;
  }
  const resp = await fetch('/api/users/students/me/', {headers: {Authorization: 'Bearer ' + token}});
  if (!resp.ok){
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location = '/login/';
    return;
  }
  const data = await resp.json();
  el.textContent = 'Logged in as ' + (data.username || data.email || 'user');
}

if (document.getElementById('logout')){
  document.getElementById('logout').addEventListener('click', ()=>{
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location = '/login/';
  });
}

if (document.getElementById('user-info')){
  loadProfile();
}