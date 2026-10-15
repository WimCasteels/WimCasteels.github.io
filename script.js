// ==========================================================================
// wimcasteels.be
// ==========================================================================

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// --------------------------------------------------------------------------
// Mobiel menu
// --------------------------------------------------------------------------
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.getElementById('nav-links');

function setMenu(open) {
    navLinks.classList.toggle('active', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
}

if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        setMenu(navToggle.getAttribute('aria-expanded') !== 'true');
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => setMenu(false));
    });

    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && navToggle.getAttribute('aria-expanded') === 'true') {
            setMenu(false);
            navToggle.focus();
        }
    });
}

// Navigatiebalk krijgt een rand zodra je scrolt
const navbar = document.querySelector('.navbar');
if (navbar) {
    const updateNavbar = () => navbar.classList.toggle('is-scrolled', window.scrollY > 20);
    window.addEventListener('scroll', updateNavbar, { passive: true });
    updateNavbar();
}

// Jaartal in de footer
document.querySelectorAll('.js-year').forEach(el => {
    el.textContent = new Date().getFullYear();
});

// --------------------------------------------------------------------------
// Handgetekende onderstreping onder sectietitels
// --------------------------------------------------------------------------
const UNDERLINE_PATH = 'M2 7 C 40 3, 80 9, 120 6 S 190 3, 218 7';

document.querySelectorAll('.section-title').forEach(title => {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'title-underline');
    svg.setAttribute('viewBox', '0 0 220 12');
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.setAttribute('aria-hidden', 'true');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', UNDERLINE_PATH);
    svg.appendChild(path);
    title.appendChild(svg);
});

// --------------------------------------------------------------------------
// Getrapte fade-in en tekenen van de onderstreping
// --------------------------------------------------------------------------
const revealGroups = [
    '.offer-cards > *',
    '.editions > *',
    '.news-cards > *',
    '.themes-grid > *',
    '.chapters > *',
    '.contact-grid > *',
    '.presskit > *',
    '.chips > *'
];

const revealObserver = (reduceMotion || !('IntersectionObserver' in window))
    ? null
    : new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add(entry.target.classList.contains('section-title') ? 'is-drawn' : 'is-visible');
            revealObserver.unobserve(entry.target);
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

// Ook gebruikt voor kaarten die later met JavaScript worden toegevoegd
function addReveal(items) {
    items.forEach(item => {
        const index = Array.prototype.indexOf.call(item.parentElement.children, item);
        item.style.setProperty('--reveal-delay', `${Math.min(index, 8) * 80}ms`);
        item.classList.add('reveal');
        if (revealObserver) revealObserver.observe(item);
        else item.classList.add('is-visible');
    });
}

revealGroups.forEach(selector => addReveal(document.querySelectorAll(selector)));

document.querySelectorAll('.section-title').forEach(title => {
    if (revealObserver) revealObserver.observe(title);
    else title.classList.add('is-drawn');
});

// --------------------------------------------------------------------------
// Kopieerknoppen (kortingscode, bio's)
// --------------------------------------------------------------------------
document.querySelectorAll('.js-copy').forEach(button => {
    const feedback = button.querySelector('.promo-feedback');
    const label = feedback ? feedback.textContent : '';

    button.addEventListener('click', async () => {
        const targetId = button.dataset.copyTarget;
        const text = targetId ? document.getElementById(targetId).textContent.trim() : button.dataset.copy;
        try {
            await navigator.clipboard.writeText(text);
            if (feedback) feedback.textContent = 'Gekopieerd ✓';
        } catch (error) {
            if (feedback) feedback.textContent = 'Kopiëren lukte niet';
        }
        setTimeout(() => {
            if (feedback) feedback.textContent = label;
        }, 2000);
    });
});

// --------------------------------------------------------------------------
// Aanvraagformulier: stelt een mail op in het e-mailprogramma van de bezoeker
// --------------------------------------------------------------------------
const requestForm = document.querySelector('.request-form');

