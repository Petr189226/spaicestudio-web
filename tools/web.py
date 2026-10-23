#!/usr/bin/env python3
"""Celý web spaicestudio.cz z jednoho místa: hlavní stránka, stránky projektů a 404.

Hlavička, menu aplikací a patička jsou na všech stránkách stejné. Texty odpovídají
bloku „ID: text“ z posouzení GPT (spaice-gpt-odpoved.md, kapitola 7), u ID je
poznamenáno, odkud text je.

    python3 tools/web.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://spaicestudio.cz'
IMG = '/assets/img/'
MAIL = 'ahoj@spaicestudio.cz'

# Projekty v pořadí na hlavní stránce: zakázka, vlastní aplikace, zakázka, vlastní aplikace
ORDER = ['gentlemens-garage', 'mojetripy', 'jj-barber-shop', 'cookpit']


def web(name, alt, sizes, eager=False, cls='shot'):
    """Snímek webu klienta: 1200 a 2400 px na šířku, poměr 16 : 10."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="{cls}"><img src="{IMG}web-{name}-1200.webp" '
            f'srcset="{IMG}web-{name}-1200.webp 1200w, {IMG}web-{name}-2400.webp 2400w" '
            f'sizes="{sizes}" width="2400" height="1500" alt="{alt}" {load} decoding="async"></div>')


def phone(src, alt, w=804, h=1748):
    return (f'<div class="phone"><div class="phone__screen"><img src="{IMG}{src}" alt="{alt}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"></div></div>')


# Obrazovky aplikací
MT_TRIP = phone('mt-trip-2610.webp', 'MojeTripy, přehled cesty Řím bez front: mapa se zastávkami, termín a příprava.')
MT_DAY = phone('mt-den-2610.webp', 'MojeTripy, první den v Římě: časová osa s Koloseem, obědem a přesuny pěšky.')
MT_MAP = phone('mt-mapa-2610.webp', 'MojeTripy, trasa dne na mapě Říma se čtyřmi zastávkami.')
MT_MONEY = phone('mt-penize-2610.webp', 'MojeTripy, peníze: cesta vyjde přibližně na 37 200 Kč za dvě osoby.')
CP_WEEK = phone('uv-tyden.webp', 'Cookpit, týden: večeře na pět dní, nákup za 583 Kč z rozpočtu 600 Kč a úspora z akcí.', 900, 1957)
CP_RECIPE = phone('uv-detail.webp', 'Cookpit, recept: špagety s míchanými vejci, cena za porci a suroviny v akci.', 900, 1957)
CP_TODAY = phone('uv-dnes.webp', 'Cookpit, dnes: tip na večeři s časem přípravy, cenou za porci a počtem porcí.', 900, 1957)

GG_HOME_ALT = 'Úvodní stránka webu Gentlemen’s Garage: tmavá fotografie vozu Porsche a tlačítko Objednat servis.'
GG_BOOK_ALT = 'Web Gentlemen’s Garage, rezervace: výběr služby, například pneuservis, autoservis, detailing a diagnostika.'
GG_PRICE_ALT = 'Web Gentlemen’s Garage, ceník: nadpis Obvyklé ceny, neobvyklá kvalita a fotografie dílny.'
JJ_HOME_ALT = 'Úvodní stránka webu J&amp;J Barber Shop: interiér barbershopu a nadpis Na Praze 10, Strašnice a Vršovice.'
JJ_PRICE_ALT = 'Web J&amp;J Barber Shop, ceník ve stylu účtenky: klasický střih 590 Kč, střih dlouhých vlasů a úprava vousů s rezervací pro obě pobočky.'

