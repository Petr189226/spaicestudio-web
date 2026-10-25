# Web spaicestudio.cz: úvodní stránka, čtyři případové studie a stránka 404.
# Hlavička, menu a patička jsou na všech stránkách stejné, proto je skládá jeden skript:
#   python3 tools/web.py
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://spaicestudio.cz'
APPSTORE = 'https://apps.apple.com/cz/app/mojetripy/id6815389423'
GPLAY = 'https://play.google.com/store/apps/details?id=cz.mojetripy.app'
MAIL = 'ahoj@spaicestudio.cz'

# Logo „Kurzor“ z tools/logo.py: písmena berou barvu textu, kurzor je vždy oranžový
_L = json.load(open(os.path.join(ROOT, 'tools', 'logo.json'), encoding='utf-8'))
LOGO = ('<svg class="logo__svg" viewBox="{}" aria-hidden="true" focusable="false">'
        '<path d="{}" fill="currentColor"/><rect x="{}" y="{}" width="{}" height="{}" fill="#c66a3d"/></svg>'
        ).format(' '.join('%g' % v for v in _L['box']), _L['d'], *('%g' % v for v in _L['bar']))


def plain(html):
    return re.sub(r'<[^>]+>', '', html).replace('&nbsp;', ' ').replace('&amp;', '&')


def head(title, desc, path, share, r, a):
    return f'''<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{SITE}{path}">
  <meta name="theme-color" content="#111210">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="spaice studio">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE}/assets/img/{share}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{a}assets/logo/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{a}assets/logo/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="{a}assets/logo/apple-touch-icon.png">
  <link rel="preload" href="{a}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{a}assets/fonts/archivo-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{a}assets/css/style.css">
  <script src="{a}assets/js/main.js" defer></script>
</head>
<body>
<!--email_off-->
  <a class="skip" href="#obsah">Přeskočit na obsah</a>

  <header class="nav">
    <div class="nav__inner frame">
      <a class="logo" href="{r or './'}" aria-label="spaice studio, úvodní stránka">{LOGO}</a>
      <nav class="nav__links" aria-label="Hlavní navigace">
        <a href="{r}#prace">Práce</a>
        <a href="{r}#aplikace">Aplikace</a>
        <a href="{r}#sluzby">Služby</a>
        <a href="{r}#studio">Studio</a>
      </nav>
      <a class="btn btn--line nav__cta" href="{r}#kontakt">Probrat projekt</a>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu" data-menu-toggle>Menu</button>
    </div>
  </header>

  <div class="menu" id="menu" data-menu hidden>
    <nav class="menu__links frame" aria-label="Mobilní navigace">
      <a href="{r}#prace">Práce</a>
      <a href="{r}#aplikace">Aplikace</a>
      <a href="{r}#sluzby">Služby</a>
      <a href="{r}#studio">Studio</a>
      <a href="{r}#kontakt">Kontakt</a>
    </nav>
    <p class="menu__mail frame"><a href="mailto:{MAIL}">{MAIL}</a></p>
  </div>
'''


def foot(r):
    return f'''
  <footer class="footer">
    <div class="footer__inner frame grid">
      <a class="logo footer__logo" href="{r or './'}" aria-label="spaice studio, úvodní stránka">{LOGO}</a>
      <div class="footer__about">
        <p>Design a&nbsp;vývoj webů a&nbsp;aplikací. Praha.</p>
        <a class="footer__mail" href="mailto:{MAIL}">{MAIL}</a>
      </div>
      <nav class="footer__nav" aria-label="Patička">
        <a href="{r}#prace">Práce</a>
        <a href="{r}#aplikace">Aplikace</a>
        <a href="{r}#sluzby">Služby</a>
        <a href="{r}#studio">Studio</a>
        <a href="{r}#kontakt">Kontakt</a>
        <a href="{r}prace/mojetripy/">MojeTripy</a>
        <a href="{r}prace/cookpit/">Cookpit</a>
        <a href="https://jetopodvod.spaicestudio.cz/">Je to podvod?</a>
      </nav>
      <p class="footer__legal">©&nbsp;2026 spaice studio. IČO 23250607</p>
    </div>
  </footer>
<!--/email_off-->
</body>
</html>
'''


