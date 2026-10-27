// Separate authentication views keep the original URL for survey share links.
function auth(username = '') {
  root.innerHTML = `<section class="auth"><h1>登录账号</h1>
    <p class="muted">登录后创建或填写问卷。</p><form id="auth">
    <label>用户名<input id="username" required pattern="[a-zA-Z0-9_]{3,40}" autocomplete="username" value="${esc(username)}"></label>
    <label>密码<input id="password" type="password" required maxlength="128" autocomplete="current-password"></label>
    <button>登录</button></form><p>还没有账号？<button type="button" class="secondary" id="register">注册账号</button></p></section>`;
  bind('auth', 'submit', async () => {
    token = (await api('/auth/login', 'POST', {
      username: document.querySelector('#username').value,
      password: document.querySelector('#password').value
    })).access_token;
    sessionStorage.setItem('survey_token', token);
    await boot();
  });
  bind('register', 'click', () => { notice.textContent = ''; registration(); });
}

function registration() {
  root.innerHTML = `<section class="auth"><h1>注册账号</h1>
    <p class="muted">用户名为3～40位英文字母、数字或下划线；密码为8～16个字符。</p>
    <form id="registration" novalidate>
    <label>用户名<input id="username" required maxlength="40" autocomplete="username"></label>
    <label>密码<input id="password" type="password" required autocomplete="new-password"></label>
    <label>确认密码<input id="confirmPassword" type="password" required autocomplete="new-password"></label>
    <button id="submitRegistration">注册</button></form>
    <p>已有账号？<button id="backToLogin" type="button" class="secondary">返回登录</button></p></section>`;
  bind('backToLogin', 'click', () => { notice.textContent = ''; auth(); });
  bind('registration', 'submit', async () => {
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    const confirmation = document.querySelector('#confirmPassword').value;
    if (!username || !password || !confirmation) throw Error('请填写用户名、密码和确认密码。');
    if (!/^[a-zA-Z0-9_]{3,40}$/.test(username)) throw Error('用户名须为3～40位英文字母、数字或下划线。');
    const passwordLength = Array.from(password).length;
    if (passwordLength < 8 || passwordLength > 16) throw Error('密码长度须为8～16个字符。');
    if (password !== confirmation) throw Error('两次输入的密码不一致，请重新确认。');
    const button = document.querySelector('#submitRegistration');
    button.disabled = true;
    try {
      await api('/auth/register', 'POST', { username, password });
      auth(username);
      message('注册成功，请使用新账号登录。');
    } catch (error) {
      if (error.message === '用户名已存在') throw Error('该用户名已存在，请更换用户名；已有账号可返回登录。');
      throw error;
    } finally {
      button.disabled = false;
    }
  });
}