PROJECTS = {
    'gentlemens-garage': dict(
        name='Gentlemen’s Garage', title='Web s rezervacemi pro Gentlemen’s Garage',
        kind='Web pro klienta',                                                     # GG.META
        desc='Pro autoservis ve Všechromech u&nbsp;Strančic jsme vytvořili web s&nbsp;online rezervacemi a&nbsp;systém pro vedení zakázek v&nbsp;dílně.',  # GG.DESC
        extra='Dílna poblíž sjezdu z&nbsp;D1 opravuje i&nbsp;motorky <span class="nowrap">Harley-Davidson</span>. Na webu představujeme servis, pneuservis, detailing a&nbsp;výběrové vozy. Součástí je ceník a&nbsp;poradna.',  # GG.PAGE_EXTRA
        facts=['Web', 'Rezervace', 'CRM'],                                          # GG.FACTS
        out=('https://www.gentlemensgarage.cz/', 'gentlemensgarage.cz'),
        share_alt='Rezervace na webu Gentlemen’s Garage. Nápis: Gentlemen’s Garage, web s online rezervacemi a CRM.',
    ),
    'mojetripy': dict(
        name='MojeTripy', title='MojeTripy, plánovač cest pro iPhone',
        kind='Vlastní aplikace pro iPhone, v&nbsp;App Storu',                       # MT.META
        desc='Plán cesty den po dni se zastávkami na mapě a&nbsp;rozpočtem v&nbsp;korunách. Průvodce Manažer zná váš plán, poradí, kam na večeři, a&nbsp;navrhne změny programu.',  # MT.DESC
        extra='Plán, doklady, mapy dnů a&nbsp;počasí máte v&nbsp;telefonu i&nbsp;bez signálu.',  # MT.PAGE_EXTRA
        facts=['Hodnocení 5,0 v&nbsp;App Storu', '13&nbsp;jazyků', 'Přes 200&nbsp;destinací v&nbsp;katalogu'],  # MT.FACTS
        out=('https://apps.apple.com/cz/app/mojetripy/id6815389423', 'Stáhnout v&nbsp;App Storu'),  # MT.STORE
        share_alt='Obrazovky aplikace MojeTripy s plánem cesty do Říma. Nápis: MojeTripy, vlastní aplikace pro iPhone.',
    ),
    'jj-barber-shop': dict(
        name='J&amp;J Barber Shop', title='Web pro J&amp;J Barber Shop',
        kind='Web pro klienta',                                                     # JJ.META
        desc='Pro barbershop ve Vršovicích a&nbsp;Strašnicích jsme vytvořili web s&nbsp;rezervacemi pro každou pobočku, ceníkem ve stylu účtenky a&nbsp;dárkovými poukazy.',  # JJ.DESC
        extra='J&amp;J Barber Shop má čtrnáct lidí v&nbsp;týmu a&nbsp;pobočky ve Vršovické a&nbsp;Černokostelecké. Ceník ve stylu účtenky uvádí mytí, masáž hlavy a&nbsp;styling jako součást ceny střihu.',  # JJ.PAGE_EXTRA
        facts=['Web', 'Rezervace', 'Poukazy'],                                      # JJ.FACTS
        out=('https://www.jjbarbershop.cz/', 'jjbarbershop.cz'),
        share_alt='Ceník ve stylu účtenky na webu J&amp;J Barber Shop. Nápis: J&amp;J Barber Shop, web s rezervacemi pro dvě pobočky.',
    ),
    'cookpit': dict(
        name='Cookpit', title='Cookpit, večeře podle akcí v obchodech',
        kind='Vlastní aplikace pro iPhone, před vydáním v&nbsp;App Storu',         # CP.META
        desc='Naplánuje večeře na celý týden podle akcí v&nbsp;obchodech a&nbsp;toho, co máte doma.',  # CP.DESC
        extra='Cookpit hlídá zásoby ve spíži a&nbsp;jejich trvanlivost. Z&nbsp;plánu sestaví nákupní seznam, který sdílíte s&nbsp;domácností.',  # CP.PAGE_EXTRA
        facts=['467&nbsp;receptů', 'Akce z&nbsp;11&nbsp;obchodů včetně Lidlu, Kauflandu a&nbsp;Albertu'],  # CP.FACTS
        out=('https://cookpit.spaicestudio.cz/', 'cookpit.spaicestudio.cz'),
        share_alt='Obrazovky aplikace Cookpit s plánem večeří na týden. Nápis: Cookpit, vlastní aplikace pro iPhone.',
    ),
}

