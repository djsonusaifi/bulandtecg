# BulandTech Website — Quick Setup Guide

Ye guide batati hai ki website kaise chalani hai, update karni hai aur live karni hai.
Website ka overview [README.md](README.md) me hai.

---

## 1. Computer pe website chalana (preview)

**Option A — Python (sabse aasaan)**

`bulandtecg-main` folder me terminal kholo aur chalao:

```bash
python -m http.server 5500
```

Phir browser me kholo: http://localhost:5500

**Option B — VS Code**
1. VS Code me `bulandtecg-main` folder kholo
2. Extensions (Ctrl+Shift+X) me **Live Server** install karo
3. `index.html` pe right-click → **Open with Live Server**

> `index.html` ko seedha double-click karke mat kholna — kuch cheezein (videos, forms) server ke bina theek se nahi chalti.

**Phone view check karna:** Chrome me F12 → Ctrl+Shift+M → iPhone/Android select karo.

---

## 2. Website live karna (GitHub Pages + bulandtech.in)

`CNAME` file me `bulandtech.in` already likha hai, isliye GitHub Pages pe domain apne aap lag jayega.

> **Dhyan do:** free GitHub Pages ke liye repository **Public** honi chahiye — repo ki files koi bhi dekh sakta hai.
> `.gitignore` file ki wajah se `_tools/` (page generator) aur `.idea/` upload **nahi** honge — ye sirf aapke computer pe rahenge. Unka backup alag se (pen drive / Google Drive) rakhna.

### 2A. GitHub Desktop se upload karna (zaroori)
GitHub website pe browser se **25MB se badi file upload nahi hoti** — `media/cinematic-wedding.mp4` 32MB ki hai. Isliye **GitHub Desktop** app use karo (isme 100MB tak chalta hai):

1. https://desktop.github.com se GitHub Desktop install karo aur GitHub account se login karo.
2. **File → Add local repository** → `bulandtecg-main` folder chuno.
   Agar likha aaye "not a Git repository" → **create a repository** click karo → **Create repository**.
3. Upar **Publish repository** dabao → naam (jaise `bulandtech-website`) →
   **"Keep this code private" ka tick HATA do** (Pages free me public repo chahiye) → **Publish**.
4. Aage se jab bhi kuch badlo: GitHub Desktop kholo → neeche Summary me likho (jaise "prices update") → **Commit to main** → **Push origin**.

### 2B. GitHub Pages chalu karna
1. GitHub pe repository kholo → **Settings → Pages**.
2. **Source:** Deploy from a branch → Branch: `main`, folder `/ (root)` → **Save**.
3. **Custom domain** me `bulandtech.in` dikhna chahiye (CNAME file se). Na dikhe to likh ke **Save** karo.
4. DNS check pass hone ke baad **Enforce HTTPS** tick karo.

### 2C. Domain ke DNS records
Apne domain provider (GoDaddy, Hostinger, BigRock, etc.) ke DNS settings me ye records daalo — purane A / CNAME records (`@` aur `www` wale) hata do:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<aapka-github-username>.github.io` |

DNS badalne ke baad site live hone me kuch ghante (kabhi 24 ghante tak) lag sakte hain. Live hone pe check karo:
- https://bulandtech.in khul raha hai
- https://bulandtech.in/_tools/build.py pe **404 (Page not found)** aana chahiye

> **Code chhupana ho to:** private repo + free hosting ke liye `netlify.toml` already bana hai — Netlify pe private repo se free me chal jata hai. Shared hosting (Hostinger cPanel) pe bhi saari files `public_html` me upload karke chala sakte ho.

---

## 3. Live hone ke baad zaroori kaam

### 3.1 Forms chalu karna (sirf ek baar)
Contact form aur review form **support@bulandtech.in** pe email bhejte hain (FormSubmit service se).

1. Live website pe contact form se ek **test message** bhejo.
2. support@bulandtech.in pe FormSubmit ki **"Activate Form"** email aayegi — uska link click karo.
3. Bas. Ab saare messages aur reviews isi email pe aayenge. (Spam folder bhi check karna.)

### 3.2 Google Search Console (Google me jaldi aane ke liye)
1. https://search.google.com/search-console kholo → **Add property** → `https://bulandtech.in`
2. Ownership verify karo (DNS TXT record ya HTML file — Google batayega).
3. **Sitemaps** me likho `sitemap.xml` → **Submit**.

### 3.3 Google Business Profile (Maps + "near me" search — sabse zaroori)
1. https://business.google.com pe business banao: **BulandTech**
2. Address: Bugrasi Road, Syana, Dist. Bulandshahr, UP 203412
3. Category: *Website designer* (aur *Software company*, *Video editing service* add karo)
4. Phone +91 82659 99762, website https://bulandtech.in, aur photos lagao.
5. Verification ke baad clients se **Google review** mangwao.

