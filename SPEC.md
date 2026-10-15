# Spec: website-update wimcasteels.be

Doel: de site duidelijker en gebruiksvriendelijker maken, zodat een bezoeker binnen een paar seconden weet (1) wie Wim is, (2) wat hij aanbiedt en (3) hoe hij of zij actie onderneemt: een lezing boeken, het boek kopen of de nieuwsbrief volgen.

## Beslissingen

- **Hoofddoel: lezingen boeken.** Elke pagina stuurt naar een lezingaanvraag. Het boek en de nieuwsbrief zijn secundaire acties: ze ondersteunen je geloofwaardigheid als spreker.
- **De huisstijl van "Het masker van AI" wordt overgenomen** (zie sectie 8).
- **De site blijft gewone HTML**, zonder Jekyll of andere bouwstap.

## Uitvoering (15 oktober 2026)

Alle punten zijn uitgevoerd, met deze uitzonderingen en keuzes:

| Punt | Status |
|---|---|
| 1.3 | **Bewust niet uitgevoerd:** de site blijft gewone HTML (beslist op 15 oktober 2026, na een korte test met Jekyll). Menu en footer staan daardoor in elke pagina: bij een wijziging alle 7 HTML-bestanden aanpassen. |
| 2.2 | De geldigheidsdatum van de kortingscode ontbreekt nog (onbekend). |
| 3.1 | Boekpagina zonder recensies (geen beschikbaar) en alleen een Lannoo-bestellink. De 12 hoofdstukken komen uit de slides van de boekvoorstelling. |
| 3.2 | Geen e-mailveld op de site: de knop "Abonneer gratis" opent de inschrijfpagina op Substack. |
| 3.3 | Aanvraagformulier zonder verplichte velden, stelt een mail op in het e-mailprogramma van de bezoeker (geen externe dienst nodig). Geen quotes of video (niet beschikbaar). Duur staat als "in overleg". |
| 4.1 | Nieuws staat in **`nieuws.json`** met ISO-datums en de categorieën `lezing`, `workshop`, `opinie` en `media`. Sorteren gebeurt automatisch. |
| 4.5 | Lukt het laden van `nieuws.json` niet, dan toont de nieuwspagina een melding. Lokaal bekijken via Live Server, niet door te dubbelklikken (de browser blokkeert dan het inladen). |
| 5.1 | Weboptimale versies staan in `images/web/`. De originelen staan er nog, maar worden niet meer geladen. |
| 5.2 | PDF's niet gecomprimeerd, wel de bestandsgrootte bij de link (`fileInfo`). |
| 7 | Google Analytics laadt pas na akkoord via een cookiemelding. Privacyverklaring op `privacy.html`. |
| 8.3 | Line art: alleen het masker op de 404-pagina. Nieuw paars logo als `images/logo.svg`. |

Elke aanpassing heeft een prioriteit:
- **P1**: grootste winst voor weinig werk, eerst doen
- **P2**: duidelijke verbetering, middelgroot werk
- **P3**: nice-to-have

---

## 1. Navigatie en structuur

### 1.1 Navigatie herordenen naar wat bezoekers zoeken (P1)
**Nu:** `Activiteiten · Lezingen · Over · Nieuws · Contact`. "Activiteiten" en "Lezingen" overlappen, en het boek en de nieuwsbrief, twee kernproducten, staan niet in het menu.
**Voorstel:** `Lezingen · Boek · Nieuwsbrief · Nieuws · Over`, met rechts een opvallende knop **"Boek een lezing"**. Die knop vervangt "Contact" en springt naar het aanvraagformulier of de contactgegevens.
- "Boek" verwijst naar een eigen sectie of pagina (zie 3.1).
- "Nieuwsbrief" linkt rechtstreeks naar Substack, of naar een sectie met inschrijfveld (zie 3.2).