CP_SCREENS = [  # CP.S1 až CP.S3
    (CP_TODAY, 'Dnešní večeře', 'Tip na večeři s&nbsp;cenou za porci. Výběr vychází z&nbsp;akcí v&nbsp;obchodech a&nbsp;ze zásob doma.'),
    (CP_WEEK, 'Večeře na celý týden', 'U&nbsp;plánu večeří vidíte cenu nákupu a&nbsp;rozpočet. Cookpit spočítá také úsporu z&nbsp;akcí v&nbsp;obchodech.'),
    (CP_RECIPE, 'Recept a&nbsp;cena porce', 'U&nbsp;receptu vidíte cenu za porci. Při vaření vás Cookpit provede postupem krok za krokem a&nbsp;nabídne časovač.'),
]

MT_PANELS = [
    ('mt-panel-01.webp', '„Tvůj osobní průvodce“: Manažer zná plán cesty a navrhuje, kam zajít.'),
    ('mt-panel-02.webp', '„Změň plán. Jedním klepnutím.“ Manažer navrhne úpravu programu, uživatel ji potvrdí.'),
    ('mt-panel-03.webp', '„Tvůj plán. I bez signálu.“ Uložený plán, mapy dnů a počasí dostupné offline.'),
    ('mt-panel-04.webp', '„Začni hotovým plánem“: Budapešť na tři dny s mapou a rozpočtem cesty.'),
    ('mt-panel-05.webp', '„Více měst. Jedna cesta.“ Plán cesty rozdělený do etap se zastávkami na mapě.'),
    ('mt-panel-06.webp', '„Hotel podle tvých představ“: tipy na ubytování podle rozpočtu a čtvrti.'),
]

APPS = [  # APPS.MT, APPS.CP, APPS.JTP
    ('https://apps.apple.com/cz/app/mojetripy/id6815389423', True, 'app-mojetripy.webp', 'MojeTripy', 'Plán cesty den po dni', 'App Store'),
    ('https://cookpit.spaicestudio.cz/', False, 'app-cookpit.webp', 'Cookpit', 'Večeře na týden', 'Před vydáním'),
    ('https://jetopodvod.spaicestudio.cz/', False, 'app-jetopodvod.webp', 'Je to podvod?', 'Podezřelé zprávy a&nbsp;odkazy', 'Před vydáním'),
]
APP_PREVIEWS = [('mt-main-2610.webp', 804, 1748), ('uv-dnes.webp', 900, 1957), ('app-preview-jetopodvod.webp', 900, 1957)]

OUT = '<span class="arrow arrow--out" aria-hidden="true"></span>'


def out_link(href, label):
    return f'<a class="link" href="{href}" target="_blank" rel="noopener">{label}{OUT}</a>'


def app_rows(preview):
    rows = []
    for i, (href, ext, icon, name, desc, status) in enumerate(APPS):
        target = ' target="_blank" rel="noopener"' if ext else ''
        arrow = OUT if ext else ''
        prev = f' data-preview="{i}"' if preview else ''
        rows.append(f'''<li>
            <a class="app" href="{href}"{target}{prev}>
              <img class="app__icon" src="{IMG}{icon}" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">{name}</span>
              <span class="app__desc">{desc}</span>
              <span class="app__status">{status}{arrow}</span>
            </a>
          </li>''')
    return '\n          '.join(rows)


