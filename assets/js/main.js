(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* Navigace: podklad po odjetí z úvodu stránky */
  const nav = $('[data-nav]');
  const hero = $('.hero');
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

  /* Scény: fotka v pevných souřadnicích, na displeje se napasují skutečné screenshoty */

  // Homografie: obdélník screenshotu -> čtyři rohy displeje na fotce
  const solve = (A, b) => {
    const n = b.length;
    for (let i = 0; i < n; i++) {
      let p = i;
      for (let r = i + 1; r < n; r++) if (Math.abs(A[r][i]) > Math.abs(A[p][i])) p = r;
      [A[i], A[p]] = [A[p], A[i]];
      [b[i], b[p]] = [b[p], b[i]];
      for (let r = i + 1; r < n; r++) {
        const f = A[r][i] / A[i][i];
        for (let c = i; c < n; c++) A[r][c] -= f * A[i][c];
        b[r] -= f * b[i];
      }
    }
    const x = new Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) {
      let s = b[i];
      for (let c = i + 1; c < n; c++) s -= A[i][c] * x[c];
      x[i] = s / A[i][i];
    }
    return x;
  };
  const quadToCss = (w, h, quad) => {
    const src = [[0, 0], [w, 0], [w, h], [0, h]];
    const A = [];
    const b = [];
    src.forEach(([x, y], i) => {
      const [u, v] = quad[i];
      A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
      A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
    });
    const [a, bb, c, d, e, f, g, hh] = solve(A, b);
    return `matrix3d(${a},${d},0,${g},${bb},${e},0,${hh},0,0,1,0,${c},${f},0,1)`;
  };

  const setupStage = (stage) => {
    const W = Number(stage.dataset.w);
    const H = Number(stage.dataset.h);
    const box = stage.parentElement;
    const screens = $$('[data-quad]', stage);

    screens.forEach((screen) => {
      const quad = screen.dataset.quad.trim().split(/\s+/).map((pt) => pt.split(',').map(Number));
      const w = Number(screen.dataset.srcW);
      const h = Number(screen.dataset.srcH);
      screen.style.width = `${w}px`;
      screen.style.height = `${h}px`;
      screen.style.transform = quadToCss(w, h, quad);
    });

    // Scéna vyplní rám jako object-fit: cover, ohnisko drží zařízení v záběru
    const fit = () => {
      const bw = box.clientWidth;
      const bh = box.clientHeight;
      const s = Math.max(bw / W, bh / H);
      const fx = Number(getComputedStyle(stage).getPropertyValue('--focus-x')) || 0.5;
      const fy = Number(getComputedStyle(stage).getPropertyValue('--focus-y')) || 0.5;
      const x = Math.min(0, Math.max(bw - W * s, bw / 2 - fx * W * s));
      const y = Math.min(0, Math.max(bh - H * s, bh / 2 - fy * H * s));
      stage.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${s})`;
    };
    fit();
    new ResizeObserver(fit).observe(box);

    // Obrazovky se střídají, jen když je scéna vidět
    const count = Math.max(0, ...screens.map((screen) => $$('img', screen).length));
    const states = stage.closest('.hero') ? $$('[data-onscreen-state]', hero) : [];
    const toggle = stage.closest('.hero') ? $('[data-cycle-toggle]', hero) : null;
    const every = Number(stage.dataset.interval) || 5200;
    let index = 0;
    let timer = null;
    let visible = false;
    let paused = reducedMotion.matches;

    const show = (i) => {
      index = (i + count) % count;
      screens.forEach((screen) => $$('img', screen).forEach((img, k) => img.classList.toggle('is-active', k === index)));
      states.forEach((s, k) => { s.hidden = k !== index; });
    };
    const sync = () => {
      const run = count > 1 && visible && !paused && !document.hidden;
      if (run && !timer) timer = setInterval(() => show(index + 1), every);
      else if (!run && timer) { clearInterval(timer); timer = null; }
    };
    const label = () => {
      if (!toggle) return;
      toggle.classList.toggle('is-paused', paused);
      toggle.setAttribute('aria-label', paused ? 'Spustit střídání projektů' : 'Pozastavit střídání projektů');
    };

    show(0);
    label();
    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; sync(); }).observe(box);
    document.addEventListener('visibilitychange', sync);
    if (toggle) {
      toggle.addEventListener('click', () => {
        paused = !paused;
        if (!paused) show(index + 1);
        label();
        sync();
      });
    }
  };
  $$('[data-stage]').forEach(setupStage);

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

  /* Kontakt: poptávka jako věta */
  const form = $('[data-config]');
  if (form) {
    const done = $('[data-config-done]');
    const picks = $$('input[name="typ"]', form);
    const STUDIO_MAIL = 'ahoj@spaicestudio.cz';
    // Ve větě stojí služby ve čtvrtém pádu, v předmětu e-mailu v prvním
    const SUBJECT = { web: 'web', aplikaci: 'aplikace', 'správu webu': 'správa webu' };

    const values = () => {
      const data = new FormData(form);
      return {
        typ: data.getAll('typ'),
        jmeno: (data.get('jmeno') || '').trim(),
        email: (data.get('email') || '').trim(),
        zprava: (data.get('zprava') || '').trim(),
      };
    };

    const joinCz = (items) => items.length > 1 ? `${items.slice(0, -1).join(', ')} a ${items.at(-1)}` : (items[0] || '');

    const setError = (name, message) => {
      $(`[data-error="${name}"]`, form).textContent = message || '';
      const inputs = name === 'typ' ? picks : [form.elements[name]];
      inputs.forEach((input) => input.setAttribute('aria-invalid', message ? 'true' : 'false'));
    };

    const validate = (v) => {
      const errors = {};
      if (!v.jmeno) errors.jmeno = 'Napište, jak vám máme říkat.';
      if (!v.typ.length) errors.typ = 'Zaškrtněte web, aplikaci nebo správu webu.';
      if (!v.email) errors.email = 'Bez e-mailu se vám neozveme.';
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) errors.email = 'V e-mailu je asi překlep.';
      ['jmeno', 'typ', 'email'].forEach((k) => setError(k, errors[k]));
      return errors;
    };

    form.addEventListener('input', (e) => {
      if (e.target.getAttribute('aria-invalid') !== 'true') return;
      if (e.target.name === 'typ') { if (picks.some((p) => p.checked)) setError('typ', ''); }
      else setError(e.target.name, '');
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const v = values();
      const first = Object.keys(validate(v))[0];
      if (first) {
        (first === 'typ' ? picks[0] : form.elements[first]).focus();
        return;
      }
      const subject = `Poptávka: ${joinCz(v.typ.map((t) => SUBJECT[t] || t))}`;
      const body = [
        'Dobrý den,',
        '',
        `jmenuji se ${v.jmeno} a potřebuji ${joinCz(v.typ)}. Ozvěte se mi na ${v.email}.`,
        ...(v.zprava ? ['', v.zprava] : []),
        '',
        v.jmeno,
      ].join('\n');
      window.location.href = `mailto:${STUDIO_MAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      done.hidden = false;
    });
  }
})();
