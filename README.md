# OH AUDIO Landing Page

Moderne, responsiv landingsside for OH AUDIO (Olve Husby) bygget med ren HTML/CSS/JS.

## Strukturer

- `index.html` – midlertidig “coming soon”-side publiseres på `ohaudio.no`.
- `styles.css` – styling til placeholderen.
- `script.js` – intersection animations, mailto-håndtering og enkel live-reload-kontroll.
- `server.py` – lettvekts utviklingsserver med auto-refresh (polling).
- `assets/` – logoer, bakgrunnsfoto, mønstre.
- `CNAME` – peker GitHub Pages til `ohaudio.no`.
- `site-full/` – komplette filer for hovedsiden (kopier til rot når du er klar for lansering).

## Lokal utvikling

```bash
python3 server.py -p 8080
```

Åpne `http://localhost:8080`. Nettleseren refresher automatisk når du lagrer filer.

## Deploy til GitHub Pages

1. Opprett et GitHub-repo (f.eks. `oh-audio-site`) og sett `main` som standardbranch.
2. Legg dette prosjektet i repoet og kjør:

   ```bash
   git add .
   git commit -m "Initial site"
   git remote add origin git@github.com:<bruker>/oh-audio-site.git
   git push -u origin main
   ```

3. I repo Settings → Pages:
   - Source: `Deploy from a branch`
   - Branch: `main`, folder `/ (root)`
4. GitHub Pages vil bygge og eksponere siden på `https://<bruker>.github.io/oh-audio-site/`.
5. Under *Custom domain*, skriv `ohaudio.no`. GitHub verifiserer at `CNAME`-fila finnes.

> Når du er klar for full lansering, kopier `site-full/index.html` → `index.html` og `site-full/styles.css` → `styles.css`, commit/push igjen og GitHub Pages oppdaterer seg.

## DNS-oppsett hos domene.no

Opprett følgende poster:

| Type | Name            | Value                                    |
| ---- | --------------- | ---------------------------------------- |
| A    | `@`             | `185.199.108.153`                        |
| A    | `@`             | `185.199.109.153`                        |
| A    | `@`             | `185.199.110.153`                        |
| A    | `@`             | `185.199.111.153`                        |
| CNAME| `www`           | `<bruker>.github.io.`                    |

> GitHub anbefaler de fire A-records for `@` (root) og en CNAME for `www`.

Når DNS har propagert, aktiverer du “Enforce HTTPS” i GitHub Pages. Siden vil da være tilgjengelig på `https://ohaudio.no`.

## E-post (valgfritt)

Velg en leverandør (f.eks. domeneshop, Zoho, Fastmail) og følg instruksene deres for å legge til MX + SPF/DKIM i DNS. GitHub Pages leverer ikke e-post, men domenet kan peke begge steder samtidig (web via A/CNAME, e-post via MX).
