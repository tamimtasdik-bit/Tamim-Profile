(() => {
  const toggle = document.querySelector('.mobile-toggle');
  const mobile = document.querySelector('#mobile-navigation');
  if (toggle && mobile) {
    toggle.addEventListener('click', () => {
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!isOpen));
      mobile.hidden = isOpen;
    });
  }
  document.addEventListener('click', event => {
    document.querySelectorAll('.nav-menu[open]').forEach(menu => {
      if (!menu.contains(event.target)) menu.removeAttribute('open');
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      document.querySelectorAll('.nav-menu[open]').forEach(menu => menu.removeAttribute('open'));
      if (toggle && mobile) { toggle.setAttribute('aria-expanded', 'false'); mobile.hidden = true; }
    }
  });
  document.querySelectorAll('[data-current-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();