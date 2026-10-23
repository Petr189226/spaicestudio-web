# Stránky projektů /prace/<slug>/: vlastní adresa a vlastní náhled odkazu pro každý projekt.
# Hlavička a patička jsou stejné jako v index.html; po jejich změně skript pusť znovu: python3 tools/projekty.py
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://spaicestudio.cz'
A = '../../assets/img/'

def plain(html):
    return re.sub(r'<[^>]+>', '', html).replace('&nbsp;', ' ').replace('&amp;', '&')

def imgs(names, w, h, first_eager=True):
    out = []
    for i, n in enumerate(names):
        cls = ' class="is-active"' if i == 0 else ''
        lazy = '' if (i == 0 and first_eager) else ' loading="lazy"'
        out.append(f'<img{cls} src="{A}{n}" alt="" width="{w}" height="{h}"{lazy} decoding="async">')
    return ('\n' + ' ' * 18).join(out)

PROJECTS = [
    {
        'slug': 'mojetripy', 'name': 'MojeTripy', 'name_html': 'MojeTripy',
        'title': 'MojeTripy, plánovač cest pro iPhone',
        'more': 'Funguje i&nbsp;bez signálu: plán, doklady, mapy dnů a&nbsp;počasí máte v&nbsp;telefonu offline.',
        'kind': 'Vlastní aplikace pro iPhone, 2026',
        'body': 'Program den po dni, zastávky na mapě a&nbsp;rozpočet v&nbsp;korunách. Průvodce Manažer zná váš plán a&nbsp;poradí, kam na večeři nebo jak přeplánovat den.',
        'facts': ['Hodnocení 5,0 v&nbsp;App Storu', '13&nbsp;jazyků', 'Přes 200&nbsp;destinací v&nbsp;katalogu'],
        'link': ('https://apps.apple.com/cz/app/mojetripy/id6815389423', 'Stáhnout v&nbsp;App Storu'),
        'alt': 'Telefon s aplikací MojeTripy na zídce nad Lisabonem. Nápis: MojeTripy, vlastní aplikace pro iPhone, hodnocení 5,0 v App Storu.',
        'focus': '.7', 'focus_y': '.51', 'interval': '5200', 'scene': 'scene-mt',
        'screen': ('phone', '1792,420 2137,415 2099,1155 1734,1150', 804, 1748,
                   imgs(['screen-mt-main.webp', 'screen-mt-den.webp', 'screen-mt-mapa.webp', 'screen-mt-penize.webp'], 804, 1748)),
        'extra': 'reel',
    },
    {
        'slug': 'cookpit', 'name': 'Cookpit', 'name_html': 'Cookpit',
        'title': 'Cookpit, večeře podle akcí v obchodech',
        'more': 'Spíž hlídá, co máte doma a&nbsp;co brzy projde. Nákupní seznam se složí z&nbsp;plánu sám a&nbsp;sdílí se s&nbsp;celou domácností.',
        'kind': 'Vlastní aplikace pro iPhone, brzy v&nbsp;App Storu',
        'body': 'Naplánuje večeře na celý týden podle toho, co je v&nbsp;akci a&nbsp;co máte doma.',
        'facts': ['467&nbsp;receptů', 'Akce z&nbsp;Lidlu, Kauflandu, Albertu a&nbsp;osmi dalších obchodů'],
        'link': ('https://cookpit.spaicestudio.cz/', 'cookpit.spaicestudio.cz'),
        'alt': 'Telefon s aplikací Cookpit vedle talíře špaget v kuchyni. Nápis: Cookpit, vlastní aplikace pro iPhone, brzy v App Storu.',
        'focus': '.63', 'focus_y': '.58', 'interval': '5600', 'scene': 'scene-uv',
        'screen': ('phone', '1638,599.5 1917,597 1841,1184 1563,1166', 804, 1748,
                   imgs(['uv-dnes.webp', 'uv-tyden.webp', 'uv-detail.webp'], 900, 1957)),
        'extra': 'screens',
    },
    {
        'slug': 'gentlemens-garage', 'name': "Gentlemen's Garage", 'name_html': 'Gentlemen’s Garage',
        'title': "Web s rezervacemi pro Gentlemen's Garage",
        'more': 'Dílna sídlí ve Všechromech u&nbsp;Strančic, kousek od sjezdu z&nbsp;D1. Na webu najdete servis, pneuservis, detailing i&nbsp;výběrové vozy, ceník a&nbsp;poradnu. Termín si zákazník objedná přímo z&nbsp;webu.',
        'kind': 'Web pro klienta, 2026',
        'body': 'Autoservis u&nbsp;Prahy, který opravuje i&nbsp;motorky <span class="nowrap">Harley-Davidson</span>. Dostal od nás web s&nbsp;online rezervací termínů a&nbsp;systém, ve kterém dílna vede zakázky.',
        'facts': ['Web', 'Rezervace', 'CRM'],
        'link': ('https://www.gentlemensgarage.cz/', 'gentlemensgarage.cz'),
        'alt': "Notebook s webem Gentlemen's Garage v dílně vedle vínového Porsche. Nápis: Gentlemen's Garage, web s online rezervacemi a CRM.",
        'focus': '.26', 'focus_y': '.46', 'interval': '6400', 'scene': 'scene-gg',
        'screen': ('laptop', '350,468 1027,492 1075,915 380,960', 1440, 900,
                   imgs(['screen-gg.webp', 'screen-gg-2.webp'], 1440, 900)),
        'extra': ('shots', [('screen-gg.webp', "Úvodní stránka webu Gentlemen's Garage.", 'Úvodní stránka'),
                            ('screen-gg-2.webp', "Ceník služeb na webu Gentlemen's Garage.", 'Ceník služeb')]),
    },
    {
        'slug': 'jj-barber-shop', 'name': 'J&J Barber Shop', 'name_html': 'J&amp;J Barber Shop',
        'title': 'Web pro J&J Barber Shop',
        'more': 'Čtrnáct lidí v&nbsp;týmu a&nbsp;dvě pobočky, Vršovická a&nbsp;Černokostelecká. Ceník jsme pojali jako účtenku: mytí, masáž hlavy a&nbsp;styling jsou v&nbsp;ceně střihu.',
        'kind': 'Web pro klienta',
        'body': 'Barbershop ve Vršovicích a&nbsp;Strašnicích. Každá pobočka má na webu vlastní rezervace, k&nbsp;tomu ceník ve stylu účtenky a&nbsp;dárkové poukazy.',
        'facts': ['Web', 'Rezervace', 'Poukazy'],
        'link': ('https://www.jjbarbershop.cz/', 'jjbarbershop.cz'),
        'alt': 'Notebook s webem J&J Barber Shop v barbershopu. Nápis: J&J Barber Shop, web s rezervacemi pro dvě pobočky.',
        'focus': '.73', 'focus_y': '.57', 'interval': '6400', 'scene': 'scene-jj',
        'screen': ('laptop', '1587,565 2479,555 2448,1211 1523,1161', 1440, 900,
                   imgs(['screen-jj.webp', 'screen-jj-2.webp'], 1440, 900)),
        'extra': ('shots', [('screen-jj.webp', 'Úvodní stránka webu J&J Barber Shop.', 'Úvodní stránka'),
                            ('screen-jj-2.webp', 'Ceník na webu J&J Barber Shop.', 'Ceník')]),
    },
]

