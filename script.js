/* BulandTech — site script (no dependencies) */
(() => {
    const $ = (s, el = document) => el.querySelector(s);
    const $$ = (s, el = document) => [...el.querySelectorAll(s)];

    /* ---------- Splash screen (full on first visit of a session, quick after) ---------- */
    const splash = $('#splash');
    if (splash) {
        let seen = false;
        try { seen = sessionStorage.getItem('bt-splash') === '1'; sessionStorage.setItem('bt-splash', '1'); } catch (_) {}
        // First open in a session: full 5s brand splash. Moving between pages: a quick 0.7s flash.
        const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const minTime = reduce ? 400 : (seen ? 700 : 5000);
        splash.style.setProperty('--splash-ms', minTime + 'ms');
        const t0 = performance.now();
        document.body.classList.add('loading');
        let done = false;
        const hide = () => {
            if (done) return;
            done = true;
            splash.classList.add('hide');            // white screen fades out (.9s)
            document.body.classList.remove('loading');
            document.body.classList.add('loaded');
            setTimeout(() => splash.remove(), 1000);
        };
        const ready = () => setTimeout(hide, Math.max(0, minTime - (performance.now() - t0)));
        if (document.readyState === 'complete') ready(); else window.addEventListener('load', ready);
        setTimeout(hide, minTime + 1500); // never block the page if something is slow to load
    }

    /* ---------- Navbar + scroll progress ---------- */
    const nav = $('.nav');
    const bar = $('.scroll-progress');
    const onScroll = () => {
        if (nav) nav.classList.toggle('scrolled', window.scrollY > 20);
        if (bar) {
            const max = document.documentElement.scrollHeight - innerHeight;
            bar.style.transform = `scaleX(${max > 0 ? window.scrollY / max : 0})`;
        }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ---------- Cursor glow on cards ---------- */
    $$('.svc, .step, .price, .app, .tool-group, .why > div, .offer, .support-card, .contact-item, .hb-item, .stats-row > div').forEach(card => {
        card.classList.add('glow');
        card.addEventListener('pointermove', e => {
            const r = card.getBoundingClientRect();
            card.style.setProperty('--mx', `${e.clientX - r.left}px`);
            card.style.setProperty('--my', `${e.clientY - r.top}px`);
        });
    });

    /* ---------- Stagger reveal for items in the same group ---------- */
    $$('[data-reveal]').forEach(el => {
        const sibs = [...el.parentElement.children].filter(c => c.hasAttribute('data-reveal'));
        if (sibs.length > 1) el.style.setProperty('--d', `${Math.min(sibs.indexOf(el), 8) * 80}ms`);
    });

    const burger = $('.burger');
    if (burger && nav) {
        burger.addEventListener('click', () => {
            const open = nav.classList.toggle('open');
            burger.setAttribute('aria-expanded', open);
        });
        $$('.nav-links a').forEach(a => a.addEventListener('click', () => {
            nav.classList.remove('open');
            burger.setAttribute('aria-expanded', 'false');
        }));
        document.addEventListener('keydown', e => { if (e.key === 'Escape') nav.classList.remove('open'); });
    }

    /* Active link on the home page */
    const sectionLinks = $$('.nav-links a[href^="#"]');
    if (sectionLinks.length && 'IntersectionObserver' in window) {
        const map = new Map(sectionLinks.map(a => [a.getAttribute('href').slice(1), a]));
        const spy = new IntersectionObserver(entries => {
            entries.forEach(en => {
                if (en.isIntersecting && map.has(en.target.id)) {
                    sectionLinks.forEach(a => a.classList.remove('active'));
                    map.get(en.target.id).classList.add('active');
                }
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        map.forEach((_, id) => { const s = document.getElementById(id); if (s) spy.observe(s); });
    }

    /* ---------- Bottom tab bar (phones & tablets): highlight the section in view ---------- */
    const tabs = $$('.tabbar a[href^="#"]');
    if (tabs.length && 'IntersectionObserver' in window) {
        const tabMap = { home: 'home', services: 'services', work: 'work', process: 'work', pricing: 'work', reviews: 'work', contact: 'contact' };
        const setTab = key => $$('.tabbar a').forEach(a => a.classList.toggle('active', a.dataset.tab === key));
        const tabSpy = new IntersectionObserver(entries => {
            entries.forEach(en => { if (en.isIntersecting && tabMap[en.target.id]) setTab(tabMap[en.target.id]); });
        }, { rootMargin: '-45% 0px -50% 0px' });
        Object.keys(tabMap).forEach(id => { const s = document.getElementById(id); if (s) tabSpy.observe(s); });
    }
    $$('.tabbar a').forEach(a => a.addEventListener('click', () => {
        if (navigator.vibrate) { try { navigator.vibrate(8); } catch (_) {} }
        if (nav) nav.classList.remove('open');
    }));

    /* ---------- Swipe rails: page dots under horizontal card rows ---------- */
    const railSel = '.services-grid, .pricing-grid, .process, .why, .tools, .stats-row, .support-grid, .highlight-box';
    $$(railSel).forEach(rail => {
        const items = [...rail.children];
        if (items.length < 2) return;
        const dots = document.createElement('div');
        dots.className = 'rail-hint';
        dots.setAttribute('aria-hidden', 'true');
        dots.innerHTML = items.map((_, i) => `<i${i ? '' : ' class="on"'}></i>`).join('');
        rail.after(dots);
        const update = () => {
            if (rail.scrollWidth <= rail.clientWidth + 4) { dots.style.display = 'none'; return; }
            dots.style.display = '';
            const step = items[1].offsetLeft - items[0].offsetLeft || 1;
            const idx = Math.min(items.length - 1, Math.round(rail.scrollLeft / step));
            [...dots.children].forEach((d, i) => d.classList.toggle('on', i === idx));
        };
        rail.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
        window.addEventListener('resize', update);
        update();
    });

    /* ---------- Reveal on scroll ---------- */
    const reveals = $$('[data-reveal]');
    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver(entries => {
            entries.forEach(en => {
                if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        reveals.forEach(el => io.observe(el));
    } else {
        reveals.forEach(el => el.classList.add('in'));
    }

    /* ---------- Counters ---------- */
    const counters = $$('[data-count]');
    if (counters.length && 'IntersectionObserver' in window) {
        const co = new IntersectionObserver(entries => {
            entries.forEach(en => {
                if (!en.isIntersecting) return;
                const el = en.target;
                const target = +el.dataset.count;
                const suffix = el.dataset.suffix || '';
                const start = performance.now();
                const dur = 1400;
                const tick = now => {
                    const p = Math.min((now - start) / dur, 1);
                    el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
                    if (p < 1) requestAnimationFrame(tick);
                };
                requestAnimationFrame(tick);
                co.unobserve(el);
            });
        }, { threshold: 0.6 });
        counters.forEach(c => co.observe(c));
    }

    /* ---------- Infinite marquees (clone content once) ---------- */
    $$('[data-marquee]').forEach(track => {
        track.innerHTML += track.innerHTML;
        $$(':scope > *', track).slice(track.children.length / 2).forEach(c => c.setAttribute('aria-hidden', 'true'));
    });

    /* ---------- Gallery filters ---------- */
    const filterBar = $('.filters');
    if (filterBar) {
        const tiles = $$('.gallery .tile');
        filterBar.addEventListener('click', e => {
            const btn = e.target.closest('button');
            if (!btn) return;
            $$('button', filterBar).forEach(b => b.classList.toggle('active', b === btn));
            const f = btn.dataset.filter;
            tiles.forEach(t => {
                const hide = f !== 'all' && t.dataset.cat !== f;
                t.classList.toggle('hide', hide);
                t.classList.remove('pop');
                if (!hide) { void t.offsetWidth; t.classList.add('pop'); }
            });
        });
    }

    /* ---------- Lightbox (image tiles) ---------- */
    const tiles = $$('.tile[data-lightbox]');
    if (tiles.length) {
        const lb = document.createElement('div');
        lb.className = 'lightbox';
        lb.setAttribute('role', 'dialog');
        lb.setAttribute('aria-modal', 'true');
        lb.innerHTML = `
            <button class="lb-btn lb-close" aria-label="Close"><i class="fas fa-xmark"></i></button>
            <button class="lb-btn lb-prev" aria-label="Previous"><i class="fas fa-arrow-left"></i></button>
            <figure><img alt=""><figcaption></figcaption></figure>
            <button class="lb-btn lb-next" aria-label="Next"><i class="fas fa-arrow-right"></i></button>`;
        document.body.appendChild(lb);
        const img = $('img', lb), cap = $('figcaption', lb);
        let list = [], idx = 0;

        const show = i => {
            idx = (i + list.length) % list.length;
            const t = list[idx], im = $('img', t);
            img.src = im.dataset.full || im.currentSrc || im.src;
            img.alt = im.alt;
            cap.textContent = t.dataset.title || im.alt;
        };
        const open = t => {
            list = tiles.filter(x => !x.classList.contains('hide') && x.offsetParent !== null);
            if (!list.includes(t)) list = [t];
            show(list.indexOf(t));
            lb.classList.add('open');
            document.body.style.overflow = 'hidden';
        };
        const close = () => { lb.classList.remove('open'); document.body.style.overflow = ''; img.src = ''; };

        tiles.forEach(t => {
            t.tabIndex = 0;
            t.addEventListener('click', () => open(t));
            t.addEventListener('keydown', e => { if (e.key === 'Enter') open(t); });
        });
        $('.lb-close', lb).addEventListener('click', close);
        $('.lb-prev', lb).addEventListener('click', () => show(idx - 1));
        $('.lb-next', lb).addEventListener('click', () => show(idx + 1));
        lb.addEventListener('click', e => { if (e.target === lb) close(); });
        document.addEventListener('keydown', e => {
            if (!lb.classList.contains('open')) return;
            if (e.key === 'Escape') close();
            if (e.key === 'ArrowLeft') show(idx - 1);
            if (e.key === 'ArrowRight') show(idx + 1);
        });
    }

    /* ---------- Video cards ---------- */
    const pauseOthers = except => $$('video').forEach(v => { if (v !== except) v.pause(); });

    $$('.vcard').forEach(card => {
        const btn = $('.vplay', card);
        const video = $('video', card);
        const yt = card.dataset.youtube;
        if (!btn) return;

        btn.addEventListener('click', () => {
            if (yt) {
                const frame = $('.vframe', card);
                frame.innerHTML = `<iframe src="https://www.youtube.com/embed/${yt}?autoplay=1&rel=0&modestbranding=1"
                    title="${card.dataset.title || 'Video'}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
                    allowfullscreen loading="lazy"></iframe>`;
                pauseOthers();
            } else if (video) {
                video.controls = true;
                video.play();
            }
            card.classList.add('playing');
        });
        if (video) video.addEventListener('play', () => { pauseOthers(video); card.classList.add('playing'); });
    });

    /* ---------- Contact + review forms → support@bulandtech.in (FormSubmit) ---------- */
    const FORM_EMAIL = 'support@bulandtech.in';
    $$('form[data-formsubmit]').forEach(form => {
        const msg = $('.form-msg', form);
        form.addEventListener('submit', async e => {
            e.preventDefault();
            const btn = $('button[type="submit"]', form);
            const label = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = 'Sending… <i class="fas fa-spinner fa-spin"></i>';
            msg.className = 'form-msg';
            try {
                const data = new FormData(form);
                data.append('_subject', form.dataset.subject || 'New message from bulandtech.in');
                data.append('_template', 'table');
                data.append('_captcha', 'false');
                const res = await fetch('https://formsubmit.co/ajax/' + FORM_EMAIL, {
                    method: 'POST',
                    body: data,
                    headers: { Accept: 'application/json' }
                });
                const json = await res.json().catch(() => ({}));
                if (!res.ok || String(json.success) === 'false') throw new Error('Request failed');
                msg.className = 'form-msg success';
                msg.textContent = form.dataset.success || 'Thank you! Your message has been sent.';
                form.reset();
                msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } catch (err) {
                msg.className = 'form-msg error';
                msg.innerHTML = 'Something went wrong. Please call or WhatsApp us at <a href="tel:+918265999762"><strong>+91 82659 99762</strong></a>.';
            } finally {
                btn.disabled = false;
                btn.innerHTML = label;
            }
        });
    });

    /* ---------- Footer year ---------- */
    $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