> Naam, address aur phone har jagah (Google, Facebook, Instagram, JustDial) **bilkul ek jaise** rakho.

---

## 4. Website update karna

Saare 13 pages ek script se bante hain: **`_tools/build.py`**. Usme badlav karo, phir chalao:

```bash
python _tools/build.py .
```

Ye saare pages, `sitemap.xml` aur `robots.txt` dobara bana deta hai.

> ⚠️ Kisi `.html` file ko seedha edit kiya to agli baar `build.py` chalane pe wo badlav mit jayega. Permanent badlav hamesha `build.py` me karo.

`build.py` me kya kahan hai (Ctrl+F se dhundho):

| Kya badalna hai | `build.py` me dhundho |
|---|---|
| Address | `ADDRESS =` |
| Phone, email | `PHONE, PHONE_TEL, EMAIL =` |
| WhatsApp number | `WA = 'https://wa.me/` |
| Prices | `PRICING = [` |
| Home page service cards | `SVC_CARDS = [` |
| Graphic design portfolio | `DESIGNS = [` |
| Wedding videos | `VIDEOS = [` |
| YouTube video | `YOUTUBE = [` |
| Play Store apps | `APPS = [` |
| Home page reviews | `REVIEWS = [` |
| Page titles, descriptions, keywords | `SEO = {` |
| Service page FAQ | `SERVICE_FAQ = {` |
| Help page FAQ | `FAQS = [` |
| Service areas (cities) | `AREAS = [` |

### Naya review lagana
Review form se aaya **asli** review `REVIEWS = [` list me jodo — customer ke **apne shabdon me**, jitne star diye utne hi:

```python
('Rahul Sharma', 5, 'Website bahut achhi bani, time pe delivery mili.'),
```

### Naya graphic design jodna
1. Design ki PNG file `assetts/` folder me rakho (jaise `assetts/new-logo.png`).
2. Compress karo (neeche section 5 dekho) — `media/new-logo.webp` aur `media/new-logo-sm.webp` ban jayenge.
3. `DESIGNS = [` me line jodo. Category: `wedding`, `thumbnail`, `banner`, `logo`, `illustration`, `uiux`, `poster`.

```python
('assetts/new-logo.png', 'Cafe Logo Design', 'logo'),
```

4. `python _tools/build.py .` chalao.

### Nayi app jodna
`APPS = [` me jodo — naam, category, ek line, Play Store icon ka link aur app ka package id:

```python
('App Name', 'Category', 'One line about the app.', 'https://play-lh.googleusercontent.com/...=s128', 'com.bulandtech.appname'),
```

### Splash screen ka time
`script.js` me dhundho `minTime =` — `5000` matlab 5 second (pehli baar), `700` matlab baaki pages pe 0.7 second.

### Rang badalna
`styles.css` ke upar `:root` me `--accent` (orange) aur `--grad` (gradient) badlo.

---

## 5. Images aur videos compress karna

Bhari PNG/MP4 seedha mat lagao — site slow ho jayegi. Pehli baar tools install karo:

```bash
pip install pillow imageio-ffmpeg
```

Images (`assetts/` aur root ki saari PNG → `media/` me WebP):

```bash
python _tools/compress.py . images
```

Videos ke liye `_tools/compress.py` me `vids = {` list me file ka naam jodo, phir:

```bash
python _tools/compress.py . videos
```

Ye 1080p MP4 aur cover image (`-poster.webp`) banata hai. Compress hone ke baad `assetts/` ki original files upload karna zaroori nahi.

---

## 6. Launch checklist

Live karne se pehle:
- [ ] Phone, email, address, WhatsApp number sahi hain
- [ ] Prices sahi hain
- [ ] Phone aur desktop dono pe site check ki
- [ ] Har service page aur portfolio khul raha hai
- [ ] `media/` folder upload hua hai (GitHub Desktop se)
- [ ] `_tools/` ka backup computer ke bahar bhi rakha

Live karne ke baad:
- [ ] FormSubmit activation link click kiya (section 3.1)
- [ ] Contact form aur review form se test message aaya
- [ ] Google Search Console me sitemap submit kiya
- [ ] Google Business Profile banaya aur verify kiya
- [ ] Purane clients ko review ka WhatsApp message bheja
- [ ] Facebook, Instagram, JustDial pe website link aur same address daala

---

## Madad

**BulandTech** — Bugrasi Road, Syana, Dist. Bulandshahr, UP 203412
Call / WhatsApp: +91 82659 99762 · Email: support@bulandtech.in