def img(src, w, h, alt='', sizes='100vw', srcset=None, lazy=True, cls=''):
    s = f' srcset="{srcset}" sizes="{sizes}"' if srcset else ''
    l = ' loading="lazy"' if lazy else ''
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}"{s} alt="{alt}" width="{w}" height="{h}"{l} decoding="async">'


# Úvodní stránka

def home():
    r, a = '', ''
    A = N = 'assets/img/'
    V = 'assets/video/'
    gg_home = img(N + 'gg-home-1600.webp', 2400, 1340, 'Úvodní stránka webu Gentlemen’s Garage: autoservis a&nbsp;Harley-Davidson servis u&nbsp;Prahy',
                  '(min-width: 900px) 66vw, 100vw', f'{N}gg-home-1000.webp 1000w, {N}gg-home-1600.webp 1600w, {N}gg-home-2400.webp 2400w')
    mt_screens = ['mt-main-2610.webp', 'mt-trip-2610.webp', 'mt-den-2610.webp', 'mt-mapa-2610.webp', 'mt-penize-2610.webp']
    phone = '\n'.join(
        f'''              <img{' class="is-on"' if i == 0 else ''} src="{A}{s}" alt="" width="804" height="1748"{'' if i == 0 else ' loading="lazy"'} decoding="async">'''
        for i, s in enumerate(mt_screens))
    flag = '\n'.join(f'''            <figure>
              {img(A + s, 804, 1748, '', '(min-width: 900px) 16vw, 30vw', cls='phone-shot')}
              <figcaption>{c}</figcaption>
            </figure>''' for s, c in [('mt-trip-2610.webp', 'Plán cesty'), ('mt-mapa-2610.webp', 'Mapa dne'), ('mt-penize-2610.webp', 'Rozpočet')])
    body = f'''
  <main id="obsah">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__inner frame grid">
        <div class="hero__text">
          <p class="hero__label">spaice studio · Praha</p>
          <h1 class="hero__title" id="hero-title">
            <span class="hero__line">Od první skici</span>
            <span class="hero__line">po další verzi.</span>
          </h1>
          <p class="hero__lead">Navrhujeme a&nbsp;vyvíjíme weby a&nbsp;aplikace. Pro&nbsp;vaše zákazníky i&nbsp;každodenní práci.</p>
          <div class="hero__actions">
            <a class="btn btn--solid" href="#kontakt">Probrat projekt</a>
            <a class="hero__more" href="#prace">Vybraná práce <span aria-hidden="true">↓</span></a>
          </div>
        </div>

        <figure class="stage" data-stage aria-label="Ukázky práce: záznam webu klienta a&nbsp;obrazovky aplikace MojeTripy">
          <div class="stage__visual">
          <div class="stage__web">
            <video muted playsinline preload="none" poster="{V}jj-poster-2410.webp" width="1600" height="1000"
                   data-videos="{V}jj-2410.mp4|{V}gg-2410.mp4" data-posters="{V}jj-poster-2410.webp|{V}gg-poster-2410.webp" data-names="J&amp;J Barber Shop|Gentlemen’s Garage"></video>
          </div>
          <div class="stage__phone" aria-hidden="true">
{phone}
          </div>
          </div>
          <figcaption class="stage__cap">
            <span><span class="stage__name" data-stage-name>J&amp;J Barber Shop</span>: web · MojeTripy: aplikace</span>
            <button class="stage__pause" type="button" data-stage-pause aria-pressed="false">Pozastavit ukázky</button>
          </figcaption>
        </figure>
      </div>
    </section>

    <section class="paper" id="prace" aria-labelledby="prace-title">
      <div class="work frame grid">
        <h2 class="section-title" id="prace-title">Z&nbsp;naší práce.</h2>

        <article class="project project--gg" aria-labelledby="gg-title">
          <figure class="project__whole">{gg_home}</figure>
          <figure class="detail" aria-hidden="true">
            {img(N + 'gg-rezervace-detail-640.webp', 1110, 1515, '', '(min-width: 900px) 22vw, 70vw', f'{N}gg-rezervace-detail-640.webp 640w, {N}gg-rezervace-detail.webp 1110w')}
            <figcaption>Rezervace začíná výběrem služby.</figcaption>
          </figure>
          <div class="project__head">
            <p class="eyebrow">Gentlemen’s Garage</p>
            <h3 class="project__title" id="gg-title">Z&nbsp;webu až do dílny.</h3>
          </div>
          <div class="project__body">
            <p>Web s&nbsp;online rezervacemi a&nbsp;systém pro vedení zakázek autoservisu. Rozhraní pro zákazníky i&nbsp;pro každodenní práci v&nbsp;dílně.</p>
            <p class="project__scope">Web · Rezervace · Systém zakázek</p>
            <a class="more" href="prace/gentlemens-garage/">Prohlédnout projekt<span class="arrow" aria-hidden="true"></span></a>
          </div>
        </article>

        <article class="project project--jj" aria-labelledby="jj-title">
          <div class="project__head">
            <p class="eyebrow">J&amp;J Barber Shop</p>
            <h3 class="project__title" id="jj-title">Dvě pobočky. Jedna cesta k&nbsp;rezervaci.</h3>
            <p class="project__text">Web pro barbershop ve Vršovicích a&nbsp;Strašnicích. S&nbsp;rezervací pro každou pobočku, ceníkem ve stylu účtenky a&nbsp;dárkovými poukazy.</p>
            <p class="project__scope">Web · Rezervace · Poukazy</p>
            <a class="more" href="prace/jj-barber-shop/">Prohlédnout projekt<span class="arrow" aria-hidden="true"></span></a>
          </div>
          <figure class="project__whole">
            {img(N + 'web-jj-home-2400.webp', 2400, 1500, 'Úvodní stránka webu J&amp;J Barber Shop: Strašnice a&nbsp;Vršovice na Praze 10.', '(min-width: 900px) 45vw, 100vw')}
          </figure>
          <figure class="detail" aria-hidden="true">
            {img(N + 'jj-uctenka-600.webp', 900, 2025, '', '(min-width: 900px) 22vw, 70vw', f'{N}jj-uctenka-600.webp 600w, {N}jj-uctenka.webp 900w')}
            <figcaption>Ceník jako účtenka: všechno, co patří ke střihu, za 0&nbsp;Kč.</figcaption>
          </figure>
        </article>
      </div>
    </section>

    <section class="ink apps" id="aplikace" aria-labelledby="apps-title">
      <div class="apps__inner frame grid">
        <h2 class="section-title" id="apps-title">Vyvíjíme i&nbsp;vlastní aplikace.</h2>
        <p class="apps__intro">MojeTripy jsme dovedli až do App Storu a&nbsp;na Google Play. Cookpit a&nbsp;Je to podvod? připravujeme k&nbsp;vydání. Známe tak i&nbsp;rozhodování o&nbsp;tom, co má produkt umět dál.</p>

        <article class="flagship" aria-labelledby="mt-title">
          <div class="flagship__text">
            <div class="app-id">
              {img(N + 'app-mojetripy-m.webp', 512, 512, '', '56px', cls='app-icon')}
              <div>
                <h3 class="app-id__name" id="mt-title">MojeTripy</h3>
                <p class="app-id__status">Pro iPhone a&nbsp;Android · Hodnocení 5,0 v&nbsp;App Storu</p>
              </div>
            </div>
            <p class="flagship__claim">Celá cesta pohromadě.</p>
            <p class="flagship__desc">Plán cesty den po dni, zastávky na mapě a&nbsp;rozpočet na jednom místě. Průvodce Manažer zná váš plán, poradí, kam na večeři, a&nbsp;navrhne změny programu.</p>
            <ul class="flagship__facts" role="list">
              <li>Plán, mapy a&nbsp;počasí i&nbsp;bez signálu</li>
              <li>13&nbsp;jazyků</li>
              <li>Přes 200&nbsp;destinací v&nbsp;katalogu</li>
            </ul>
            <div class="flagship__actions">
              <a class="btn btn--solid btn--store" href="{APPSTORE}" target="_blank" rel="noopener">App Store<span class="arrow arrow--out" aria-hidden="true"></span></a>
              <a class="btn btn--line btn--store" href="{GPLAY}" target="_blank" rel="noopener">Google Play<span class="arrow arrow--out" aria-hidden="true"></span></a>
              <a class="more" href="prace/mojetripy/">Prohlédnout projekt<span class="arrow" aria-hidden="true"></span></a>
            </div>
          </div>
          <div class="flagship__screens">
{flag}
          </div>
        </article>

        <div class="apps__more">
          <article class="app-item" aria-labelledby="cookpit-title">
            {img(A + 'uv-dnes.webp', 900, 1957, '', '(min-width: 900px) 14vw, 40vw', cls='app-item__screen phone-shot')}
            <div class="app-item__text">
              <div class="app-id">
                {img(A + 'app-cookpit.webp', 256, 256, '', '48px', cls='app-icon')}
                <div>
                  <h3 class="app-id__name" id="cookpit-title">Cookpit</h3>
                  <p class="app-id__status">Připravujeme pro iPhone</p>
                </div>
              </div>
              <p class="app-item__claim">Co bude k&nbsp;večeři příští týden?</p>
              <p class="app-item__desc">Aplikace, která plánuje večeře podle akcí v&nbsp;obchodech a&nbsp;toho, co máte doma.</p>
              <a class="more" href="prace/cookpit/">O&nbsp;projektu<span class="arrow" aria-hidden="true"></span></a>
            </div>
          </article>

          <article class="app-item" aria-labelledby="jtp-title">
            {img(A + 'app-preview-jetopodvod.webp', 900, 1957, '', '(min-width: 900px) 14vw, 40vw', cls='app-item__screen phone-shot')}
            <div class="app-item__text">
              <div class="app-id">
                {img(A + 'app-jetopodvod.webp', 256, 256, '', '48px', cls='app-icon')}
                <div>
                  <h3 class="app-id__name" id="jtp-title">Je to podvod?</h3>
                  <p class="app-id__status">Připravujeme pro iPhone</p>
                </div>
              </div>
              <p class="app-item__claim">Prověřte zprávu dřív, než kliknete.</p>
              <p class="app-item__desc">Pošlete podezřelou SMS, e-mail, odkaz, číslo nebo účet. Aplikace řekne, co je na nich podezřelé a&nbsp;co máte udělat teď.</p>
              <a class="more" href="https://jetopodvod.spaicestudio.cz/" target="_blank" rel="noopener">jetopodvod.spaicestudio.cz<span class="arrow arrow--out" aria-hidden="true"></span></a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="paper" id="sluzby" aria-labelledby="sluzby-title">
      <div class="services frame grid">
        <h2 class="section-title" id="sluzby-title">Co pro vás můžeme postavit.</h2>
        <ul class="rows" role="list">
          <li class="row">
            <h3 class="row__name">Weby a&nbsp;webové aplikace</h3>
            <p class="row__text">Firemní web, e-shop nebo nástroj pro každodenní práci. Navrhneme rozhraní, zajistíme vývoj a&nbsp;podle potřeby přidáme správu obsahu.</p>
          </li>
          <li class="row">
            <h3 class="row__name">Mobilní aplikace</h3>
            <p class="row__text">Aplikace pro iPhone a&nbsp;Android. Od návrhu obrazovek přes účty a&nbsp;platby až po přípravu k&nbsp;vydání v&nbsp;obchodech.</p>
          </li>
          <li class="row">
            <h3 class="row__name">Správa a&nbsp;další rozvoj</h3>
            <p class="row__text">Aktualizace, zálohy, hosting a&nbsp;domény. Po spuštění se staráme o&nbsp;provoz webu a&nbsp;navazujeme dalším vývojem.</p>
          </li>
        </ul>
      </div>
    </section>

    <section class="ink" id="studio" aria-labelledby="studio-title">
      <div class="ink__inner frame grid">
        <div class="studio">
        <h2 class="section-title" id="studio-title">Studio z&nbsp;Prahy.</h2>
        <p class="studio__text">Studio vzniklo v&nbsp;Praze v&nbsp;roce 2026. Vedle klientských webů a&nbsp;aplikací tu vznikají i&nbsp;vlastní produkty: MojeTripy, Cookpit a&nbsp;Je to podvod?</p>
        </div>

        <div class="contact" id="kontakt">
        <h2 class="section-title contact__title">Pojďme probrat váš projekt.</h2>
        <p class="contact__lead">Napište, pro koho projekt je a&nbsp;co má umět. Pokud znáte termín nebo rozpočet, přidejte je.</p>
        <div class="contact__mail">
          <a class="contact__address" href="mailto:{MAIL}">{MAIL}</a>
          <button class="contact__copy" type="button" data-copy="{MAIL}">Zkopírovat adresu</button>
          <span class="contact__copied" role="status" data-copy-status></span>
        </div>

        <form class="form" data-form novalidate>
          <div class="form__fields">
            <div class="field">
              <label for="f-jmeno">Jméno <span class="field__opt">(nepovinné)</span></label>
              <input id="f-jmeno" name="jmeno" type="text" autocomplete="name">
            </div>
            <div class="field">
              <label for="f-email">E-mail pro odpověď <span class="field__opt">(nepovinné)</span></label>
              <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" aria-describedby="f-email-err">
              <p class="field__err" id="f-email-err" hidden>Zkontrolujte prosím e-mailovou adresu.</p>
            </div>
            <div class="field field--wide">
              <label for="f-co">Co chcete vytvořit?</label>
              <textarea id="f-co" name="co" rows="5" required aria-describedby="f-co-err"></textarea>
              <p class="field__err" id="f-co-err" hidden>Napište prosím, co chcete vytvořit.</p>
            </div>
            <div class="field field--wide">
              <label for="f-termin">Termín a&nbsp;rozpočet <span class="field__opt">(nepovinné)</span></label>
              <input id="f-termin" name="termin" type="text">
            </div>
            <div class="form__send">
              <button class="btn btn--solid" type="submit">Připravit e-mail</button>
            </div>
            <p class="form__status" role="status" data-form-status></p>
          </div>
          <p class="form__note">Otevře se váš e-mailový program. Zprávu odešlete až v&nbsp;něm.</p>
        </form>
        </div>
      </div>
    </section>
  </main>
'''
    title = 'spaice studio | Design a vývoj webů a aplikací'
    desc = 'Pražské studio pro návrh a vývoj webů, mobilních aplikací a zakázkových systémů. Od prvního návrhu přes spuštění po další rozvoj.'
    return head(title, desc, '/', 'share-2510.jpg', r, a) + body + foot(r)


