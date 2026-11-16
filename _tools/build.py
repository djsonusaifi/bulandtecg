"""Generates the BulandTech static pages with a shared header/footer."""
import json, sys, os, html

OUT = sys.argv[1]
META = json.load(open(os.path.join(os.path.dirname(__file__), 'meta.json'), encoding='utf-8'))

WA = 'https://wa.me/918265999762'
def wa(text): return WA + '?text=' + text.replace(' ', '%20').replace("'", '%27').replace(',', '%2C')

SERVICES = [
    ('website-development.html', 'Website Development', 'fa-code'),
    ('app-development.html', 'App Development', 'fa-mobile-screen'),
    ('graphic-design.html', 'Graphic Design', 'fa-pen-nib'),
    ('video-editing.html', 'Video Editing', 'fa-film'),
    ('web-design.html', 'Web Design (UI/UX)', 'fa-object-group'),
    ('digital-marketing.html', 'Digital Marketing', 'fa-chart-line'),
    ('music-production.html', 'Music Production', 'fa-headphones'),
]

# ----------------------------------------------------------------- partials
ADDRESS = 'Bugrasi Road, Syana, Dist. Bulandshahr, Uttar Pradesh, India 203412'
ADDRESS_SHORT = 'Bugrasi Road, Syana, Bulandshahr, UP 203412'
PHONE, PHONE_TEL, EMAIL = '+91 82659 99762', '+918265999762', 'support@bulandtech.in'

_logo_n = [0]
def logo_svg(size=38):
    """BulandTech mark: rising bars + upward arrow (Buland = high)."""
    _logo_n[0] += 1
    g = f'btg{_logo_n[0]}'
    return (f'<svg class="logo-mark" width="{size}" height="{size}" viewBox="0 0 40 40" aria-hidden="true">'
            f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a3d"/><stop offset="1" stop-color="#e8283f"/></linearGradient></defs>'
            f'<rect width="40" height="40" rx="11" fill="url(#{g})"/>'
            '<rect class="lb lb1" x="9" y="23" width="5.5" height="9" rx="1.6" fill="#fff" opacity=".65"/>'
            '<rect class="lb lb2" x="17.25" y="18" width="5.5" height="14" rx="1.6" fill="#fff" opacity=".85"/>'
            '<rect class="lb lb3" x="25.5" y="12" width="5.5" height="20" rx="1.6" fill="#fff"/>'
            '<path class="la" d="M8.5 17.5 L16 11.5 L20.5 14 L29 7.5" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M24.5 7.2 L29.4 7.2 L29.4 12" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '</svg>')

def brand(href='index.html'):
    return (f'<a href="{href}" class="brand" aria-label="BulandTech home">'
            f'<img class="logo-mark" src="media/logo-192.webp" alt="" width="40" height="40">'
            f'<span class="brand-word">Buland<em>tech</em></span></a>')

CURRENT = ['index.html']
SPLASH_ART = [  # (file, css position)
    ('marketing', 'top:7%;left:5%;width:min(200px,34vw);--r:-8deg;--d:0s'),
    ('music', 'top:9%;right:4%;width:min(230px,38vw);--r:6deg;--d:-2s'),
    ('video', 'top:40%;left:-2%;width:min(150px,26vw);--r:10deg;--d:-4s'),
    ('ios', 'top:44%;right:1%;width:min(150px,26vw);--r:-6deg;--d:-1s'),
    ('android', 'bottom:7%;left:9%;width:min(110px,20vw);--r:-10deg;--d:-3s'),
    ('plugin', 'bottom:9%;right:12%;width:min(110px,20vw);--r:8deg;--d:-5s'),
    ('exe', 'bottom:24%;left:40%;width:min(84px,16vw);--r:12deg;--d:-2.5s'),
]

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%23ff7a3d'/%3E%3Cstop offset='1' stop-color='%23e8283f'/%3E%3C/linearGradient%3E%3C/defs%3E"
           "%3Crect width='40' height='40' rx='11' fill='url(%23g)'/%3E%3Crect x='9' y='23' width='5.5' height='9' rx='1.6' fill='%23fff' opacity='.65'/%3E%3Crect x='17.25' y='18' width='5.5' height='14' rx='1.6' fill='%23fff' opacity='.85'/%3E%3Crect x='25.5' y='12' width='5.5' height='20' rx='1.6' fill='%23fff'/%3E"
           "%3Cpath d='M8.5 17.5 L16 11.5 L20.5 14 L29 7.5 M24.5 7.2 L29.4 7.2 L29.4 12' fill='none' stroke='%23fff' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")

# ----------------------------------------------------------------- SEO data
SITE = 'https://bulandtech.in/'
TODAY = '2026-11-16'
AREAS = ['Bulandshahr', 'Syana', 'Bugrasi', 'Khurja', 'Sikandrabad', 'Anupshahr', 'Jahangirabad', 'Garhmukteshwar',
         'Hapur', 'Ghaziabad', 'Noida', 'Greater Noida', 'Delhi NCR', 'Meerut', 'Aligarh', 'Moradabad']

SEO = {
    'index.html': dict(
        title='Website & App Development Company in Bulandshahr | BulandTech',
        h1='Website, App Development &amp; Video Editing Company in Bulandshahr',
        desc='BulandTech is a website development, app development and video editing company in Syana, Bulandshahr. Graphic design, SEO and digital marketing for UP &amp; Delhi NCR. Call +91 82659 99762.',
        kw='website development company in bulandshahr, app development company bulandshahr, video editing bulandshahr, web designer syana, android app developer bulandshahr, website design noida, wedding video editing bulandshahr, graphic designer bulandshahr, digital marketing bulandshahr, it company bulandshahr, bulandtech'),
    'website-development.html': dict(
        title='Website Development Company in Bulandshahr, Noida | BulandTech',
        h1='Website Development Company in Bulandshahr',
        desc='Professional website development in Bulandshahr, Syana, Noida &amp; Delhi NCR. Business websites, e-commerce stores and landing pages — fast, mobile-friendly and SEO-ready. From ₹5,000.',
        kw='website development company in bulandshahr, website developer bulandshahr, website banane wala bulandshahr, web developer syana, ecommerce website bulandshahr, website design noida, business website delhi ncr, website development hapur, website development khurja, seo friendly website, responsive website design'),
    'app-development.html': dict(
        title='Android &amp; iOS App Development Company in Bulandshahr | BulandTech',
        h1='App Development Company in Bulandshahr',
        desc='Android, iOS and Flutter app development in Bulandshahr, Syana, Noida &amp; Delhi NCR. 7 apps live on Google Play. Delivery, e-commerce, education and business apps from ₹20,000.',
        kw='app development company in bulandshahr, android app developer bulandshahr, app banwane wale bulandshahr, mobile app development syana, ios app developer, flutter app developer, app development noida, app development delhi ncr, play store app publish, delivery app development, ecommerce app development'),
    'video-editing.html': dict(
        title='Video Editing Services in Bulandshahr – Wedding, Reels | BulandTech',
        h1='Video Editing Services in Bulandshahr',
        desc='Wedding video editing, teasers, highlights, Instagram reels, YouTube and music video editing in Bulandshahr, Syana, Noida &amp; Delhi NCR. Cinematic colour grading. From ₹1,500.',
        kw='video editing bulandshahr, video editor in bulandshahr, wedding video editing bulandshahr, wedding teaser editing, cinematic wedding film, reel editing syana, youtube video editor, music video editing, video editing noida, video editing delhi ncr, premiere pro editor, colour grading'),
    'graphic-design.html': dict(
        title='Graphic Designer in Bulandshahr – Logo, Poster, Cards | BulandTech',
        h1='Graphic Design Services in Bulandshahr',
        desc='Logo design, wedding cards, posters, banners, YouTube thumbnails and brand identity in Bulandshahr, Syana &amp; Delhi NCR. See 28+ real designs. Logo from ₹2,000.',
        kw='graphic designer in bulandshahr, logo design bulandshahr, wedding card design, poster design syana, banner design bulandshahr, youtube thumbnail design, brand identity design, flyer design, election pamphlet design, graphic design noida'),
    'web-design.html': dict(
        title='Web Design &amp; UI/UX Design Services in Bulandshahr | BulandTech',
        h1='Web Design &amp; UI/UX Services in Bulandshahr',
        desc='Website design and UI/UX design in Bulandshahr — wireframes, Figma prototypes, landing pages and app interfaces that convert. Serving UP, Noida &amp; Delhi NCR.',
        kw='web design bulandshahr, ui ux designer bulandshahr, website designer syana, figma designer, landing page design, app ui design, web design noida, web design delhi ncr'),
    'digital-marketing.html': dict(
        title='Digital Marketing &amp; SEO Services in Bulandshahr | BulandTech',
        h1='Digital Marketing &amp; SEO Company in Bulandshahr',
        desc='SEO, Google Ads, Facebook &amp; Instagram ads and social media marketing in Bulandshahr, Syana, Noida &amp; Delhi NCR. Local SEO that brings calls and leads. From ₹5,000/month.',
        kw='digital marketing company bulandshahr, seo expert bulandshahr, seo services syana, google ads bulandshahr, facebook ads expert, instagram marketing, social media marketing bulandshahr, local seo, google business profile, digital marketing noida'),
    'music-production.html': dict(
        title='Music Production &amp; Beat Making Studio in Bulandshahr | BulandTech',
        h1='Music Production Studio in Bulandshahr',
        desc='Beat making, remixes, mixing &amp; mastering and background music in Bulandshahr and Syana. Haryanvi, Bollywood, hip-hop and lo-fi production. Beats from ₹2,000.',
        kw='music production bulandshahr, beat maker bulandshahr, music studio syana, remix song, mixing and mastering, haryanvi music production, background music, fl studio producer'),
    'about.html': dict(
        title='About BulandTech – Digital Agency in Syana, Bulandshahr',
        h1='About BulandTech – Digital Agency in Syana, Bulandshahr',
        desc='BulandTech is a digital agency in Syana, Bulandshahr offering website development, app development, video editing, graphic design and digital marketing across UP &amp; Delhi NCR.',
        kw='bulandtech, about bulandtech, digital agency bulandshahr, it company syana, software company bulandshahr'),
    'help-support.html': dict(
        title='Help &amp; Support | BulandTech Bulandshahr',
        h1='BulandTech Help &amp; Support',
        desc='Get help from BulandTech by call, WhatsApp or email. Answers about payments, ID verification, timelines, revisions and support after delivery.',
        kw=''),
    'terms-and-conditions.html': dict(title='Terms &amp; Conditions | BulandTech', h1='', kw='',
        desc='BulandTech terms and conditions — valid ID and 70% advance before work starts, payment terms, revisions, ownership and refunds.'),
    'privacy-policy.html': dict(title='Privacy Policy | BulandTech', h1='', kw='',
        desc='How BulandTech collects, uses and protects your personal information, including ID verification and payment records.'),
    'submit-review.html': dict(title='Submit a Review | BulandTech', h1='', kw='',
        desc='Worked with BulandTech? Share your experience with our website, app, design, video or marketing services.'),
}

SERVICE_SCHEMA = {
    'website-development.html': 'Website Development', 'app-development.html': 'Mobile App Development',
    'video-editing.html': 'Video Editing', 'graphic-design.html': 'Graphic Design', 'web-design.html': 'Web Design and UI/UX Design',
    'digital-marketing.html': 'Digital Marketing and SEO', 'music-production.html': 'Music Production',
}

