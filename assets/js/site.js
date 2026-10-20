(() => {
  const toggle = document.querySelector('.menu-toggle');
  const panel = document.querySelector('#mobile-panel');
  if (toggle && panel) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      panel.hidden = open;
      document.body.classList.toggle('menu-open', !open);
    });
  }

  document.querySelectorAll('[data-current-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  document.addEventListener('click', (event) => {
    document.querySelectorAll('.desktop-nav details[open]').forEach((detail) => {
      if (!detail.contains(event.target)) detail.removeAttribute('open');
    });
  });
})();