if (requestForm) {
    const sessie = requestForm.querySelector('#f-sessie');

    document.querySelectorAll('.js-preselect').forEach(link => {
        link.addEventListener('click', () => {
            if (sessie) sessie.value = link.dataset.sessie;
        });
    });

    requestForm.addEventListener('submit', event => {
        event.preventDefault();
        if (!requestForm.reportValidity()) return;

        const lines = [];
        requestForm.querySelectorAll('input, select, textarea').forEach(field => {
            if (field.value.trim()) lines.push(`${field.name}: ${field.value.trim()}`);
        });

        const subject = `Aanvraag: ${sessie ? sessie.value : 'lezing of workshop'}`;
        const body = `Dag Wim,\n\nIk wil graag een sessie aanvragen.\n\n${lines.join('\n')}\n`;
        window.location.href = `mailto:wim.casteels@ap.be?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });
}

// --------------------------------------------------------------------------
// Nieuws en nieuwsbrief inladen uit nieuws.json en substack.json
// --------------------------------------------------------------------------
const MAANDEN = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'];
const LABELS = { opinie: 'Opiniestuk', lezing: 'Lezing', workshop: 'Workshop', media: 'Media' };

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text == null ? '' : String(text);
    return div.innerHTML;
}

// "2026-09-25" wordt "25 september 2026"
function formatDate(iso) {
    const [year, month, day] = iso.split('-').map(Number);
    return `${day} ${MAANDEN[month - 1]} ${year}`;
}

function isExternal(url) {
    return /^https?:/.test(url);
}

function linkAttributes(url) {
    return `href="${escapeHtml(url)}"${isExternal(url) ? ' target="_blank" rel="noopener"' : ''}`;
}

function createNewsEntry(item) {
    const article = document.createElement('article');
    article.className = 'news-entry';
    article.dataset.category = item.category;
    article.dataset.date = item.date;

    const url = item.titleUrl || item.linkUrl;
    const title = url ? `<a ${linkAttributes(url)}>${escapeHtml(item.title)}</a>` : escapeHtml(item.title);
    const link = item.linkUrl && item.linkText
        ? `<a ${linkAttributes(item.linkUrl)} class="news-entry-link">${escapeHtml(item.linkText)}`
          + (item.fileInfo ? ` <span class="file-info">(${escapeHtml(item.fileInfo)})</span>` : '')
          + (isExternal(item.linkUrl) ? ' <span aria-hidden="true">↗</span>' : '')
          + '</a>'
        : '';

    article.innerHTML = `
        <time class="news-entry-date" datetime="${escapeHtml(item.date)}">${formatDate(item.date)}</time>
        <div class="news-entry-content">
            <span class="news-label news-label-${escapeHtml(item.category)}">${LABELS[item.category] || 'Media'}</span>
            <h3>${title}</h3>
            ${item.description ? `<p>${escapeHtml(item.description)}</p>` : ''}
            ${link}
        </div>`;
    return article;
}

function createEdition(edition) {
    const link = document.createElement('a');
    link.className = 'card edition';
    link.href = edition.url;
    link.target = '_blank';
    link.rel = 'noopener';
    link.innerHTML = `
        ${edition.image ? `<div class="edition-image"><img src="${escapeHtml(edition.image)}" alt="" loading="lazy" width="600" height="400"></div>` : ''}
        <div class="edition-body">
            <time datetime="${escapeHtml(edition.date)}" class="edition-date">${formatDate(edition.date)}</time>
            <h3>${escapeHtml(edition.title)}</h3>
            <p>${escapeHtml(edition.description)}</p>
        </div>`;
    return link;
}

async function loadJson(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`${url}: ${response.status}`);
    return response.json();
}

// Homepage: de 3 laatste nieuwsitems
const latestNews = document.getElementById('latest-news');
if (latestNews) {
    loadJson('nieuws.json')
        .then(items => {
            items.sort((a, b) => b.date.localeCompare(a.date)).slice(0, 3)
                .forEach(item => latestNews.appendChild(createNewsEntry(item)));
            addReveal(latestNews.children);
        })
        .catch(error => console.warn('Nieuws niet geladen:', error));
}

// Homepage: de 3 laatste edities van de nieuwsbrief
const editions = document.getElementById('editions');
if (editions) {
    loadJson('substack.json')
        .then(items => {
            items.slice(0, 3).forEach(edition => editions.appendChild(createEdition(edition)));
            addReveal(editions.children);
        })
        .catch(error => console.warn('Nieuwsbrief niet geladen:', error));
}

// Nieuwspagina: alle items, gegroepeerd per jaar
const newsList = document.getElementById('news-list');
if (newsList) {
    loadJson('nieuws.json')
        .then(items => {
            let previousYear = '';
            items.sort((a, b) => b.date.localeCompare(a.date)).forEach(item => {
                const year = item.date.slice(0, 4);
                if (year !== previousYear) {
                    const heading = document.createElement('h2');
                    heading.className = 'news-year';
                    heading.textContent = year;
                    newsList.appendChild(heading);
                    previousYear = year;
                }
                newsList.appendChild(createNewsEntry(item));
            });
            initNewsPage();
        })
        .catch(error => {
            console.warn('Nieuws niet geladen:', error);
            const empty = document.querySelector('.news-empty');
            if (empty) {
                empty.textContent = 'Het nieuws kon niet geladen worden. Probeer het later opnieuw.';
                empty.hidden = false;
            }
        });
}

// --------------------------------------------------------------------------
// Nieuwspagina: filters, tellers en "Binnenkort"
// --------------------------------------------------------------------------
function initNewsPage() {
    const today = new Date().toISOString().slice(0, 10);
    const upcoming = document.getElementById('binnenkort');
    const upcomingList = document.querySelector('.js-upcoming-list');

    // Lezingen en workshops met een datum vanaf vandaag gaan naar "Binnenkort"
    const future = Array.from(newsList.querySelectorAll('.news-entry'))
        .filter(entry => entry.dataset.date >= today && entry.dataset.category !== 'opinie' && entry.dataset.category !== 'media')
        .sort((a, b) => a.dataset.date.localeCompare(b.dataset.date));

    if (future.length && upcoming && upcomingList) {
        future.forEach(entry => upcomingList.appendChild(entry));
        upcoming.hidden = false;
    }

    const entries = Array.from(document.querySelectorAll('.news-page .news-entry'));
    const years = Array.from(newsList.querySelectorAll('.news-year'));
    const buttons = Array.from(document.querySelectorAll('.filter-btn'));
    const empty = document.querySelector('.news-empty');

    buttons.forEach(button => {
        const filter = button.dataset.filter;
        const count = entries.filter(entry => filter === 'all' || entry.dataset.category === filter).length;
        const counter = button.querySelector('.filter-count');
        if (counter) counter.textContent = `(${count})`;
    });

    function applyFilter(filter) {
        if (!buttons.some(button => button.dataset.filter === filter)) filter = 'all';

        buttons.forEach(button => {
            const active = button.dataset.filter === filter;
            button.classList.toggle('active', active);
            button.setAttribute('aria-pressed', String(active));
        });

        let visible = 0;
        entries.forEach(entry => {
            const show = filter === 'all' || entry.dataset.category === filter;
            entry.classList.toggle('is-hidden', !show);
            if (show) visible++;
        });

        // Jaartitels verbergen als er in dat jaar niets zichtbaar is
        years.forEach(year => {
            let sibling = year.nextElementSibling;
            let hasVisible = false;
            while (sibling && !sibling.classList.contains('news-year')) {
                if (!sibling.classList.contains('is-hidden')) hasVisible = true;
                sibling = sibling.nextElementSibling;
            }
            year.classList.toggle('is-hidden', !hasVisible);
        });

        if (upcoming && !upcoming.hidden) {
            const upcomingVisible = upcomingList.querySelector('.news-entry:not(.is-hidden)');
            upcoming.style.display = upcomingVisible ? '' : 'none';
        }

        if (empty) empty.hidden = visible > 0;
    }

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.dataset.filter;
            history.replaceState(null, '', filter === 'all' ? location.pathname : `#${filter}`);
            applyFilter(filter);
        });
    });

    applyFilter(location.hash.slice(1) || 'all');
    window.addEventListener('hashchange', () => applyFilter(location.hash.slice(1) || 'all'));
}