REEL = '''      <div class="reel" data-reel>
        <div class="reel__viewport">
          <ul class="reel__track" data-reel-track aria-label="Grafika aplikace MojeTripy z App Storu">
            <li><img src="{A}mt-panel-01.webp" width="760" height="1651" loading="lazy" decoding="async" alt="„Tvůj osobní průvodce“: Manažer zná plán cesty a navrhuje, kam zajít."></li>
            <li><img src="{A}mt-panel-02.webp" width="760" height="1651" loading="lazy" decoding="async" alt="„Změň plán. Jedním klepnutím.“ Manažer navrhne úpravu programu, uživatel ji potvrdí."></li>
            <li><img src="{A}mt-panel-03.webp" width="760" height="1651" loading="lazy" decoding="async" alt="„Tvůj plán. I bez signálu.“ Uložený plán, mapy dnů a počasí dostupné offline."></li>
            <li><img src="{A}mt-panel-04.webp" width="760" height="1651" loading="lazy" decoding="async" alt="„Začni hotovým plánem“: Budapešť na tři dny s mapou a rozpočtem cesty."></li>
            <li><img src="{A}mt-panel-05.webp" width="760" height="1651" loading="lazy" decoding="async" alt="„Více měst. Jedna cesta.“ Plán cesty rozdělený do etap se zastávkami na mapě."></li>
            <li><img src="{A}mt-panel-06.webp" width="760" height="1651" loading="lazy" decoding="async" alt="„Hotel podle tvých představ“: tipy na ubytování podle rozpočtu a čtvrti."></li>
          </ul>
        </div>
      </div>
'''.replace('{A}', A)