### 1.2 Logo-link op de homepage (P1)
Op `index.html` staat `href="#"`, en `script.js` doet dan niets (`if (targetId === '#') return;` na `preventDefault`). Klikken op het logo doet dus niets. Overal `index.html` gebruiken, of op de homepage naar boven scrollen.

### 1.3 Gedeelde header en footer (P2)
Navigatie en footer staan nu gekopieerd in drie HTML-bestanden, dus elke menuwijziging moet drie keer gebeuren. Opties:
- Jekyll-includes gebruiken (wordt standaard ondersteund door GitHub Pages: `_includes/nav.html`), of
- een kleine JS-include.
Jekyll heeft de voorkeur: het werkt zonder JavaScript en is beter voor SEO.

### 1.4 Toegankelijk mobiel menu (P2)
- `aria-expanded` en `aria-controls` toevoegen aan `.nav-toggle` en ze bijwerken in `script.js`.
- Menu sluiten met de Escape-toets.
- Een "Spring naar inhoud"-link voor toetsenbordgebruikers.

---

## 2. Homepage

### 2.1 Een scherpere hero (P1)
- De tagline "Docent | Onderzoeker | Schrijver | Spreker" is een lijst van rollen, geen boodschap. Voorstel: één zin over wat de bezoeker eraan heeft, bijvoorbeeld *"Ik maak AI begrijpelijk: kritisch, wetenschappelijk en zonder hype."* De rollen kunnen eronder, kleiner.
- Eén primaire knop: **"Boek een lezing"**. Eén secundaire knop: **"Bekijk de lezingen"**, die naar het aanbod gaat. "Activiteiten" als knoptekst zegt weinig.
- In de hero mag een korte zin over de lezingen staan, bijvoorbeeld *"Keynotes en workshops over AI voor organisaties, scholen en events."*
- Sociaal bewijs onder de hero, bijvoorbeeld een strook "Bekend van: Knack · De Tijd · EOS · VAIA · Frankwatching" en "1000+ lezers van de nieuwsbrief".

### 2.2 Duidelijkere tegels (P1)
- Elke tegel krijgt één knop met een werkwoord dat precies zegt wat er gebeurt ("Bekijk lezingen", "Bestel bij Lannoo", "Abonneer gratis").
- Een externe link krijgt een ↗-icoon en `target="_blank" rel="noopener"`. De Lannoo-link opent nu in hetzelfde tabblad.
- De Lannoo-link verschilt tussen de pagina's (`lannoocampus.be` op de homepage, `lannoo.com` op de lezingenpagina). Eén URL kiezen.
- Kortingscode **MaskerAI10** kopieerbaar maken met een klik, en tonen tot wanneer de code geldig is.

### 2.3 Volgorde van de secties (P2)
Voorstel, gericht op lezingen: Hero → **Lezingen (de 4 sessies kort, met een link per sessie)** → Sociaal bewijs (eerder te gast bij, quotes van organisatoren) → Boek en nieuwsbrief (twee kleinere tegels) → Nieuws → Over mij → **Aanvraag lezing**.
Het lezingenaanbod wordt dan de eerste sectie na de hero, en niet één tegel van drie.
"Over mij" mag beknopter op de homepage (2 à 3 zinnen), met een link naar een volledige bio (zie 3.3).

### 2.4 Nieuwsblok op de homepage (P1)
- De nieuwsitems in de HTML zijn verouderd (feb 2026) en worden door JS overschreven. Wie geen JS heeft, of een zoekmachine, ziet oud nieuws. Ofwel bij elke update meewerken, ofwel genereren met Jekyll (zie 4.1).
- "Lees meer" verwijst nu naar `nieuws.html` en niet naar het item zelf. Beter: rechtstreeks naar het artikel of de PDF linken.
- Het label (Media / Lezing) ook op de homepage tonen.