def header(home):
    """home: předpona odkazů na sekce hlavní stránky ('' na hlavní stránce, '/' jinde)."""
    logo_href = '#top' if home == '' else '/'
    previews = '\n            '.join(
        f'<img{" class=\"is-active\"" if i == 0 else ""} src="{IMG}{f}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'
        for i, (f, w, h) in enumerate(APP_PREVIEWS))
    return f'''  <a class="skip" href="#obsah">Přeskočit na obsah</a>

  <header class="nav" data-nav>
    <div class="nav__inner">
      <a class="logo" href="{logo_href}" aria-label="spaice studio, úvodní stránka">spa<span class="logo__i">ı</span>ce</a>
      <nav class="nav__links" aria-label="Hlavní navigace">
        <a href="{home}#prace">Práce</a>
        <button class="nav__apps" type="button" aria-expanded="false" aria-controls="aplikace" data-apps-toggle>Naše aplikace<span class="nav__plus" aria-hidden="true"></span></button>
        <a href="{home}#sluzby">Služby</a>
      </nav>
      <a class="btn btn--sm nav__cta" href="{home}#kontakt">Probrat projekt</a>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu" data-menu-toggle>Menu</button>
    </div>
    <div class="apps" id="aplikace" data-apps hidden>
      <div class="apps__inner wrap">
        <ul class="apps__list" aria-label="Naše aplikace">
          {app_rows(True)}
        </ul>
        <div class="apps__preview phone" aria-hidden="true">
          <div class="phone__screen">
            {previews}
          </div>
        </div>
      </div>
    </div>
  </header>

  <div class="menu" id="menu" data-menu hidden>
    <nav aria-label="Mobilní navigace">
      <a class="menu__link" href="{home}#prace">Práce</a>
      <a class="menu__link" href="{home}#sluzby">Služby</a>
      <div class="menu__apps">
        <p class="menu__label">Naše aplikace</p>
        <ul aria-label="Naše aplikace">
          {app_rows(False)}
        </ul>
      </div>
    </nav>
    <div class="menu__foot">
      <a class="btn btn--lg" href="{home}#kontakt">Probrat projekt</a>
      <a class="menu__mail" href="mailto:{MAIL}">{MAIL}</a>
    </div>
  </div>'''


def footer(home):
    return f'''  <footer class="footer">
    <div class="footer__inner wrap">
      <div class="footer__brand">
        <a class="logo logo--footer" href="{'#top' if home == '' else '/'}" aria-label="spaice studio, úvodní stránka">spa<span class="logo__i">ı</span>ce</a>
        <p class="footer__tag">Weby a&nbsp;mobilní aplikace. Praha.</p>
      </div>
      <nav class="footer__nav" aria-label="Patička">
        <a href="{home}#prace">Práce</a>
        <a href="{home}#sluzby">Služby</a>
        <a href="{home}#kontakt">Kontakt</a>
      </nav>
      <a class="footer__mail" href="mailto:{MAIL}">{MAIL}</a>
      <p class="footer__copy">©&nbsp;2026 spaice studio. Petr Chajda, IČO 23250607, Průběžná 1033/4, 100&nbsp;00 Praha&nbsp;10</p>
    </div>
  </footer>'''


def head(title, desc, url, share, share_alt, og_desc=None, robots=False, preload=''):
    canon = '<meta name="robots" content="noindex">' if robots else f'<link rel="canonical" href="{url}">'
    og = '' if robots else f'''
  <!-- Náhled při sdílení odkazu (iMessage, WhatsApp, Messenger, LinkedIn, Slack, X). Adresy musí být absolutní. -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="spaice studio">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc or desc}">
  <meta property="og:image" content="{SITE}{IMG}{share}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{share_alt}">
  <meta name="twitter:card" content="summary_large_image">'''
    return f'''<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  {canon}
  <meta name="theme-color" content="#0a0908">
  <meta name="apple-mobile-web-app-title" content="spaice">{og}
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/archivo-latin-ext.woff2" as="font" type="font/woff2" crossorigin>{preload}
  <link rel="stylesheet" href="/assets/css/style.css">
  <script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.spaiceReady)document.documentElement.classList.add('no-script-run')}},3000)</script>
  <script src="/assets/js/main.js" defer></script>
</head>
<body>
<!--email_off-->
'''


TAIL = '''
<!--/email_off-->
</body>
</html>
'''


def facts(items):
    return '<ul class="facts">' + ''.join(f'<li>{f}</li>' for f in items) + '</ul>'