SCREENS = '''      <ul class="screens wrap" aria-label="Obrazovky aplikace Cookpit">
        <li class="screens__item" data-reveal>
          <div class="phone"><div class="phone__screen"><img src="{A}uv-dnes.webp" alt="Obrazovka Dnes: tip na večeři s časem přípravy, cenou za porci a počtem porcí." width="900" height="1957" loading="lazy" decoding="async"></div></div>
          <h2>Dnešní večeře</h2>
          <p>Jeden tip na večeři. Hned vidíte čas přípravy, cenu za porci i&nbsp;počet porcí.</p>
        </li>
        <li class="screens__item" data-reveal style="--d:.08s">
          <div class="phone"><div class="phone__screen"><img src="{A}uv-tyden.webp" alt="Obrazovka Týden: jídelníček, cena nákupu, rozpočet a úspora díky akcím." width="900" height="1957" loading="lazy" decoding="async"></div></div>
          <h2>Večeře na celý týden</h2>
          <p>Jídelníček na celý týden. Hned vidíte, kolik stojí nákup, jestli se vejdete do rozpočtu a&nbsp;kolik ušetříte na akcích.</p>
        </li>
        <li class="screens__item" data-reveal style="--d:.16s">
          <div class="phone"><div class="phone__screen"><img src="{A}uv-detail.webp" alt="Detail receptu: suroviny, cena za porci podle dnešních akcí a postup." width="900" height="1957" loading="lazy" decoding="async"></div></div>
          <h2>Recept krok za krokem</h2>
          <p>Cena za porci podle dnešních akcí, suroviny a&nbsp;postup. Při vaření máte na displeji jen jeden krok a&nbsp;u&nbsp;něj časovač.</p>
        </li>
      </ul>
'''.replace('{A}', A)

def shots(items):
    out = ['      <div class="shots wrap">']
    for i, (src, alt, cap) in enumerate(items):
        d = f' style="--d:.08s"' if i else ''
        out.append(f'''        <figure class="shots__item" data-reveal{d}>
          <img src="{A}{src}" alt="{alt.replace('&', '&amp;')}" width="1440" height="900" loading="lazy" decoding="async">
          <figcaption>{cap}</figcaption>
        </figure>''')
    out.append('      </div>\n')
    return '\n'.join(out)

