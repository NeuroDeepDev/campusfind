async function postJSON(url, data){
  const res = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(data),
  });
  return res;
}

async function onLogin(e){
  e.preventDefault();
  const user = document.getElementById('username').value;
  const pass = document.getElementById('password').value;
  const resp = await postJSON('/api/token/', {username: user, password: pass});
  const msg = document.getElementById('message');
  if (resp.ok){
    const data = await resp.json();
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    // fetch profile
    const profile = await fetch('/api/users/students/me/', {headers: {Authorization: 'Bearer ' + data.access}});
    if (profile.ok){
      window.location = '/dashboard/';
    } else {
      msg.textContent = 'Login succeeded but failed to load profile.';
    }
  } else {
    msg.textContent = 'Login failed';
  }
}

async function onRegister(e){
  e.preventDefault();
  const user = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const pass = document.getElementById('password').value;
  const phone = document.getElementById('phone').value;
  const resp = await postJSON('/api/users/students/register/', {username: user, email: email, password: pass, phone: phone});
  const msg = document.getElementById('message');
  if (resp.ok){
    msg.style.color = 'green';
    msg.textContent = 'Registered. Redirecting to login...';
    setTimeout(()=> window.location = '/login/', 1200);
  } else {
    const txt = await resp.text();
    msg.textContent = 'Register failed: ' + txt;
  }
}

if (document.getElementById('login-form')){
  document.getElementById('login-form').addEventListener('submit', onLogin);
}
if (document.getElementById('register-form')){
  document.getElementById('register-form').addEventListener('submit', onRegister);
}