def show(slug, page=False):
    """Ukázka práce. Každý projekt má jinou skladbu, na stránce projektu je větší."""
    if slug == 'gentlemens-garage':
        return f'''<figure class="show show--wide">
          {web('gg-rezervace', GG_BOOK_ALT, '(max-width: 900px) 100vw, 90vw')}
        </figure>'''
    if slug == 'mojetripy':
        phones = [MT_TRIP, MT_DAY, MT_MAP, MT_MONEY] if page else [MT_TRIP, MT_DAY]
        return f'''<div class="show show--panel{' show--four' if page else ''}">
          {''.join(phones)}
        </div>'''
    if slug == 'jj-barber-shop':
        if page:
            return f'''<figure class="show show--receipt">
          {web('jj-cenik', JJ_PRICE_ALT, '(max-width: 900px) 100vw, 90vw', cls='shot shot--tall')}
          <figcaption>Ceník</figcaption>
        </figure>'''
        return f'''<div class="show show--duo">
          {web('jj-cenik', JJ_PRICE_ALT, '(max-width: 900px) 100vw, 60vw', cls='shot shot--tall')}
          <figure class="show__side">
            {web('jj-home', JJ_HOME_ALT, '(max-width: 900px) 100vw, 30vw')}
          </figure>
        </div>'''
    if slug == 'cookpit':
        items = CP_SCREENS if page else CP_SCREENS[1:]
        return '<ul class="show show--screens">' + ''.join(
            f'<li class="screen-item">{p}<h3>{t}</h3><p>{x}</p></li>' for p, t, x in items) + '</ul>'
    raise KeyError(slug)


def work(slug):
    p = PROJECTS[slug]
    href, label = p['out']
    return f'''
      <article class="work work--{slug}" id="{slug}" aria-labelledby="{slug}-name">
        <header class="work__head wrap">
          <div class="work__title">
            <h2 class="work__name" id="{slug}-name">{p['name']}</h2>
            <p class="work__kind">{p['kind']}</p>
          </div>
          <div class="work__body">
            <p>{p['desc']}</p>
            {facts(p['facts'])}
            <div class="work__links">
              <a class="link" href="/prace/{slug}/">O&nbsp;projektu</a>
              {out_link(href, label)}
            </div>
          </div>
        </header>
        <div class="work__show wrap" data-reveal>
        {show(slug)}
        </div>
      </article>'''


SERVICES = [  # SV.*
    ('Weby', 'Navrhujeme a&nbsp;programujeme firemní weby, e-shopy a&nbsp;webové aplikace. Součástí může být redakční systém pro úpravy obsahu.',
     ['Firemní a&nbsp;prezentační weby', 'E-shopy', 'Webové aplikace podle zadání', 'Redakční systém pro úpravy obsahu']),
    ('Aplikace', 'Vyvíjíme aplikace pro iPhone a&nbsp;Android včetně přihlášení a&nbsp;plateb. Připravíme je ke schválení v&nbsp;obchodech. Vydáním v&nbsp;App Storu jsme prošli s&nbsp;vlastními MojeTripy.',
     ['Aplikace pro iPhone a&nbsp;Android', 'Účty a&nbsp;přihlášení', 'Platby a&nbsp;předplatné', 'Schvalování v&nbsp;App Storu a&nbsp;Google Play']),
    ('Správa webů', 'Po spuštění se staráme o&nbsp;aktualizace a&nbsp;zálohy webu. Hlídáme jeho dostupnost, zabezpečení a&nbsp;certifikáty. Zajišťujeme také hosting a&nbsp;domény.',
     ['Aktualizace a&nbsp;zálohy', 'Hlídání dostupnosti', 'Zabezpečení a&nbsp;certifikáty', 'Hosting a&nbsp;domény']),
]

JSONLD = '''
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "spaice studio",
      "url": "https://spaicestudio.cz/",
      "email": "ahoj@spaicestudio.cz",
      "logo": "https://spaicestudio.cz/apple-touch-icon.png",
      "founder": { "@type": "Person", "name": "Petr Chajda" },
      "address": { "@type": "PostalAddress", "addressLocality": "Praha", "addressCountry": "CZ" },
      "description": "Navrhujeme a vyvíjíme weby a aplikace pro iPhone i Android. O weby se staráme i po spuštění."
    }
  </script>'''