# Případové studie

def facts_html(facts):
    out = []
    for k, v in facts:
        out.append(f'          <div><dt>{k}</dt><dd>{v}</dd></div>')
    return '\n'.join(out)


def ext(href, label):
    return f'<a class="more" href="{href}" target="_blank" rel="noopener">{label}<span class="arrow arrow--out" aria-hidden="true"></span></a>'


CASES = [
    {
        'slug': 'gentlemens-garage', 'name': 'Gentlemen’s Garage', 'kind': 'Web pro klienta',
        'title': 'Gentlemen’s Garage: web s rezervacemi a systém zakázek',
        'claim': 'Z&nbsp;webu až do dílny.',
        'lead': 'Web s&nbsp;online rezervacemi a&nbsp;systém pro vedení zakázek autoservisu ve Všechromech u&nbsp;Strančic.',
        'facts': [('Klient', 'Autoservis a&nbsp;Harley-Davidson servis u&nbsp;Prahy'),
                  ('Rozsah', 'Web · Rezervace · Systém zakázek'),
                  ('Web', ext('https://www.gentlemensgarage.cz/', 'gentlemensgarage.cz'))],
        'main': ('whole', 'gg-home', 2400, 1340, 'Úvodní stránka webu Gentlemen’s Garage s&nbsp;vínovým Porsche a&nbsp;nabídkou služeb.'),
        'story': ('Jeden celek pro zákazníky i&nbsp;dílnu.',
                  ['Dílna u&nbsp;sjezdu 15 z&nbsp;D1 opravuje auta i&nbsp;motorky <span class="nowrap">Harley-Davidson</span>. Na webu představujeme servis, pneuservis, detailing a&nbsp;výběrové vozy. Součástí je ceník a&nbsp;poradna.',
                   'Zákazník si na webu vybere službu a&nbsp;termín. Pro každodenní práci v&nbsp;dílně jsme připravili systém, ve kterém se vedou zakázky.']),
        'details': [
            ('web-gg-rezervace-2400.webp', 2400, 1500, 'Rezervace na webu Gentlemen’s Garage: výběr služby s&nbsp;orientační délkou.',
             'Rezervace začíná službou', 'Každá služba ukazuje orientační délku. Zákazník ji pak upřesní a&nbsp;zvolí termín. Vedle aut nabízí rezervace i&nbsp;služby pro motorky z&nbsp;Kubajz Garage.'),
            ('web-gg-cenik-2400.webp', 2400, 1500, 'Stránka Ceník služeb na webu Gentlemen’s Garage.',
             'Ceník bez vyptávání', 'Pneuservis a&nbsp;péče o&nbsp;vůz mají pevné ceny, autoservis se počítá podle vozu. Ceník to říká hned v&nbsp;úvodu.'),
            ('web-gg-home-m.webp', 900, 1125, 'Úvodní stránka Gentlemen’s Garage na telefonu s&nbsp;tlačítkem Rezervovat termín.',
             'Rezervace po ruce i&nbsp;na telefonu', 'Na mobilu zůstává tlačítko Rezervovat termín v&nbsp;horní liště.'),
        ],
        'link': ('https://www.gentlemensgarage.cz/', 'Navštívit gentlemensgarage.cz'),
        'share': 'share-gentlemens-garage-2510.jpg',
    },
    {
        'slug': 'mojetripy', 'name': 'MojeTripy', 'kind': 'Vlastní aplikace pro iPhone a&nbsp;Android',
        'title': 'MojeTripy: plánovač cest pro iPhone a Android',
        'claim': 'Celá cesta pohromadě.',
        'lead': 'Plán cesty den po dni, zastávky na mapě a&nbsp;rozpočet na jednom místě. Naše vlastní aplikace pro iPhone a&nbsp;Android.',
        'facts': [('Stav', 'Dostupné pro iPhone a&nbsp;Android'),
                  ('Rozsah', 'Vlastní produkt · Mobilní aplikace'),
                  ('App Store', ext(APPSTORE, 'Hodnocení 5,0')),
                  ('Google Play', ext(GPLAY, 'MojeTripy pro Android'))],
        'main': ('screens', [('mt-trip-2610.webp', 'Plán', 'Přehled cesty Řím bez front: dny, příprava a&nbsp;doklady.'),
                             ('mt-mapa-2610.webp', 'Mapa', 'Zastávky dne na mapě s&nbsp;časy a&nbsp;přesuny.'),
                             ('mt-penize-2610.webp', 'Rozpočet', 'Odhad nákladů cesty v&nbsp;korunách pro dvě osoby.')]),
        'story': ('Plán, mapa a&nbsp;rozpočet na sebe navazují.',
                  ['Plán cesty den po dni se zastávkami na mapě a&nbsp;rozpočtem v&nbsp;korunách. Průvodce Manažer zná váš plán, poradí, kam na večeři, a&nbsp;navrhne změny programu.',
                   'Plán, doklady, mapy dnů a&nbsp;počasí máte v&nbsp;telefonu i&nbsp;bez signálu. Aplikace mluví 13&nbsp;jazyky a&nbsp;v&nbsp;katalogu má přes 200&nbsp;destinací.']),
        'details': [
            ('../assets/img/mt-den-2610.webp', 804, 1748, 'Den v&nbsp;aplikaci MojeTripy: přílet, přesuny a&nbsp;zastávky po hodinách.',
             'Den po hodinách', 'Přílet, přesuny i&nbsp;volná okna mezi zastávkami. Když prší, aplikace nabídne program pod střechou.'),
            ('../assets/img/mt-main-2610.webp', 804, 1748, 'Úvodní obrazovka MojeTripy s&nbsp;odpočtem do odletu a&nbsp;přípravou cesty.',
             'Příprava před odletem', 'Odpočet do odletu, neověřené doklady a&nbsp;přesuny bez lístku na jednom místě.'),
        ],
        'link': (APPSTORE, 'Stáhnout v&nbsp;App Storu'),
        'link2': (GPLAY, 'Stáhnout na Google Play'),
        'share': 'share-mojetripy-2510.jpg',
    },
    {
        'slug': 'jj-barber-shop', 'name': 'J&amp;J Barber Shop', 'kind': 'Web pro klienta',
        'title': 'J&amp;J Barber Shop: web s rezervacemi pro dvě pobočky',
        'claim': 'Dvě pobočky. Jedna cesta k&nbsp;rezervaci.',
        'lead': 'Web pro barbershop ve Vršovicích a&nbsp;Strašnicích. S&nbsp;rezervací pro každou pobočku, ceníkem ve stylu účtenky a&nbsp;dárkovými poukazy.',
        'facts': [('Klient', 'Barbershop na Praze 10'),
                  ('Rozsah', 'Web · Rezervace · Poukazy'),
                  ('Web', ext('https://www.jjbarbershop.cz/', 'jjbarbershop.cz'))],
        'main': ('whole', 'web-jj-home', 2400, 1500, 'Úvodní stránka webu J&amp;J Barber Shop: Strašnice a&nbsp;Vršovice na Praze 10.'),
        'story': ('Všechno v&nbsp;ceně, na obou pobočkách.',
                  ['J&amp;J Barber Shop má čtrnáct lidí v&nbsp;týmu a&nbsp;dvě pobočky: ve Vršovické a&nbsp;v&nbsp;Černokostelecké ulici.',
                   'Mytí, masáž hlavy i&nbsp;styling jsou vždycky v&nbsp;ceně střihu. Web to říká hned v&nbsp;úvodu a&nbsp;ceník to ukazuje položku po položce.']),
        'details': [
            ('jj-pobocky-2400.webp', 2400, 1500, 'Sekce Pobočky: Vršovice a&nbsp;Strašnice, každá s&nbsp;adresou, otevírací dobou a&nbsp;vlastní rezervací.',
             'Výběr pobočky', 'Každá pobočka má vlastní adresu, otevírací dobu a&nbsp;tlačítko rezervace. To vede rovnou do rezervačního systému vybrané pobočky.'),
            ('jj-uctenky-1600.webp', 1600, 2108, 'Ceník ve stylu účtenky: klasický střih za 590&nbsp;Kč a&nbsp;položky v&nbsp;ceně za 0&nbsp;Kč.',
             'Ceník jako účtenka', 'Klasický střih za 590&nbsp;Kč a&nbsp;pod ním všechno, co je v&nbsp;ceně, každá položka za 0&nbsp;Kč. Doplatek 0&nbsp;Kč.'),
        ],
        'link': ('https://www.jjbarbershop.cz/', 'Navštívit jjbarbershop.cz'),
        'share': 'share-jj-barber-shop-2510.jpg',
    },
    {
        'slug': 'cookpit', 'name': 'Cookpit', 'kind': 'Vlastní aplikace pro iPhone, ve vývoji',
        'title': 'Cookpit: večeře podle akcí v obchodech',
        'claim': 'Co bude k&nbsp;večeři příští týden?',
        'lead': 'Aplikace, která plánuje večeře podle akcí v&nbsp;obchodech a&nbsp;toho, co máte doma.',
        'facts': [('Stav', 'Připravujeme pro iPhone. Zatím není v&nbsp;App Storu.'),
                  ('Rozsah', 'Vlastní produkt · Mobilní aplikace'),
                  ('Web', ext('https://cookpit.spaicestudio.cz/', 'cookpit.spaicestudio.cz'))],
        'main': ('screens', [('uv-dnes.webp', 'Dnešní večeře', 'Tip na večeři s&nbsp;cenou za porci. Výběr vychází z&nbsp;akcí v&nbsp;obchodech a&nbsp;ze zásob doma.'),
                             ('uv-tyden.webp', 'Večeře na celý týden', 'U&nbsp;plánu večeří vidíte cenu nákupu a&nbsp;rozpočet. Cookpit spočítá také úsporu z&nbsp;akcí.'),
                             ('uv-detail.webp', 'Recept a&nbsp;cena porce', 'Při vaření vás Cookpit provede postupem krok za krokem a&nbsp;nabídne časovač.')]),
        'story': ('Od letáku k&nbsp;talíři.',
                  ['Cookpit každý týden projde letáky vybraných obchodů a&nbsp;složí z&nbsp;nich večeře podle rozpočtu i&nbsp;času na vaření. Vybrat si můžete až tři obchody z&nbsp;jedenácti.',
                   'Suroviny z&nbsp;plánu se samy složí do nákupního seznamu, který sdílíte s&nbsp;domácností. Den předem aplikace připomene, co ve spíži končí.']),
        'details': [],
        'link': ('https://cookpit.spaicestudio.cz/', 'Navštívit cookpit.spaicestudio.cz'),
        'share': 'share-cookpit-2510.jpg',
    },
]