PAGE = '''<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0a0908">
  <!-- Náhled při sdílení odkazu na tento projekt. Adresy musí být absolutní. -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="spaice studio">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{site}/assets/img/share-{slug}.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{alt}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../../favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="../../apple-touch-icon.png">
  <link rel="preload" href="../../assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../../assets/fonts/archivo-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="../../assets/css/style.css">
  <script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.spaiceReady)document.documentElement.classList.add('no-script-run')}},3000)</script>
  <script src="../../assets/js/main.js" defer></script>
</head>
<body>
<!--email_off-->
  <a class="skip" href="#obsah">Přeskočit na obsah</a>

  <header class="nav" data-nav>
    <div class="nav__inner">
      <a class="logo" href="../../" aria-label="spaice studio, úvodní stránka">spa<span class="logo__i">ı</span>ce</a>
      <nav class="nav__links" aria-label="Hlavní navigace">
        <a href="../../#prace" aria-current="true">Práce</a>
        <button class="nav__apps" type="button" aria-expanded="false" aria-controls="aplikace" data-apps-toggle>Naše aplikace<span class="nav__plus" aria-hidden="true"></span></button>
        <a href="../../#sluzby">Služby</a>
      </nav>
      <a class="btn btn--sm nav__cta" href="../../#kontakt">Probrat projekt<span class="arrow" aria-hidden="true"></span></a>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu" data-menu-toggle>Menu</button>
    </div>
    <div class="apps" id="aplikace" data-apps hidden>
      <div class="apps__inner wrap">
        <ul class="apps__list" aria-label="Naše aplikace">
          <li>
            <a class="app" href="https://apps.apple.com/cz/app/mojetripy/id6815389423" target="_blank" rel="noopener" data-preview="0">
              <img class="app__icon" src="../../assets/img/app-mojetripy.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">MojeTripy</span>
              <span class="app__desc">Plánovač cest den po dni</span>
              <span class="app__status">App Store<span class="arrow arrow--out" aria-hidden="true"></span></span>
            </a>
          </li>
          <li>
            <a class="app" href="https://cookpit.spaicestudio.cz/" data-preview="1">
              <img class="app__icon" src="../../assets/img/app-cookpit.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">Cookpit</span>
              <span class="app__desc">Večeře z&nbsp;akcí na celý týden</span>
              <span class="app__status">Brzy</span>
            </a>
          </li>
          <li>
            <a class="app" href="https://jetopodvod.spaicestudio.cz/" data-preview="2">
              <img class="app__icon" src="../../assets/img/app-jetopodvod.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">Je to podvod?</span>
              <span class="app__desc">Prověří zprávu dřív, než kliknete</span>
              <span class="app__status">Brzy</span>
            </a>
          </li>
        </ul>
        <div class="apps__preview phone" aria-hidden="true">
          <div class="phone__screen">
            <img class="is-active" src="../../assets/img/screen-mt-main.webp" alt="" width="804" height="1748" loading="lazy" decoding="async">
            <img src="../../assets/img/uv-dnes.webp" alt="" width="900" height="1957" loading="lazy" decoding="async">
            <img src="../../assets/img/app-preview-jetopodvod.webp" alt="" width="900" height="1957" loading="lazy" decoding="async">
          </div>
        </div>
      </div>
    </div>
  </header>

  <div class="menu" id="menu" data-menu hidden>
    <nav aria-label="Mobilní navigace">
      <a class="menu__link" href="../../#prace">Práce</a>
      <a class="menu__link" href="../../#sluzby">Služby</a>
      <div class="menu__apps">
        <p class="menu__label">Naše aplikace</p>
        <ul aria-label="Naše aplikace">
          <li>
            <a class="app" href="https://apps.apple.com/cz/app/mojetripy/id6815389423" target="_blank" rel="noopener">
              <img class="app__icon" src="../../assets/img/app-mojetripy.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">MojeTripy</span>
              <span class="app__desc">Plánovač cest den po dni</span>
              <span class="app__status">App Store<span class="arrow arrow--out" aria-hidden="true"></span></span>
            </a>
          </li>
          <li>
            <a class="app" href="https://cookpit.spaicestudio.cz/">
              <img class="app__icon" src="../../assets/img/app-cookpit.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">Cookpit</span>
              <span class="app__desc">Večeře z&nbsp;akcí na celý týden</span>
              <span class="app__status">Brzy</span>
            </a>
          </li>
          <li>
            <a class="app" href="https://jetopodvod.spaicestudio.cz/">
              <img class="app__icon" src="../../assets/img/app-jetopodvod.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
              <span class="app__name">Je to podvod?</span>
              <span class="app__desc">Prověří zprávu dřív, než kliknete</span>
              <span class="app__status">Brzy</span>
            </a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="menu__foot">
      <a class="btn btn--solid btn--lg" href="../../#kontakt">Probrat projekt<span class="arrow" aria-hidden="true"></span></a>
      <a class="menu__mail" href="mailto:ahoj@spaicestudio.cz">ahoj@spaicestudio.cz</a>
    </div>
  </div>

  <main id="obsah">
    <article class="case work--bleed" aria-labelledby="case-title">
      <header class="case__head wrap" data-top>
        <p class="case__kind">{kind}</p>
        <h1 class="case__name" id="case-title">{name_html}</h1>
      </header>

      <figure class="work__media" aria-hidden="true">
        <div class="work__frame" style="--focus-x:{focus};--focus-y:{focus_y}">
          <div class="work__zoom">
            <div class="stage" data-stage data-w="2752" data-h="1536" data-interval="{interval}">
              <img class="stage__bg" src="{A}{scene}-2048.webp" srcset="{A}{scene}-1200.webp 1200w, {A}{scene}-2048.webp 2048w, {A}{scene}-2752.webp 2752w" sizes="(max-width: 900px) 700px, 100vw" width="2752" height="1536" alt="" fetchpriority="high" decoding="async">
              <div class="screen screen--{stype}" data-quad="{quad}" data-src-w="{sw}" data-src-h="{sh}">
                  {simgs}
              </div>
            </div>
          </div>
        </div>
      </figure>

      <div class="case__body wrap">
        <div class="case__text" data-reveal>
          <p class="case__lead">{body}</p>
          <p class="case__more">{more}</p>
        </div>
        <div class="case__side" data-reveal style="--d:.08s">
          <ul class="work__facts">
{facts}
          </ul>
{link}
        </div>
      </div>
{extra}    </article>

    <nav class="next" aria-label="Další projekt">
      <a class="next__link wrap" href="../{next_slug}/">
        <span class="next__label">Další projekt<span class="arrow" aria-hidden="true"></span></span>
        <span class="next__name">{next_name}</span>
      </a>
    </nav>

    <section class="cta" aria-labelledby="cta-title">
      <div class="wrap">
        <h2 class="headline" id="cta-title">Postavíme i&nbsp;ten váš.</h2>
        <a class="btn btn--solid btn--lg" href="../../#kontakt" data-reveal style="--d:.06s">Probrat projekt<span class="arrow" aria-hidden="true"></span></a>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="footer__inner wrap">
      <a class="logo logo--footer" href="../../" aria-label="spaice studio, úvodní stránka">spa<span class="logo__i">ı</span>ce</a>
      <p class="footer__tag">Studio pro weby a&nbsp;mobilní aplikace</p>
      <nav class="footer__nav" aria-label="Patička">
        <a href="../../#prace">Práce</a>
        <a href="../../#sluzby">Služby</a>
        <a href="../../#kontakt">Kontakt</a>
      </nav>
      <a class="footer__mail" href="mailto:ahoj@spaicestudio.cz">ahoj@spaicestudio.cz</a>
      <p class="footer__copy">©&nbsp;2026 spaice studio. Petr Chajda, IČO 23250607, Průběžná 1033/4, 100&nbsp;00 Praha&nbsp;10</p>
    </div>
  </footer>
<!--/email_off-->
</body>
</html>
'''

