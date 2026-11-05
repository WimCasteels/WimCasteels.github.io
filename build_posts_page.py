"""Build posts.html: a standalone page listing your LinkedIn posts.

  python build_posts_page.py

Its only input is posts.json (see posts_store.py), which dma_sync.py keeps up to date.
"""

import json
import re
from pathlib import Path

from posts_store import load_posts, post_key

ROOT = Path(__file__).parent
OUTPUT = ROOT / "posts.html"
SAMPLE_OUTPUT = ROOT / "posts-random.js"  # small sample for the "random post" block on the homepage
SAMPLE_SIZE = 300  # most recent posts the homepage picks from
SINCE = "2026-03-01"  # only posts from this date on (local time, YYYY-MM-DD)

# Themes are assigned from hashtags; a post can have several themes.
THEMES = {
    "Ethiek, maatschappij & media": "aiethiek aiethics ethiek techethiek verantwoordeai maatschappij democratie transparantie techkritiek kritischdenken aihype "
                                    "desinformatie deepfakes journalistiek auteursrecht copyright",
    "Veiligheid & security": "aiveiligheid aisafety frontierai agi autonomewapens alignment aialignment "
                             "cybersecurity privacy surveillance digitaleveiligheid",
    "Beleid & geopolitiek": "aibeleid airegulering aigovernance techbeleid aiact technologiebeleid techpolicy techpolitiek eu gdpr "
                            "europa digitalesoevereiniteit aisoevereiniteit europeseai geopolitiek china mistral vlaanderen belgië exportcontroles exportcontrole",
    "Big Tech & AI-bedrijven": "openai anthropic google meta microsoft nvidia apple bigtech deepmind spacex techindustrie aibubbel aieconomie techeconomie startups xai",
    # Only specific model tags: #llm and #generatieveai are on almost every post, so they don't discriminate.
    "Modellen & chatbots": "aimodellen chatgpt claude gemini deepseek chatbots openweights benchmarks grok llama",
    "Infrastructuur, chips & energie": "datacenters aiinfrastructuur chips halfgeleiders compute energie duurzaamheid klimaat energietransitie cloudcomputing",
    "Werk & economie": "toekomstvanwerk futureofwork arbeidsmarkt automatisering productiviteit aiadoptie enterpriseai economie aistrategie",
    "Onderwijs & geletterdheid": "onderwijs hogeronderwijs aigeletterdheid digitalegeletterdheid mediawijsheid edtech aphogeschool aidetectie",
    "Agents & software": "aiagents agenticai softwareontwikkeling vibecoding claudecode opensource",
    "Wetenschap & zorg": "wetenschap onderzoek aionderzoek wiskunde gezondheidszorg robotica",
}
THEME_NAMES = list(THEMES)
TAG_TO_THEMES = {}
for index, name in enumerate(THEME_NAMES):
    for tag in THEMES[name].split():
        TAG_TO_THEMES.setdefault(tag, set()).add(index)


def post_themes(text):
    """Sorted theme indices for a post, based on its hashtags."""
    tags = {t.lower() for t in re.findall(r"#(\w+)", text)}
    return sorted(set().union(*(TAG_TO_THEMES.get(t, set()) for t in tags))) if tags else []


PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts | Wim Casteels</title>
    <meta name="description" content="Korte stukken van Wim Casteels over AI, technologie en samenleving, eerder verschenen op LinkedIn.">
    <link rel="canonical" href="https://wimcasteels.be/posts.html">

    <meta property="og:type" content="website">
    <meta property="og:locale" content="nl_BE">
    <meta property="og:site_name" content="Wim Casteels">
    <meta property="og:title" content="Posts | Wim Casteels">
    <meta property="og:description" content="Korte stukken van Wim Casteels over AI, technologie en samenleving, eerder verschenen op LinkedIn.">
    <meta property="og:url" content="https://wimcasteels.be/posts.html">
    <meta property="og:image" content="https://wimcasteels.be/images/web/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">

    <link rel="icon" type="image/svg+xml" href="images/logo.svg">
    <link rel="icon" type="image/png" href="images/web/favicon-64.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:wght@500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <script>document.documentElement.classList.add('js');</script>
    <style>
    /* Page-specific styles; colors, fonts, buttons and the shared .card come from styles.css. */
    .posts-tools { display: flex; flex-wrap: wrap; gap: 1rem 2rem; align-items: flex-end; margin-top: 1.75rem; }
    .posts-search { width: min(100%, 360px); }
    .theme-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.25rem; }
    .theme-chip[aria-pressed="true"] { color: var(--on-accent); background-color: var(--accent-color); border-color: var(--accent-color); }
    .swatch { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; }

    /* One color per theme, assigned by theme size, so a post's theme tags can be told apart. */
    :root {
        --c0: #5B3A8C; --c1: #C0623A; --c2: #2E8A6B; --c3: #C89211; --c4: #C2577F; --c5: #3F7A2A; --c6: #3D6FB0;
        --c7: #B5413F; --c8: #1F3D66; --c9: #8C6232; --c10: #7A7180; --c11: #9B3F86; --c12: #1F8590;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --c0: #B79BE0; --c1: #E0875E; --c2: #4FB894; --c3: #E0B040; --c4: #E07FA3; --c5: #7DBE5E; --c6: #7FA8E0;
            --c7: #E57C7A; --c8: #8FB0DE; --c9: #C9A06E; --c10: #A99FB8; --c11: #D37FC0; --c12: #4FBBC5;
        }
    }

    /* Period: two range inputs stacked on one track; only the thumbs take pointer events. */
    .period { display: flex; flex-direction: column; gap: 2px; width: min(100%, 340px); font-size: 0.875rem; }
    .period .readout { color: var(--text-muted); font-variant-numeric: tabular-nums; }
    .slider { position: relative; height: 24px; }
    .slider .track, .slider .fill { position: absolute; top: 10px; height: 4px; border-radius: 2px; }
    .slider .track { left: 0; right: 0; background: var(--border-color); }
    .slider .fill { background: var(--accent-color); }
    .slider input[type=range] { position: absolute; inset: 0; width: 100%; margin: 0; padding: 0; border: 0; background: none;
                                box-shadow: none; pointer-events: none; -webkit-appearance: none; appearance: none; }
    .slider input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; pointer-events: auto; cursor: pointer;
        width: 18px; height: 18px; border-radius: 50%; background: var(--bg-card); border: 2px solid var(--accent-color); }
    .slider input[type=range]::-moz-range-thumb { pointer-events: auto; cursor: pointer;
        width: 14px; height: 14px; border-radius: 50%; background: var(--bg-card); border: 2px solid var(--accent-color); }
    .slider input[type=range]::-moz-range-track { background: none; }

    .posts-page { padding: 3rem 0 5rem; }
    .post-grid { display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
    .post-card { cursor: pointer; display: flex; flex-direction: column; overflow: hidden; }
    .post-card.deleted { opacity: 0.55; }
    .post-card-body { padding: 1.1rem 1.25rem 1.25rem; display: flex; flex-direction: column; gap: 0.45rem; flex: 1; }
    .post-card h3 { font-size: 1.05rem; line-height: 1.35;
                    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .post-excerpt { color: var(--text-light); font-size: 0.9rem; line-height: 1.55;
                    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
    .post-themes { display: flex; flex-wrap: wrap; gap: 0.35rem 0.4rem; margin-top: auto; padding-top: 0.35rem; }
    .post-meta { display: flex; flex-wrap: wrap; gap: 0.4rem 0.5rem; align-items: center;
                 font-size: 0.75rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent-color); }
    .post-tag { background: var(--accent-tint); color: var(--text-color); border-radius: 999px; padding: 0.1rem 0.6rem;
                font-size: 0.72rem; font-weight: 500; letter-spacing: 0; text-transform: none; white-space: nowrap; }
    .post-tag .swatch { width: 8px; height: 8px; margin-right: 5px; vertical-align: 0; }
    .posts-more { display: flex; justify-content: center; margin-top: 2rem; }
    .posts-more[hidden] { display: none; }
    .posts-empty { color: var(--text-muted); text-align: center; padding: 2.5rem 0; grid-column: 1 / -1; }

    .post-dialog {
        width: min(720px, calc(100vw - 32px)); max-height: calc(100vh - 48px); margin: auto; padding: 0;
        border: 1px solid var(--border-color); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg);
        background: var(--bg-card); color: var(--text-color);
    }
    .post-dialog::backdrop { background: rgba(31, 26, 46, 0.6); }
    .dialog-bar { position: sticky; top: 0; display: flex; justify-content: space-between; align-items: center;
                  gap: 8px; padding: 0.75rem 1rem; background: var(--bg-card); border-bottom: 1px solid var(--border-color); }
    .dialog-bar button { font: inherit; font-size: 1.15rem; line-height: 1; padding: 0.4rem 0.75rem; cursor: pointer;
                         color: var(--accent-color); background: var(--accent-tint); border: 0; border-radius: var(--radius); }
    .dialog-bar button:hover:not(:disabled) { color: var(--on-accent); background: var(--accent-color); }
    .dialog-bar button:disabled { opacity: 0.35; cursor: default; }
    .dialog-content { padding: 1.25rem 1.5rem 1.5rem; }
    .dialog-content .post-meta { margin-bottom: 1rem; }
    .post-text { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.7; }
    .post-text .hashtag { color: var(--accent-color); }
    .post-links { margin-top: 1.25rem; display: flex; gap: 0.75rem; flex-wrap: wrap; }

    .featured { margin-bottom: 3rem; }
    .featured-bar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 0.75rem;
                    max-width: 640px; margin-inline: auto; }
    .featured-bar h2 { font-size: 1.35rem; }
    .featured-bar .btn:disabled { opacity: 0.5; cursor: default; }
    /* The featured post sits on the outside of a drum (cylinder) that rotates around its
       horizontal axis. Faces are 3D-placed around it; the reel window clips the rest. */
    .reel { position: relative; max-width: 640px; margin-inline: auto; height: 350px; overflow: hidden; perspective: 1100px;
            border-radius: var(--radius-lg); }
    .drum { position: absolute; left: 0; right: 0; top: 75px; height: 200px; transform-style: preserve-3d; }
    .drum .post-card { position: absolute; inset: 0; backface-visibility: hidden; border-color: var(--accent-light); }
    .drum .post-card:hover { box-shadow: var(--shadow-sm); }
    .drum .post-excerpt { -webkit-line-clamp: 2; }
    /* Once the drum stops, the winning post flashes briefly. */
    @media (prefers-reduced-motion: no-preference) {
        .drum .post-card.won { animation: won 1.4s ease-out; }
    }
    @keyframes won {
        0%, 100% { box-shadow: inset 0 0 0 0 var(--accent-color); background: var(--bg-card); }
        25% { box-shadow: inset 0 0 0 3px var(--accent-color); background: var(--accent-tint); }
    }
    /* Shade the top and bottom so the curve reads as a cylinder. */
    .reel::after { content: ""; position: absolute; inset: 0; pointer-events: none;
                   background: linear-gradient(var(--bg-color), transparent 14%, transparent 86%, var(--bg-color)); }
    </style>
