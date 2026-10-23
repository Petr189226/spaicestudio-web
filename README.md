# spaicestudio.cz

Statický web studia spaice. Bez buildu: co je v repozitáři, to se nasadí.

| Cesta | Obsah |
|---|---|
| `index.html` | hlavní stránka |
| `prace/<projekt>/` | stránky projektů s vlastním náhledem odkazu (MojeTripy, Cookpit, Gentlemen's Garage, J&J Barber Shop) |
| `assets/` | styly, skript, písmo Archivo, obrázky (`share*.jpg` jsou náhledy odkazů 1200 × 630) |
| `404.html` | stránka pro neexistující adresy |
| `tools/projekty.py` | vygeneruje `prace/*/index.html`. Hlavička a patička jsou stejné jako v `index.html`, po jejich změně skript pusť znovu. |

Lokální náhled: `python3 -m http.server 4321` a otevřít http://localhost:4321.

## Nasazení na GitHub Pages

Weby jsou dva, každý ve vlastním repozitáři, protože GitHub Pages umí jen jednu doménu na repozitář:

| Repozitář | Složka | Doména |
|---|---|---|
| `spaicestudio-web` | tato složka | `spaicestudio.cz` (a `www`) |
| `cookpit-web` | `cookpit/` | `cookpit.spaicestudio.cz` |

Soubor `CNAME` s doménou a prázdný `.nojekyll` jsou v obou repozitářích připravené.

1. Na GitHubu vytvoř oba repozitáře jako veřejné (Pages pro soukromé repozitáře chce placený účet) a nahraj do nich větev `main`.
2. V každém repozitáři: **Settings → Pages → Build and deployment**, zdroj **Deploy from a branch**, větev `main`, složka `/ (root)`. Doména se načte ze souboru `CNAME`.
3. V Cloudflare (**DNS → Records**) přidej záznamy. Proxy nech vypnutou (šedý mráček), jinak GitHub nevydá certifikát:

   | Typ | Název | Hodnota |
   |---|---|---|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | AAAA | `@` | `2606:50c0:8000::153` |
   | AAAA | `@` | `2606:50c0:8001::153` |
   | AAAA | `@` | `2606:50c0:8002::153` |
   | AAAA | `@` | `2606:50c0:8003::153` |
   | CNAME | `www` | `<účet>.github.io` |
   | CNAME | `cookpit` | `<účet>.github.io` |

4. Až GitHub v **Settings → Pages** ukáže, že DNS sedí a certifikát je vydaný, zapni **Enforce HTTPS**.
5. Doménu si na GitHubu ověř (**Settings účtu → Pages → Add a domain**, TXT záznam `_github-pages-challenge-<účet>` v Cloudflare). Nikdo jiný ji pak nepřipojí ke svému repozitáři.

Další web na subdoméně (například pro další aplikaci) funguje stejně: vlastní repozitář, soubor `CNAME` se subdoménou a záznam CNAME v Cloudflare.

## E-maily

Adresy `ahoj@spaicestudio.cz` (web studia) a `cookpit@spaicestudio.cz` (podpora aplikace) zatím nic nepřijímají, doména nemá MX záznamy. Nejjednodušší je **Cloudflare → Email → Email Routing**: zapnout pro `spaicestudio.cz` (MX a SPF přidá sám) a obě adresy přeposílat do vlastní schránky.

## Po spuštění

- Náhledy odkazů: [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) (zároveň obnoví uložený náhled pro Messenger a WhatsApp), [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/), odkaz poslaný sám sobě v iMessage.
- Adresy v meta tazích počítají s `https://spaicestudio.cz` bez `www`. Kdyby web běžel na `www`, je potřeba je přepsat.