### 2.5 Kleine tekstfouten (P1)
- "Geinteresseerd" → "Geïnteresseerd".
- Er staat een losse `"` achteraan de derde alinea van "Over mij" ("…maatschappelijke impact."").
- De Google Scholar-link gebruikt `scholar.google.co.th`. Beter: `scholar.google.com`.
- De huisstijl spreekt de lezer aan met "je". De tegel "Lezingen & Workshops" zegt nog "uw organisatie".

---

## 3. Inhoudspagina's

### 3.1 Aparte boekpagina `boek.html` (P2)
Met de cover, een korte samenvatting, de 12 hoofdstukthema's, citaten uit recensies of van lezers, de kortingscode, bestellinks (Lannoo, Standaard Boekhandel, bol.com) en een link naar de boekvoorstelling of lezing 1.

### 3.2 Nieuwsbrief: inschrijven zonder de site te verlaten (P2)
Het embed-formulier van Substack (een e-mailveld met een knop) op de homepage en/of in de footer plaatsen, eventueel met een link naar de laatste editie.

### 3.3 Lezingenpagina sterker maken (P1/P2)
- ✅ **Gedaan op 15 oktober 2026:** het aanbod is herleid tot de lezing *Het masker van AI* (met de boekcover en 10 mogelijke thema's) en de workshop *AI-vaardigheid* (met de afbeelding van de vier V's). Bij allebei staat dat de inhoud wordt afgestemd op het publiek en op de actualiteit. Elk heeft een eigen mail-knop met voorgevuld onderwerp. De lezingen *De spiegel van AI* en *Van chatbot naar AI-agent* zijn van de pagina gehaald.
- **P1:** contactgegevens of een rechtstreekse mail-knop op de pagina zelf, met een voorgevuld onderwerp, bijvoorbeeld `mailto:…?subject=Aanvraag lezing`. Nu moet de bezoeker eerst terug naar de homepage.
- **P1:** per lezing praktische info: duur, doelpubliek, niveau (inleidend of technisch), formaat (keynote of workshop), taal, online of fysiek.
- **P2:** een strook "Eerder te gast bij…" met logo's of namen (ICT Praktijkdag, KU Leuven, Dag van de Wetenschap, …) en 2 à 3 quotes van organisatoren.
- **P2:** per lezing een foto, en waar mogelijk een korte video of de slides (`pdf/`).
- **P1 (opgewaardeerd, want dit is het hoofddoel):** een aanvraagformulier (Formspree of Tally, gratis) met velden voor organisatie, datum, locatie of online, aantal deelnemers, gewenste lezing en budget. Een formulier verlaagt de drempel ten opzichte van een blanco mail, en je krijgt meteen de info die je nodig hebt.
- **P2:** onder het formulier een korte uitleg van wat er na de aanvraag gebeurt ("Je krijgt binnen 3 werkdagen antwoord").

### 3.4 Perskit / over-pagina (P3)
Een korte en een lange bio om te kopiëren, foto's in hoge resolutie om te downloaden, en de kernthema's. Dat bespaart organisatoren mails.

---

## 4. Nieuwspagina

### 4.1 Uniforme en sorteerbare datums (P1)
`nieuws.json` mengt Nederlandse en Engelse maandnamen en verschillende schrijfwijzen ("Juni 9", "Jun 18", "Mar 21", "Mrt 07", "Okt", "Mei"). Voorstel:
- In de JSON een ISO-datum opslaan (`"date": "2026-06-09"`).
- In JS formatteren met `toLocaleDateString('nl-BE', { day: 'numeric', month: 'long', year: 'numeric' })`, wat "9 juni 2026" geeft.
- Automatisch sorteren op datum, zodat de volgorde in het bestand niet meer uitmaakt.

### 4.2 Betere filtering (P2)
- Extra categorieën: *Opiniestukken*, *Lezingen*, *Workshops*, *Podcasts/interviews*.
- Optioneel: filteren per jaar of groeperen met jaartallen als tussenkoppen.
- Het aantal items per filter tonen ("Media (23)").
- De gekozen filter in de URL bewaren (`nieuws.html#media`), zodat je er rechtstreeks naar kunt linken.

### 4.3 Komende en voorbije events scheiden (P2)
Lezingen met een datum in de toekomst bovenaan tonen in een blok "Binnenkort".

### 4.4 Ontbrekende opiniestukken (P1, ✅ gedaan op 15 oktober 2026: de 6 stukken hieronder staan nu in `nieuws.json`)
Vergeleken met de auteurspagina van Knack (15 oktober 2026) ontbreken deze stukken in `nieuws.json`:
- 25 sep 2026: *"AI-agent die plots 'ontsnapt' is? Zo'n model doet exact wat gevraagd wordt"*
- 11 aug 2026: *"De eerste autonome AI-hack is een feit, wie houdt de controle?"*
- 21 jul 2026: *"Het schrijven was het denken (maar nu zit er steeds vaker AI tussen ons in)"*
- 10 jul 2026: *"Parkeerboete terwijl ik in de wagen zat? Scanwagens hebben geen oogje om dicht te knijpen"*

Van De Tijd (de auteurspagina werd manueel gecontroleerd, want de site blokkeert scripts) ontbreken:
- *"Laten we AI vooral niet als een natuurverschijnsel zien"* (18 sep 2026)
- *"Waarom subsidieert Vlaanderen de chipfabrieken van Taiwan?"* (16 jul 2026)

Het meest recente item op de site dateert van 9 juni 2026. Voor een spreker oogt een nieuwspagina die vier maanden stilstaat minder actief dan je in werkelijkheid bent.

### 4.5 Lege toestand en foutmelding (P3)
Lukt het laden van `nieuws.json` niet, dan blijft de pagina nu leeg. Toon dan een melding.

---

## 5. Performantie

### 5.1 Afbeeldingen optimaliseren (P1)
De afbeeldingen zijn veel te zwaar voor het web:

| Bestand | Nu | Doel |
|---|---|---|
| `nieuwsbrief1.png` | 6,2 MB | < 150 kB (WebP/JPG) |
| `prof_pic.jpg` | 1,9 MB | < 150 kB |
| `lezing.jpg` | 1,7 MB | < 200 kB |
| `logo.png` | 900 kB | < 20 kB (of SVG) |
| `book.jpg` | 760 kB | < 150 kB |

Daarnaast `width`/`height` en `loading="lazy"` toevoegen aan afbeeldingen onder de vouw. Waarschijnlijk is dit de grootste snelheidswinst, zeker op mobiel.

### 5.2 PDF's (P2)
De slides-PDF's zijn 2 tot 20 MB groot. Comprimeer ze, of toon de bestandsgrootte bij de link ("PDF, 20 MB").

### 5.3 Animatie zonder JS-afhankelijkheid (P3)
`script.js` zet `opacity: 0` op alle secties en laat ze daarna invaden. Faalt het script of laadt het traag, dan blijft de inhoud onzichtbaar. Beter: de verborgen toestand in CSS laten afhangen van een klasse `js` op `<html>`, en `prefers-reduced-motion` respecteren.

---

## 6. Vindbaarheid en delen

### 6.1 Metadata (P1)
- Open Graph- en Twitter-tags (`og:title`, `og:description`, `og:image`), zodat links op LinkedIn en WhatsApp er verzorgd uitzien.
- Een betere `meta description` op de homepage. Nu is die gelijk aan de titel.
- `<link rel="canonical">`.

### 6.2 Structured data (P2)
JSON-LD voor `Person` (met `sameAs`-links naar LinkedIn, Substack en Scholar) en voor `Book` (Het masker van AI).

### 6.3 Sitemap en 404 (P3)
`sitemap.xml`, `robots.txt` en een eigen `404.html` met links naar de hoofdpagina's.

---

## 7. Privacy en juridisch (P2)

Google Analytics laadt zonder toestemming van de bezoeker. Voor een Belgische site valt dat onder de GDPR- en cookieregels. Opties:
- overstappen op een cookieloze tool (Plausible, GoatCounter, Cloudflare Web Analytics), zodat geen banner nodig is, of
- een eenvoudige consentbanner toevoegen.

Daarnaast een korte privacyverklaring linken in de footer.

---

## 8. Visuele stijl: huisstijl "Het masker van AI" (P1, beslist)

De site stapt over van blauw op wit naar **paars op cream**, zodat site, boek, nieuwsbrief en sociale media één herkenbaar geheel vormen.

### 8.1 Kleuren (CSS-variabelen in `styles.css`)
| Variabele | Nu | Nieuw | Rol |
|---|---|---|---|
| `--accent-color` | `#3b82f6` | `#5B3A8C` masker-paars | knoppen, links, accenten |
| `--accent-hover` | `#2563eb` | `#3A2459` diep paars | hover, actieve toestand |
| `--primary-color` | `#0f172a` | `#3A2459` diep paars | titels |
| `--text-color` | `#1e293b` | `#1F1A2E` inkt-zwart | lopende tekst |
| `--bg-color` | `#ffffff` | `#F5EFE3` cream paper | achtergrond |
| `--bg-secondary` | `#f8fafc` | een iets donkerdere cream, bijvoorbeeld `#EDE4D3` | afwisselende secties |
| `--border-color` | `#e2e8f0` | een zacht paars of beige, bijvoorbeeld `#D9CDE8` | randen |
| (nieuw) `--accent-light` | | `#9B7DC4` zacht paars | badges, labels, decoratie |

Regels uit de huisstijl:
- **Eén kleur: paars.** De news-labels per categorie (nu mogelijk in verschillende kleuren) worden tinten paars.
- **Warm cream, geen klinisch wit** als achtergrond. Kaarten mogen een lichtere cream krijgen voor contrast.
- Contrast controleren: zacht paars `#9B7DC4` is te licht voor tekst op cream, dus alleen gebruiken voor decoratie.

### 8.2 Typografie
- Inter blijft voor de lopende tekst. De huisstijl beveelt een rustige schreefloze letter voor het web aan.
- Titels optioneel in een serif (Georgia, of via Google Fonts bijvoorbeeld *Lora* of *Fraunces*), in lijn met de grafieken van het merk. Rust en lucht, weinig vet.

### 8.3 Beeld
- Paarse line-art-illustraties op cream (in de stijl van de nieuwsbriefcovers) als sfeerbeelden, bijvoorbeeld bij de hero, de lezingen en de 404-pagina.
- Foto's (profielfoto, lezingfoto) blijven foto's, maar krijgen afgeronde hoeken en een dunne paarse rand, of een subtiele duotoon, zodat ze in het palet passen.
- Het logo en de favicon in paars. Een SVG-versie maken (zie 5.1).

### 8.4 Toon van de teksten
- Lezer aanspreken met "je", geen "u".
- Geen em dashes (—), geen uitroeptekens, geen hype-woorden.
- Kort, actief en concreet.

### 8.5 Verder
- Een rijkere footer: snelle links, sociale iconen (LinkedIn, Substack), een inschrijfveld voor de nieuwsbrief en een privacylink.
- Dark mode via `prefers-color-scheme` (P3).
- Contrastcontrole: `--text-muted: #94a3b8` op wit haalt WCAG AA niet voor gewone tekst.

---

## 9. Dynamische inhoud

### 9.1 Laatste nieuwsbriefedities automatisch tonen (P1)
**Doel:** de homepage oogt elke week vers, zonder dat je iets hoeft bij te werken.

**Werking:**
- Een GitHub Action (`.github/workflows/substack.yml`) draait elke zaterdag om 10:00 UTC, kort na het verschijnen van de nieuwsbrief, en kan ook manueel gestart worden (`workflow_dispatch`).
- Een klein script (`scripts/update_substack.py`) haalt `https://wimcasteels.substack.com/feed` op en schrijft de laatste 3 edities naar `substack.json`, met titel, datum (ISO), link, korte samenvatting en eventueel een coverafbeelding.
- De Action commit alleen als er iets veranderd is. GitHub Pages publiceert de site daarna vanzelf opnieuw.
- `script.js` laadt `substack.json` en toont een blok **"Uit de nieuwsbrief"** op de homepage, met 3 kaarten en de knop "Abonneer gratis".

**Waarom via een Action:** Substack blokkeert ophalen vanuit de browser (CORS), dus een client-side fetch werkt niet.

**Randvoorwaarden:**
- Lukt het ophalen niet, dan blijft de vorige `substack.json` staan. De site toont nooit een leeg blok.
- Het exacte feed-adres nakijken. Dat hangt af van je Substack-subdomein of eigen domein.
- Opmaak volgens de huisstijl (sectie 8): paarse accenten op cream en een lichte datum-badge.
- Plaats op de homepage: na het nieuwsblok, of samengevoegd met de tegel "Nieuwsbrief".

### 9.2 Kleine animaties (P2)
**Doel:** de site een eigen, levendig gevoel geven zonder de rust van de huisstijl te verstoren. Alles in CSS en een paar regels JS, zonder extra bibliotheek.

**a) Handgetekende onderstreping onder sectietitels**
- Onder elke `.section-title` een paarse SVG-lijn met een licht onregelmatige vorm, zoals een potloodstreep.
- Zodra de sectie in beeld komt, "tekent" de lijn zich van links naar rechts (`stroke-dasharray`/`stroke-dashoffset`, ± 0,8 s, ease-out).
- Gebeurt één keer per titel, geen herhaling.