</head>
<body data-ga="G-31NYL0FRHW">
    <a href="#inhoud" class="skip-link">Spring naar inhoud</a>
    <nav class="navbar" aria-label="Hoofdmenu">
    <div class="container navbar-inner">
        <a href="index.html" class="logo"><img src="images/logo.svg" alt="" class="logo-img" width="34" height="34">Wim Casteels</a>
        <button class="nav-toggle" aria-label="Menu openen" aria-expanded="false" aria-controls="nav-links">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <ul class="nav-links" id="nav-links">
            <li><a href="lezingen.html">Lezingen</a></li>
            <li><a href="boek.html">Boek</a></li>
            <li><a href="index.html#nieuwsbrief">Nieuwsbrief</a></li>
            <li><a href="nieuws.html">Nieuws</a></li>
            <li><a href="posts.html" class="active" aria-current="page">Posts</a></li>
            <li><a href="over.html">Over</a></li>
            <li class="nav-cta-item"><a href="lezingen.html#aanvraag" class="btn btn-primary btn-small nav-cta">Boek een lezing</a></li>
        </ul>
    </div>
</nav>

    <main id="inhoud">
    <header class="page-header">
        <div class="container">
            <h1>Posts</h1>
            <p>Korte stukken over AI, technologie en samenleving, eerder verschenen op <a href="https://www.linkedin.com/in/wim-casteels-213720b4/" target="_blank" rel="noopener">LinkedIn</a>.</p>
            <div class="posts-tools">
                <label class="posts-search">
                    <span class="visually-hidden">Zoek in posts</span>
                    <input type="search" id="search" placeholder="Zoek in posts...">
                </label>
                <div class="period">
                    <span class="readout" id="readout"></span>
                    <div class="slider">
                        <div class="track"></div><div class="fill" id="fill"></div>
                        <input type="range" id="from" aria-label="Vanaf datum">
                        <input type="range" id="to" aria-label="Tot datum">
                    </div>
                </div>
            </div>
            <div class="theme-chips" id="chips" role="group" aria-label="Filter op thema"></div>
        </div>
    </header>

    <section class="posts-page">
        <div class="container">
            <section class="featured" id="featured">
                <div class="featured-bar">
                    <h2>Willekeurige post</h2>
                    <button type="button" class="btn btn-secondary btn-small" id="shuffle" title="Kies een andere post">🎰 Vernieuw</button>
                </div>
                <div class="reel" id="featured-posts" aria-live="polite"></div>
            </section>
            <h2 class="section-title" id="all-title">Alle posts</h2>
            <div class="post-grid" id="posts"></div>
            <div class="posts-more" id="more"><button type="button" class="btn btn-secondary" id="more-button"></button></div>
        </div>
    </section>
    </main>

    <footer class="footer">
    <div class="container footer-grid">
        <div class="footer-col">
            <a href="index.html" class="logo logo-footer"><img src="images/logo.svg" alt="" class="logo-img" width="34" height="34">Wim Casteels</a>
            <p>Lezingen en workshops over AI, kritisch en wetenschappelijk onderbouwd.</p>
            <div class="footer-social">
                <a href="https://www.linkedin.com/in/wim-casteels-213720b4/" target="_blank" rel="noopener" aria-label="LinkedIn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
                </a>
                <a href="https://wimcasteels.substack.com" target="_blank" rel="noopener" aria-label="Substack">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 3h16v2.4H4zM4 7.6h16V10H4zM4 12.2h16V22l-8-4.5L4 22z"></path></svg>
                </a>
                <a href="mailto:wim.casteels@ap.be" aria-label="E-mail">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                </a>
            </div>
        </div>
        <div class="footer-col">
            <h2 class="footer-title">Snel naar</h2>
            <ul class="footer-links">
                <li><a href="lezingen.html">Lezing en workshop</a></li>
                <li><a href="lezingen.html#aanvraag">Lezing aanvragen</a></li>
                <li><a href="boek.html">Het masker van AI</a></li>
                <li><a href="nieuws.html">Nieuws</a></li>
                <li><a href="posts.html">Posts</a></li>
                <li><a href="over.html">Over en perskit</a></li>
            </ul>
        </div>
        <div class="footer-col">
            <h2 class="footer-title">Nieuwsbrief</h2>
            <p>Elke week een kritische blik op AI, in je mailbox.</p>
            <a href="https://wimcasteels.substack.com/subscribe" class="btn btn-primary btn-small subscribe-btn" target="_blank" rel="noopener">Abonneer gratis <span aria-hidden="true">↗</span></a>

        </div>
    </div>
    <div class="container footer-bottom">
        <p>&copy; <span class="js-year">2026</span> Wim Casteels</p>
        <p><a href="privacy.html">Privacy</a> · <button type="button" class="link-button js-consent-open">Cookie-instellingen</button></p>
    </div>
