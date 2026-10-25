# spaicestudio.cz

Statický web studia spaice. Bez buildu: co je v repozitáři, to se nasadí.

| Cesta | Obsah |
|---|---|
| `index.html` | hlavní stránka |
| `prace/<projekt>/` | případové studie s vlastním náhledem odkazu (Gentlemen's Garage, MojeTripy, J&J Barber Shop, Cookpit) |
| `404.html` | stránka pro neexistující adresy |
| `assets/` | styly, skript, písmo Archivo, obrázky, videa, logo (`share-*-2510.jpg` jsou náhledy odkazů 1200 × 630) |
| `assets/logo/` | logo „Kurzor“ na tmavé a světlé ploše, značka, favicon a ikona pro iPhone |
| `Dockerfile`, `Caddyfile` | nasazení na Railway (viz níže) |
| `tools/web.py` | vygeneruje `index.html`, `prace/*/index.html` a `404.html`. Hlavička, menu a patička jsou společné, texty a obrázky se mění tady, ne v HTML. |
| `tools/logo.py` | nakreslí logo z písma Archivo do `assets/logo/` a cesty pro `tools/web.py` do `tools/logo.json`. Potřebuje `pip install fonttools brotli`. |

Po změně loga z SVG vyrob PNG a ICO (ImageMagick):

```bash
magick -background none -density 300 assets/logo/spaice-znacka-ctverec.svg -resize 180x180 assets/logo/apple-touch-icon.png
for z in 16 32 48; do magick -background none -density 300 assets/logo/favicon.svg -resize ${z}x${z} /tmp/fav$z.png; done
magick /tmp/fav16.png /tmp/fav32.png /tmp/fav48.png assets/logo/favicon.ico
```

Nové PNG a ICO ulož i pod novým názvem nebo změň odkazy v `tools/web.py`; obrázky drží Cloudflare v mezipaměti až den (viz níže).

Lokální náhled: `python3 -m http.server 4321` a otevřít http://localhost:4321.

## Nasazení na Railway

Weby běží na Railway v projektu **spaicestudio.cz** (workspace petr189226), stejně jako ostatní weby: `Dockerfile` zabalí soubory do Caddy, `Caddyfile` řeší hlavičky, cache, přesměrování z `www` a stránku 404. TLS vydává Railway.

| Služba | Repozitář | Doména |
|---|---|---|
| `web` | [`spaicestudio-web`](https://github.com/Petr189226/spaicestudio-web) (tato složka) | `spaicestudio.cz`, `www` přesměruje bez `www` |
| `cookpit` | [`cookpit-web`](https://github.com/Petr189226/cookpit-web) (`cookpit/`) | `cookpit.spaicestudio.cz` |

Každý push do `main` web znovu nasadí. Obrázky drží Cloudflare v mezipaměti až den, proto upravený obrázek ulož pod **novým názvem** (například s datem `mt-den-2610.webp`), jinak se návštěvníkům ještě ukazuje ten starý. Do obrazu jdou jen soubory, které Git sleduje (viz `.gitignore`).

DNS v Cloudflare. Proxy je zapnutá (oranžový mráček): HTTPS obsluhuje certifikát Cloudflare pro `spaicestudio.cz` a `*.spaicestudio.cz` a režim SSL je „Full“, takže se Cloudflare k Railway připojí i bez certifikátu Railway. Railway vlastní certifikáty kvůli limitu Let's Encrypt z doby přepínání nevydal. Proxy tomu nevadí, pro jistotu ho nevypínej, dokud Railway u domén neukáže platný certifikát.

| Typ | Název | Hodnota |
|---|---|---|
| CNAME | `@` | `xxkevzaz.up.railway.app` |
| CNAME | `www` | `owxgc4py.up.railway.app` |
| CNAME | `cookpit` | `gz535m8r.up.railway.app` |
| CNAME | `jetopodvod` | `tk99qy3v.up.railway.app` |
| TXT | `_railway-verify`, `_railway-verify.www`, `_railway-verify.cookpit`, `_railway-verify.jetopodvod` | ověřovací hodnoty z Railway (`railway domain status <doména>`) |

Cíle CNAME přiděluje Railway při přidání domény; když doménu v Railway smažeš a přidáš znovu, cíl se změní a záznam je potřeba přepsat.

Další web na subdoméně (například pro další aplikaci): nová služba v tomtéž projektu (`railway add --service <název> --repo Petr189226/<repo>`), vlastní `Dockerfile` a `Caddyfile` jako u Cookpitu, `railway domain <subdoména> --service <název>` a záznamy CNAME a TXT v Cloudflare.

Lokálně stejně jako na Railway: `docker build -t spaice . && docker run -e PORT=8080 -p 8080:8080 spaice`.

## E-maily

**Cloudflare → Email → Email Routing** je pro `spaicestudio.cz` zapnutý (MX, SPF a DKIM přidal Cloudflare sám).

| Adresa | Kam se přeposílá |
|---|---|
| `ahoj@spaicestudio.cz` | `petr.chajda@seznam.cz` |

`cookpit@spaicestudio.cz` a `jetopodvod@spaicestudio.cz` zatím pravidlo nemají; přidává se v **Email Routing → Routing rules → Create routing rule**.

## Po spuštění

- Náhledy odkazů: [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) (zároveň obnoví uložený náhled pro Messenger a WhatsApp), [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/), odkaz poslaný sám sobě v iMessage.
- Adresy v meta tazích počítají s `https://spaicestudio.cz` bez `www`. Kdyby web běžel na `www`, je potřeba je přepsat.