// --------------------------------------------------------------------------
// Cookietoestemming: Google Analytics laadt alleen na akkoord
// --------------------------------------------------------------------------
const CONSENT_KEY = 'wc-analytics-consent';
const consentBanner = document.querySelector('.consent');
const gaId = document.body.dataset.ga;

function readConsent() {
    try {
        return localStorage.getItem(CONSENT_KEY);
    } catch (error) {
        return null;
    }
}

function storeConsent(value) {
    try {
        localStorage.setItem(CONSENT_KEY, value);
    } catch (error) {
        // Opslag niet beschikbaar: de keuze geldt dan alleen voor dit bezoek
    }
}

function loadAnalytics() {
    if (!gaId || window.gaLoaded) return;
    window.gaLoaded = true;
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
    document.head.appendChild(script);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', gaId, { anonymize_ip: true });
}

if (consentBanner) {
    const consent = readConsent();
    if (consent === 'granted') {
        loadAnalytics();
    } else if (consent !== 'denied') {
        consentBanner.hidden = false;
    }

    consentBanner.querySelector('.js-consent-accept').addEventListener('click', () => {
        storeConsent('granted');
        consentBanner.hidden = true;
        loadAnalytics();
    });

    consentBanner.querySelector('.js-consent-deny').addEventListener('click', () => {
        storeConsent('denied');
        consentBanner.hidden = true;
        // Eerder geplaatste Analytics-cookies opruimen
        document.cookie.split(';').map(c => c.split('=')[0].trim()).filter(name => name.startsWith('_ga')).forEach(name => {
            document.cookie = `${name}=; Max-Age=0; path=/; domain=${location.hostname.replace(/^www\./, '')}`;
            document.cookie = `${name}=; Max-Age=0; path=/`;
        });
    });

    document.querySelectorAll('.js-consent-open').forEach(button => {
        button.addEventListener('click', () => {
            consentBanner.hidden = false;
        });
    });
}