for i, p in enumerate(PROJECTS):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    stype, quad, sw, sh, simgs = p['screen']
    if p['extra'] == 'reel':
        extra = REEL
    elif p['extra'] == 'screens':
        extra = SCREENS
    else:
        extra = shots(p['extra'][1])
    href, label = p['link']
    cls = 'link' if 'App Storu' in label else 'link link--url'
    link = f'          <a class="{cls}" href="{href}" target="_blank" rel="noopener">{label}<span class="arrow arrow--out" aria-hidden="true"></span></a>'
    html = PAGE.format(
        title=f"{p['title']} | spaice studio".replace('&', '&amp;'),
        desc=plain(p['body']),
        url=f"{SITE}/prace/{p['slug']}/",
        site=SITE, slug=p['slug'], alt=p['alt'].replace('&', '&amp;'),
        kind=p['kind'], name_html=p['name_html'],
        focus=p['focus'], focus_y=p['focus_y'], interval=p['interval'], A=A, scene=p['scene'],
        stype=stype, quad=quad, sw=sw, sh=sh, simgs=simgs,
        body=p['body'], more=p['more'],
        facts='\n'.join(f'            <li>{f}</li>' for f in p['facts']),
        link=link, extra=extra,
        next_slug=nxt['slug'], next_name=nxt['name_html'],
    )
    d = os.path.join(ROOT, 'prace', p['slug'])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('ok', p['slug'])
