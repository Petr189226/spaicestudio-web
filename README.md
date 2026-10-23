# spaicestudio.cz

Statický web studia spaice. Bez buildu: co je v repozitáři, to se nasadí.

| Cesta | Obsah |
|---|---|
| `index.html` | hlavní stránka (generovaná, viz `tools/web.py`) |
| `prace/<projekt>/` | stránky projektů s vlastním náhledem odkazu (MojeTripy, Cookpit, Gentlemen's Garage, J&J Barber Shop) |
| `assets/` | styly, skript, písmo Archivo, obrázky (`share*.jpg` jsou náhledy odkazů 1200 × 630) |
| `404.html` | stránka pro neexistující adresy |
| `Dockerfile`, `Caddyfile` | nasazení na Railway (viz níže) |
| `tools/web.py` | vygeneruje `index.html`, `prace/*/index.html` a `404.html`. Hlavička, menu aplikací, patička a všechny texty jsou na jednom místě. Po změně pusť `python3 tools/web.py`. |

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

Adresy `ahoj@spaicestudio.cz` (web studia) a `cookpit@spaicestudio.cz` (podpora aplikace) zatím nic nepřijímají, doména nemá MX záznamy. Nejjednodušší je **Cloudflare → Email → Email Routing**: zapnout pro `spaicestudio.cz` (MX a SPF přidá sám) a obě adresy přeposílat do vlastní schránky.

## Po spuštění

- Náhledy odkazů: [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) (zároveň obnoví uložený náhled pro Messenger a WhatsApp), [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/), odkaz poslaný sám sobě v iMessage.
- Adresy v meta tazích počítají s `https://spaicestudio.cz` bez `www`. Kdyby web běžel na `www`, je potřeba je přepsat.
