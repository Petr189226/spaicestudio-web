(() => {
  window.spaiceReady = true;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* Navigace: podklad po odjetí z úvodu stránky */
  const nav = $('[data-nav]');
  const top = $('[data-top]');
  if (nav && top) {
    const sentinel = document.createElement('div');
    sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:72px;pointer-events:none';
    top.prepend(sentinel);
    new IntersectionObserver(([entry]) => {
      nav.classList.toggle('is-scrolled', !entry.isIntersecting);
    }).observe(sentinel);
  }

  /* Navigace: aktivní sekce */
  const sectionLinks = $$('.nav__links a[href^="#"]');
  const tracked = sectionLinks.map((a) => $(a.getAttribute('href'))).filter(Boolean);
  if (tracked.length) {
    // Zvýrazněná je jen sekce, která právě protíná střed okna
    const inView = new Set();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => (entry.isIntersecting ? inView.add(entry.target) : inView.delete(entry.target)));
      const current = tracked.find((s) => inView.has(s));
      sectionLinks.forEach((a) => {
        if (current && a.getAttribute('href') === `#${current.id}`) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    tracked.forEach((s) => io.observe(s));
  }

  /* Mobilní menu */
  const menu = $('[data-menu]');
  const menuToggle = $('[data-menu-toggle]');
  if (menu && menuToggle) {
    const setOpen = (open) => {
      menu.hidden = !open;
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.textContent = open ? 'Zavřít' : 'Menu';
      nav.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
      $$('main, footer, .skip').forEach((el) => { el.inert = open; });
      if (open) $('a', menu).focus();
    };
    menuToggle.addEventListener('click', () => setOpen(menu.hidden));
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menu.hidden) { setOpen(false); menuToggle.focus(); }
    });
    window.matchMedia('(min-width: 901px)').addEventListener('change', (e) => { if (e.matches) setOpen(false); });
  }

  /* Navigace: polička s našimi aplikacemi. Myší se otevře najetím, jinak klepnutím. */
  const apps = $('[data-apps]');
  const appsToggle = $('[data-apps-toggle]');
  if (nav && apps && appsToggle) {
    const hover = window.matchMedia('(hover: hover) and (pointer: fine)');
    const rows = $$('.app', apps);
    const shots = $$('.apps__preview img', apps);
    const after = appsToggle.nextElementSibling;
    let open = false;
    let openTimer = null;
    let closeTimer = null;
    let hiddenTimer = null;
    let openedAt = 0;
    let scrollStart = 0;

    const preview = (i) => {
      rows.forEach((r, k) => r.classList.toggle('is-current', k === i));
      shots.forEach((img, k) => img.classList.toggle('is-active', k === i));
    };
    const setApps = (next) => {
      clearTimeout(openTimer);
      clearTimeout(closeTimer);
      clearTimeout(hiddenTimer);
      if (next === open) return;
      open = next;
      appsToggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('has-apps', open);
      if (open) {
        preview(0);
        apps.hidden = false;
        openedAt = Date.now();
        scrollStart = window.scrollY;
        // Panel se vysune až po vykreslení, jinak by se přechod nespustil
        requestAnimationFrame(() => requestAnimationFrame(() => { if (open) apps.classList.add('is-open'); }));
      } else {
        apps.classList.remove('is-open');
        hiddenTimer = setTimeout(() => { if (!open) apps.hidden = true; }, reducedMotion.matches ? 0 : 450);
      }
    };

    appsToggle.addEventListener('click', () => {
      // Klepnutí hned po otevření najetím panel nechá otevřený
      if (open && Date.now() - openedAt < 500) return;
      setApps(!open);
    });
    appsToggle.addEventListener('pointerenter', () => {
      if (!hover.matches || open) return;
      openTimer = setTimeout(() => setApps(true), 120);
    });
    appsToggle.addEventListener('pointerleave', () => { if (!open) clearTimeout(openTimer); });
    nav.addEventListener('pointerenter', () => clearTimeout(closeTimer));
    nav.addEventListener('pointerleave', () => {
      if (hover.matches && open) closeTimer = setTimeout(() => setApps(false), 250);
    });
    rows.forEach((row, i) => {
      row.addEventListener('pointerenter', () => preview(i));
      row.addEventListener('focus', () => preview(i));
    });
    nav.addEventListener('focusout', (e) => { if (open && !nav.contains(e.relatedTarget)) setApps(false); });
    document.addEventListener('click', (e) => { if (open && !nav.contains(e.target)) setApps(false); });
    window.addEventListener('scroll', () => {
      if (open && Math.abs(window.scrollY - scrollStart) > 40) setApps(false);
    }, { passive: true });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && open) { setApps(false); appsToggle.focus(); }
    });
    // Polička leží v kódu až za navigací: Tab z tlačítka vede do ní, šipky mezi aplikacemi, z poslední zpět na Služby
    appsToggle.addEventListener('keydown', (e) => {
      if ((e.key === 'ArrowDown' || (e.key === 'Tab' && !e.shiftKey && open)) && rows.length) {
        e.preventDefault();
        setApps(true);
        rows[0].focus();
      }
    });
    apps.addEventListener('keydown', (e) => {
      const i = rows.indexOf(document.activeElement);
      if (i < 0) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); rows[Math.min(i + 1, rows.length - 1)].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); (i === 0 ? appsToggle : rows[i - 1]).focus(); }
      else if (e.key === 'Tab' && e.shiftKey && i === 0) { e.preventDefault(); appsToggle.focus(); }
      else if (e.key === 'Tab' && !e.shiftKey && i === rows.length - 1 && after) { e.preventDefault(); setApps(false); after.focus(); }
    });
  }

  /* Postupné odkrývání obsahu */
  const reveals = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }

  /* Kontakt: adresu jde zkopírovat jedním klepnutím, i když není nastavený e-mailový program */
  const copy = $('[data-copy]');
  const copied = $('[data-copied]');
  if (copy && copied) {
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(copy.dataset.copy);
        copied.textContent = 'Adresa je zkopírovaná.';
      } catch {
        const range = document.createRange();
        range.selectNodeContents($('.contact__email'));
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        copied.textContent = 'Adresa je označená, zkopírujte ji.';
      }
    });
  }
})();