def contact(title_id='ct-title'):
    return f'''
    <section class="contact wrap" id="kontakt" aria-labelledby="{title_id}">
      <h2 class="headline" id="{title_id}">Napište nám o&nbsp;projektu</h2>
      <p class="contact__lead">Napište, co potřebujete. Pokud máte termín nebo rozpočet, připojte je.</p>
      <div class="contact__mail">
        <a class="contact__email" href="mailto:{MAIL}">{MAIL}</a>
        <button class="contact__copy link" type="button" data-copy="{MAIL}">Kopírovat adresu</button>
        <span class="contact__copied" role="status" data-copied></span>
      </div>
    </section>'''


def index():
    preload = (f'\n  <link rel="preload" as="image" href="{IMG}web-gg-home-1200.webp" '
               f'imagesrcset="{IMG}web-gg-home-1200.webp 1200w, {IMG}web-gg-home-2400.webp 2400w" imagesizes="(max-width: 900px) 100vw, 90vw" media="(min-width: 601px)">')
    h = head('spaice studio | Weby a mobilní aplikace',  # META.TITLE
             'Navrhujeme a vyvíjíme weby a aplikace pro iPhone i Android. O weby se staráme i po spuštění. spaice studio, Praha.',  # META.DESC
             f'{SITE}/', 'share.jpg',
             'Úvodní stránka webu Gentlemen’s Garage. Nápis: Navrhujeme a vyvíjíme weby a aplikace.',
             og_desc='Práce studia spaice: weby pro Gentlemen’s Garage a J&amp;J Barber Shop, vlastní aplikace MojeTripy a Cookpit.',  # META.SHARE
             preload=preload)
    h = h.replace('  <link rel="icon" href="/favicon.svg"', JSONLD.lstrip('\n') + '\n  <link rel="icon" href="/favicon.svg"', 1)
    services = '\n'.join(f'''        <article class="service">
          <h3 class="service__name">{n}</h3>
          <p class="service__text">{t}</p>
          <ul class="service__list">{''.join(f'<li>{i}</li>' for i in l)}</ul>
        </article>''' for n, t, l in SERVICES)
    body = f'''{header('')}

  <main id="obsah">
    <section class="hero wrap" id="top" aria-labelledby="hero-title" data-top>
      <div class="hero__text">
        <p class="hero__meta">spaice studio, Praha</p>
        <h1 class="hero__title" id="hero-title">Navrhujeme a&nbsp;vyvíjíme weby a&nbsp;aplikace.</h1>
      </div>
      <div class="hero__side">
        <p class="hero__lead">O&nbsp;weby se staráme i&nbsp;po spuštění. Naši aplikaci MojeTripy najdete v&nbsp;App Storu.</p>
        <div class="hero__actions">
          <a class="btn btn--lg" href="#kontakt">Probrat projekt</a>
          <a class="link" href="#prace">Práce</a>
        </div>
      </div>
      <figure class="hero__shot">
        <div class="shot"><picture>
          <source media="(max-width: 600px)" srcset="{IMG}web-gg-home-m.webp" width="900" height="1125">
          <img src="{IMG}web-gg-home-1200.webp" srcset="{IMG}web-gg-home-1200.webp 1200w, {IMG}web-gg-home-2400.webp 2400w" sizes="(max-width: 900px) 100vw, 90vw" width="2400" height="1500" alt="{GG_HOME_ALT}" fetchpriority="high" decoding="async">
        </picture></div>
        <figcaption>Gentlemen’s Garage: web s&nbsp;online rezervacemi</figcaption>
      </figure>
    </section>

    <section class="intro wrap" aria-label="O studiu">
      <p class="intro__text">Vedle klientských webů vyvíjíme vlastní aplikace. MojeTripy už jsou v&nbsp;App Storu, Cookpit připravujeme k&nbsp;vydání. Cestu do App Storu jsme si prošli sami.</p>
      <p class="intro__founder">Za spaice studio stojí Petr Chajda. Studio sídlí v&nbsp;Praze a&nbsp;vzniklo v&nbsp;roce 2026.</p>
    </section>

    <div class="works" id="prace">{''.join(work(s) for s in ORDER)}
    </div>

    <section class="services wrap" id="sluzby" aria-labelledby="sv-title">
      <h2 class="headline" id="sv-title">Co pro vás uděláme</h2>
      <div class="services__rows">
{services}
      </div>
    </section>
{contact()}
  </main>

{footer('')}'''
    return h + body + TAIL