SERVICE_FAQ = {
    'website-development.html': [
        ('How much does a website cost in Bulandshahr?', 'A basic website costs ₹5,000 – 15,000, a business website ₹15,000 – 30,000 and an e-commerce website ₹30,000 – 50,000+. You get a fixed quote after a short discussion.'),
        ('How long does it take to build a website?', 'A basic website usually takes 7–15 days. Bigger business and e-commerce websites take longer — your quote mentions the exact timeline.'),
        ('Will my website work on mobile and show on Google?', 'Yes. Every website we build is mobile-friendly, fast and set up with the basic SEO Google needs — titles, descriptions, sitemap and clean structure.'),
        ('Do you make websites outside Bulandshahr?', 'Yes. We work with clients in Syana, Khurja, Hapur, Ghaziabad, Noida, Delhi NCR and across India — everything can be done over call and WhatsApp.'),
    ],
    'app-development.html': [
        ('How much does app development cost?', 'A simple app costs ₹20,000 – 40,000, a complex app ₹40,000 – 80,000 and an enterprise app ₹80,000 – 2,00,000+. The final price depends on features.'),
        ('How long does it take to make an app?', 'Most apps take 3–8 weeks depending on features, design and backend work.'),
        ('Will you publish my app on Google Play?', 'Yes. We have published 7 apps on Google Play and handle the full publishing process. The Google Play developer account fee is paid by the client.'),
        ('Do you make both Android and iOS apps?', 'Yes. We build native Android apps and cross-platform apps with Flutter or React Native that run on both Android and iPhone.'),
    ],
    'video-editing.html': [
        ('How much does video editing cost in Bulandshahr?', 'Basic editing costs ₹1,500 – 3,000, professional editing ₹3,000 – 8,000 and cinematic videos ₹8,000 – 20,000 depending on length and effects.'),
        ('Do you edit wedding videos?', 'Yes — wedding teasers, highlights and full cinematic wedding films with colour grading and music sync. You can see our wedding films on this page.'),
        ('Do you edit Instagram reels and YouTube videos?', 'Yes. We edit reels, shorts and YouTube videos with captions, transitions, thumbnails and platform-ready export settings.'),
        ('How long does video editing take?', 'Short reels and edits take a few days. Longer wedding films take more time — we confirm the timeline before starting.'),
    ],
    'graphic-design.html': [
        ('How much does logo design cost?', 'Logo design costs ₹2,000 – 5,000 and a complete branding package ₹10,000 – 25,000. Social media posts start from ₹500.'),
        ('Do you design wedding cards and invitations?', 'Yes. We design printed and digital (WhatsApp) wedding cards in traditional, royal and modern styles.'),
        ('Will I get the source files?', 'Yes. After full payment you receive print-ready and digital files, plus source files when they are part of the quote.'),
    ],
    'digital-marketing.html': [
        ('How much do SEO services cost?', 'SEO costs ₹5,000 – 15,000 per month, social media marketing ₹8,000 – 20,000 per month and a complete package ₹15,000 – 40,000 per month. Ad budget is separate.'),
        ('Can you help my business show on Google Maps?', 'Yes. We set up and optimise your Google Business Profile, local SEO and reviews so nearby customers can find you.'),
        ('When will I see results from SEO?', 'Local SEO usually shows improvement in 2–4 months. Google and Meta ads can bring leads from the first week.'),
    ],
    'music-production.html': [
        ('How much does beat making cost?', 'Beat making costs ₹2,000 – 5,000, a remix ₹3,000 – 8,000 and an original song ₹10,000 – 25,000.'),
        ('Which music styles do you produce?', 'Haryanvi, Bollywood, hip-hop, drill, lo-fi, EDM and background scores for videos and ads.'),
    ],
}

def jsonld(obj):
    import json as _j
    return '\n    <script type="application/ld+json">' + _j.dumps(obj, ensure_ascii=False) + '</script>'

def org_schema():
    return {
        '@type': ['ProfessionalService', 'LocalBusiness'], '@id': SITE + '#business', 'name': 'BulandTech',
        'url': SITE, 'logo': SITE + 'media/icon-512.png', 'image': SITE + 'media/og-image.jpg',
        'description': 'Website development, app development, video editing, graphic design and digital marketing company in Syana, Bulandshahr.',
        'telephone': '+91-8265999762', 'email': 'support@bulandtech.in', 'priceRange': '₹₹',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Bugrasi Road', 'addressLocality': 'Syana',
                    'addressRegion': 'Uttar Pradesh', 'postalCode': '203412', 'addressCountry': 'IN'},
        'areaServed': [{'@type': 'City', 'name': a} for a in AREAS],
        'sameAs': ['https://www.facebook.com/profile.php?id=61571168753695', 'https://www.instagram.com/svd_star_edit',
                   'https://x.com/FirstHumaniti', 'https://www.linkedin.com/in/sonu-saifii'],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Digital services', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'url': SITE + u}} for u, n in SERVICE_SCHEMA.items()]},
    }

def page_schema(page, title, desc):
    import html as _h
    graph = [org_schema()]
    url = SITE + ('' if page == 'index.html' else page)
    if page == 'index.html':
        graph.append({'@type': 'WebSite', '@id': SITE + '#website', 'url': SITE, 'name': 'BulandTech', 'inLanguage': 'en-IN',
                      'publisher': {'@id': SITE + '#business'}})
    else:
        crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}]
        if page in SERVICE_SCHEMA:
            crumbs.append({'@type': 'ListItem', 'position': 2, 'name': 'Services', 'item': SITE + '#services'})
        crumbs.append({'@type': 'ListItem', 'position': len(crumbs) + 1, 'name': _h.unescape(title.split('|')[0].split('–')[0].strip()), 'item': url})
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': crumbs})
    if page in SERVICE_SCHEMA:
        graph.append({'@type': 'Service', 'name': SERVICE_SCHEMA[page], 'serviceType': SERVICE_SCHEMA[page], 'url': url,
                      'description': _h.unescape(desc), 'provider': {'@id': SITE + '#business'},
                      'areaServed': [{'@type': 'City', 'name': a} for a in AREAS]})
    faqs = SERVICE_FAQ.get(page) or (FAQS if page == 'help-support.html' else None)
    if faqs:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': _h.unescape(q), 'acceptedAnswer': {'@type': 'Answer', 'text': _h.unescape(a)}} for q, a in faqs]})
    return jsonld({'@context': 'https://schema.org', '@graph': graph})

def areas_section(service_name='our services'):
    chips = ''.join(f'<span><i class="fas fa-location-dot"></i>{a}</span>' for a in AREAS)
    return f'''
    <section class="section section-alt areas">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">Service areas</span><h2>Serving Bulandshahr <span class="serif">&amp; nearby cities.</span></h2></div>
            <p>We provide {service_name} from our studio on Bugrasi Road, Syana, Bulandshahr — and work online with clients across India.</p></div>
            <div class="area-chips" data-reveal>{chips}<span class="all"><i class="fas fa-globe"></i>All of India (online)</span></div>
        </div>
    </section>
'''

def faq_section(page):
    faqs = SERVICE_FAQ.get(page)
    if not faqs:
        return ''
    items = ''.join(f'<details class="faq" data-reveal><summary>{q}<i class="fas fa-plus"></i></summary><p>{a}</p></details>' for q, a in faqs)
    return f'''
    <section class="section">
        <div class="container faq-wrap">
            <div data-reveal><span class="eyebrow">FAQ</span><h2 class="h2">Common <span class="serif">questions.</span></h2>
            <p class="muted">Still have a question? <a href="help-support.html" style="color:var(--accent);font-weight:600">Visit Help &amp; Support</a> or call us.</p></div>
            <div class="faq-list">{items}</div>
        </div>
    </section>
'''