def case(i, c):
    r, a = '../../', '../../'
    A = N = a + 'assets/img/'
    nxt = CASES[(i + 1) % len(CASES)]
    kind = c['main'][0]
    if kind == 'whole':
        _, base, w, h, alt = c['main']
        if base == 'gg-home':
            main = img(N + 'gg-home-1600.webp', w, h, alt, '(min-width: 1680px) 1600px, 100vw',
                       f'{N}gg-home-1000.webp 1000w, {N}gg-home-1600.webp 1600w, {N}gg-home-2400.webp 2400w', lazy=False)
        else:
            main = img(N + base + '-2400.webp', w, h, alt, '(min-width: 1680px) 1600px, 100vw', lazy=False)
        main = f'''      <figure class="case__main frame">
        {main}
      </figure>'''
    else:
        items = []
        for k, (src, cap, text) in enumerate(c['main'][1]):
            w, h = (804, 1748) if src.startswith('mt') else (900, 1957)
            items.append(f'''          <figure class="case__screen">
            {img(A + src, w, h, '', '(min-width: 900px) 25vw, 80vw', lazy=k > 0)}
            <figcaption><strong>{cap}</strong> {text}</figcaption>
          </figure>''')
        main = f'''      <div class="case__screens frame grid">
{chr(10).join(items)}
      </div>'''

    details = []
    for src, w, h, alt, title, text in c['details']:
        path = (a + src[3:]) if src.startswith('../') else N + src
        tall = ' case__detail--phone' if h > 1.8 * w else (' case__detail--tall' if h > w else '')
        details.append(f'''        <figure class="case__detail{tall}">
          <div class="case__shot">{img(path, w, h, alt, '(min-width: 900px) 66vw, 100vw')}</div>
          <figcaption class="case__note"><strong>{title}</strong> {text}</figcaption>
        </figure>''')
    details_html = ''
    if details:
        details_html = f'''
      <div class="case__details frame grid">
{chr(10).join(details)}
      </div>'''

    s_title, s_paras = c['story']
    story = '\n'.join(f'          <p>{p}</p>' for p in s_paras)
    lhref, llabel = c['link']

    body = f'''
  <main id="obsah">
    <article aria-labelledby="case-title">
      <header class="case-hero">
        <div class="case-hero__inner frame grid">
          <p class="hero__label">{c['kind']}</p>
          <h1 class="case-hero__name" id="case-title">{c['name']}</h1>
          <p class="case-hero__claim">{c['claim']}</p>
          <p class="case-hero__lead">{c['lead']}</p>
          <dl class="case-hero__facts">
{facts_html(c['facts'])}
          </dl>
        </div>
      </header>

      <div class="paper case">
{main}

        <div class="case__story frame grid">
          <h2 class="case__story-title">{s_title}</h2>
          <div class="case__story-text">
{story}
            {ext(lhref, llabel)}{(chr(10) + ' ' * 12 + ext(*c['link2'])) if c.get('link2') else ''}
          </div>
        </div>
{details_html}
      </div>
    </article>

    <nav class="next" aria-label="Další projekt">
      <a class="next__link frame" href="../{nxt['slug']}/">
        <span class="eyebrow">Další projekt</span>
        <span class="next__name">{nxt['name']}<span class="arrow" aria-hidden="true"></span></span>
      </a>
    </nav>

    <section class="ink case-cta" aria-labelledby="cta-title">
      <div class="frame grid">
        <h2 class="section-title" id="cta-title">Pojďme probrat váš projekt.</h2>
        <div class="case-cta__actions">
          <a class="btn btn--solid" href="{r}#kontakt">Probrat projekt</a>
          <a class="hero__more" href="mailto:{MAIL}">{MAIL}</a>
        </div>
      </div>
    </section>
  </main>
'''
    title = f"{c['title']} | spaice studio"
    return head(title, plain(c['lead']), f"/prace/{c['slug']}/", c['share'], r, a) + body + foot(r)


def not_found():
    r = a = '/'
    body = f'''
  <main id="obsah">
    <header class="case-hero">
      <div class="case-hero__inner frame grid">
        <p class="hero__label">Chyba 404</p>
        <h1 class="case-hero__name">Stránka nenalezena.</h1>
        <p class="case-hero__lead">Stránka neexistuje nebo se přesunula.</p>
        <div class="case-hero__back"><a class="btn btn--solid" href="/">Zpět na úvod</a></div>
      </div>
    </header>
  </main>
'''
    html = head('Stránka nenalezena | spaice studio', 'Stránka neexistuje nebo se přesunula.', '/404.html', 'share-2510.jpg', r, a) + body + foot(r)
    return html.replace('<link rel="canonical" href="https://spaicestudio.cz/404.html">', '<meta name="robots" content="noindex">')


def write(rel, html):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print('ok', rel)


write('index.html', home())
write('404.html', not_found())
for i, c in enumerate(CASES):
    write(f"prace/{c['slug']}/index.html", case(i, c))