**b) Knoppen**
- De knoptekst krijgt een pijltje → dat bij hover 3 à 4 px naar rechts schuift.
- Achtergrond van masker-paars `#5B3A8C` naar diep paars `#3A2459`, met een overgang van 150 à 200 ms.
- Een zichtbare focusring (paars) voor wie met het toetsenbord navigeert.

**c) Kaarten (lezingen, nieuws, tegels)**
- Bij hover komen ze 2 à 4 px omhoog, met een iets diepere schaduw en een dunne paarse rand.
- Een foto in de kaart zoomt licht in (`scale(1.03)`) binnen een kader dat overloop verbergt.
- Overgang van 200 à 250 ms. Op touchtoestellen geen hover-effect (`@media (hover: hover)`).

**d) Getrapte fade-in (vervangt de huidige fade-in)**
- Kaarten in een grid verschijnen kort na elkaar (± 80 ms ertussen) met een kleine opwaartse beweging (8 à 12 px).
- De verborgen toestand hangt af van een klasse `js` op `<html>`. Zonder JavaScript is alle inhoud meteen zichtbaar. Dit lost 5.3 mee op.

**Spelregels**
- `@media (prefers-reduced-motion: reduce)`: alle animaties en overgangen uit, alles meteen zichtbaar.
- Geen herhalende animaties, geen typemachine-effecten, geen parallax.
- Alleen `transform` en `opacity` animeren, voor vloeiende prestaties op mobiel.

## Voorgestelde aanpak in fasen

1. **Snelle winst (± 1 dag):** 1.1, 1.2, 2.1, 2.2, 2.4, 2.5, 3.3 (P1, inclusief het aanvraagformulier), 4.1, 4.4, 5.1, 6.1, 8.1, 8.4
2. **Structuur (± 1 à 2 dagen):** 1.3 (Jekyll), 2.3, 3.1, 3.2, 4.2, 4.3, 7, 8.2, 8.3, 9.1, 9.2
3. **Afwerking:** 1.4, 3.4, 5.2, 5.3, 6.2, 6.3, 8.5

## Open vragen
- Aanvragen gaan nu naar `wim.casteels@ap.be`. Liever een ander adres, of toch een formulierdienst zoals Formspree of Tally?
- Richtprijzen: voorlopig niet getoond.
- Zijn er quotes of logo's van organisatoren die gebruikt mogen worden?
- Tot wanneer is de kortingscode MaskerAI10 geldig?
- Engelstalige versie: voorlopig niet.