def write_sitemap_and_robots(out, pages):
    prio = {'index.html': ('1.0', 'weekly')}
    for p in SERVICE_SCHEMA:
        prio[p] = ('0.9', 'monthly')
    prio.update({'about.html': ('0.7', 'monthly'), 'help-support.html': ('0.6', 'monthly'), 'submit-review.html': ('0.4', 'monthly'),
                 'terms-and-conditions.html': ('0.3', 'yearly'), 'privacy-policy.html': ('0.3', 'yearly')})
    urls = ''.join(
        f'''  <url>\n    <loc>{SITE}{"" if p == "index.html" else p}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{prio[p][1]}</changefreq>\n    <priority>{prio[p][0]}</priority>\n  </url>\n'''
        for p in pages)
    with open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(out, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
    print('wrote sitemap.xml, robots.txt')

def head(title, page, extra_desc=None):
    m = META.get(page, {})
    sd = SEO.get(page, {})
    title = sd.get('title', title)
    desc = sd.get('desc') or extra_desc or m.get('description', '')
    kw = sd.get('kw', m.get('keywords', ''))
    schema = page_schema(page, title, desc)
    kw_tag = f'\n    <meta name="keywords" content="{kw}">' if kw else ''
    url = 'https://bulandtech.in/' + ('' if page == 'index.html' else page)
    CURRENT[0] = page
    art = ''.join(f'<img class="sp-art" src="media/splash/{f}.webp" alt="" style="{st}">' for f, st in SPLASH_ART)
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <meta name="description" content="{desc}">{kw_tag}
    <meta name="author" content="BulandTech">
    <meta name="robots" content="index, follow">
    <meta name="theme-color" content="#ff6a13">
    <link rel="canonical" href="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:site_name" content="BulandTech">
    <meta property="og:locale" content="en_IN">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://bulandtech.in/media/og-image.jpg">
    <meta name="geo.region" content="IN-UP">
    <meta name="geo.placename" content="Syana, Bulandshahr">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="https://bulandtech.in/media/og-image.jpg">
    <link rel="icon" type="image/png" href="media/favicon-48.png">
    <link rel="apple-touch-icon" href="media/apple-touch-icon.png">
    <link rel="manifest" href="manifest.webmanifest">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="BulandTech">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="styles.css">{schema}
</head>
<body>
    <div id="splash" aria-hidden="true">
        <div class="sp-arts">{art}</div>
        <div class="splash-inner">
            <div class="sp-logo"><img src="media/logo-512.webp" alt="BulandTech" width="200" height="200"></div>
            <p class="sp-tag">Websites · Apps · Design · Video · Marketing</p>
            <div class="splash-bar"><span></span></div>
        </div>
    </div>
    <div class="scroll-progress" aria-hidden="true"></div>
'''

def nav(home=False):
    p = '' if home else 'index.html'
    return f'''
    <header class="nav">
        <div class="container">
            {brand('#home' if home else 'index.html')}
            <nav class="nav-links" aria-label="Primary">
                <a href="{p}#services">Services</a>
                <a href="{p}#work">Work</a>
                <a href="{p}#pricing">Pricing</a>
                <a href="about.html">About</a>
                <a href="help-support.html">Help</a>
                <a href="{p}#contact">Contact</a>
                <a href="submit-review.html" class="mobile-only"><i class="fas fa-star" style="color:var(--accent-2);margin-right:8px"></i>Write a Review</a>
                <span class="mobile-only"><a href="{p}#contact" class="btn btn-primary">Start a project</a></span>
            </nav>
            <div class="nav-cta">
                <a href="submit-review.html" class="btn btn-ghost btn-sm nav-review" aria-label="Write a review"><i class="fas fa-star"></i><span>Review</span></a>
                <a href="{p}#contact" class="btn btn-primary btn-sm">Start a project <i class="fas fa-arrow-right"></i></a>
                <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
            </div>
        </div>
    </header>
'''

def bottom_nav():
    page = CURRENT[0]
    home = page == 'index.html'
    p = '' if home else 'index.html'
    svc_pages = {u for u, _, _ in SERVICES}
    items = [
        ('home', '#home' if home else 'index.html', 'fa-house', 'Home', home),
        ('services', p + '#services', 'fa-layer-group', 'Services', page in svc_pages),
        ('work', p + '#work', 'fa-images', 'Work', False),
        ('help', 'help-support.html', 'fa-circle-question', 'Help', page == 'help-support.html'),
        ('contact', p + '#contact', 'fa-paper-plane', 'Contact', False),
    ]
    links = ''.join(f'<a href="{h}" data-tab="{k}"' + (' class="active"' if a else '') + f'><i class="fas {ic}"></i><span>{t}</span></a>' for k, h, ic, t, a in items)
    return f'<nav class="tabbar" aria-label="App navigation">{links}</nav>'

def footer(chat=False):
    svc = '\n'.join(f'                        <li><a href="{u}">{n}</a></li>' for u, n, _ in SERVICES)
    return f'''
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div>
                    {brand()}
                    <p>A digital studio from Syana, Bulandshahr building websites, apps, brands and films for businesses across UP and Delhi NCR.</p>
                    <div class="socials">
                        <a href="https://www.facebook.com/profile.php?id=61571168753695" target="_blank" rel="noopener" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="https://www.instagram.com/svd_star_edit?igsh=OGQ5ZDc2ODk2ZA==" target="_blank" rel="noopener" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="https://x.com/FirstHumaniti?s=09" target="_blank" rel="noopener" aria-label="X (Twitter)"><i class="fab fa-x-twitter"></i></a>
                        <a href="https://www.linkedin.com/in/sonu-saifii" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
                <div>
                    <h5>Services</h5>
                    <ul>
{svc}
                    </ul>
                </div>
                <div>
                    <h5>Company</h5>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="help-support.html">Help &amp; Support</a></li>
                        <li><a href="index.html#reviews">Client Reviews</a></li>
                        <li><a href="submit-review.html">Submit a Review</a></li>
                        <li><a href="terms-and-conditions.html">Terms &amp; Conditions</a></li>
                        <li><a href="privacy-policy.html">Privacy Policy</a></li>
                    </ul>
                </div>
                <div>
                    <h5>Contact</h5>
                    <ul>
                        <li><i class="fas fa-phone"></i><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
                        <li><i class="fas fa-envelope"></i><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                        <li><i class="fas fa-location-dot"></i>{ADDRESS}</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <span>&copy; <span data-year>2026</span> BulandTech. All rights reserved.</span>
                <span class="footer-legal"><a href="terms-and-conditions.html">Terms</a><a href="privacy-policy.html">Privacy</a><a href="help-support.html">Support</a></span>
            </div>
        </div>
    </footer>

    {bottom_nav()}
    <div class="fb-stack">
        <a href="tel:{PHONE_TEL}" class="fbtn fb-call" aria-label="Call BulandTech"><i class="fas fa-phone"></i><span class="fb-tip">Call now</span></a>
        <a href="{wa("Hello BulandTech")}" target="_blank" rel="noopener" class="fbtn fb-wa" aria-label="Chat on WhatsApp"><i class="fab fa-whatsapp"></i><span class="fb-tip">WhatsApp</span></a>
    </div>

    <script src="script.js"></script>
</body>
</html>
'''

def cta_band(title='Have a project in mind?', text='Tell us what you need — we reply within 24 hours with a plan and a clear quote.', wa_text='Hello BulandTech, I want to discuss a project.'):
    return f'''
    <section class="section" style="padding-top:0">
        <div class="container">
            <div class="cta-band" data-reveal>
                <div>
                    <h2>{title}</h2>
                    <p>{text}</p>
                </div>
                <div class="actions">
                    <a href="{wa(wa_text)}" target="_blank" rel="noopener" class="btn btn-wa"><i class="fab fa-whatsapp"></i> WhatsApp us</a>
                    <a href="index.html#contact" class="btn btn-ghost">Get a quote</a>
                </div>
            </div>
        </div>
    </section>
'''

# ----------------------------------------------------------------- portfolio data (REAL work only)
DESIGNS = [  # (path, caption, category)
    ('assetts/file_0000000024d081f5b910458ced9a3cd0.png', 'Elegant Floral Wedding Card', 'wedding'),
    ('assetts/file_0000000029c88211aa550e3a9a43901c.png', 'Modern Minimal Wedding Card', 'wedding'),
    ('assetts/file_00000000286c81f9bb6bd35a966eda1c.png', 'Royal Invitation', 'wedding'),
    ('assetts/file_00000000000881f9ab25c2c0cc91ec74.png', 'Traditional Motif Invitation', 'wedding'),
    ('assetts/file_00000000a21481f483380a7f4a4b549c.png', 'YouTube Thumbnail — Bold', 'thumbnail'),
    ('assetts/file_00000000770082468820283061e0d5ae.png', 'YouTube Thumbnail — Creator', 'thumbnail'),
    ('assetts/file_00000000cc10823083772bd22592d420.png', 'YouTube Thumbnail — Tutorial', 'thumbnail'),
    ('assetts/file_00000000edec81fd9ddec50f879a71f0.png', 'YouTube Thumbnail — Vlog', 'thumbnail'),
    ('assetts/file_00000000e42881f6b692a22fb38dde63.png', 'Event Banner', 'banner'),
    ('assetts/file_00000000604c81f5b65f32f719d62a16.png', 'Campaign Poster', 'banner'),
    ('assetts/file_000000001e80820cbc737096280e8bd6.png', 'Outdoor Hoarding', 'banner'),
    ('assetts/file_0000000017508246bbb8c91e9c399907.png', 'Promotional Poster', 'banner'),
    ('assetts/file_00000000343c81fd885debac5a6ec6fb.png', 'Brand Logo', 'logo'),
    ('assetts/file_00000000f10c8211b4e92fd189b73f9f.png', 'Brand Identity', 'logo'),
    ('assetts/file_000000002a3c820e8decacfed07b2d40.png', 'Lettermark Concept', 'logo'),
    ('assetts/file_0000000089ec81fdbd0cc5ab08117f88.png', 'Badge & Emblem', 'logo'),
    ('assetts/file_000000008dbc81fd8a3b6d0c63ed3e0d.png', 'Ghibli-style Artwork', 'illustration'),
    ('assetts/file_00000000b16c8211a8f2100c2dc5f261.png', 'Marketing Flyer', 'illustration'),
    ('assetts/file_000000008fa48230a025bd221d02521d.png', 'Election Pamphlet', 'illustration'),
    ('assetts/file_000000003ed0820e81c03aef7a39249c.png', 'Poster Illustration', 'illustration'),
    ('assetts/othrr/file_00000000b7ac81fab2ee1d783493a440.png', 'App Onboarding Flow', 'uiux'),
    ('assetts/file_00000000a2048230a0485d8944e33966.png', 'Dashboard Interface', 'uiux'),
    ('assetts/file_000000008df08211a947f0bb8fb8e8f4.png', 'Mobile Interaction Flow', 'uiux'),
    ('file_0000000041e88211bebb79ece6bce2d7.png', 'Prototype Mockup', 'uiux'),
    ('assetts/477A74F2-56A0-4FF2-9BF9-C5ECDB1E4D87.png', 'Kurukshetra — Film Poster', 'poster'),
    ('assetts/CB000B90-D661-498F-92A7-E90C48E55A4D.png', 'Single Release Poster', 'poster'),
    ('0F324B1B-964B-49EF-ADC4-535603FF61BE.png', 'Haryanvi Song Poster', 'poster'),
    ('assetts/24AF4FDE-A958-43FB-8FFE-C513A3A1AC10.png', 'EDM Single Poster', 'poster'),
]
CATS = [('wedding', 'Wedding Cards'), ('thumbnail', 'YouTube Thumbnails'), ('banner', 'Banners & Posters'),
        ('logo', 'Logo & Branding'), ('illustration', 'Illustration & Flyers'), ('uiux', 'UI / UX'),
        ('poster', 'Movie & Song Posters')]
CAT_NAME = dict(CATS)

VIDEOS = [  # (src, title, meta)
    ('media/wedding-teaser-2025.mp4', 'Wedding Teaser 2025', 'Wedding film · Teaser'),
    ('media/cinematic-wedding.mp4', 'Cinematic Wedding', 'Wedding film · Cinematic'),
    ('media/fast-cut-teaser.mp4', 'Fast-Cut Teaser', 'Wedding film · Fast cut'),
]
YOUTUBE = [('6flPNi1wDak', 'Syncbeat Edit', 'Music video · Beat-synced edit')]

APPS = [  # (name, category, desc, icon, play id)
    ('Bastiseva', 'Food & Grocery', 'Local food and grocery ordering app.', 'https://play-lh.googleusercontent.com/rAsdb1RxbkKQiA8cNcKURxkn7g1GJ1y5LlXuflyYGRRuIq47wUqWKCf70RU-y-tVhBukBXSJNyIWZSq9J_ja=s128', 'com.bulandtech.bastisevallp'),
    ('Doortap', 'Pick & Drop', 'Parcel pick-up and delivery booking.', 'https://play-lh.googleusercontent.com/4g-PT4-Fqvg-RnjE0lZCgMLARwtKJGTluYt-6JqAH5JOVQzpx_7Lfb9ddok3p340Bp45e1iedKzew4qQZakc=s128', 'com.bulandtech.speeddrop'),
    ('Weldify', 'Fabrication', 'Inventory and design catalogue for fabricators.', 'https://play-lh.googleusercontent.com/5pcwByLftYZNoF6PKirKsoySPkb8UBMTzJRBqoSiYm1OTDWClHQbI94MNTLuNtAi6KU36RlZpwVtgISIYV_m_g=s128', 'com.bulandtech.weldify'),
    ('EMI Calculator', 'Finance', 'Quick loan EMI and interest calculator.', 'https://play-lh.googleusercontent.com/UWe2sE76sJblTpE0W0Il6K-cFCVon61kGQBl8PlqXAsYMNufqxXpyZrT_OXRcK8rb44Tb7a2DW2kDRjEcQd7MfU=s128', 'com.bulandtech.emicalculator'),
    ('English Quiz', 'Education', 'Practice English with quick quizzes.', 'https://play-lh.googleusercontent.com/KCjhlKV9vxALhd0S2MgNXH53L7zcr5sibHemai9tb5mI9_CvWaBK51aubpAFQUb78kqLnoexqrh_WfvuM8wHWco=s128', 'com.bulandtech.englishquiz'),
    ('Veg Food Book', 'Food & Recipes', 'A cookbook of vegetarian recipes.', 'https://play-lh.googleusercontent.com/cSaSm0QSTQjAkVlKOSNct0A1_zaJ9e-IUh2NdB1xj7GQ8aniOB5DhvDX-Mf7PW65uRQQ9aGMpYrZP4DvyHwO4A=s128', 'com.bulandtech.vegfoodbook'),
    ('QR Reader', 'Utility', 'Fast QR and barcode scanner.', 'https://play-lh.googleusercontent.com/9Qs8Dc7kyeNJ6K6x3Mp4vVKW4r7qXUn0sN0ZDP-AvGcoYX3m0JuwLzhiz6GV9Q3m4_dEchOVBcy_mHd1TB_4aQ=s128', 'com.bulandtech.qrreader'),
]
def play(pid): return f'https://play.google.com/store/apps/details?id={pid}'

import re as _re
def web(src, small=False):
    slug = _re.sub(r'[^a-z0-9]+', '-', os.path.splitext(os.path.basename(src))[0].lower()).strip('-')
    return f'media/{slug}{"-sm" if small else ""}.webp'

def tile(src, cap, cat='', eager=False, big=False):
    return (f'<figure class="tile" data-lightbox data-cat="{cat}" data-title="{cap}">'
            f'<img src="{web(src, small=not big)}" data-full="{web(src)}" alt="{cap}" loading="{"eager" if eager else "lazy"}" decoding="async" width="1672" height="941">'
            f'<figcaption>{cap}<small>{CAT_NAME.get(cat, "")}</small></figcaption></figure>')

def video_card(src, title, meta):
    return f'''<article class="vcard" data-reveal>
                    <div class="vframe">
                        <video preload="none" playsinline poster="{src[:-4]}-poster.webp" src="{src}"></video>
                        <button class="vplay" aria-label="Play {title}"><i class="fas fa-play"></i></button>
                    </div>
                    <div class="vmeta"><h4>{title}</h4><span>{meta}</span></div>
                </article>'''

def yt_card(vid, title, meta):
    return f'''<article class="vcard" data-youtube="{vid}" data-title="{title}" data-reveal>
                    <div class="vframe">
                        <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{title}" loading="lazy">
                        <button class="vplay" aria-label="Play {title}"><i class="fas fa-play"></i></button>
                    </div>
                    <div class="vmeta"><h4>{title}</h4><span>{meta} <i class="fab fa-youtube" style="color:#ff3b30;margin-left:6px"></i></span></div>
                </article>'''

def app_card(a):
    name, cat, desc, icon, pid = a
    return f'''<a class="app" href="{play(pid)}" target="_blank" rel="noopener" data-reveal>
                    <img src="{icon}" alt="{name} app icon" loading="lazy" width="64" height="64">
                    <div class="app-body"><span class="app-cat">{cat}</span><h4>{name}</h4><p>{desc}</p></div>
                    <span class="app-get" aria-hidden="true"><i class="fab fa-google-play"></i></span>
                </a>'''

# ----------------------------------------------------------------- home page
REVIEWS = [
    ('Aamir Malik', 5, 'BulandTech ne meri website ekdum kamaal ki banayi hai! Expectations se bhi zyada acha kaam kiya.'),
    ('Sagar Lodhi', 5, 'App development ke liye best choice. Meri Android app bahut smooth chal rahi hai, koi bug nahi.'),
    ('Akash DJ', 5, 'Music production ka kaam top-notch! Jo beat banayi hai, ekdum fire hai. Next time fir yahin se karayenge.'),
    ('Aman Tyagi', 5, 'Digital marketing services se business ko bahut boost mila. Google Ads ka result bahut acha aaya.'),
    ('Ram Bhool Jadhav', 4, 'Video editing bahut professional hai. Mere YouTube channel ke liye perfect videos banate hain.'),
    ('Ramiya Sighaal', 5, 'Graphic design ke liye inki team best hai. Logo aur banners sab kuch creative aur unique banaya.'),
    ('Arif Ali', 5, 'Website development mein inka koi muqabla nahi. Responsive aur fast site mili hai.'),
    ('Akansha', 5, 'Meri e-commerce app bahut jaldi ready ho gayi. Customer support bhi super quick hai.'),
    ('Ajit Baisla', 5, 'Affordable price mein premium quality work. BulandTech team ko dil se shukriya!'),
    ('Rinku Jatav', 4, 'Social media marketing se engagement badh gaya. Acha laga inke saath kaam karke.'),
    ('Riyaj Maksood', 5, 'Meri company ki website ka SEO bahut improve hua hai. Traffic bhi badh gaya hai.'),
    ('Manisha Rani', 5, 'Video editing mein inka kaam bahut clean hai. Har detail par dhyan dete hain.'),
    ('Deepak Sharma', 5, 'App ka UI/UX design bahut user-friendly hai. Clients ko bahut pasand aa raha hai.'),
    ('Priya Singh', 4, 'Logo design ke liye BulandTech ko recommend karungi. Bahut creative ideas dete hain.'),
    ('Gaurav Kumar', 5, 'Website ki speed aur performance zabardast hai. Meri site ab top par rank kar rahi hai.'),
    ('Sonia Devi', 5, 'Music production mein inka talent next level hai. Meri album ke liye amazing tracks banaye.'),
    ('Rahul Gupta', 5, 'Digital marketing strategy bahut effective thi. Sales mein significant increase hua hai.'),
    ('Kiran Yadav', 4, 'App development process bahut smooth tha. Har step par update milta raha.'),
    ('Vikas Rana', 5, 'Graphic design mein inka kaam bahut modern hai. Meri brand ko ek naya look mila.'),
    ('Anjali Kumari', 5, 'Website ka design bahut attractive hai. Customers ko navigate karne mein easy lagta hai.'),
    ('Mohit Tyagi', 5, 'Video editing mein inki expertise lajawab hai. Mere short films ke liye perfect output diya.'),
    ('Pooja Verma', 4, 'App ki functionality bahut strong hai. Koi technical issue nahi aaya ab tak.'),
    ('Sandeep Singh', 5, 'BulandTech ki team bahut cooperative hai. Har query ka quick response milta hai.'),
    ('Neha Malik', 5, "Meri website ka content bahut engaging hai. Thanks to BulandTech's content writing."),
    ('Amit Kumar', 5, 'Music production mein inka sound quality bahut high hai. Studio level output milta hai.'),
    ('Ritu Sharma', 4, 'Digital marketing campaigns se brand awareness bahut badh gayi hai.'),
    ('Vijay Pal', 5, 'App development mein inka professionalism bahut acha hai. Time par delivery mili.'),
    ('Shweta Gupta', 5, 'Graphic design mein inka detailing bahut impressive hai. Har element perfect lagta hai.'),
    ('Harish Chandra', 5, 'Website ka maintenance aur support bhi bahut acha hai. Problem aati hai to turant solve karte hain.'),
    ('Kavita Devi', 4, 'Overall experience bahut acha raha. Next project bhi BulandTech se hi karayenge.'),
]
def review(r):
    name, stars, text = r
    initials = ''.join(w[0] for w in name.split()[:2]).upper()
    return (f'<div class="review"><div class="stars" aria-label="{stars} out of 5">{"★" * stars}{"☆" * (5 - stars)}</div>'
            f'<p>{html.escape(text)}</p><div class="who"><span class="avatar">{initials}</span>{name}</div></div>')

SVC_CARDS = [
    ('website-development.html', 'fa-code', 'Website Development', 'Fast, responsive, SEO-ready websites — from business sites to full e-commerce stores.', ['Business sites', 'E-commerce', 'Landing pages', 'SEO'], True),
    ('app-development.html', 'fa-mobile-screen', 'App Development', 'Android, iOS and cross-platform apps. Seven of our apps are live on Google Play.', ['Android', 'iOS', 'Flutter', 'Backend'], True),
    ('graphic-design.html', 'fa-pen-nib', 'Graphic Design', 'Logos, wedding cards, posters, thumbnails and complete brand identities.', ['Logos', 'Posters', 'Thumbnails'], False),
    ('video-editing.html', 'fa-film', 'Video Editing', 'Cinematic wedding films, reels, YouTube edits and beat-synced music videos.', ['Weddings', 'Reels', 'Colour grading'], False),
    ('web-design.html', 'fa-object-group', 'Web Design (UI/UX)', 'Wireframes, prototypes and design systems that make products easy to use.', ['Figma', 'Prototyping', 'Design systems'], False),
    ('digital-marketing.html', 'fa-chart-line', 'Digital Marketing', 'SEO, Google Ads and Meta ads that bring measurable leads to your business.', ['SEO', 'Google Ads', 'Meta Ads'], True),
    ('music-production.html', 'fa-headphones', 'Music Production', 'Beats, remixes, mixing & mastering and background scores for your projects.', ['Beats', 'Remix', 'Mix & master'], True),
]
def svc_card(i, c):
    url, icon, title, desc, tags, wide = c
    t = ''.join(f'<span>{x}</span>' for x in tags)
    return f'''<a href="{url}" class="svc{' wide' if wide else ''}" data-reveal>
                    <span class="num">0{i}</span>
                    <span class="svc-icon"><i class="fas {icon}"></i></span>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <div class="tags">{t}</div>
                    <span class="link-arrow">Explore service <i class="fas fa-arrow-right"></i></span>
                </a>'''

PRICING = [
    ('fa-code', 'Website Development', [('Basic Website', '₹5,000 – 15,000'), ('Business Website', '₹15,000 – 30,000'), ('E-commerce Website', '₹30,000 – 50,000+')], False),
    ('fa-mobile-screen', 'App Development', [('Simple App', '₹20,000 – 40,000'), ('Complex App', '₹40,000 – 80,000'), ('Enterprise App', '₹80,000 – 2,00,000+')], True),
    ('fa-chart-line', 'Digital Marketing', [('SEO Services', '₹5,000 – 15,000/mo'), ('Social Media Marketing', '₹8,000 – 20,000/mo'), ('Complete Package', '₹15,000 – 40,000/mo')], False),
    ('fa-pen-nib', 'Graphic Design', [('Logo Design', '₹2,000 – 5,000'), ('Branding Package', '₹10,000 – 25,000'), ('Social Media Post', '₹500 – 2,000')], False),
    ('fa-film', 'Video Editing', [('Basic Editing', '₹1,500 – 3,000'), ('Professional Editing', '₹3,000 – 8,000'), ('Cinematic Video', '₹8,000 – 20,000')], False),
    ('fa-headphones', 'Music Production', [('Beat Making', '₹2,000 – 5,000'), ('Remix Song', '₹3,000 – 8,000'), ('Original Song', '₹10,000 – 25,000')], False),
]
def price_card(p):
    icon, title, rows, featured = p
    lis = ''.join(f'<li><span>{a}</span><strong>{b}</strong></li>' for a, b in rows)
    badge = '<span class="badge">Most popular</span>' if featured else ''
    return f'''<div class="price{' featured' if featured else ''}" data-reveal>
                    {badge}
                    <div class="price-head"><i class="fas {icon}"></i><h3>{title}</h3></div>
                    <ul>{lis}</ul>
                    <a href="#contact" class="btn {'btn-primary' if featured else 'btn-ghost'} btn-block">Get a quote</a>
                </div>'''

def words(text, start=0):
    return ' '.join(f'<span class="w" style="--i:{start + i}"><span>{w}</span></span>' for i, w in enumerate(text.split()))

def build_index():
    home_designs = [DESIGNS[24], DESIGNS[0], DESIGNS[4], DESIGNS[26], DESIGNS[21], DESIGNS[12]]
    strip = ''.join(f'<span>{n}</span>' for n in ['Websites', 'Mobile Apps', 'Brand Identity', 'Wedding Films', 'YouTube Thumbnails', 'UI/UX Design', 'SEO & Ads', 'Music Production'])
    half = len(REVIEWS) // 2
    body = f'''{nav(home=True)}
    <main>
    <section class="hero" id="home">
        <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="container">
            <div>
                <span class="pill"><span class="dot"></span> Taking new projects · Bulandshahr, UP</span>
                <h1 class="eyebrow hero-kw">{SEO['index.html']['h1']}</h1>
                <p class="h1-display split">{words("We design, build &amp; grow brands that")} <span class="w" style="--i:8"><span class="serif grad-text">stand tall.</span></span></p>
                <p class="hero-lead">BulandTech is a digital studio for websites, mobile apps, graphic design, video editing and digital marketing — helping businesses across UP and Delhi NCR look sharp and sell more online.</p>
                <div class="hero-actions">
                    <a href="#work" class="btn btn-primary">See our work <i class="fas fa-arrow-right"></i></a>
                    <a href="{wa("Hello BulandTech, I want to discuss a project.")}" target="_blank" rel="noopener" class="btn btn-ghost"><i class="fab fa-whatsapp"></i> Chat on WhatsApp</a>
                </div>
                <div class="hero-stats">
                    <div><strong data-count="50" data-suffix="+">50+</strong><span>Projects delivered</span></div>
                    <div><strong data-count="40" data-suffix="+">40+</strong><span>Happy clients</span></div>
                    <div><strong data-count="7">7</strong><span>Apps on Google Play</span></div>
                </div>
            </div>
            <div class="hero-visual" aria-hidden="true">
                <div class="shot s1"><img src="{web(DESIGNS[24][0])}" alt="" fetchpriority="high"></div>
                <div class="shot s2"><img src="{web(DESIGNS[0][0], True)}" alt=""></div>
                <div class="shot s3"><img src="{web(DESIGNS[4][0], True)}" alt="" loading="lazy"></div>
                <div class="hero-badge"><i class="fab fa-google-play"></i><div><strong>7 live apps</strong><span>Published on Play Store</span></div></div>
            </div>
        </div>
    </section>

    <div class="strip" aria-hidden="true"><div class="strip-track" data-marquee>{strip}</div></div>

    <section class="section" id="services">
        <div class="container">
            <div class="section-head" data-reveal>
                <div>
                    <span class="eyebrow">What we do</span>
                    <h2>Everything your brand needs, <span class="serif">under one roof.</span></h2>
                </div>
                <p>One team for strategy, design, development and marketing — so your website, app and content all look and feel like the same brand.</p>
            </div>
            <div class="services-grid">
                {''.join(svc_card(i + 1, c) for i, c in enumerate(SVC_CARDS))}
            </div>
        </div>
    </section>

    <section class="section section-alt" id="work">
        <div class="container">
            <div class="section-head" data-reveal>
                <div>
                    <span class="eyebrow">Selected work</span>
                    <h2>Real projects, <span class="serif">real clients.</span></h2>
                </div>
                <p>A few pieces from our portfolio — design, film and apps we have shipped. Click any image to view it full size.</p>
            </div>

            <div class="work-block" data-reveal>
                <div class="work-block-head">
                    <h3>Graphic Design <small>{len(DESIGNS)} pieces</small></h3>
                    <a href="graphic-design.html#portfolio" class="link-arrow">View all designs <i class="fas fa-arrow-right"></i></a>
                </div>
                <div class="work-grid">
                    {''.join(tile(s, c, cat, eager=(i == 0), big=(i == 0)) for i, (s, c, cat) in enumerate(home_designs))}
                </div>
            </div>

            <div class="work-block">
                <div class="work-block-head" data-reveal>
                    <h3>Video Editing <small>{len(VIDEOS) + len(YOUTUBE)} films</small></h3>
                    <a href="video-editing.html#portfolio" class="link-arrow">View all films <i class="fas fa-arrow-right"></i></a>
                </div>
                <div class="video-grid">
                    {video_card(*VIDEOS[0])}
                    {yt_card(*YOUTUBE[0])}
                </div>
            </div>

            <div class="work-block">
                <div class="work-block-head" data-reveal>
                    <h3>Apps on Google Play <small>{len(APPS)} apps</small></h3>
                    <a href="app-development.html#portfolio" class="link-arrow">View all apps <i class="fas fa-arrow-right"></i></a>
                </div>
                <div class="apps-grid">
                    {''.join(app_card(a) for a in APPS[:6])}
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="process">
        <div class="container">
            <div class="section-head" data-reveal>
                <div>
                    <span class="eyebrow">How we work</span>
                    <h2>A simple process, <span class="serif">no surprises.</span></h2>
                </div>
                <p>Clear steps, regular updates and a fixed quote before we start.</p>
            </div>
            <div class="process">
                <div class="step" data-reveal><h4>Discovery call</h4><p>We understand your business, goals and budget — on call or WhatsApp.</p></div>
                <div class="step" data-reveal><h4>Plan &amp; quote</h4><p>Clear scope, timeline and fixed price. Work starts after ID verification and a 70% advance.</p></div>
                <div class="step" data-reveal><h4>Design &amp; build</h4><p>We share progress at every stage and refine it with your feedback.</p></div>
                <div class="step" data-reveal><h4>Launch &amp; support</h4><p>We go live, hand over everything and stay available for support.</p></div>
            </div>
        </div>
    </section>

    <section class="section section-alt" id="pricing">
        <div class="container">
            <div class="section-head" data-reveal>
                <div>
                    <span class="eyebrow">Pricing</span>
                    <h2>Transparent pricing <span class="serif">for every budget.</span></h2>
                </div>
                <p>Starting ranges for our most requested work. Every project gets a fixed quote after a short discussion.</p>
            </div>
            <div class="pricing-grid">
                {''.join(price_card(p) for p in PRICING)}
            </div>
            <p class="note"><i class="fas fa-circle-info"></i>Final price depends on scope. A valid ID and 70% advance are required before work begins — see our <a href="terms-and-conditions.html">Terms</a>.</p>
        </div>
    </section>

    <section class="section reviews" id="reviews">
        <div class="container">
            <div class="section-head center" data-reveal>
                <span class="eyebrow">Client reviews</span>
                <h2>What our clients <span class="serif">say about us.</span></h2>
            </div>
        </div>
        <div class="review-rows">
            <div class="review-track" data-marquee>{''.join(review(r) for r in REVIEWS[:half])}</div>
            <div class="review-track reverse" data-marquee>{''.join(review(r) for r in REVIEWS[half:])}</div>
        </div>
        <div class="container center" style="margin-top:40px">
            <a href="submit-review.html" class="link-arrow">Worked with us? Leave a review <i class="fas fa-arrow-right"></i></a>
        </div>
    </section>

{areas_section("website development, app development, video editing, graphic design and digital marketing")}
    <section class="section" id="contact">
        <div class="container contact-grid">
            <div data-reveal>
                <span class="eyebrow">Contact</span>
                <div class="section-head" style="margin-bottom:0"><h2>Let's build something <span class="serif">great together.</span></h2></div>
                <p style="color:var(--muted);margin-top:16px;font-size:17px">Share a few details and we will reply within 24 hours. Prefer to talk? Call or WhatsApp us directly.</p>
                <div class="contact-list">
                    <a class="contact-item" href="tel:+918265999762"><i class="fas fa-phone"></i><div><small>Call us</small><strong>+91 82659 99762</strong></div></a>
                    <a class="contact-item" href="mailto:support@bulandtech.in"><i class="fas fa-envelope"></i><div><small>Email</small><strong>support@bulandtech.in</strong></div></a>
                    <div class="contact-item"><i class="fas fa-location-dot"></i><div><small>Studio</small><strong>{ADDRESS}</strong></div></div>
                </div>
            </div>
            <form class="form" id="contactForm" data-formsubmit data-subject="New enquiry from bulandtech.in" data-success="Thank you! Your message has been sent — we will get back to you within 24 hours." data-reveal>
                <div class="form-row">
                    <div class="field"><label for="f-name">Your name</label><input id="f-name" type="text" name="name" placeholder="Full name" required autocomplete="name"></div>
                    <div class="field"><label for="f-phone">Phone</label><input id="f-phone" type="tel" name="phone" placeholder="+91" required autocomplete="tel"></div>
                </div>
                <div class="field"><label for="f-email">Email</label><input id="f-email" type="email" name="email" placeholder="you@company.com" required autocomplete="email"></div>
                <div class="field"><label for="f-service">Service</label>
                    <select id="f-service" name="service" required>
                        <option value="">Select a service</option>
                        {''.join(f'<option>{n}</option>' for _, n, _ in SERVICES)}
                        <option>Something else</option>
                    </select>
                </div>
                <div class="field"><label for="f-msg">Project details</label><textarea id="f-msg" name="message" placeholder="Tell us about your project, timeline and budget" required></textarea></div>
                <button type="submit" class="btn btn-primary btn-block">Send message <i class="fas fa-paper-plane"></i></button>
                <div class="form-msg" role="status" aria-live="polite"></div>
            </form>
        </div>
    </section>
    </main>
'''
    return head('BulandTech — Website, App, Design & Video Studio in Bulandshahr', 'index.html') + body + footer(chat=True)

# ----------------------------------------------------------------- service page template
def offers(items): return ''.join(f'<div class="offer" data-reveal><i class="fas fa-check"></i><span>{x}</span></div>' for x in items)
def tools(groups):
    return ''.join(f'<div class="tool-group" data-reveal><h4>{g}</h4><div class="chips">{"".join(f"<span>{t}</span>" for t in ts)}</div></div>' for g, ts in groups)
def whys(items): return ''.join(f'<div data-reveal><i class="fas {i}"></i><h4>{h}</h4><p>{p}</p></div>' for i, h, p in items)

def service_page(page, title_tag, eyebrow, h1, lead, wa_text, facts, offer_items, portfolio_html, tool_groups, why_items, tools_title='Tools &amp; technologies'):
    fx = ''.join(f'<span><i class="fas fa-circle-check"></i>{f}</span>' for f in facts)
    body = f'''{nav()}
    <main>
    <section class="page-hero">
        <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="container">
            <div class="crumbs"><a href="index.html">Home</a><i class="fas fa-chevron-right"></i><a href="index.html#services">Services</a><i class="fas fa-chevron-right"></i><span>{eyebrow}</span></div>
            <h1 class="eyebrow">{SEO.get(page, {}).get('h1') or eyebrow}</h1>
            <p class="h1-display">{h1}</p>
            <p class="lead">{lead}</p>
            <div class="hero-actions">
                <a href="{wa(wa_text)}" target="_blank" rel="noopener" class="btn btn-wa"><i class="fab fa-whatsapp"></i> Discuss on WhatsApp</a>
                <a href="index.html#pricing" class="btn btn-ghost">View pricing</a>
            </div>
            <div class="facts">{fx}</div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">What we offer</span><h2>Services <span class="serif">we deliver.</span></h2></div></div>
            <div class="offer-grid">{offers(offer_items)}</div>
        </div>
    </section>
{portfolio_html}
    <section class="section{' section-alt' if not portfolio_html else ''}">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">Toolkit</span><h2>{tools_title}</h2></div><p>Industry-standard software, used by a team that knows it well.</p></div>
            <div class="tools">{tools(tool_groups)}</div>
        </div>
    </section>

    <section class="section{' section-alt' if portfolio_html else ''}">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">Why BulandTech</span><h2>Why clients <span class="serif">choose us.</span></h2></div></div>
            <div class="why">{whys(why_items)}</div>
        </div>
    </section>
{faq_section(page)}{areas_section(SERVICE_SCHEMA.get(page, "our services").lower())}{cta_band(wa_text=wa_text)}
    </main>
'''
    return head(title_tag, page) + body + footer()

def portfolio_section(title_html, sub, inner):
    return f'''
    <section class="section section-alt" id="portfolio">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">Portfolio</span><h2>{title_html}</h2></div><p>{sub}</p></div>
            {inner}
        </div>
    </section>
'''

WHY_COMMON = [
    ('fa-bolt', 'Fast turnaround', 'Clear timelines and on-time delivery, every time.'),
    ('fa-rotate', 'Revisions included', 'We refine the work until you are happy with it.'),
    ('fa-indian-rupee-sign', 'Fair pricing', 'Premium quality at prices that suit local businesses.'),
    ('fa-headset', 'Direct support', 'Talk to the people doing the work — on call or WhatsApp.'),
]

def build_graphic():
    counts = {k: sum(1 for d in DESIGNS if d[2] == k) for k, _ in CATS}
    btns = f'<button class="active" data-filter="all">All<sup>{len(DESIGNS)}</sup></button>' + ''.join(
        f'<button data-filter="{k}">{n}<sup>{counts[k]}</sup></button>' for k, n in CATS)
    gallery = f'<div class="filters" role="toolbar" aria-label="Filter designs" data-reveal>{btns}</div><div class="gallery">' + ''.join(tile(s, c, cat) for s, c, cat in DESIGNS) + '</div>'
    return service_page('graphic-design.html', 'Graphic Design Services in Bulandshahr — BulandTech', 'Graphic Design',
        'Designs that make your brand <span class="serif grad-text">impossible to ignore.</span>',
        'From logos and wedding cards to film posters and YouTube thumbnails — we create visuals that look premium and communicate clearly.',
        "Hello BulandTech, I'm interested in your Graphic Design services.",
        [f'{len(DESIGNS)}+ portfolio pieces', 'Print &amp; digital ready', 'Source files included'],
        ['Logo Design &amp; Brand Identity', 'Wedding &amp; Event Invitations', 'Social Media Graphics &amp; Campaigns', 'YouTube Thumbnails', 'Posters, Banners &amp; Hoardings', 'Brochures, Flyers &amp; Pamphlets', 'UI/UX Design for Websites &amp; Apps', 'Packaging &amp; Presentation Design'],
        portfolio_section('Recent <span class="serif">design work.</span>', 'Filter by category and click any piece to view it full size.', gallery),
        [('Design &amp; Illustration', ['Adobe Photoshop', 'Adobe Illustrator', 'CorelDRAW', 'Affinity Designer', 'Procreate']),
         ('Layout &amp; Publishing', ['Adobe InDesign', 'QuarkXPress']),
         ('UI/UX &amp; Prototyping', ['Figma', 'Adobe XD', 'Sketch', 'InVision']),
         ('Quick &amp; Open-source', ['Canva', 'GIMP', 'Inkscape'])],
        [('fa-wand-magic-sparkles', 'Original concepts', 'Every design is made for your brand — no recycled templates.'), *WHY_COMMON[:3]])

def build_video():
    cards = ''.join(video_card(*v) for v in VIDEOS) + ''.join(yt_card(*y) for y in YOUTUBE)
    inner = f'<div class="video-grid">{cards}</div>'
    return service_page('video-editing.html', 'Video Editing Services in Bulandshahr — BulandTech', 'Video Editing',
        'Raw footage, turned into <span class="serif grad-text">cinematic stories.</span>',
        'Wedding films, teasers, reels and music videos — edited with cinematic pacing, clean colour grading and sound that hits.',
        "Hello BulandTech, I'm interested in your Video Editing services.",
        ['4K-ready exports', 'Colour grading', 'Optimised for YouTube &amp; Instagram'],
        ['Wedding Films, Teasers &amp; Highlights', 'YouTube &amp; Reels Editing', 'Music Videos &amp; Beat-Sync Edits', 'Brand Promos &amp; Product Ads', 'Corporate &amp; Training Videos', 'VFX &amp; Motion Graphics', 'Colour Grading &amp; LUT Design', 'Cinematic Trailers &amp; Intros'],
        portfolio_section('Recent <span class="serif">films &amp; edits.</span>', 'Press play to watch. Full-length films available on request.', inner),
        [('Editing', ['Adobe Premiere Pro', 'Final Cut Pro', 'DaVinci Resolve', 'CapCut Pro', 'VN']),
         ('Motion &amp; VFX', ['After Effects', 'Blender', 'Cinema 4D', 'Mocha Pro', 'Red Giant']),
         ('Audio &amp; Colour', ['Adobe Audition', 'Fairlight', 'iZotope RX', 'Color Finale'])],
        [('fa-clapperboard', 'Cinematic eye', 'Pacing, colour and music chosen to tell your story.'), *WHY_COMMON[:3]])

def build_app():
    inner = f'<div class="apps-grid">{"".join(app_card(a) for a in APPS)}</div>'
    return service_page('app-development.html', 'App Development Company in Bulandshahr — BulandTech', 'App Development',
        'Mobile apps that people <span class="serif grad-text">actually use.</span>',
        'We design and build Android, iOS and cross-platform apps — fast, secure and easy to use. Seven of our apps are live on Google Play today.',
        "Hi BulandTech, I'm interested in your App Development services.",
        [f'{len(APPS)} apps on Google Play', 'Android · iOS · Cross-platform', 'Play Store publishing'],
        ['Business &amp; E-commerce Apps', 'Booking &amp; Delivery Apps', 'Education &amp; Finance Apps', 'Music &amp; Video Streaming Apps', 'Custom Utility Tools', 'KaiOS Feature-Phone Apps', 'Admin Panels &amp; Backends', 'Play Store Publishing &amp; ASO'],
        portfolio_section('Apps <span class="serif">live on Google Play.</span>', 'Built and published by BulandTech. Tap any app to open it on the Play Store.', inner),
        [('Android', ['Java', 'Kotlin', 'Jetpack Compose']), ('iOS', ['Swift', 'SwiftUI']),
         ('Cross-platform', ['Flutter', 'React Native', 'Ionic']), ('Web apps (PWA)', ['Next.js', 'Vue.js', 'Angular']),
         ('Backend', ['Node.js', 'Python (FastAPI / Django)', 'Laravel', 'Firebase']), ('Databases', ['MySQL', 'PostgreSQL', 'MongoDB', 'Firebase'])],
        [('fa-shield-halved', 'Secure &amp; scalable', 'Clean architecture that grows with your users.'), ('fa-wand-magic-sparkles', 'Modern UI/UX', 'Interfaces designed for real people, not just screenshots.'), *WHY_COMMON[:2]])

def build_web():
    return service_page('website-development.html', 'Website Development Company in Bulandshahr — BulandTech', 'Website Development',
        'Websites that load fast and <span class="serif grad-text">bring in business.</span>',
        'We build fast, responsive and secure websites tailored to your business — from personal portfolios to full-scale e-commerce platforms.',
        'Hi BulandTech, I want to know more about your Website Development service.',
        ['Mobile-first &amp; responsive', 'SEO-ready', 'Hosting &amp; domain setup'],
        ['Business Websites', 'E-commerce Stores', 'Portfolio &amp; Resume Sites', 'Landing Pages', 'Custom Web Portals', 'Website Maintenance &amp; Support'],
        '',
        [('Frontend', ['HTML5', 'CSS3', 'JavaScript', 'React', 'Next.js']), ('Backend', ['Node.js', 'PHP', 'Laravel', 'Python (Django, Flask)']),
         ('Database', ['MySQL', 'MongoDB', 'Firebase']), ('Hosting', ['AWS', 'Hostinger', 'DigitalOcean', 'Vercel'])],
        [('fa-gauge-high', 'Built for speed', 'Lightweight, optimised pages that rank and convert.'), ('fa-magnifying-glass', 'SEO from day one', 'Clean structure, meta tags and local SEO built in.'), *WHY_COMMON[:2]])

def build_webdesign():
    return service_page('web-design.html', 'Web Design &amp; UI/UX Services — BulandTech', 'Web Design (UI/UX)',
        'Interfaces that feel <span class="serif grad-text">effortless to use.</span>',
        'We design responsive, user-centred websites and app interfaces that reflect your brand and turn visitors into customers.',
        "Hello BulandTech, I'm interested in your Web Design services.",
        ['Figma-first workflow', 'Clickable prototypes', 'Developer-ready handoff'],
        ['Custom Website Design', 'UI/UX Wireframing &amp; Prototyping', 'Landing Page Design', 'Dashboard &amp; Web App UI', 'E-commerce Storefront Design', 'Design Systems &amp; Component Libraries'],
        '',
        [('UI/UX &amp; Web Design', ['Figma', 'Adobe XD', 'Sketch', 'Framer', 'Webflow']), ('Prototyping', ['ProtoPie', 'Principle', 'Axure RP']),
         ('AI-assisted', ['Uizard', 'Relume AI', 'Midjourney']), ('Handoff', ['Figma Dev Mode', 'Zeplin', 'Notion'])],
        [('fa-ruler-combined', 'Pixel-perfect', 'Responsive layouts that look right on every screen.'), ('fa-arrow-trend-up', 'Built to convert', 'Design decisions driven by clarity and conversions.'), *WHY_COMMON[:2]])

def build_marketing():
    return service_page('digital-marketing.html', 'Digital Marketing &amp; SEO Company in Bulandshahr — BulandTech', 'Digital Marketing',
        'Marketing that brings <span class="serif grad-text">measurable growth.</span>',
        'SEO, Google Ads and social media campaigns that put your business in front of the right customers — with clear reports on what is working.',
        "Hello BulandTech, I'm interested in your Digital Marketing services.",
        ['Local SEO', 'Google &amp; Meta Ads', 'Monthly reports'],
        ['Search Engine Optimisation (SEO)', 'Google Ads &amp; PPC Campaigns', 'Facebook &amp; Instagram Ads', 'Social Media Management', 'Content Strategy &amp; Copywriting', 'Email &amp; WhatsApp Marketing', 'YouTube &amp; Video Ads', 'Analytics &amp; Reporting'],
        '',
        [('SEO &amp; Analytics', ['Google Analytics 4', 'Search Console', 'Ahrefs', 'SEMrush', 'Screaming Frog']),
         ('Advertising', ['Google Ads', 'Meta Business Suite', 'LinkedIn Ads']),
         ('Content &amp; Social', ['Canva Pro', 'Buffer', 'Hootsuite', 'Notion']),
         ('Automation', ['HubSpot CRM', 'Zapier', 'Mailchimp'])],
        [('fa-chart-pie', 'ROI-focused', 'Every rupee tracked against leads and sales.'), ('fa-file-lines', 'Transparent reports', 'Clear monthly reports — no vanity metrics.'), *WHY_COMMON[2:]],
        tools_title='Tools &amp; platforms')

def build_music():
    inner = f'''<div class="empty-state" data-reveal>
                <i class="fas fa-headphones"></i>
                <h3>Samples available on request</h3>
                <p>Tell us the genre you need — Haryanvi, Bollywood, hip-hop, drill, lo-fi or EDM — and we will send matching samples from our recent work on WhatsApp.</p>
                <a href="{wa("Hello BulandTech, please share music production samples.")}" target="_blank" rel="noopener" class="btn btn-wa"><i class="fab fa-whatsapp"></i> Request samples</a>
            </div>'''
    return service_page('music-production.html', 'Music Production Studio in Bulandshahr — BulandTech', 'Music Production',
        'Beats and mixes that sound <span class="serif grad-text">studio-ready.</span>',
        'Beat making, remixes, mixing &amp; mastering and background scores for artists, creators and brands — produced to industry standards.',
        "Hello BulandTech, I'm interested in your Music Production services.",
        ['All genres', 'Mixing &amp; mastering', 'Stems delivered'],
        ['Beat Making (Hip-Hop, Lo-Fi, EDM, Trap, Pop, Bollywood)', 'Audio Mixing &amp; Mastering', 'Vocal Processing &amp; Pitch Correction', 'Song Arrangement &amp; Composition', 'Background Scores &amp; Jingles', 'Remix &amp; Mashup Production', 'Podcast Editing &amp; Audio Restoration', 'Sound Design for Ads, Games &amp; Films'],
        portfolio_section('Hear our <span class="serif">sound.</span>', 'Every track is made for a client, so we share samples privately.', inner),
        [('DAWs', ['FL Studio', 'Ableton Live', 'Logic Pro', 'Cubase Pro', 'Studio One', 'Pro Tools']),
         ('Plugins', ['FabFilter', 'Waves', 'iZotope Ozone', 'Serum', 'Kontakt', 'Omnisphere']),
         ('Vocal &amp; Repair', ['Melodyne', 'Auto-Tune Pro', 'iZotope RX', 'Soundtoys'])],
        [('fa-sliders', 'Studio-grade sound', 'Mixes that translate on phones, cars and speakers.'), *WHY_COMMON[:3]])

# ----------------------------------------------------------------- simple pages
def simple_page(page, title, eyebrow, h1, lead, content, desc=None):
    body = f'''{nav()}
    <main>
    <section class="page-hero">
        <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="container">
            <div class="crumbs"><a href="index.html">Home</a><i class="fas fa-chevron-right"></i><span>{eyebrow}</span></div>
            <h1 class="eyebrow">{SEO.get(page, {}).get('h1') or eyebrow}</h1>
            <p class="h1-display">{h1}</p>
            <p class="lead">{lead}</p>
        </div>
    </section>
    <section class="section">
        <div class="container"><div class="prose{' prose-wide' if page == 'submit-review.html' else ''}">{content}</div></div>
    </section>
    </main>
'''
    return head(title, page, desc) + body + footer()

def build_review():
    stars = ''.join(f'<input type="radio" id="st{n}" name="rating" value="{n} star" required><label for="st{n}" title="{n} star"><i class="fas fa-star"></i></label>' for n in range(5, 0, -1))
    options = ''.join(f'<option>{n}</option>' for _, n, _ in SERVICES)
    content = f'''
        <div class="review-layout">
            <form class="form review-form" id="reviewForm" data-formsubmit data-subject="New review from bulandtech.in" data-success="Shukriya! Aapka review mil gaya hai. Verify karne ke baad hum ise website par laga denge." data-reveal>
                <h2 style="margin-top:0"><i class="fas fa-star"></i> Write your review</h2>
                <div class="field"><label>Your rating</label><div class="star-input" role="radiogroup" aria-label="Rating">{stars}</div></div>
                <div class="form-row">
                    <div class="field"><label for="r-name">Your name</label><input id="r-name" name="name" required autocomplete="name" placeholder="Jaise: Rahul Sharma"></div>
                    <div class="field"><label for="r-city">City</label><input id="r-city" name="city" autocomplete="address-level2" placeholder="Jaise: Bulandshahr"></div>
                </div>
                <div class="form-row">
                    <div class="field"><label for="r-phone">Phone (sirf verification ke liye)</label><input id="r-phone" type="tel" name="phone" required autocomplete="tel" placeholder="+91"></div>
                    <div class="field"><label for="r-service">Service used</label><select id="r-service" name="service" required><option value="">Select service</option>{options}</select></div>
                </div>
                <div class="field"><label for="r-text">Your review</label><textarea id="r-text" name="review" required minlength="10" placeholder="Apne shabdon me likhiye — Hindi, English ya Hinglish, jaise aap chahein."></textarea></div>
                <label class="check"><input type="checkbox" name="publish_permission" value="Yes - BulandTech may publish my name, city and review" required> <span>Main BulandTech ko apna naam, city aur review website par dikhane ki permission deta/deti hoon.</span></label>
                <button type="submit" class="btn btn-primary btn-block">Submit review <i class="fas fa-paper-plane"></i></button>
                <div class="form-msg" role="status" aria-live="polite"></div>
            </form>
            <aside class="review-policy" data-reveal>
                <h2 style="margin-top:0"><i class="fas fa-shield-halved"></i> Our review policy</h2>
                <p>Hum sirf unhi logon ke reviews lagate hain jinhone sach me hamari service li hai.</p>
                <ul>
                    <li>Har review publish hone se pehle phone se verify hota hai.</li>
                    <li>Review aapke apne shabdon me lagta hai. Hum text badalte nahi hain.</li>
                    <li>Achha ho ya bura, har asli review ka swagat hai.</li>
                    <li>Hum review ke badle koi paisa ya discount nahi dete.</li>
                    <li>Aapka phone number kabhi publish nahi hota.</li>
                </ul>
                <p class="hi">Review hatwana ya badalna hai? <a href="{wa("Hello BulandTech, I want to update my review.")}" target="_blank" rel="noopener">WhatsApp karein</a>.</p>
            </aside>
        </div>'''
    return simple_page('submit-review.html', 'Submit a Review — BulandTech', 'Submit a Review',
        'Share your <span class="serif grad-text">experience.</span>',
        'BulandTech ke saath kaam kiya hai? Do line me bataiye kaisa laga — aapka review dusre logon ko sahi faisla lene me madad karta hai.', content,
        desc='Submit a review for BulandTech. Share your experience with our website, app, design, video or marketing services.')

def sec(icon, title, en, hi='', items=None):
    out = f'<h2 data-reveal><i class="fas {icon}"></i> {title}</h2>'
    out += f'<p>{en}</p>'
    if hi:
        out += f'<p class="hi">{hi}</p>'
    if items:
        out += '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
    return out

def contact_card(title='Contact us / हमसे संपर्क करें', text='Questions? Reach us any time:'):
    return f'''<div class="card" data-reveal><h3 style="margin-top:0">{title}</h3>
            <p class="hi">{text}</p>
            <p><i class="fas fa-phone ic"></i> <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
            <p><i class="fab fa-whatsapp ic"></i> <a href="{wa("Hello BulandTech")}" target="_blank" rel="noopener">WhatsApp {PHONE}</a></p>
            <p><i class="fas fa-envelope ic"></i> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
            <p><i class="fas fa-location-dot ic"></i> {ADDRESS}</p></div>'''

UPDATED = 'Last updated: 16 November 2026'

PAYMENT_BOX = '''<div class="highlight-box" data-reveal>
            <div class="hb-item"><i class="fas fa-id-card"></i><div><strong>Valid ID first</strong><span>A valid government photo ID (Aadhaar, PAN, Voter ID, Driving Licence or Passport) is required before any work starts.</span></div></div>
            <div class="hb-item"><i class="fas fa-indian-rupee-sign"></i><div><strong>70% advance</strong><span>70% of the quoted amount is paid in advance. Work begins only after it is received.</span></div></div>
            <div class="hb-item"><i class="fas fa-flag-checkered"></i><div><strong>30% on delivery</strong><span>The remaining 30% is paid before final files, source code or live handover.</span></div></div>
        </div>'''

# ----------------------------------------------------------------- Terms & Conditions
def build_terms():
    content = (
        f'<p>These Terms &amp; Conditions apply to every project, service and purchase made with BulandTech ("we", "us", "our"). By confirming a quote, paying an advance or using our services, you ("client") agree to these terms.</p>'
        '<p class="hi">BulandTech के साथ कोई भी काम शुरू करने से पहले कृपया ये नियम ध्यान से पढ़ें। Quote confirm करने या advance देने पर आप इन नियमों से सहमत माने जाएंगे।</p>'
        + PAYMENT_BOX
        + sec('fa-id-card', '1. Identity verification / पहचान सत्यापन',
              'Before any work begins, the client must share a valid government-issued photo ID. The name on the ID should match the person or business placing the order. We may decline a project if verification is not completed.',
              'कोई भी काम शुरू होने से पहले client को एक valid government photo ID देनी होगी। ID के बिना कोई काम शुरू नहीं होगा।',
              ['Accepted IDs: Aadhaar Card, PAN Card, Voter ID, Driving Licence or Passport', 'For businesses: GST certificate or a business registration document may also be requested', 'ID details are used only for verification — see our <a href="privacy-policy.html">Privacy Policy</a>'])
        + sec('fa-indian-rupee-sign', '2. Payment terms / भुगतान की शर्तें',
              'All projects follow a 70 / 30 payment structure unless agreed otherwise in writing.',
              'हर काम से पहले कुल राशि का 70% advance लिया जाएगा। बाकी 30% final delivery से पहले देना होगा।',
              ['<strong>70% advance</strong> of the quoted amount must be paid before work starts', '<strong>30% balance</strong> must be paid before final delivery, source files, app publishing or website go-live', 'Monthly services (SEO, social media, ads management) are billed in advance at the start of each month', 'Payments are accepted by UPI, bank transfer or other methods we confirm in writing', 'Work may be paused if a payment is overdue'])
        + sec('fa-file-signature', '3. Quotes &amp; scope',
              'Every project is based on a written quote describing the scope, deliverables and timeline. Work outside the agreed scope is quoted and billed separately.',
              items=['Quotes are valid for 15 days from the date they are shared', 'Timelines start after the advance, ID and all required content are received'])
        + sec('fa-boxes-stacked', '4. Client responsibilities',
              'The client is responsible for providing accurate information, content (text, images, logos, product details) and timely feedback. Delays in content or feedback extend the timeline accordingly.',
              items=['The client confirms they own or have the right to use all content they provide', 'We are not responsible for legal issues arising from content supplied by the client'])
        + sec('fa-rotate', '5. Revisions',
              'Each quote includes a reasonable number of revision rounds as stated in the quote. Additional revisions or major changes after approval may be charged extra.')
        + sec('fa-receipt', '6. Third-party costs',
              'Costs charged by third parties are paid by the client and are not part of our service fee unless stated in the quote.',
              items=['Domain names, hosting and SSL certificates', 'Google Play / Apple developer account fees', 'Paid plugins, stock images, fonts or music licences', 'Advertising budget for Google, Meta or other ad platforms'])
        + sec('fa-copyright', '7. Ownership &amp; portfolio rights',
              'Ownership of the final deliverables is transferred to the client after full payment (100%) is received. Until then, all work remains the property of BulandTech.',
              items=['We may show completed work in our portfolio and social media unless the client asks us in writing not to', 'Pre-existing tools, code libraries and templates used by us remain our property or that of their owners'])
        + sec('fa-ban', '8. Cancellation &amp; refunds',
              'If the client cancels a project after work has started, the advance is non-refundable as it covers time and resources already committed. If BulandTech is unable to start the project, the advance will be refunded in full.',
              'काम शुरू होने के बाद project cancel करने पर advance वापस नहीं होगा।')
        + sec('fa-clock', '9. Delivery &amp; delays',
              'We aim to deliver within the agreed timeline. We are not liable for delays caused by late content, late payments, third-party services (hosting, app stores, ad platforms) or events beyond our control.')
        + sec('fa-headset', '10. Support after delivery',
              'Free support for bug fixes related to our own work is provided for the period mentioned in the quote. New features, content updates and maintenance after that period are charged separately.')
        + sec('fa-user-secret', '11. Confidentiality',
              'We keep your business information, login details and documents confidential and use them only to complete your project.')
        + sec('fa-scale-balanced', '12. Limitation of liability',
              'Our total liability for any claim is limited to the amount paid by the client for the specific service. We are not liable for indirect losses such as loss of profit, data or business.')
        + sec('fa-gavel', '13. Governing law',
              'These terms are governed by the laws of India. Any dispute is subject to the jurisdiction of the courts of Bulandshahr, Uttar Pradesh.')
        + sec('fa-pen-to-square', '14. Changes to these terms',
              'We may update these terms from time to time. The version published on this page at the time you confirm a project applies to that project.')
        + contact_card('Questions about these terms?', 'We are happy to explain anything before you start:'))
    return simple_page('terms-and-conditions.html', 'Terms &amp; Conditions — BulandTech', 'Terms &amp; Conditions',
        'Terms &amp; <span class="serif grad-text">Conditions.</span>', UPDATED, content,
        desc='BulandTech terms and conditions — valid ID and 70% advance payment required before any work starts, payment terms, revisions, ownership and refunds.')

# ----------------------------------------------------------------- Privacy Policy
def build_privacy():
    content = (
        '<p>At BulandTech, we respect your privacy. This policy explains what personal information we collect, why we collect it and how we keep it safe when you use our website or services.</p>'
        '<p class="hi">BulandTech आपकी गोपनीयता का सम्मान करता है। यह policy बताती है कि हम कौन सी जानकारी लेते हैं, क्यों लेते हैं और उसे कैसे सुरक्षित रखते हैं।</p>'
        + PAYMENT_BOX
        + sec('fa-database', 'Information we collect / हम क्या जानकारी लेते हैं', 'We collect only what we need to deliver your project:',
              items=['<strong>Contact details</strong> — name, phone, email and address', '<strong>Identity proof</strong> — a copy or details of a valid government photo ID, collected before any work starts', '<strong>Payment records</strong> — amount, date and transaction reference of advance and balance payments (we never store card or UPI PINs)', '<strong>Project information</strong> — requirements, content, logos and files you share', '<strong>Website usage</strong> — IP address, browser, device and pages visited'])
        + sec('fa-id-card', 'Why we collect your ID / ID क्यों ली जाती है',
              'A valid ID is required before any work begins. It helps us confirm that orders are genuine, protects both parties from fraud and keeps a clear record of who the project belongs to.',
              'कोई भी काम शुरू करने से पहले valid ID ली जाती है ताकि order genuine हो और fraud से दोनों पक्ष सुरक्षित रहें।',
              ['ID is used only for verification and billing records', 'It is never shared, sold or published', 'Access is limited to the BulandTech team handling your project', 'You may ask us to delete your ID copy once the project is complete and all payments are settled'])
        + sec('fa-gears', 'How we use your information', 'We use your information to:',
              items=['Respond to enquiries and send quotations', 'Verify identity and record advance (70%) and balance (30%) payments', 'Plan, build and deliver your project', 'Send project updates and support', 'Send offers — only with your permission'])
        + sec('fa-share-nodes', 'Information sharing', 'We do not sell, rent or trade your personal information. We share it only:',
              items=['With service providers needed for your project (hosting, domain, app stores, ad platforms)', 'When required by law or a government authority', 'When you give us explicit permission'])
        + sec('fa-lock', 'Data security', 'We use reasonable technical and organisational measures to protect your data, including restricted access, secure storage and regular updates. No method of transmission over the internet is 100% secure, but we work hard to protect your information.')
        + sec('fa-box-archive', 'Data retention', 'We keep project and payment records for as long as needed for support, accounting and legal obligations. ID copies are kept only as long as necessary for verification and records.')
        + sec('fa-cookie-bite', 'Cookies &amp; third-party tools', 'Our website may use cookies and third-party tools (such as the live chat widget, Google Fonts and embedded YouTube videos) to work properly and understand traffic. You can disable cookies in your browser settings.')
        + sec('fa-user-check', 'Your rights', 'You can ask us to:',
              items=['Access the personal information we hold about you', 'Correct or update your information', 'Delete your information (subject to legal and payment records)', 'Stop marketing messages at any time'])
        + sec('fa-child', "Children's privacy", 'Our services are not intended for anyone under 18. We do not knowingly collect information from children; a parent or guardian must place orders on their behalf.')
        + sec('fa-gavel', 'Legal compliance', "We comply with India's Information Technology Act, 2000, the Digital Personal Data Protection Act, 2023 and other applicable laws.")
        + sec('fa-pen-to-square', 'Changes to this policy', 'We may update this policy from time to time. The latest version will always be available on this page.')
        + contact_card('Contact us / हमसे संपर्क करें', 'For privacy questions or to exercise your data rights:')
        + '<p class="hi" style="margin-top:32px">By using our website or services, you agree to this Privacy Policy and our <a href="terms-and-conditions.html">Terms &amp; Conditions</a>.</p>')
    return simple_page('privacy-policy.html', 'Privacy Policy — BulandTech', 'Privacy Policy',
        'Privacy <span class="serif grad-text">Policy.</span>', UPDATED, content,
        desc='Privacy Policy of BulandTech — how we collect, use and protect your personal information, including ID verification and payment records.')

# ----------------------------------------------------------------- About Us
def build_about():
    vals = [('fa-handshake', 'Honest work', 'Clear quotes, real portfolio and no hidden charges.'),
            ('fa-bolt', 'Fast delivery', 'Clear timelines and regular updates on every project.'),
            ('fa-wand-magic-sparkles', 'Creative quality', 'Design, film and code that look premium and work well.'),
            ('fa-people-group', 'Local &amp; personal', 'Talk directly to the people doing your work.')]
    body = f'''{nav()}
    <main>
    <section class="page-hero">
        <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="container">
            <div class="crumbs"><a href="index.html">Home</a><i class="fas fa-chevron-right"></i><span>About Us</span></div>
            <h1 class="eyebrow">{SEO['about.html']['h1']}</h1>
            <p class="h1-display">A small-town studio with <span class="serif grad-text">big ambitions.</span></p>
            <p class="lead">BulandTech is a digital studio from Syana, Bulandshahr. We help businesses, creators and families across UP and Delhi NCR go online, look professional and grow — with websites, apps, design, video and marketing under one roof.</p>
        </div>
    </section>

    <section class="section">
        <div class="container about-grid">
            <div data-reveal>
                <span class="eyebrow">Our story</span>
                <h2 class="h2">Why we started <span class="serif">BulandTech.</span></h2>
                <p>"Buland" means high, strong and confident — and that is exactly how we want every client's brand to stand. We started BulandTech in Syana because local businesses deserve the same quality of digital work that big-city companies get, at prices that make sense.</p>
                <p>Today we design and build websites, publish Android apps on Google Play, create wedding cards, posters and thumbnails, edit cinematic wedding films and run marketing campaigns — all from one team that you can call, message or meet.</p>
                <p>BulandTech is founded and led by <strong>Sonu Saifi</strong>.</p>
            </div>
            <div class="about-visual" data-reveal>
                <img src="{web(DESIGNS[24][0])}" alt="Kurukshetra film poster designed by BulandTech" loading="lazy">
                <img src="{web(DESIGNS[0][0], True)}" alt="Wedding card designed by BulandTech" loading="lazy">
            </div>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <div class="stats-row" data-reveal>
                <div><strong data-count="50" data-suffix="+">50+</strong><span>Projects delivered</span></div>
                <div><strong data-count="40" data-suffix="+">40+</strong><span>Happy clients</span></div>
                <div><strong data-count="7">7</strong><span>Apps on Google Play</span></div>
                <div><strong data-count="7">7</strong><span>Services under one roof</span></div>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">What we believe</span><h2>Our <span class="serif">values.</span></h2></div></div>
            <div class="why">{whys(vals)}</div>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">What we do</span><h2>Seven services, <span class="serif">one team.</span></h2></div><p>Pick one service or combine them — your brand stays consistent everywhere.</p></div>
            <div class="offer-grid">{''.join(f'<a class="offer" href="{u}" data-reveal><i class="fas {ic}"></i><span>{n}</span></a>' for u, n, ic in SERVICES)}</div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="section-head" data-reveal><div><span class="eyebrow">How we work</span><h2>Simple, safe <span class="serif">and transparent.</span></h2></div><p>Every project follows the same clear process.</p></div>
            {PAYMENT_BOX}
        </div>
    </section>
{cta_band()}
    </main>
'''
    return head('About Us — BulandTech, Syana Bulandshahr', 'about.html',
                'About BulandTech — a digital studio in Syana, Bulandshahr offering website development, app development, graphic design, video editing and digital marketing.') + body + footer()

# ----------------------------------------------------------------- Help & Support
FAQS = [
    ('How do I start a project?', 'Call or WhatsApp us, or fill the contact form. We discuss your needs, share a written quote, and start once your ID is verified and the 70% advance is received.'),
    ('What documents do you need before starting?', 'A valid government photo ID — Aadhaar, PAN, Voter ID, Driving Licence or Passport. Businesses may also be asked for a GST or registration document.'),
    ('How does payment work?', '70% of the quoted amount is paid in advance and 30% before final delivery or go-live. Monthly services are billed at the start of each month. We accept UPI and bank transfer.'),
    ('How long will my project take?', 'It depends on the scope. A basic website usually takes 7–15 days, an app 3–8 weeks, and designs or video edits a few days. Your quote mentions the exact timeline.'),
    ('How many revisions do I get?', 'Every quote includes revision rounds. Extra rounds or major changes after approval may be charged separately.'),
    ('Do you provide support after delivery?', 'Yes. Bug fixes related to our work are free for the support period mentioned in your quote. Updates and new features after that are charged separately.'),
    ('Can I get a refund?', 'If we are unable to start your project, the advance is refunded in full. Once work has started, the advance is non-refundable. See our Terms &amp; Conditions for details.'),
    ('Who pays for domain, hosting and Play Store fees?', 'These third-party costs are paid by the client unless they are included in your quote. We help you buy and set them up.'),
    ('How do I check my project status?', 'Message us on WhatsApp with your name and project — we share an update the same day.'),
    ('How can I leave a review?', 'Contact us for your personal review link. We publish reviews only from verified clients.'),
]
def build_help():
    faqs = ''.join(f'<details class="faq" data-reveal><summary>{q}<i class="fas fa-plus"></i></summary><p>{a}</p></details>' for q, a in FAQS)
    body = f'''{nav()}
    <main>
    <section class="page-hero">
        <div class="blobs" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="container">
            <div class="crumbs"><a href="index.html">Home</a><i class="fas fa-chevron-right"></i><span>Help &amp; Support</span></div>
            <h1 class="eyebrow">{SEO['help-support.html']['h1']}</h1>
            <p class="h1-display">How can we <span class="serif grad-text">help you?</span></p>
            <p class="lead">Questions about a project, payment or delivery? Reach us on any channel below, or find quick answers in the FAQ.</p>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="support-grid">
                <a class="support-card" href="tel:{PHONE_TEL}" data-reveal><i class="fas fa-phone"></i><h3>Call us</h3><p>Talk to us directly about your project.</p><span>{PHONE}</span></a>
                <a class="support-card wa" href="{wa("Hello BulandTech, I need help.")}" target="_blank" rel="noopener" data-reveal><i class="fab fa-whatsapp"></i><h3>WhatsApp</h3><p>Fastest way to get updates and share files.</p><span>Chat now</span></a>
                <a class="support-card" href="mailto:{EMAIL}" data-reveal><i class="fas fa-envelope"></i><h3>Email</h3><p>For documents, quotes and detailed requests.</p><span>{EMAIL}</span></a>
                <div class="support-card" data-reveal><i class="fas fa-location-dot"></i><h3>Visit us</h3><p>{ADDRESS}</p><span>By appointment</span></div>
            </div>
        </div>
    </section>

    <section class="section section-alt">
        <div class="container faq-wrap">
            <div data-reveal>
                <span class="eyebrow">FAQ</span>
                <h2 class="h2">Frequently asked <span class="serif">questions.</span></h2>
                <p class="muted">Can't find your answer? Message us — we usually reply within 24 hours.</p>
                <div class="faq-links">
                    <a href="terms-and-conditions.html" class="link-arrow">Terms &amp; Conditions <i class="fas fa-arrow-right"></i></a>
                    <a href="privacy-policy.html" class="link-arrow">Privacy Policy <i class="fas fa-arrow-right"></i></a>
                    <a href="submit-review.html" class="link-arrow">Submit a review <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>
            <div class="faq-list">{faqs}</div>
        </div>
    </section>
{cta_band('Still need help?', 'Our team is one call or message away.', 'Hello BulandTech, I need help.')}
    </main>
'''
    return head('Help &amp; Support — BulandTech', 'help-support.html',
                'BulandTech help and support — contact by phone, WhatsApp or email, and answers to common questions about payments, ID verification, timelines and revisions.') + body + footer()

PAGES = {
    'index.html': build_index, 'graphic-design.html': build_graphic, 'video-editing.html': build_video,
    'app-development.html': build_app, 'website-development.html': build_web, 'web-design.html': build_webdesign,
    'digital-marketing.html': build_marketing, 'music-production.html': build_music,
    'submit-review.html': build_review, 'privacy-policy.html': build_privacy,
    'terms-and-conditions.html': build_terms, 'about.html': build_about, 'help-support.html': build_help,
}
for name, fn in PAGES.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fn())
    print('wrote', name)
write_sitemap_and_robots(OUT, list(PAGES))
