#!/usr/bin/env python3
"""
Static site generator for the Dr. Sameen Zahra demo site.

Content lives in js/data.js (window.SITE). This script reads it with Node,
renders every page into the repository root, and shares one header/footer.
Run:  python3 build.py
"""
from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://solaceaesthetics.pk"
YEAR = date.today().year

NAV = [
    ("index", "Home"),
    ("about", "About"),
    ("treatments", "Treatments"),
    ("products", "Products"),
    ("education", "Education"),
    ("contact", "Contact"),
]

# --------------------------------------------------------------------------- icons
ICONS = {
    "arrow-right": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "arrow-up-right": '<path d="M7 17 17 7M8 7h9v9"/>',
    "chevron-left": '<path d="m15 5-7 7 7 7"/>',
    "chevron-right": '<path d="m9 5 7 7-7 7"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "check": '<path d="m4 12.5 5 5L20 6.5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.5l3.5 2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "message": '<path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.5L3 21l2-5.4A8.5 8.5 0 1 1 21 11.5Z"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "youtube": '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="m10.5 9.5 5 2.5-5 2.5Z"/>',
    "star": '<path d="m12 3.5 2.7 5.7 6.3.8-4.6 4.4 1.2 6.1L12 17.6l-5.6 2.9 1.2-6.1L3 10l6.3-.8Z"/>',
    "drop": '<path d="M12 3s6 6.5 6 10.5A6 6 0 0 1 6 13.5C6 9.5 12 3 12 3Z"/>',
    "spark": '<path d="m12 3 1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9Z"/><path d="M18.5 15.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7Z"/>',
    "sun": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.2M12 19.8V22M4.2 12H2M22 12h-2.2M5.6 5.6l1.6 1.6M16.8 16.8l1.6 1.6M18.4 5.6l-1.6 1.6M7.2 16.8l-1.6 1.6"/>',
    "shield": '<path d="M12 3 5 5.8v5.4c0 4.4 2.9 7.5 7 9 4.1-1.5 7-4.6 7-9V5.8Z"/><path d="m9 12 2 2 4-4"/>',
    "layers": '<path d="m12 3 9 4.7-9 4.7-9-4.7Z"/><path d="m3 12.4 9 4.7 9-4.7"/><path d="m3 16.6 9 4.7 9-4.7"/>',
    "zap": '<path d="M13.5 2 4.5 14h6l-1 8 9-12h-6Z"/>',
    "leaf": '<path d="M20.5 3.5S9 3.7 5.4 9.3A8.2 8.2 0 0 0 4 19.7c5 .4 10.2-1.6 13.2-6.7 2-3.4 3.3-9.5 3.3-9.5Z"/><path d="M4 20c2.8-5.2 6.2-7.6 11.5-9.7"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m16.5 16.5 4.5 4.5"/>',
    "heart": '<path d="M20.7 5.7a5.4 5.4 0 0 0-7.7 0l-1 1-1-1a5.4 5.4 0 0 0-7.7 7.7L12 21.5l8.7-8.1a5.4 5.4 0 0 0 0-7.7Z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="16" rx="2.5"/><path d="M8 3v4M16 3v4M3.5 10.5h17"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.8h.01"/>',
    "quote": '<path d="M9.5 6C6.4 7.6 5 10.2 5 13.4V18h6v-6H8.2c0-2 .8-3.5 2.5-4.6Z"/><path d="M19 6c-3.1 1.6-4.5 4.2-4.5 7.4V18h6v-6h-2.8c0-2 .8-3.5 2.5-4.6Z"/>',
}

DATA = None
ACTIVE_CLS = ' class="is-active"'
DOT_ACTIVE = ' class="is-active"'
ARIA_CURRENT = ' aria-current="page"'


