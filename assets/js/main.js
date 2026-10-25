// spaice studio: menu na telefonu, kopírování adresy a příprava e-mailu z formuláře.
(function () {
  var toggle = document.querySelector('[data-menu-toggle]');
  var menu = document.querySelector('[data-menu]');
  if (toggle && menu) {
    var set = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Zavřít' : 'Menu';
      menu.hidden = !open;
      document.documentElement.classList.toggle('menu-open', open);
      if (open) menu.querySelector('a').focus();
    };
    toggle.addEventListener('click', function () { set(menu.hidden); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !menu.hidden) { set(false); toggle.focus(); }
    });
    matchMedia('(min-width: 900px)').addEventListener('change', function (e) { if (e.matches && !menu.hidden) set(false); });
  }

  var copy = document.querySelector('[data-copy]');
  var copied = document.querySelector('[data-copy-status]');
  if (copy && copied) {
    copy.addEventListener('click', function () {
      var text = copy.getAttribute('data-copy');
      var done = function (ok) {
        copied.textContent = ok ? 'Adresa je ve schránce.' : 'Zkopírujte prosím adresu ručně.';
        clearTimeout(copy._t);
        copy._t = setTimeout(function () { copied.textContent = ''; }, 4000);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      } else {
        done(false);
      }
    });
  }

  // Scéna v úvodu: na počítači se střídají záznamy klientských webů, telefon listuje obrazovkami MojeTripy.
  // Na telefonu se video nenačítá, zůstává plakát. Při omezeném pohybu stojí všechno.
  var stage = document.querySelector('[data-stage]');
  if (stage) {
    var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    var wide = matchMedia('(min-width: 900px)').matches;
    var video = stage.querySelector('video');
    var shots = stage.querySelectorAll('.stage__phone img');
    var nameEl = stage.querySelector('[data-stage-name]');
    var pause = stage.querySelector('[data-stage-pause]');
    var srcs = video.getAttribute('data-videos').split('|');
    var posters = video.getAttribute('data-posters').split('|');
    var names = video.getAttribute('data-names').split('|');
    var cur = 0, shot = 0, timer = null, held = false, seen = false;

    if (still) {
      document.documentElement.classList.add('no-motion');
    } else {
      var show = function (i) {
        cur = i;
        video.poster = posters[i];
        nameEl.textContent = names[i];
        if (wide) { video.src = srcs[i]; video.load(); }
      };
      var run = function () {
        if (held || !seen) return;
        if (wide && video.src) video.play().catch(function () {});
        if (!timer) timer = setInterval(function () {
          shots[shot].classList.remove('is-on');
          shot = (shot + 1) % shots.length;
          shots[shot].classList.add('is-on');
        }, 3200);
      };
      var stop = function () {
        video.pause();
        clearInterval(timer);
        timer = null;
      };
      video.addEventListener('ended', function () { show((cur + 1) % srcs.length); run(); });
      new IntersectionObserver(function (e) {
        seen = e[0].isIntersecting;
        if (seen && wide && !video.src) show(0);
        seen ? run() : stop();
      }, { threshold: 0.25 }).observe(stage);
      pause.addEventListener('click', function () {
        held = !held;
        pause.setAttribute('aria-pressed', String(held));
        pause.textContent = held ? 'Spustit ukázky' : 'Pozastavit ukázky';
        held ? stop() : run();
      });
    }
  }

  // Formulář nic neodesílá: poskládá zprávu a otevře ji v e-mailovém programu návštěvníka.
  var form = document.querySelector('[data-form]');
  if (!form) return;
  var status = form.querySelector('[data-form-status]');
  var co = form.elements.co;
  var email = form.elements.email;

  var flag = function (field, bad) {
    var err = document.getElementById(field.getAttribute('aria-describedby'));
    field.setAttribute('aria-invalid', String(bad));
    if (err) err.hidden = !bad;
  };
  co.addEventListener('input', function () { if (co.value.trim()) flag(co, false); });
  email.addEventListener('input', function () { if (email.validity.valid) flag(email, false); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var badCo = !co.value.trim();
    var badMail = !email.validity.valid;
    flag(co, badCo);
    flag(email, badMail);
    if (badCo || badMail) {
      status.textContent = '';
      (badMail && !badCo ? email : co).focus();
      return;
    }
    var name = form.elements.jmeno.value.trim();
    var termin = form.elements.termin.value.trim();
    var lines = ['Dobrý den,', '', co.value.trim()];
    if (termin) lines.push('', 'Termín a rozpočet: ' + termin);
    if (name || email.value.trim()) lines.push('');
    if (name) lines.push(name);
    if (email.value.trim()) lines.push(email.value.trim());
    var body = lines.join('\r\n').replace(/(\r\n)+$/, '');
    var subject = name ? 'Poptávka z webu: ' + name : 'Poptávka z webu';
    window.location.href = 'mailto:ahoj@spaicestudio.cz?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    status.textContent = 'Zpráva by se měla otevřít ve vašem e-mailovém programu. Pokud se neotevřela, napište nám na ahoj@spaicestudio.cz.';
  });
})();