def case(slug):
    p = PROJECTS[slug]
    nxt = ORDER[(ORDER.index(slug) + 1) % len(ORDER)]
    href, label = p['out']
    plain = p['desc'].replace('&nbsp;', ' ').replace('<span class="nowrap">', '').replace('</span>', '')
    h = head(f"{p['title']} | spaice studio", plain, f'{SITE}/prace/{slug}/', f'share-{slug}.jpg', p['share_alt'])
    more = ''
    if slug == 'gentlemens-garage':
        more = f'''
      <div class="case__more wrap">
        <figure>{web('gg-home', GG_HOME_ALT, '(max-width: 900px) 100vw, 45vw')}<figcaption>Úvodní stránka</figcaption></figure>
        <figure>{web('gg-cenik', GG_PRICE_ALT, '(max-width: 900px) 100vw, 45vw')}<figcaption>Ceník služeb</figcaption></figure>
      </div>'''
    elif slug == 'jj-barber-shop':
        more = f'''
      <div class="case__more case__more--single wrap">
        <figure>{web('jj-home', JJ_HOME_ALT, '(max-width: 900px) 100vw, 90vw')}<figcaption>Úvodní stránka</figcaption></figure>
      </div>'''
    elif slug == 'mojetripy':
        reel = ''.join(f'<li><img src="{IMG}{f}" width="760" height="1651" loading="lazy" decoding="async" alt="{a}"></li>' for f, a in MT_PANELS)
        more = f'''
      <div class="reel">
        <div class="reel__viewport">
          <ul class="reel__track" aria-label="Grafika aplikace MojeTripy z App Storu">{reel}</ul>
        </div>
      </div>'''
    body = f'''{header('/')}

  <main id="obsah">
    <article class="case" aria-labelledby="case-title">
      <header class="case__head wrap" data-top>
        <p class="case__kind">{p['kind']}</p>
        <h1 class="case__name" id="case-title">{p['name']}</h1>
        <div class="case__intro">
          <div class="case__text">
            <p class="case__lead">{p['desc']}</p>
            <p class="case__more-text">{p['extra']}</p>
          </div>
          <div class="case__side">
            {facts(p['facts'])}
            {out_link(href, label)}
          </div>
        </div>
      </header>
      <div class="case__show wrap">
        {show(slug, page=True)}
      </div>{more}
    </article>

    <nav class="next" aria-label="Další projekt">
      <a class="next__link wrap" href="/prace/{nxt}/">
        <span class="next__label">Další projekt</span>
        <span class="next__name">{PROJECTS[nxt]['name']}</span>
      </a>
    </nav>

    <section class="cta wrap" aria-labelledby="cta-title">
      <h2 class="headline" id="cta-title">Proberme vaše zadání</h2>
      <a class="btn btn--lg" href="/#kontakt">Probrat projekt</a>
    </section>
  </main>

{footer('/')}'''
    return h + body + TAIL


def not_found():
    h = head('Stránka nenalezena | spaice studio', 'Stránka nenalezena.', '', '', '', robots=True)
    body = f'''{header('/')}

  <main id="obsah">
    <header class="case__head wrap" data-top>
      <p class="case__kind">Chyba 404</p>
      <h1 class="case__name">Stránka nenalezena</h1>
      <p class="case__lead">Stránka neexistuje nebo se přesunula.</p>
      <a class="link" href="/">Zpět na úvod</a>
    </header>
  </main>

{footer('/')}'''
    return h + body + TAIL


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('ok', rel)


if __name__ == '__main__':
    write('index.html', index())
    for s in ORDER:
        write(f'prace/{s}/index.html', case(s))
    write('404.html', not_found())
