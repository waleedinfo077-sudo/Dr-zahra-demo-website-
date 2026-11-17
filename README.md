# Dr. Sameen Zahra — Dermatology & Aesthetics (demo site)

A fast, accessible, static marketing site for a dermatology and aesthetics practice in Lahore.
No frameworks, no build step required to view it, no external JavaScript dependencies.

## Quick start

Open `index.html` directly, or serve the folder (recommended, so fonts and paths behave):

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## What's in here

```
index.html           Home
about.html           About Dr. Zahra, philosophy, credentials, clinics
treatments.html      Ten treatments, filterable, with expandable details
products.html        Routine builder, product shelf, guidance
education.html       Searchable guides, skincare myths
contact.html         Appointment form + clinic information
404.html             Not-found page
css/style.css        Design system and all components
js/data.js           All site content (single source of truth)
js/main.js           Interactions (nav, slider, filters, form, gallery)
build.py             Renders the HTML pages from data + shared layout
assets/images/       Photography (AI-generated placeholders — see below)
assets/favicon.svg   Mark
sitemap.xml, robots.txt
```

## Editing content

Everything text-based lives in **`js/data.js`** — clinics, phone/WhatsApp, treatments,
products, guides, testimonials, FAQs and stats. Edit it, then regenerate the pages:

```bash
python3 build.py      # requires Node.js (reads js/data.js and writes the HTML)
```

`build.py` also renders `index.html`, `about.html`, `treatments.html`, `products.html`,
`education.html`, `contact.html` and `404.html`, plus `sitemap.xml` and `robots.txt`.
Never hand-edit the generated HTML — your changes will be overwritten.

### Before going live — replace these placeholders

| What | Where |
| --- | --- |
| Phone, WhatsApp, email, addresses, hours | `js/data.js` → first block + `clinics` |
| Instagram / YouTube / Google Maps links | `js/data.js` → `instagram`, `youtube`, `maps` |
| Canonical domain for SEO tags & sitemap | `build.py` → `BASE` |
| Credentials, years, registration numbers | `build.py` → `about()` credentials list |
| Testimonials | `js/data.js` → `testimonials` (use consented, real reviews) |
| Products and prices | `js/data.js` → `products` |
| Google Analytics / Meta Pixel | add before `</head>` in `build.py` → `render()` |

The clinic hours card, medical disclaimer and demo notices are intentionally marked as
placeholder content in the UI so nothing misleading ships by accident.

## Photography

`assets/images/` contains **AI-generated placeholder photography** created for this demo:
clinic interiors, a doctor portrait, treatment scenes and product stills. They are
representative only and are **not** photos of the real Dr. Zahra or her clinics.
Before publishing, replace them with the practice's own photography (portrait/editorial
crops, roughly 4:5, at least 1200 × 1500px) using the same filenames:

```
hero-portrait.jpg     about-seated.jpg      about-consult.jpg
clinic-reception.jpg  clinic-room.jpg       clinic-detail.jpg
treatment-facial.jpg  treatment-laser.jpg   products-flatlay.jpg
education-desk.jpg    og-image.jpg (1200 × 630 social card)
```

## The appointment form

There is no backend. Submitting validates the form, shows a confirmation state and
prepares a pre-filled WhatsApp message — an honest, working flow for a small clinic.
To use email instead, point the form at a service such as Formspree, Netlify Forms or
Basin, or add a small serverless function; the field names are `name`, `phone`, `email`,
`concern`, `clinic`, `date`, `time`, `visit`, `message`, `consent`.

## Accessibility & performance notes

- Semantic landmarks, skip link, visible focus states, labelled form fields and errors.
- All interactive components are keyboard operable; the gallery uses a native `<dialog>`.
- FAQ accordions use native `<details>`, so they work without JavaScript.
- Respects `prefers-reduced-motion`; images are lazy-loaded with intrinsic dimensions
  to avoid layout shift.
- No fonts or scripts block rendering; the only third-party request is Google Fonts.

## Deploying

The site is fully static. Push the repository and enable GitHub Pages, or drag the folder
into Netlify/Vercel. For GitHub Pages, update `BASE` in `build.py`, run the build, commit,
then publish the repository root.

## Credits

Design and build: custom, hand-written HTML/CSS/JS. Typefaces: Fraunces and DM Sans
(Google Fonts, open licence). Imagery: AI-generated for this demo.