def load_data() -> dict:
    js = (
        "const fs=require('fs');global.window={};"
        "eval(fs.readFileSync('js/data.js','utf8'));"
        "process.stdout.write(JSON.stringify(window.SITE));"
    )
    out = subprocess.run(["node", "-e", js], cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("Could not read js/data.js:\n" + out.stderr)
    return json.loads(out.stdout)


def icon(name: str, cls: str = "") -> str:
    klass = f" ico {cls}".strip()
    return f'<svg class="{klass}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def sprite() -> str:
    symbols = "".join(
        f'<symbol id="i-{name}" viewBox="0 0 24 24">{body}</symbol>'
        for name, body in ICONS.items()
    )
    return (
        '<svg class="sprite" aria-hidden="true" focusable="false" width="0" height="0">'
        f"{symbols}</svg>"
    )


# --------------------------------------------------------------------------- chrome
def brand(mark_class="brand"):
    return f'''<a class="{mark_class}" href="index.html" aria-label="Dr. Sameen Zahra — home">
        <span class="brand-mark" aria-hidden="true">SZ</span>
        <span class="brand-text"><strong>Dr. Sameen Zahra</strong><small>Dermatology &amp; Aesthetics</small></span>
      </a>'''


def header(file: str) -> str:
    links = "".join(
        f'<a href="{slug}.html"{ACTIVE_CLS if slug == file else ""}{ARIA_CURRENT if slug == file else ""}>{label}</a>'
        for slug, label in NAV
    )
    drawer_links = "".join(
        f'<a href="{slug}.html"{ACTIVE_CLS if slug == file else ""}><span>{label}</span>{icon("arrow-up-right")}</a>'
        for slug, label in NAV
    )
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-head" id="site-head">
  <div class="utility">
    <div class="shell utility-in">
      <p class="utility-note"><span class="pulse" aria-hidden="true"></span> Accepting new patients in Lahore <span class="utility-sep" aria-hidden="true">·</span> <a href="contact.html">Book a consultation</a></p>
      <div class="utility-meta">
        <a href="tel:{DATA['phoneHref']}" class="utility-link">{icon("phone")}<span>{DATA['phoneDisplay']}</span></a>
        <span class="utility-sep" aria-hidden="true">·</span>
        <a href="{DATA['instagram']}" class="utility-link" target="_blank" rel="noopener">Instagram</a>
        <a href="{DATA['youtube']}" class="utility-link" target="_blank" rel="noopener">YouTube</a>
      </div>
    </div>
  </div>
  <div class="head">
    <div class="shell head-in">
      {brand()}
      <nav class="nav" id="nav" aria-label="Primary">{links}</nav>
      <div class="head-actions">
        <a class="btn btn--sm btn--primary" href="contact.html">Book a consultation {icon("arrow-right")}</a>
        <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">
          <span></span><span></span>
        </button>
      </div>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-top">{brand("brand brand--stack")}
    <button class="drawer-close" type="button" aria-label="Close menu">{icon("close")}</button>
  </div>
  <nav class="drawer-nav" aria-label="Mobile">{drawer_links}</nav>
  <div class="drawer-foot">
    <a class="btn btn--primary" href="contact.html">Book a consultation {icon("arrow-right")}</a>
    <a class="drawer-call" href="tel:{DATA['phoneHref']}">{icon("phone")} {DATA['phoneDisplay']}</a>
    <p>{DATA['clinics'][0]['address']}</p>
  </div>
</div>
<div class="scrim" id="scrim" hidden></div>'''


def footer() -> str:
    explore = "".join(f'<a href="{s}.html">{l}</a>' for s, l in NAV)
    treatments = "".join(
        f'<a href="treatments.html">{t["title"]}</a>' for t in DATA["treatments"][:5]
    )
    clinics = "".join(
        f'<div class="foot-clinic"><b>{c["name"]}</b><span>{c["address"]}</span><span>{c["hours"]}</span></div>'
        for c in DATA["clinics"]
    )
    return f'''<footer class="site-foot">
  <div class="shell foot-grid">
    <div class="foot-brand">
      {brand("brand brand--foot")}
      <p>Evidence-based dermatology and aesthetics in Lahore, led by Dr. Sameen Zahra — MSc Dermatology (USA), MPH.</p>
      <div class="foot-social">
        <a href="{DATA['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
        <a href="{DATA['youtube']}" target="_blank" rel="noopener" aria-label="YouTube">{icon("youtube")}</a>
        <a href="mailto:{DATA['email']}" aria-label="Email">{icon("mail")}</a>
      </div>
    </div>
    <nav class="foot-col" aria-label="Explore">
      <h2 class="foot-title">Explore</h2>
      {explore}
    </nav>
    <nav class="foot-col" aria-label="Treatments">
      <h2 class="foot-title">Treatments</h2>
      {treatments}
      <a href="treatments.html" class="foot-more">All treatments {icon("arrow-right")}</a>
    </nav>
    <div class="foot-col foot-col--visit">
      <h2 class="foot-title">Visit</h2>
      {clinics}
      <p class="foot-contact"><a href="tel:{DATA['phoneHref']}">{DATA['phoneDisplay']}</a><br><a href="mailto:{DATA['email']}">{DATA['email']}</a></p>
    </div>
  </div>
  <div class="shell foot-bottom">
    <p>&copy; {YEAR} Dr. Sameen Zahra. All rights reserved.</p>
    <p class="foot-disc">This site is for information only and is not medical advice. For urgent concerns, contact the clinic directly.</p>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{DATA['wa']}" data-wa target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <span class="wa-float-icon">{icon("message")}</span><span class="wa-float-text">Chat with the clinic</span>
</a>
<button class="to-top" type="button" aria-label="Back to top">{icon("arrow-right")}</button>'''


def lightbox() -> str:
    return '''<dialog class="lightbox" id="lightbox" aria-label="Clinic gallery">
  <button class="lightbox-close" type="button" aria-label="Close gallery">&#215;</button>
  <button class="lightbox-nav lightbox-prev" type="button" aria-label="Previous image">&#8249;</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lightbox-nav lightbox-next" type="button" aria-label="Next image">&#8250;</button>
</dialog>'''


# --------------------------------------------------------------------------- components
def eyebrow(text: str, light: bool = False) -> str:
    return f'<p class="eyebrow{" eyebrow--light" if light else ""}"><span class="eyebrow-dash" aria-hidden="true"></span>{text}</p>'


def section_head(number: str, label: str, title: str, lead: str = "", link: tuple[str, str] | None = None) -> str:
    link_html = (
        f'<a class="link-arrow" href="{link[0]}">{link[1]} {icon("arrow-right")}</a>' if link else ""
    )
    lead_html = f'<p class="sec-lead">{lead}</p>' if lead else ""
    return f'''<div class="sec-head reveal">
      <div class="sec-head-main">
        {eyebrow(f"{number} — {label}" if number else label)}
        <h2>{title}</h2>
      </div>
      <div class="sec-head-side">{lead_html}{link_html}</div>
    </div>'''


def page_hero(
    file: str,
    label: str,
    title: str,
    lead: str,
    image: str,
    alt: str,
    meta: list[str] | None = None,
    eyebrow_text: str = "",
    secondary: tuple[str, str] = ("treatments.html", "View treatments"),
) -> str:
    crumbs = f'<a href="index.html">Home</a><span aria-hidden="true">/</span><span>{label}</span>'
    meta_html = ""
    if meta:
        meta_html = '<ul class="page-hero-meta">' + "".join(
            f'<li>{m}</li>' for m in meta
        ) + "</ul>"
    return f'''<section class="page-hero">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
    <div class="page-hero-grid">
      <div class="page-hero-copy">
        {eyebrow(eyebrow_text or label)}
        <h1 class="display">{title}</h1>
        <p class="lead">{lead}</p>
        {meta_html}
        <div class="row">
          <a class="btn btn--primary" href="contact.html">Book a consultation {icon("arrow-right")}</a>
          <a class="btn btn--ghost" href="{secondary[0]}">{secondary[1]}</a>
        </div>
      </div>
      <figure class="arch arch--page reveal">
        <img src="{image}" alt="{alt}" width="768" height="1376" fetchpriority="high">
      </figure>
    </div>
  </div>
</section>'''


def marquee() -> str:
    words = ["Acne", "Rosacea", "Pigmentation", "Psoriasis", "Chemical peels", "Laser &amp; light", "Skin boosters", "Hair &amp; scalp", "Skin checks"]
    items = "".join(f'<span class="marquee-item">{w} <i aria-hidden="true">&#10022;</i></span>' for w in words)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{items}{items}</div></div>'


def stat_band() -> str:
    stats = "".join(
        f'''<div class="stat reveal">
          <b data-count="{s['n']}" data-suffix="{s['suffix']}">{s['n']}{s['suffix']}</b>
          <span>{s['label']}</span>
        </div>'''
        for s in DATA["stats"]
    )
    return f'''<section class="stat-band" aria-label="Practice at a glance">
  <div class="shell">
    <div class="stat-grid">{stats}</div>
  </div>
</section>'''


def treatments_preview() -> str:
    cards = "".join(
        f'''<a class="tx-mini reveal" href="treatments.html">
          <span class="tx-icon">{icon(t["icon"])}</span>
          <span class="tx-tag">{t["tag"]}</span>
          <h3>{t["title"]}</h3>
          <p>{t["summary"]}</p>
          <span class="tx-go">{icon("arrow-up-right")}</span>
        </a>'''
        for t in DATA["treatments"][:6]
    )
    return f'''<section class="section section--cream" id="treatments">
  <div class="shell">
    {section_head("02", "Treatments", "Care for the skin you actually have", "Medical dermatology and considered aesthetics, chosen after an assessment — never off a trend.", ("treatments.html", "All treatments"))}
    <div class="tx-grid">{cards}</div>
  </div>
</section>'''


def process(number: str = "03") -> str:
    steps = [
        ("01", "Consultation", "We go through your history, triggers, current products and goals — then look closely at your skin, in good light."),
        ("02", "Your plan", "You leave with a written, staged plan: what to use, what to stop, what it costs, and how long it should realistically take."),
        ("03", "Review", "Follow-ups happen at set intervals. We adjust the plan based on how your skin responds, not on a fixed script."),
    ]
    cards = "".join(
        f'''<li class="step reveal">
          <span class="step-num">{n}</span>
          <h3>{title}</h3>
          <p>{text}</p>
        </li>'''
        for n, title, text in steps
    )
    return f'''<section class="section" id="how-it-works">
  <div class="shell">
    {section_head(number, "How it works", "Three steps, no surprises", "The same consultation-first process at both clinics.")}
    <ol class="steps">{cards}</ol>
    <p class="steps-note reveal">{icon("info")} First consultations usually last 30–45 minutes. Bring your current products and any past prescriptions.</p>
  </div>
</section>'''


def products_preview() -> str:
    cards = "".join(product_card(p, i) for i, p in enumerate(DATA["products"][:3]))
    return f'''<section class="section section--cream" id="products">
  <div class="shell">
    {section_head("04", "The routine", "Fewer products. Better skin.", "Three steps do most of the work. Everything else is optional — this is the shelf we actually recommend.", ("products.html", "Build your routine"))}
    <div class="prod-grid prod-grid--3">{cards}</div>
  </div>
</section>'''


def product_card(p: dict, i: int) -> str:
    return f'''<article class="prod-card reveal" data-time="{p["time"]}">
      <div class="prod-top"><span class="pill">{p["time"]}</span><span class="prod-num">{i + 1:02d}</span></div>
      <h3>{p["name"]}</h3>
      <p class="prod-actives">{p["actives"]}</p>
      <p class="prod-desc">{p["desc"]}</p>
      <details class="prod-use"><summary>How to use {icon("chevron-down")}</summary><p>{p["use"]}</p></details>
    </article>'''


def testimonials() -> str:
    slides = "".join(
        f'''<figure class="slide" role="group" aria-roledescription="slide" aria-label="{i + 1} of {len(DATA["testimonials"])}">
          <span class="stars" aria-label="Five out of five">{icon("star") * 5}</span>
          <blockquote>{t["quote"]}</blockquote>
          <figcaption><span class="avatar" aria-hidden="true">{t["name"][0]}</span><span><b>{t["name"]}</b><small>{t["meta"]}</small></span></figcaption>
        </figure>'''
        for i, t in enumerate(DATA["testimonials"])
    )
    dots = "".join(
        f'<button type="button" aria-label="Show story {i + 1}"{DOT_ACTIVE if i == 0 else ""}></button>'
        for i in range(len(DATA["testimonials"]))
    )
    return f'''<section class="section section--ink" id="stories">
  <div class="shell stories-grid">
    <div class="stories-copy reveal">
      {eyebrow("05 — Patient stories", True)}
      <h2>In their words.</h2>
      <p class="sec-lead">A calm clinic, clear explanations and plans people can keep.</p>
      <div class="slider-controls">
        <button class="round-btn" type="button" data-slide="prev" aria-label="Previous story">{icon("arrow-right")}</button>
        <button class="round-btn" type="button" data-slide="next" aria-label="Next story">{icon("arrow-right")}</button>
      </div>
    </div>
    <div class="slider reveal" data-slider>
      <div class="slider-track">{slides}</div>
      <div class="slider-dots">{dots}</div>
      <p class="slider-note">Sample stories for this demo — replace with consented patient reviews.</p>
    </div>
  </div>
</section>'''


GALLERY = [
    ("assets/images/clinic-reception.jpg", "The reception at Solace Aesthetics — warm plaster, oak and soft light."),
    ("assets/images/clinic-room.jpg", "A treatment room, set up for a consultation and peel."),
    ("assets/images/clinic-detail.jpg", "Linen, glass and steel — the quiet details of the clinic."),
    ("assets/images/treatment-facial.jpg", "A gentle peel applied by hand, in clinic."),
    ("assets/images/treatment-laser.jpg", "Laser equipment, maintained and calibrated in-house."),
    ("assets/images/products-flatlay.jpg", "The shelf: sunscreen, a barrier cream and a single active."),
]


def gallery(number: str = "06") -> str:
    figs = ""
    for i, (src, alt) in enumerate(GALLERY):
        span = " wide" if i in (1, 3) else ""
        figs += f'''<figure class="g-item reveal{span}">
          <a href="{src}" data-lightbox data-caption="{alt}" aria-label="View larger: {alt}">
            <img src="{src}" alt="{alt}" width="768" height="1376" loading="lazy" decoding="async">
            <span class="g-plus" aria-hidden="true">{icon("plus")}</span>
          </a>
        </figure>'''
    return f'''<section class="section" id="clinic">
  <div class="shell">
    {section_head(number, "The clinic", "Inside Solace", "Quiet rooms, honest equipment and enough time to talk. Placeholder images for this demo — swap in your own photography.")}
    <div class="gallery">{figs}</div>
  </div>
</section>'''


def faq_list(items, start=0, limit=None) -> str:
    subset = items[start: limit] if limit else items[start:]
    return "".join(
        f'''<details class="faq-item reveal">
          <summary class="faq-q"><span>{f["q"]}</span><span class="faq-icon" aria-hidden="true">{icon("plus")}</span></summary>
          <div class="faq-a"><p>{f["a"]}</p></div>
        </details>'''
        for f in subset
    )


def faq_home() -> str:
    return f'''<section class="section section--cream" id="faq">
  <div class="shell faq-grid">
    <div class="reveal">
      {eyebrow("07 — Questions")}
      <h2>Before you book.</h2>
      <p class="sec-lead">Still unsure about something? Message the clinic — a real person replies.</p>
      <div class="help-card">
        <span class="help-icon">{icon("message")}</span>
        <div>
          <b>Ask a quick question</b>
          <p>WhatsApp is usually answered within a working day.</p>
          <a class="link-arrow" href="https://wa.me/{DATA['wa']}" data-wa target="_blank" rel="noopener">Message the clinic {icon("arrow-right")}</a>
        </div>
      </div>
    </div>
    <div class="faq-list">{faq_list(DATA["faqs"], limit=4)}</div>
  </div>
</section>'''


def cta_band(title="Ready for calmer, clearer skin?", text="Book a consultation with Dr. Sameen Zahra in Lahore. We'll confirm your slot by phone or WhatsApp.", light=True) -> str:
    return f'''<section class="cta-band">
  <img class="cta-bg" src="assets/images/clinic-reception.jpg" alt="" aria-hidden="true" loading="lazy">
  <div class="shell cta-in reveal">
    {eyebrow("Book your visit", True)}
    <h2 class="display">{title}</h2>
    <p>{text}</p>
    <div class="row">
      <a class="btn btn--light" href="contact.html">Book a consultation {icon("arrow-right")}</a>
      <a class="btn btn--ghost-light" href="https://wa.me/{DATA['wa']}" data-wa target="_blank" rel="noopener">{icon("message")} WhatsApp the clinic</a>
    </div>
    <ul class="cta-meta">
      <li>{icon("pin")} DHA, Lahore</li>
      <li>{icon("clock")} Mon–Sat, 10:00–19:00</li>
      <li>{icon("phone")} {DATA['phoneDisplay']}</li>
    </ul>
  </div>
</section>'''


# --------------------------------------------------------------------------- pages
def home() -> str:
    t = DATA["treatments"]
    principles = [
        ("search", "Diagnosis before products", "A proper look at your skin, history and routine comes before anything is prescribed."),
        ("shield", "Routines people can keep", "Three steps you will do daily beat ten you will abandon by Friday."),
        ("clock", "Honest about timelines", "Real results take weeks to months. You get a realistic plan, not a promise."),
    ]
    principle_cards = "".join(
        f'''<li class="principle reveal">
          <span class="principle-icon">{icon(i)}</span>
          <h3>{h}</h3>
          <p>{p}</p>
        </li>'''
        for i, h, p in principles
    )
    return f'''<section class="hero-home">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="shell hero-grid">
    <div class="hero-copy">
      {eyebrow("Dermatologist &amp; cosmetologist — Lahore")}
      <h1 class="display">Skin care that starts with <em>science</em>, and ends with you.</h1>
      <p class="lead">Evidence-based dermatology and considered aesthetics, led by Dr. Sameen Zahra — MSc Dermatology (USA), MPH. Consultation first. Trends never.</p>
      <div class="row hero-cta">
        <a class="btn btn--primary btn--lg" href="contact.html">Book a consultation {icon("arrow-right")}</a>
        <a class="btn btn--ghost btn--lg" href="treatments.html">Explore treatments</a>
      </div>
      <ul class="hero-trust">
        <li>{icon("check")} MSc Dermatology (USA)</li>
        <li>{icon("check")} Master of Public Health</li>
        <li>{icon("check")} 10+ years in practice</li>
      </ul>
    </div>
    <div class="hero-media reveal">
      <figure class="arch arch--hero">
        <img src="assets/images/hero-portrait.jpg" alt="Dr. Sameen Zahra, dermatologist, in her clinic in Lahore" width="768" height="1376" fetchpriority="high">
      </figure>
      <div class="float-card float-card--a">
        <span class="float-icon">{icon("shield")}</span>
        <div><b>Consultation-first</b><span>Every plan starts with your skin — not a product.</span></div>
      </div>
      <div class="float-chip"><b>91K</b><span>community</span></div>
    </div>
  </div>
</section>
{marquee()}
<section class="section">
  <div class="shell">
    {section_head("01", "The practice", "Dermatology that treats the cause, not the trend", "Two clinics in Lahore — one for medical dermatology, one for aesthetics — run on the same consultation-first standard.")}
    <div class="split">
      <figure class="arch arch--split reveal">
        <img src="assets/images/about-consult.jpg" alt="Dr. Zahra talking a patient through a skincare plan" width="768" height="1376" loading="lazy" decoding="async">
        <figcaption>Consultation room, Solace Aesthetics</figcaption>
      </figure>
      <div class="split-copy">
        <p class="statement reveal">Your skin is not a trend cycle. It deserves a clinician who will look, listen and then decide — with you.</p>
        <ul class="principles">{principle_cards}</ul>
        <a class="link-arrow reveal" href="about.html">Meet Dr. Zahra {icon("arrow-right")}</a>
      </div>
    </div>
  </div>
</section>
{treatments_preview()}
{stat_band()}
<section class="section">
  <div class="shell split split--rev">
    <figure class="arch arch--doctor reveal">
      <img src="assets/images/about-seated.jpg" alt="Dr. Sameen Zahra seated in the clinic" width="768" height="1376" loading="lazy" decoding="async">
    </figure>
    <div class="split-copy">
      {eyebrow("Meet your dermatologist")}
      <h2>Dr. Sameen Zahra</h2>
      <p class="lead">MSc Dermatology (USA) · MPH · Founder, Solace Medical Centre and Solace Aesthetics.</p>
      <p>Dr. Zahra pairs clinical dermatology with a public-health view: prevention first, clear explanations, and routines that survive a real week. She shares the same advice with a 91,000-strong community on Instagram and YouTube.</p>
      <ul class="cred-list">
        <li>{icon("check")} Medical dermatology: acne, rosacea, psoriasis, pigmentation</li>
        <li>{icon("check")} Aesthetic medicine, practised conservatively</li>
        <li>{icon("check")} Care planned for South Asian skin tones</li>
      </ul>
      <div class="row">
        <a class="btn btn--primary" href="about.html">Read her story {icon("arrow-right")}</a>
        <a class="btn btn--ghost" href="contact.html">Book a visit</a>
      </div>
      <p class="signature" aria-hidden="true">Sameen Zahra</p>
    </div>
  </div>
</section>
{process()}
{products_preview()}
{testimonials()}
{gallery()}
{faq_home()}
{cta_band()}'''


def about() -> str:
    principles = [
        ("heart", "Listen first", "The first ten minutes are yours. History, triggers and what you have already tried matter more than a product list."),
        ("search", "Evidence over trends", "If the published evidence is thin, I will say so — even when a treatment is popular."),
        ("sun", "Skin tone matters", "Peels, lasers and pigmentation plans are chosen for your skin tone, because the same settings do not suit everyone."),
        ("shield", "Prevent before treat", "Sunscreen, sleep and a stable barrier do more over a decade than any single procedure."),
    ]
    cards = "".join(
        f'''<li class="principle principle--card reveal">
          <span class="principle-icon">{icon(i)}</span>
          <h3>{h}</h3>
          <p>{p}</p>
        </li>'''
        for i, h, p in principles
    )
    creds = [
        ("MSc Dermatology", "Advanced dermatology training, United States"),
        ("Master of Public Health (MPH)", "Population health and prevention"),
        ("Bachelor of Medicine, Bachelor of Surgery", "Medical degree"),
        ("Founder &amp; CEO", "Solace Medical Centre and Solace Aesthetics, Lahore"),
    ]
    cred_html = "".join(
        f'''<li class="cred reveal"><b>{t}</b><span>{d}</span></li>'''
        for t, d in creds
    )
    clinics = "".join(
        f'''<article class="clinic-card reveal">
          <span class="clinic-tag">{c["tag"]}</span>
          <h3>{c["name"]}</h3>
          <p class="clinic-line">{icon("pin")} {c["address"]}</p>
          <p class="clinic-line">{icon("clock")} {c["hours"]}</p>
          <a class="link-arrow" href="{DATA['maps']}" target="_blank" rel="noopener">Get directions {icon("arrow-up-right")}</a>
        </article>'''
        for c in DATA["clinics"]
    )
    return f'''{page_hero("about", "About", "A dermatologist who thinks in public health.", "MSc Dermatology (USA), MPH, and founder of two Lahore clinics — medical dermatology at Solace Medical Centre, aesthetics at Solace Aesthetics.", "assets/images/about-seated.jpg", "Dr. Sameen Zahra seated in her clinic", ["MSc Dermatology (USA)", "MPH", "10+ years", "Lahore"], "The doctor")}
<section class="section">
  <div class="shell split">
    <figure class="arch arch--split reveal">
      <img src="assets/images/education-desk.jpg" alt="Dr. Zahra recording an educational video at her desk" width="768" height="1376" loading="lazy" decoding="async">
      <figcaption>Filming a skincare explainer, Solace Aesthetics</figcaption>
    </figure>
    <div class="split-copy">
      {eyebrow("Her story")}
      <h2>Clinical dermatology, explained like a person.</h2>
      <p>Dr. Sameen Zahra trained in dermatology in the United States and holds a Master of Public Health. That combination shapes how she practises: treat what is in front of her, and prevent what will come next.</p>
      <p>She founded <b>Solace Medical Centre</b> for medical dermatology and <b>Solace Aesthetics</b> for cosmetic care, so patients get the right room for the right concern — and never a procedure they do not need.</p>
      <p>Outside the clinic she teaches a community of more than 91,000 people on Instagram and YouTube, mostly by debunking things they were told to buy.</p>
      <p class="signature" aria-hidden="true">Sameen Zahra</p>
    </div>
  </div>
</section>
<section class="section section--cream">
  <div class="shell">
    {section_head("01", "Philosophy", "How the clinic works", "Four principles that decide what gets prescribed — and what does not.")}
    <ul class="principle-grid">{cards}</ul>
  </div>
</section>
<section class="section">
  <div class="shell split split--rev split--top">
    <div class="split-copy">
      {eyebrow("Training &amp; credentials")}
      <h2>Qualified, and happy to show it.</h2>
      <ol class="cred-list cred-list--big">{cred_html}</ol>
      <p class="note">{icon("info")} Demo note: replace these entries with exact institutions, years and registration numbers before publishing.</p>
    </div>
    <figure class="arch arch--split reveal">
      <img src="assets/images/hero-portrait.jpg" alt="Portrait of Dr. Sameen Zahra" width="768" height="1376" loading="lazy" decoding="async">
    </figure>
  </div>
</section>
<section class="quote-band">
  <div class="shell reveal">
    {icon("quote", "quote-mark")}
    <p class="pull-quote">The best skincare routine is the one you will actually follow.</p>
    <p class="pull-by">Dr. Sameen Zahra — dermatologist &amp; cosmetologist</p>
  </div>
</section>
<section class="section">
  <div class="shell">
    {section_head("02", "Clinics", "Two clinics, one standard", "Medical care and aesthetics under one clinical philosophy, in DHA Lahore.")}
    <div class="clinic-grid">{clinics}</div>
  </div>
</section>
{gallery("03")}
{cta_band("Let's start with your skin.", "Book a consultation with Dr. Sameen Zahra. We will confirm your slot by phone or WhatsApp.")}'''


def treatments() -> str:
    cats = []
    for t in DATA["treatments"]:
        if t["tag"] not in cats:
            cats.append(t["tag"])
    chips = '<button class="chip is-active" type="button" data-filter="all" aria-pressed="true">All treatments</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{c.lower()}" aria-pressed="false">{c}</button>'
        for c in cats
    )
    cards = ""
    for i, t in enumerate(DATA["treatments"]):
        cards += f'''<article class="tx-card reveal" data-cat="{t["tag"].lower()}">
          <div class="tx-card-head">
            <span class="tx-icon">{icon(t["icon"])}</span>
            <div>
              <span class="tx-tag">{t["tag"]}</span>
              <h3>{t["title"]}</h3>
              <p>{t["summary"]}</p>
            </div>
          </div>
          <button class="tx-toggle" type="button" aria-expanded="false" aria-controls="tx-panel-{i}">
            <span>Treatment details</span><span class="tx-plus" aria-hidden="true">{icon("plus")}</span>
          </button>
          <div class="tx-panel" id="tx-panel-{i}" hidden>
            <dl class="tx-facts">
              <div><dt>Who it's for</dt><dd>{t["who"]}</dd></div>
              <div><dt>What to expect</dt><dd>{t["expect"]}</dd></div>
            </dl>
            <ul class="tx-meta">
              <li>{icon("clock")}{t["duration"]}</li>
              <li>{icon("calendar")}{t["sessions"]}</li>
            </ul>
            <a class="link-arrow" href="contact.html">Book a consultation {icon("arrow-right")}</a>
          </div>
        </article>'''
    return f'''{page_hero("treatments", "Treatments", "Medical and aesthetic care, one plan.", "Ten focused treatments — chosen after a proper assessment, never from a menu. Expand any treatment to see who it suits and what to expect.", "assets/images/treatment-facial.jpg", "A gentle peel being applied in clinic", ["10 treatments", "Consultation first", "All skin tones"], "What we treat", ("#treatments-list", "Browse treatments"))}
<section class="section" id="treatments-list">
  <div class="shell">
    <div class="filter-bar reveal">
      <div class="chips" role="group" aria-label="Filter treatments">{chips}</div>
      <p class="filter-count" aria-live="polite"><span data-count-shown>{len(DATA["treatments"])}</span> treatments</p>
    </div>
    <div class="tx-list" data-filter-list>{cards}</div>
    <p class="filter-empty" data-filter-empty hidden>No treatments in this category yet.</p>
    <p class="note reveal">{icon("info")} Prices, session counts and downtime are confirmed at consultation. Nothing here is a substitute for an in-person assessment.</p>
  </div>
</section>
{process("")}
<section class="section section--cream">
  <div class="shell faq-grid">
    <div class="reveal">
      {eyebrow("Questions")}
      <h2>Good to know.</h2>
      <p class="sec-lead">The things patients ask before their first appointment.</p>
      <div class="help-card">
        <span class="help-icon">{icon("message")}</span>
        <div>
          <b>Not sure what you need?</b>
          <p>Send a message with your concern and we will point you to the right appointment.</p>
          <a class="link-arrow" href="https://wa.me/{DATA['wa']}" data-wa target="_blank" rel="noopener">Ask the clinic {icon("arrow-right")}</a>
        </div>
      </div>
    </div>
    <div class="faq-list">{faq_list(DATA["faqs"])}</div>
  </div>
</section>
{cta_band()}'''


def products() -> str:
    groups = [("AM", "Morning", "Protect and balance.", "sun"), ("PM", "Evening", "Repair while you sleep.", "layers"), ("Weekly", "Weekly", "One controlled reset.", "spark")]
    columns = ""
    for key, title, sub, ic in groups:
        picks = [p for p in DATA["products"] if p["time"] == key][:3]
        steps = "".join(
            f'<li><span class="step-dot" aria-hidden="true"></span><div><b>{p["name"]}</b><span>{p["actives"]}</span></div></li>'
            for p in picks
        )
        columns += f'''<div class="routine-col reveal">
          <span class="routine-icon">{icon(ic)}</span>
          <h3>{title}</h3>
          <p>{sub}</p>
          <ul class="routine-steps">{steps}</ul>
        </div>'''
    chips = (
        '<button class="chip is-active" type="button" data-filter="all" aria-pressed="true">All</button>'
        '<button class="chip" type="button" data-filter="am" aria-pressed="false">AM</button>'
        '<button class="chip" type="button" data-filter="pm" aria-pressed="false">PM</button>'
        '<button class="chip" type="button" data-filter="weekly" aria-pressed="false">Weekly</button>'
    )
    cards = "".join(product_card(p, i) for i, p in enumerate(DATA["products"]))
    tips = [
        ("One new thing at a time", "Introduce a single active, use it for two weeks, then decide. Stacking three at once makes reactions impossible to trace."),
        ("Sunscreen is the treatment", "For pigmentation and post-acne marks, SPF matters more than the serum. Reapply, and use enough."),
        ("Stop if it stings", "A brief tingle can be normal. Burning, swelling or blistering is not — stop and message the clinic."),
    ]
    tip_html = "".join(
        f'<li class="tip reveal"><h3>{h}</h3><p>{p}</p></li>' for h, p in tips
    )
    return f'''{page_hero("products", "Products", "The routine, simplified.", "Dermatologist-guided skincare in three steps. No ten-step scroll, no miracle claims — just the products that do the work.", "assets/images/products-flatlay.jpg", "Minimal skincare products laid out on linen", ["AM · PM · Weekly", "Fragrance-aware", "Guidance included"], "Dermatologist-guided", ("#routine", "See the routine"))}
<section class="section" id="routine">
  <div class="shell">
    {section_head("01", "Build a routine", "Structure before products", "Start with three steps. Add more only when the basics are consistent.")}
    <div class="routine-grid">{columns}</div>
  </div>
</section>
<section class="section section--cream">
  <div class="shell">
    {section_head("02", "The shelf", "What we actually recommend", "Representative products from the clinic's recommendation list. This demo has no online checkout.", ("contact.html", "Get a personalised routine"))}
    <div class="filter-bar reveal">
      <div class="chips" role="group" aria-label="Filter products">{chips}</div>
      <p class="filter-count" aria-live="polite"><span data-count-shown>{len(DATA["products"])}</span> products</p>
    </div>
    <div class="prod-grid" data-filter-list>{cards}</div>
    {"" if False else '<p class="filter-empty" data-filter-empty hidden>Nothing in this category.</p>'}
  </div>
</section>
<section class="section">
  <div class="shell">
    {section_head("03", "Getting started", "Three rules that save skin", "")}
    <ul class="tips">{tip_html}</ul>
    <div class="note-card reveal">
      {icon("info")}
      <div><b>Please note</b><p>Product names, actives and routines are illustrative content for this demo site. Replace them with the clinic's own recommendations before publishing.</p></div>
    </div>
  </div>
</section>
{cta_band("Not sure where to start?", "Book a consultation and leave with a short, affordable routine matched to your skin — not a shelf.")}'''


def education() -> str:
    topics = []
    for e in DATA["edu"]:
        if e["topic"] not in topics:
            topics.append(e["topic"])
    chips = '<button class="chip is-active" type="button" data-filter="all" aria-pressed="true">All topics</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{t.lower()}" aria-pressed="false">{t}</button>'
        for t in topics
    )
    cards = "".join(
        f'''<a class="edu-card reveal" href="{DATA['youtube']}" target="_blank" rel="noopener" data-topic="{e["topic"].lower()}" data-search="{e["title"].lower()} {e["desc"].lower()} {e["topic"].lower()}">
          <span class="pill">{e["topic"]}</span>
          <h3>{e["title"]}</h3>
          <p>{e["desc"]}</p>
          <span class="edu-foot"><span>{e["length"]}</span><span class="edu-go">Watch {icon("arrow-up-right")}</span></span>
        </a>'''
        for e in DATA["edu"]
    )
    myths = [
        ("If it tingles, it's working.", "Tingling can be harmless, but burning is a signal to stop. Stronger is not better — irritation causes pigmentation and barrier damage that takes months to undo."),
        ("Oily skin doesn't need moisturiser.", "Oil is not hydration. Skipping moisturiser often pushes skin to produce more oil, and makes actives harder to tolerate."),
        ("You only need sunscreen in summer.", "UV levels in Lahore stay high year-round, and pigmentation responds to visible light too. Daily SPF is the single best anti-ageing step."),
    ]
    myth_html = "".join(
        f'''<li class="myth reveal">
          <p class="myth-label">Myth</p>
          <p class="myth-q">“{q}”</p>
          <p class="myth-a">{a}</p>
        </li>'''
        for q, a in myths
    )
    return f'''{page_hero("education", "Education", "Learn what actually works.", "Short explainers on rosacea, SPF, psoriasis and the mistakes almost everyone makes — written the way they are explained in clinic.", "assets/images/education-desk.jpg", "Dr. Zahra recording an educational video", ["8 guides", "No jargon", "Clinic-reviewed"], "Learn with us", ("#guides", "Browse guides"))}
<section class="section" id="guides">
  <div class="shell">
    <div class="edu-toolbar reveal">
      <label class="search-field">
        {icon("search")}
        <input type="search" placeholder="Search topics, e.g. sunscreen" aria-label="Search education topics" data-search-input>
      </label>
      <div class="chips" role="group" aria-label="Filter topics">{chips}</div>
    </div>
    <div class="edu-grid" data-filter-list>{cards}</div>
    <p class="filter-empty" data-filter-empty hidden>No guides match that search yet.</p>
  </div>
</section>
<section class="section section--cream">
  <div class="shell">
    {section_head("01", "Myths", "Things worth unlearning", "The three claims that come up in almost every consultation.")}
    <ul class="myths">{myth_html}</ul>
  </div>
</section>
<section class="section">
  <div class="shell ask-grid">
    <div class="reveal">
      {eyebrow("Ask the clinic")}
      <h2>A question that isn't in a video?</h2>
      <p class="sec-lead">Send it over. General questions are answered on WhatsApp; anything personal needs a consultation.</p>
      <div class="row">
        <a class="btn btn--primary" href="https://wa.me/{DATA['wa']}" data-wa target="_blank" rel="noopener">{icon("message")} Ask on WhatsApp</a>
        <a class="btn btn--ghost" href="contact.html">Book a consultation</a>
      </div>
      <p class="note">{icon("info")} Education content is general information, not a diagnosis. If a lesion is changing, book a skin check.</p>
    </div>
    <figure class="arch arch--split reveal">
      <img src="assets/images/clinic-detail.jpg" alt="Clinic still life with linen and a glass dropper bottle" width="768" height="1376" loading="lazy" decoding="async">
    </figure>
  </div>
</section>
{cta_band()}'''


def field(name, label, kind="text", required=False, placeholder="", autocomplete="", options=None, extra="") -> str:
    req = " required" if required else ""
    req_attr = ' <span class="req" aria-hidden="true">*</span>' if required else ""
    aria_req = ' aria-required="true"' if required else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    if kind == "select":
        opts = "".join(f'<option value="{o}">{o}</option>' for o in (options or []))
        control = f'<select id="f-{name}" name="{name}"{req}{aria_req}{ac}>{opts}</select>'
    elif kind == "textarea":
        control = f'<textarea id="f-{name}" name="{name}" rows="4" placeholder="{placeholder}"{req}{aria_req}></textarea>'
    else:
        control = f'<input id="f-{name}" name="{name}" type="{kind}" placeholder="{placeholder}"{req}{aria_req}{ac}{extra}>'
    return f'''<div class="field">
      <label for="f-{name}">{label}{req_attr}</label>
      {control}
      <span class="field-err" data-err="{name}" aria-live="polite"></span>
    </div>'''


def contact() -> str:
    concerns = [
        "Acne or scarring", "Rosacea or redness", "Pigmentation or melasma", "Psoriasis or eczema",
        "Chemical peel", "Laser or light", "Anti-ageing", "Hair or scalp", "Skin check", "Something else",
    ]
    clinic_opts = [c["name"] for c in DATA["clinics"]] + ["Either clinic"]
    times = ["Morning (10:00 – 13:00)", "Afternoon (13:00 – 16:00)", "Evening (16:00 – 19:00)", "Any time"]
    clinics = "".join(
        f'''<article class="clinic-card clinic-card--compact reveal">
          <span class="clinic-tag">{c["tag"]}</span>
          <h3>{c["name"]}</h3>
          <p class="clinic-line">{icon("pin")} {c["address"]}</p>
          <p class="clinic-line">{icon("clock")} {c["hours"]}</p>
          <a class="link-arrow" href="{DATA['maps']}" target="_blank" rel="noopener">Open in maps {icon("arrow-up-right")}</a>
        </article>'''
        for c in DATA["clinics"]
    )
    steps = [
        ("01", "You send a request", "Name, number and a line about your concern. Takes under a minute."),
        ("02", "We call you back", "Within one working day, to agree a time and answer initial questions."),
        ("03", "You come in", "Allow 30–45 minutes for a first consultation. Bring your current products."),
    ]
    step_html = "".join(
        f'<li class="step reveal"><span class="step-num">{n}</span><h3>{t}</h3><p>{p}</p></li>' for n, t, p in steps
    )
    return f'''<section class="page-hero page-hero--contact">
  <div class="shell">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Contact</span></nav>
    <div class="contact-head">
      <div>
        {eyebrow("Book an appointment")}
        <h1 class="display">Book a consultation.</h1>
        <p class="lead">Tell us what is bothering your skin. We will confirm your slot by phone or WhatsApp within one working day.</p>
        <ul class="contact-quick">
          <li><a href="tel:{DATA['phoneHref']}">{icon("phone")}<span><small>Call the clinic</small><b>{DATA['phoneDisplay']}</b></span></a></li>
          <li><a href="https://wa.me/{DATA['wa']}" data-wa target="_blank" rel="noopener">{icon("message")}<span><small>WhatsApp</small><b>Message us</b></span></a></li>
          <li><a href="mailto:{DATA['email']}">{icon("mail")}<span><small>Email</small><b>{DATA['email']}</b></span></a></li>
        </ul>
      </div>
      <aside class="aside-card reveal">
        <span class="aside-icon">{icon("clock")}</span>
        <h2>Clinic hours</h2>
        <dl class="hours">
          <div><dt>Monday – Friday</dt><dd>10:00 – 19:00</dd></div>
          <div><dt>Saturday</dt><dd>10:00 – 16:00</dd></div>
          <div><dt>Sunday</dt><dd>Closed</dd></div>
        </dl>
        <p class="aside-note">Hours are indicative for this demo. Update them to match your clinics.</p>
      </aside>
    </div>
  </div>
</section>
<section class="section">
  <div class="shell book-grid">
    <form class="booking-form" id="bookingForm" novalidate>
      <div class="form-head">
        <h2>Appointment request</h2>
        <p>Fields marked <span class="req">*</span> are required. This demo form does not email anyone — it prepares a WhatsApp message for you.</p>
      </div>
      <div class="form-grid">
        {field("name", "Full name", "text", True, "e.g. Ayesha Khan", "name")}
        {field("phone", "Phone number", "tel", True, "03XX XXXXXXX", "tel")}
        {field("email", "Email (optional)", "email", False, "you@example.com", "email")}
        {field("concern", "Main concern", "select", False, "", "", concerns)}
        {field("clinic", "Preferred clinic", "select", False, "", "", clinic_opts)}
        {field("date", "Preferred date", "date", False, "", "", [], ' min="' + date.today().isoformat() + '"')}
        {field("time", "Preferred time", "select", False, "", "", times)}
        {field("visit", "Have you visited before?", "select", False, "", "", ["First visit", "Returning patient"])}
        {field("message", "Anything we should know?", "textarea", False, "Previous treatments, medication, or a question")}
      </div>
      <label class="check">
        <input type="checkbox" name="consent" required>
        <span>I agree to be contacted about this request. I understand this form is not for emergencies. <span class="req" aria-hidden="true">*</span></span>
      </label>
      <span class="field-err" data-err="consent" aria-live="polite"></span>
      <p class="field-err" data-err="form" aria-live="polite"></p>
      <div class="row form-actions">
        <button class="btn btn--primary" type="submit">Request appointment {icon("arrow-right")}</button>
        <button class="btn btn--ghost" type="button" id="waSend">{icon("message")} Send on WhatsApp</button>
      </div>
      <div class="form-success" data-success hidden role="status" aria-live="polite">
        <span class="success-icon">{icon("check")}</span>
        <div>
          <h3>Request ready</h3>
          <p data-success-text>Your details are ready. Send them on WhatsApp to finish booking — the clinic replies within one working day.</p>
          <div class="row">
            <a class="btn btn--primary" href="#" data-wa data-success-wa target="_blank" rel="noopener">{icon("message")} Send on WhatsApp</a>
            <button class="btn btn--ghost" type="button" data-reset>Edit details</button>
          </div>
        </div>
      </div>
      <p class="form-emergency">{icon("info")}<span>For severe swelling, blistering or a reaction, call us directly on <a href="tel:{DATA['phoneHref']}">{DATA['phoneDisplay']}</a>.</span></p>
    </form>
    <aside class="book-aside">
      <div class="map-card reveal">
        <div class="map-art" aria-hidden="true">
          <svg viewBox="0 0 400 260" role="presentation">
            <rect width="400" height="260" fill="#E9E2D4"/>
            <path d="M0 190 C90 160 140 205 230 175 C310 148 350 170 400 140" fill="none" stroke="#CFC3AC" stroke-width="14"/>
            <path d="M60 0 C80 70 40 120 70 260" fill="none" stroke="#D8CDB8" stroke-width="10"/>
            <path d="M250 0 C240 60 300 110 280 260" fill="none" stroke="#D8CDB8" stroke-width="8"/>
            <rect x="95" y="55" width="120" height="80" rx="6" fill="#DED4C2"/>
            <rect x="255" y="120" width="105" height="95" rx="6" fill="#DED4C2"/>
            <circle cx="200" cy="130" r="13" fill="#2F6F63"/>
            <circle cx="200" cy="130" r="26" fill="#2F6F63" opacity=".18"/>
          </svg>
        </div>
        <div class="map-meta">
          <b>{DATA['clinics'][0]['name']}</b>
          <span>{DATA['clinics'][0]['address']}</span>
          <a class="link-arrow" href="{DATA['maps']}" target="_blank" rel="noopener">Open in Google Maps {icon("arrow-up-right")}</a>
        </div>
      </div>
      {clinics}
      <div class="aside-note-card reveal">
        {icon("info")}
        <p>This is a demonstration website. Address, phone number and hours are placeholders.</p>
      </div>
    </aside>
  </div>
</section>
<section class="section section--cream">
  <div class="shell">
    {section_head("01", "What happens next", "From message to appointment", "No phone tag, no deposit, no surprises.")}
    <ol class="steps">{step_html}</ol>
  </div>
</section>
<section class="section">
  <div class="shell faq-grid">
    <div class="reveal">
      {eyebrow("Before you visit")}
      <h2>Practical answers.</h2>
      <p class="sec-lead">Everything else is covered on the treatments page.</p>
      <a class="link-arrow" href="treatments.html">Browse treatments {icon("arrow-right")}</a>
    </div>
    <div class="faq-list">{faq_list(DATA["faqs"], limit=4)}</div>
  </div>
</section>
{cta_band("Prefer to talk it through?", "Call or message the clinic and we will help you choose the right appointment.")}'''


def not_found() -> str:
    return f'''<section class="page-hero page-hero--404">
  <div class="shell notfound">
    {eyebrow("Error 404")}
    <p class="notfound-code">404</p>
    <h1 class="display">This page has shed.</h1>
    <p class="lead">The link may be old, or the page may have moved. Here is the way back.</p>
    <div class="row">
      <a class="btn btn--primary" href="index.html">Back to home {icon("arrow-right")}</a>
      <a class="btn btn--ghost" href="contact.html">Book a consultation</a>
    </div>
    <ul class="notfound-links">
      <li><a href="treatments.html">Treatments</a></li>
      <li><a href="products.html">Products</a></li>
      <li><a href="education.html">Education</a></li>
      <li><a href="about.html">About</a></li>
    </ul>
  </div>
</section>'''


# --------------------------------------------------------------------------- shell
PAGES = {
    "index": dict(
        title="Dermatologist & Cosmetologist in Lahore | Dr. Sameen Zahra",
        desc="Evidence-based dermatology and aesthetics in Lahore with Dr. Sameen Zahra (MSc Dermatology, MPH). Acne, rosacea, pigmentation, peels and laser. Consultation first.",
        body=home,
        image="assets/images/hero-portrait.jpg",
        schema=True,
    ),
    "about": dict(
        title="About Dr. Sameen Zahra | Dermatologist in Lahore",
        desc="Dr. Sameen Zahra holds an MSc in Dermatology (USA) and an MPH, and founded Solace Medical Centre and Solace Aesthetics in Lahore.",
        body=about,
        image="assets/images/about-seated.jpg",
        breadcrumb="About",
    ),
    "treatments": dict(
        title="Treatments | Medical & Aesthetic Dermatology in Lahore",
        desc="Acne, rosacea, pigmentation, psoriasis, chemical peels, laser, skin boosters and skin checks in Lahore. Every plan starts with a consultation.",
        body=treatments,
        image="assets/images/treatment-facial.jpg",
        breadcrumb="Treatments",
        faq=True,
    ),
    "products": dict(
        title="Skincare Products | Dermatologist-Guided Routine",
        desc="A simplified, dermatologist-guided routine: mineral SPF, niacinamide, barrier moisturiser, retinal and azelaic acid, chosen for your skin.",
        body=products,
        image="assets/images/products-flatlay.jpg",
        breadcrumb="Products",
    ),
    "education": dict(
        title="Skincare Education | Dr. Sameen Zahra",
        desc="Short, evidence-based guides on rosacea, sunscreen, acne, psoriasis and the skincare mistakes worth unlearning.",
        body=education,
        image="assets/images/education-desk.jpg",
        breadcrumb="Education",
    ),
    "contact": dict(
        title="Book an Appointment | Dr. Sameen Zahra, Lahore",
        desc="Book a dermatology or aesthetics consultation with Dr. Sameen Zahra at Solace Aesthetics or Solace Medical Centre, DHA Lahore.",
        body=contact,
        image="assets/images/clinic-reception.jpg",
        breadcrumb="Contact",
        faq=True,
    ),
    "404": dict(
        title="Page not found | Dr. Sameen Zahra",
        desc="This page could not be found. Return to the homepage or book a consultation.",
        body=not_found,
        image="assets/images/clinic-detail.jpg",
        robots="noindex",
    ),
}


def schema_json() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Physician",
        "name": "Dr. Sameen Zahra",
        "description": "Dermatologist and cosmetologist in Lahore, Pakistan. Founder of Solace Medical Centre and Solace Aesthetics.",
        "medicalSpecialty": "Dermatology",
        "url": BASE + "/",
        "image": f"{BASE}/assets/images/hero-portrait.jpg",
        "telephone": DATA["phoneHref"],
        "email": DATA["email"],
        "address": [
            {
                "@type": "PostalAddress",
                "streetAddress": c["address"],
                "addressLocality": "Lahore",
                "addressCountry": "PK",
            }
            for c in DATA["clinics"]
        ],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "10:00",
                "closes": "19:00",
            }
        ],
        "sameAs": [DATA["instagram"], DATA["youtube"]],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def faq_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
            }
            for f in DATA["faqs"]
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def breadcrumb_schema(slug: str, label: str) -> str:
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"}]
    if slug != "index":
        items.append(
            {"@type": "ListItem", "position": 2, "name": label, "item": f"{BASE}/{slug}.html"}
        )
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def render(slug: str, spec: dict) -> str:
    canonical = f"{BASE}/" + ("" if slug == "index" else f"{slug}.html")
    robots = '<meta name="robots" content="noindex,follow">' if spec.get("robots") else ""
    schema_blocks = []
    if spec.get("schema"):
        schema_blocks.append(schema_json())
    if spec.get("faq"):
        schema_blocks.append(faq_schema())
    if spec.get("breadcrumb"):
        schema_blocks.append(breadcrumb_schema(slug, spec["breadcrumb"]))
    schema = "\n".join(schema_blocks)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{spec["title"]}</title>
<meta name="description" content="{spec["desc"]}">
<meta name="theme-color" content="#FBF8F3">
<meta name="color-scheme" content="light">
<link rel="canonical" href="{canonical}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dr. Sameen Zahra">
<meta property="og:locale" content="en_PK">
<meta property="og:title" content="{spec["title"]}">
<meta property="og:description" content="{spec["desc"]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/images/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Dr. Sameen Zahra — dermatology and aesthetics in Lahore">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{spec["title"]}">
<meta name="twitter:description" content="{spec["desc"]}">
<meta name="twitter:image" content="{BASE}/assets/images/og-image.jpg">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{spec.get("image", "assets/images/hero-portrait.jpg")}">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..600;1,9..40,400&family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{schema}
</head>
<body data-page="{slug}">
{sprite()}
{header(slug)}
<main id="main">
{spec["body"]()}
</main>
{footer()}
{lightbox()}
<script src="js/data.js" defer></script>
<script src="js/main.js" defer></script>
</body>
</html>
'''


FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Dr. Sameen Zahra">
  <rect width="64" height="64" rx="16" fill="#2F6F63"/>
  <path d="M32 13c0 0 12 13.4 12 21.2A12 12 0 0 1 20 34.2C20 26.4 32 13 32 13Z" fill="#FBF8F3"/>
  <path d="M26 36c1 3 3.6 5 7 5" stroke="#2F6F63" stroke-width="2.6" stroke-linecap="round" fill="none"/>
  <circle cx="45" cy="19" r="3" fill="#E3C9B8"/>
</svg>
'''

SITEMAP = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
''' + "".join(
    f'  <url><loc>{BASE}/{"" if s == "index" else s + ".html"}</loc><changefreq>monthly</changefreq><priority>{"1.0" if s == "index" else "0.8"}</priority></url>\n'
    for s in ["index", "about", "treatments", "products", "education", "contact"]
) + "</urlset>\n"

ROBOTS = f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"


def main() -> None:
    global DATA
    DATA = load_data()
    (ROOT / "css").mkdir(exist_ok=True)
    (ROOT / "assets" / "images").mkdir(parents=True, exist_ok=True)
    for slug, spec in PAGES.items():
        name = "index.html" if slug == "index" else f"{slug}.html"
        (ROOT / name).write_text(render(slug, spec), encoding="utf-8")
        print(f"  ✓ {name}")
    (ROOT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    (ROOT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    print(f"  ✓ favicon.svg, sitemap.xml, robots.txt\nBuilt {len(PAGES)} pages.")


if __name__ == "__main__":
    main()