</footer>

    <div class="consent" role="dialog" aria-live="polite" aria-label="Cookies" hidden>
    <p>Mag deze site anonieme bezoekersstatistieken bijhouden via Google Analytics? Dat gebeurt alleen als je akkoord gaat. <a href="privacy.html">Meer info</a></p>
    <div class="consent-buttons">
        <button type="button" class="btn btn-secondary btn-small js-consent-deny">Weigeren</button>
        <button type="button" class="btn btn-primary btn-small js-consent-accept">Akkoord</button>
    </div>
</div>

<dialog class="post-dialog" id="dialog">
  <div class="dialog-bar">
    <div>
      <button type="button" id="prev" title="Vorige (←)">‹</button>
      <button type="button" id="next" title="Volgende (→)">›</button>
    </div>
    <button type="button" id="close" title="Sluiten (Esc)">×</button>
  </div>
  <div class="dialog-content" id="dialog-content"></div>
</dialog>
<script id="data" type="application/json">__DATA__</script>
<script>
  const data = JSON.parse(document.getElementById("data").textContent);
  const posts = data.posts;
  const themes = data.themes;
  const container = document.getElementById("posts");

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c]));
  }
  function formatText(s) {
    return escapeHtml(s)
      .replace(/(https?:\\/\\/[^\\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>')
      .replace(/(^|\\s)(#[\\p{L}\\p{N}_]+)/gu, '$1<span class="hashtag">$2</span>');
  }

  // First non-empty line is the title, the rest is the excerpt.
  function splitText(text) {
    const lines = text.split("\\n").map(l => l.trim()).filter(Boolean);
    return { title: lines[0] || "(geen tekst)", excerpt: lines.slice(1).join(" ") };
  }

  // Theme labels in chip order, with the same color as their chip.
  function themeTags(p) {
    return themeOrder.filter(t => p.themes.includes(t)).map(t =>
      `<span class="post-tag"><span class="swatch" style="background:${color[t]}"></span>${escapeHtml(themes[t])}</span>`).join("");
  }

  function metaHtml(p) {
    return `
      <span>${p.date.slice(8, 10)}/${p.date.slice(5, 7)}/${p.date.slice(0, 4)}</span>
      ${p.deleted ? '<span class="post-tag">verwijderd</span>' : ""}`;
  }

  // Chips and theme tags share one fixed order: largest theme first. Color follows the
  // theme, so filtering never repaints a tag.
  const themeOrder = themes.map((_, t) => t)
    .sort((a, b) => posts.filter(p => p.themes.includes(b)).length - posts.filter(p => p.themes.includes(a)).length);
  const color = {};
  themeOrder.forEach((t, slot) => { color[t] = `var(--c${slot})`; });

  // ---- Period filter: a two-thumb slider over every day from the first to the last post ----
  const DAY = 86400000;
  const ascending = posts.map(p => p.date.slice(0, 10)).sort();
  const toMs = d => Date.UTC(+d.slice(0, 4), +d.slice(5, 7) - 1, +d.slice(8, 10));
  const isoDay = ms => new Date(ms).toISOString().slice(0, 10);
  const fmtDay = d => `${d.slice(8, 10)}/${d.slice(5, 7)}/${d.slice(0, 4)}`;
  const firstMs = toMs(ascending[0] || "2026-01-01");
  const dayCount = Math.round((toMs(ascending[ascending.length - 1] || "2026-01-01") - firstMs) / DAY);
  const fromInput = document.getElementById("from"), toInput = document.getElementById("to");
  for (const input of [fromInput, toInput]) { input.min = 0; input.max = dayCount; input.step = 1; }
  fromInput.value = 0;
  toInput.value = dayCount;
  let rangeFrom = isoDay(firstMs), rangeTo = isoDay(firstMs + dayCount * DAY);

  function updateRange(moved) {
    let a = +fromInput.value, b = +toInput.value;
    if (a > b) {  // thumbs can't cross: the moved one pushes the other
      if (moved === fromInput) toInput.value = b = a; else fromInput.value = a = b;
    }
    rangeFrom = isoDay(firstMs + a * DAY);
    rangeTo = isoDay(firstMs + b * DAY);
    document.getElementById("readout").textContent = `${fmtDay(rangeFrom)} – ${fmtDay(rangeTo)}`;
    const fill = document.getElementById("fill");
    fill.style.left = `${a / Math.max(1, dayCount) * 100}%`;
    fill.style.width = `${(b - a) / Math.max(1, dayCount) * 100}%`;
  }
  function postInRange(p) {
    const d = p.date.slice(0, 10);
    return d >= rangeFrom && d <= rangeTo;
  }
  for (const input of [fromInput, toInput]) {
    input.addEventListener("input", () => { updateRange(input); render(document.getElementById("search").value); });
  }
  updateRange(null);

  // ---- Theme filter ----
  const selectedThemes = new Set();  // empty = all themes; otherwise a post needs at least one
  const chipsEl = document.getElementById("chips");

  function renderChips() {
    const chip = (t, label) =>
      `<button class="filter-btn theme-chip" data-theme="${t}" aria-pressed="${t === "" ? !selectedThemes.size : selectedThemes.has(t)}">` +
      (t === "" ? "" : `<span class="swatch" style="background:${color[t]}"></span>`) +
      `${escapeHtml(label)}</button>`;
    chipsEl.innerHTML = chip("", "Alle thema's") + themeOrder.map(t => chip(t, themes[t])).join("");
  }
  chipsEl.addEventListener("click", e => {
    const chip = e.target.closest(".theme-chip");
    if (chip) selectTheme(chip.dataset.theme === "" ? null : +chip.dataset.theme);
  });

  // Clicking a theme toggles it; "Alle thema's" clears the selection.
  function selectTheme(t) {
    if (t === null) selectedThemes.clear();
    else if (!selectedThemes.delete(t)) selectedThemes.add(t);
    render(document.getElementById("search").value);
  }

  let shown = [];
  let current = -1;

  function cardHtml(p, i) {
    const { title, excerpt } = splitText(p.text);
    return `
      <article class="card post-card ${p.deleted ? "deleted" : ""}" data-index="${i}" tabindex="0">
        <div class="post-card-body">
          <div class="post-meta"><span>${fmtDay(p.date)}</span>${p.deleted ? '<span class="post-tag">verwijderd</span>' : ""}</div>
          <h3>${escapeHtml(title)}</h3>
          ${excerpt ? `<p class="post-excerpt">${escapeHtml(excerpt)}</p>` : ""}
          ${p.themes.length ? `<div class="post-themes">${themeTags(p)}</div>` : ""}
        </div>
      </article>`;
  }

  // One random post on the front face of a rotating drum. It only changes when the button
  // is pressed; the filters decide which posts the next spin can land on.
  // Faces carry data-index into `posts` (not `shown`), so they stay valid when filters change.
  const reel = document.getElementById("featured-posts");
  const shuffleButton = document.getElementById("shuffle");
  const randomPost = pool => pool[Math.floor(Math.random() * pool.length)];
  const FACES = 10, STEP = 360 / FACES, FACE_HEIGHT = 200;
  const RADIUS = FACE_HEIGHT / 2 / Math.tan(Math.PI / FACES);  // faces meet edge to edge
  reel.innerHTML = '<div class="drum" id="drum"></div>';
  const drum = document.getElementById("drum");
  let rotation = 0;  // degrees; face i is in front when rotation ≡ i * STEP

  const frontFace = () => ((Math.round(rotation / STEP) % FACES) + FACES) % FACES;
  // Angle of face i relative to the viewer, in [-180, 180): 0 is front, positive is above.
  const faceAngle = i => ((i * STEP - rotation) % 360 + 540) % 360 - 180;
  function setFace(i, post) {
    drum.children[i].outerHTML = cardHtml(post, posts.indexOf(post));
    drum.children[i].style.transform = `rotateX(${i * STEP}deg) translateZ(${RADIUS}px)`;
  }
  function placeDrum() {
    drum.style.transform = `translateZ(${-RADIUS}px) rotateX(${-rotation}deg)`;
  }
  drum.innerHTML = "<div></div>".repeat(FACES);
  for (let i = 0; i < FACES; i++) setFace(i, randomPost(posts));
  placeDrum();

  // Spin the drum a few turns with a decelerating ease and a small overshoot at the end.
  // Faces passing behind the drum get a fresh random post, so the reel never repeats itself;
  // the face that will land in front gets the winning post once it is out of sight.
  function spin() {
    const pool = shown.slice();  // the selection at the moment the button is pressed
    if (!pool.length) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { setFace(frontFace(), randomPost(pool)); return; }
    shuffleButton.disabled = true;
    const start = rotation, target = Math.round(rotation / STEP) * STEP + 3 * 360 + (2 + Math.floor(Math.random() * FACES)) * STEP;
    const winner = ((Math.round(target / STEP) % FACES) + FACES) % FACES;
    const duration = 3600, t0 = performance.now();
    const back = new Array(FACES).fill(true);  // whether a face was already refreshed this time behind
    let locked = false;
    const ease = t => { const c = 0.8; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2; };  // easeOutBack
    (function frame(now) {
      const t = Math.min(1, (now - t0) / duration);
      rotation = start + (target - start) * ease(t);
      placeDrum();
      for (let i = 0; i < FACES; i++) {
        const behind = Math.abs(faceAngle(i)) > 120;
        if (behind && !back[i]) {
          if (target - rotation < 300) {  // final approach: only the winner still changes
            if (i === winner && !locked) { setFace(i, randomPost(pool)); locked = true; }
          } else setFace(i, randomPost(pool));
        }
        back[i] = behind;
      }
      if (t < 1) requestAnimationFrame(frame);
      else {
        rotation = target;
        placeDrum();
        shuffleButton.disabled = false;
        drum.children[winner].classList.add("won");
      }
    })(t0);
  }
  shuffleButton.addEventListener("click", spin);

  function render(query) {
    const q = query.trim().toLowerCase();
    renderChips();
    shown = posts.filter(p => (!q || p.text.toLowerCase().includes(q)) && postInRange(p) &&
                              (!selectedThemes.size || p.themes.some(t => selectedThemes.has(t))));
    document.getElementById("all-title").hidden = !shown.length;
    container.innerHTML = shown.length ? "" : '<p class="posts-empty">Geen posts gevonden.</p>';
    loaded = 0;
    showMore();
  }

  // Cards are added in pages: by the button, or automatically when it scrolls into view.
  const PAGE_SIZE = 60;
  let loaded = 0;
  const moreEl = document.getElementById("more"), moreButton = document.getElementById("more-button");
  function showMore() {
    const next = shown.slice(loaded, loaded + PAGE_SIZE);
    container.insertAdjacentHTML("beforeend", next.map((p, i) => cardHtml(p, loaded + i)).join(""));
    loaded += next.length;
    moreEl.hidden = loaded >= shown.length;
    moreButton.textContent = `Toon meer (nog ${shown.length - loaded})`;
  }
  moreButton.addEventListener("click", showMore);
  new IntersectionObserver(entries => {
    if (entries[0].isIntersecting && loaded < shown.length) showMore();
  }, { rootMargin: "600px" }).observe(moreEl);

  const dialog = document.getElementById("dialog");

  let browsing = [];  // the list prev/next step through
  function openPost(index, list = browsing) {
    browsing = list;
    current = index;
    const p = list[index];
    document.getElementById("dialog-content").innerHTML = `
      <div class="post-meta">${metaHtml(p)}${themeTags(p)}</div>
      <div class="post-text">${formatText(p.text) || "<em>(geen tekst)</em>"}</div>
      <div class="post-links">
        ${p.url ? `<a class="btn btn-primary btn-small" href="${escapeHtml(p.url)}" target="_blank" rel="noopener">Bekijk op LinkedIn</a>` : ""}
        ${p.sharedUrl ? `<a class="btn btn-secondary btn-small" href="${escapeHtml(p.sharedUrl)}" target="_blank" rel="noopener">Gedeelde link</a>` : ""}
      </div>`;
    document.getElementById("prev").disabled = index === 0;
    document.getElementById("next").disabled = index === list.length - 1;
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
  }

  function openCard(el, card) {
    if (el === container) return openPost(+card.dataset.index, shown);
    const post = posts[+card.dataset.index];
    const i = shown.indexOf(post);
    i >= 0 ? openPost(i, shown) : openPost(0, [post]);
  }
  for (const el of [container, reel]) {
    el.addEventListener("click", e => {
      const card = e.target.closest(".post-card");
      if (card) openCard(el, card);
    });
    el.addEventListener("keydown", e => {
      const card = e.target.closest(".post-card");
      if (card && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); openCard(el, card); }
    });
  }
  document.getElementById("close").addEventListener("click", () => dialog.close());
  document.getElementById("prev").addEventListener("click", () => current > 0 && openPost(current - 1));
  document.getElementById("next").addEventListener("click", () => current < browsing.length - 1 && openPost(current + 1));
  dialog.addEventListener("click", e => { if (e.target === dialog) dialog.close(); });  // backdrop click
  dialog.addEventListener("keydown", e => {
    if (e.key === "ArrowLeft" && current > 0) openPost(current - 1);
    if (e.key === "ArrowRight" && current < browsing.length - 1) openPost(current + 1);
  });

  document.getElementById("search").addEventListener("input", e => render(e.target.value));
  render("");

  // Links from the homepage, like posts.html#post-<id>, open that post.
  function openFromHash() {
    const match = location.hash.match(/^#post-(\\w+)$/);
    if (!match) return;
    const i = shown.findIndex(p => p.id === match[1]);
    if (i >= 0) openPost(i, shown);
  }
  openFromHash();
  window.addEventListener("hashchange", openFromHash);
</script>
    <script src="script.js" defer></script>
</body>
</html>
"""


def shorten(text, limit=220):
    """Cut text at a word boundary, with an ellipsis when it was longer."""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def write_sample(posts):
    """posts-random.js: the most recent posts, trimmed to what the homepage block shows.

    A plain script (not JSON) so it also loads when the site is opened from disk.
    """
    visible = [p for p in posts if not p["deleted"]]
    sample = []
    for post in visible[:SAMPLE_SIZE]:
        lines = [line.strip() for line in post["text"].splitlines() if line.strip()]
        body = re.sub(r"(^|\s)#[\w-]+", "", " ".join(lines[1:])).strip()
        sample.append({
            "id": post["id"],
            "date": post["date"][:10],
            "title": lines[0],
            "excerpt": shorten(body),
            "themes": [THEME_NAMES[t] for t in post["themes"]],
        })
    data = json.dumps({"count": len(visible), "posts": sample}, ensure_ascii=False)
    SAMPLE_OUTPUT.write_text(f"// Generated by build_posts_page.py\nwindow.POSTS_SAMPLE = {data};\n", encoding="utf-8")
    print(f"{len(sample)} posts -> {SAMPLE_OUTPUT}")


def main():
    ordered = [p for p in load_posts() if p["date"] >= SINCE and p["text"].strip()]
    for index, post in enumerate(ordered):
        post["themes"] = post_themes(post["text"])
        post["id"] = post_key(post["url"]) or f"n{index}"  # stable id for links like posts.html#post-<id>

    data = json.dumps({"themes": THEME_NAMES, "posts": ordered}, ensure_ascii=False).replace("</", "<\\/")
    OUTPUT.write_text(PAGE.replace("__DATA__", data), encoding="utf-8")
    print(f"{len(ordered)} posts -> {OUTPUT}")
    write_sample(ordered)


if __name__ == "__main__":
    main()
