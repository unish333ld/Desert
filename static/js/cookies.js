// Cookie уведомление
function acceptCookies() {
    localStorage.setItem('cookiesAccepted', 'true');
    document.getElementById('cookieNotice').style.display = 'none';
}

if (!localStorage.getItem('cookiesAccepted')) {
    document.getElementById('cookieNotice').style.display = 'block';
}
