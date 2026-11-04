#!/usr/bin/env python3
"""Builds the Impex Studios static site into ./public (deploy that folder to Cloudflare Pages).
Edit copy here, run `python3 build.py`, commit, push."""
import json, os, shutil, html
from datetime import date

SITE = "https://impexstudios.com"
NAME = "Impex Studios"
PHONE = "+1 (289) 608-9883"
PHONE_TEL = "+12896089883"
EMAIL = "contact@impexstudios.com"
TODAY = date(2026, 10, 26).isoformat()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
import hashlib
def ver(rel):
    return hashlib.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), rel),"rb").read()).hexdigest()[:8]

# ---------- icons ----------
I = {
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/></svg>',
}
LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#8B93FF"/>'
        '<path d="M11 11h4v18h-4z" fill="#0D1233"/><path d="M20 12l9 16M29 12l-9 16" stroke="#0D1233" stroke-width="3.8" stroke-linecap="round"/>'
        '<circle cx="33" cy="33" r="2.4" fill="#3DF5B0"/></svg>')

def esc(s): return html.escape(s, quote=True)

# ---------- shared schema ----------
ORG = {
 "@type": ["ProfessionalService", "Organization"],
 "@id": SITE + "/#org",
 "name": NAME,
 "url": SITE + "/",
 "logo": SITE + "/assets/img/logo.png",
 "image": SITE + "/assets/img/og.png",
 "description": "Digital marketing and AI automation agency in Toronto serving businesses across Canada and the United States: web design, SEO, AI search optimization, AI phone agents, chatbots, workflow automation and social media marketing.",
 "telephone": PHONE_TEL,
 "email": EMAIL,
 "priceRange": "$$",
 "address": {"@type": "PostalAddress", "addressLocality": "Toronto", "addressRegion": "ON", "addressCountry": "CA"},
 "areaServed": [{"@type": "Country", "name": "Canada"}, {"@type": "Country", "name": "United States"}],
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00"}],
 "knowsAbout": ["Web design", "Search engine optimization", "Local SEO", "Generative engine optimization", "AI phone agents", "AI chatbots", "Marketing automation", "Social media marketing"],
 # "sameAs": ["https://www.linkedin.com/company/...", "https://www.instagram.com/..."],  # add your real profiles
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en"}

NAV = [("/services/", "Services"), ("/pricing/", "Pricing"), ("/about/", "About"), ("/contact/", "Contact")]

def header(path):
    cur = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{cur if path.startswith(h) else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap nav">
  <a class="brand" href="/" aria-label="{NAME} home">{LOGO}<span>Impex Studios</span></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu"><span></span><span></span><span></span></button>
  <ul class="nav-links" id="nav-links">{items}<li class="nav-cta"><a class="btn btn-primary" href="/free-growth-plan/">Get a free growth plan</a></li></ul>
</div></header>'''

FOOTER = f'''<footer class="site-footer"><div class="wrap">
  <div class="foot-grid">
    <div><a class="brand" href="/">{LOGO}<span>Impex Studios</span></a>
      <p style="margin-top:16px">Websites, search visibility and AI automation for businesses across Canada and the US. Based in Toronto.</p></div>
    <div><h4>Services</h4><ul>
      <li><a href="/services/web-design/">Web design &amp; development</a></li>
      <li><a href="/services/seo/">SEO &amp; AI search</a></li>
      <li><a href="/services/ai-automation/">AI phone agents &amp; automation</a></li>
      <li><a href="/services/social-media/">Social media marketing</a></li></ul></div>
    <div><h4>Company</h4><ul>
      <li><a href="/pricing/">Pricing</a></li><li><a href="/about/">About</a></li>
      <li><a href="/free-growth-plan/">Free growth plan</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/canada/">Canada</a></li><li><a href="/usa/">United States</a></li></ul></div>
    <div><h4>Talk to us</h4><ul>
      <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span class="muted small">Mon–Fri, 9 am–6 pm ET</span></li></ul></div>
  </div>
  <div class="foot-base"><span>© <span data-year>2026</span> Impex Studios. Toronto, Ontario.</span>
    <span><a href="/privacy/">Privacy</a> &nbsp; <a href="/sitemap.xml">Sitemap</a></span></div>
</div></footer>'''

def crumbs_html(trail):
    li = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' if u else f'<li aria-current="page">{esc(t)}</li>' for t, u in trail)
    return f'<ol class="crumbs">{li}</ol>'

def crumbs_schema(trail, path):
    items = []
    for i, (t, u) in enumerate(trail, 1):
        items.append({"@type": "ListItem", "position": i, "name": t, "item": SITE + (u or path)})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in faqs) + '</div>'

def faq_schema(faqs):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}

def cta_band(h="Tell us where you want to be in 12 months.",
             p="You’ll get a written growth plan with recommendations and fixed pricing within one business day. No sales script, no obligation."):
    return f'''<section class="section"><div class="wrap"><div class="cta-band">
  <h2>{h}</h2><p>{p}</p>
  <div class="btn-row"><a class="btn btn-primary" href="/free-growth-plan/">Get my free growth plan</a>
  <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call or text {PHONE}</a></div>
</div></div></section>'''

def page(path, title, desc, body, extra_schema=(), trail=None, noindex=False, og_type="website"):
    url = SITE + path
    graph = [ORG, WEBSITE, {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
             "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}, "inLanguage": "en", "dateModified": TODAY}]
    if trail: graph.append(crumbs_schema(trail, path))
    graph += list(extra_schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0D1233">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_CA"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ver('assets/css/site.css')}">
<script type="application/ld+json">{ld}</script>
<!-- Analytics: paste your GA4 or Cloudflare Web Analytics snippet here -->
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="/assets/js/site.js?v={ver('assets/js/site.js')}" defer></script>
</body>
</html>'''
    if path.endswith(".html"):
        fn = os.path.join(OUT, path.strip("/"))
    else:
        d = os.path.join(OUT, path.strip("/")); os.makedirs(d, exist_ok=True)
        fn = os.path.join(d, "index.html")
    with open(fn, "w", encoding="utf-8") as f: f.write(doc)
    if not noindex: SITEMAP.append((path, "1.0" if path == "/" else "0.8"))

SITEMAP = []

def page_hero(trail, h1, lede, ctas=True):
    btns = f'''<div class="btn-row"><a class="btn btn-primary" href="/free-growth-plan/">Get my free growth plan</a>
<a class="btn btn-ghost" href="/pricing/">See pricing</a></div>''' if ctas else ""
    return f'''<section class="page-hero"><div class="wrap">{crumbs_html(trail)}
<h1>{h1}</h1><p class="lede">{lede}</p>{btns}</div></section>'''

def checks(items):
    return '<ul class="checks">' + "".join(
        f'<li>{I["check"]}<div><strong>{t}</strong><span>{d}</span></div></li>' for t, d in items) + '</ul>'

# ---------- shared blocks ----------
CALL_DEMO = f'''<div class="call" data-call aria-label="Example of an after-hours call answered by an AI receptionist">
  <div class="call-top">
    <div class="call-who"><div class="call-avatar">A</div><div><strong>AI receptionist</strong><small>Northside Heating &amp; Air · 9:47 pm</small></div></div>
    <span class="live-pill"><i></i>On a call</span>
  </div>
  <div class="wave" aria-hidden="true">{"".join(f'<b style="animation-delay:{(i*83)%900}ms"></b>' for i in range(34))}</div>
  <ol class="transcript">
    <li class="caller"><span class="who">Caller</span>Hi, our furnace stopped working. Can someone come out tomorrow?</li>
    <li class="agent"><span class="who">AI receptionist</span>Sorry to hear that. I can book a technician for 8:30 am or 1:00 pm tomorrow. Which works better?</li>
    <li class="caller"><span class="who">Caller</span>8:30, please.</li>
    <li class="agent"><span class="who">AI receptionist</span>You’re booked for 8:30 am. I’m texting you a confirmation now.</li>
  </ol>
  <div class="call-result">
    <span class="chip">{I["check"]}Appointment booked</span>
    <span class="chip">{I["check"]}Added to calendar</span>
    <span class="chip">{I["check"]}Lead saved to CRM</span>
    <span class="chip">{I["check"]}Text confirmation sent</span>
  </div>
  <p class="call-caption">Example call. We build agents like this on your phone number, calendar and CRM.</p>
</div>'''

PROMISES = '''<div class="promises">
  <div><strong>Fixed price</strong><span>The quote is the invoice. No hourly creep.</span></div>
  <div><strong>50/50 payment</strong><span>Half to start, half only when you approve the finished site.</span></div>
  <div><strong>You own it</strong><span>100% of the code, content and accounts are yours.</span></div>
  <div><strong>Launch date in writing</strong><span>Landing pages in 1–2 days, full sites in about a week.</span></div>
  <div><strong>30 days of support</strong><span>Fixes and small edits after launch are included.</span></div>
</div>
<div class="stack"><em>We build with</em><span>WordPress</span><span>Supabase</span><span>n8n</span><span>Make</span><span>Vapi</span><span>GoHighLevel</span><span>Airtable</span><span>Cloudflare</span></div>'''

SERVICES = [
 ("/services/web-design/", "Web design &amp; development",
  "Fast, custom websites designed to turn visitors into booked calls and quote requests, from a one-page launch to a full online store.",
  ["Custom design", "Landing pages", "E-commerce", "Booking & quote forms", "Core Web Vitals"]),
 ("/services/seo/", "SEO, local SEO &amp; AI search",
  "Rank on Google, show up in the map pack, and get recommended by ChatGPT, Perplexity, Gemini and Google’s AI Overviews.",
  ["Technical SEO", "Google Business Profile", "Schema markup", "Content", "AI search (GEO)"]),
 ("/services/ai-automation/", "AI phone agents &amp; automation",
  "AI receptionists that answer every call, chatbots that qualify leads, and workflows that move data so your team doesn’t have to.",
  ["AI phone agents", "Website chatbots", "CRM automation", "n8n & Make workflows", "Follow-up sequences"]),
 ("/services/social-media/", "Social media marketing",
  "Consistent, on-brand content and campaigns that build trust with your audience and send traffic back to your site.",
  ["Content calendars", "Post design", "Short-form video", "Community management", "Paid social"]),
]

def svc_rows():
    out = '<ul class="svc-list">'
    for href, t, d, tags in SERVICES:
        out += (f'<li><a class="svc-row" href="{href}"><h3>{t}</h3><div><p>{d}</p><ul>' +
                "".join(f"<li>{x}</li>" for x in tags) + f'</ul></div><span class="svc-go">{I["arrow"]}</span></a></li>')
    return out + '</ul>'

STEPS = '''<ol class="steps">
  <li><h3>Free growth plan</h3><p>Tell us about your business. Within one business day you get a written plan: what to fix, what to build, and a fixed price.</p></li>
  <li><h3>Build sprint</h3><p>We design and build on a set schedule with a staging link you can review at any time. Senior people do the work.</p></li>
  <li><h3>Launch &amp; track</h3><p>We launch, connect analytics and call tracking, and confirm every form, booking and automation works end to end.</p></li>
  <li><h3>Grow</h3><p>Optional monthly SEO, content, social and automation work, reported against leads and revenue, not vanity metrics.</p></li>
</ol>'''

CALC = '''<div class="calc" data-calc>
  <div class="calc-in">
    <div class="field-range"><label for="calls">Calls you miss per week <output>10</output></label>
      <input id="calls" type="range" min="1" max="60" value="10"></div>
    <div class="field-range"><label for="rate">Share that would have booked <output>30%</output></label>
      <input id="rate" type="range" min="5" max="80" step="5" value="30"></div>
    <div class="field-range"><label for="value">Average job or sale value <output>$350</output></label>
      <input id="value" type="range" min="50" max="5000" step="50" value="350"></div>
  </div>
  <div class="calc-out" aria-live="polite">
    <span class="muted">Revenue you could be missing each month</span>
    <div class="calc-big" data-monthly>$4,547</div>
    <p>That’s about <strong data-yearly>$54,560</strong> a year walking to whoever picked up the phone. An AI receptionist answers every call, day or night, and books it into your calendar.</p>
    <div><a class="btn btn-primary" href="/free-growth-plan/?package=AI%20phone%20agent">Get an AI receptionist quote</a></div>
  </div>
</div>'''

PACKAGES = [
 ("Landing page", 499, "Delivered in 1–2 days", False,
  ["One custom high-converting page", "Built for ads and local lead capture", "Mobile-first, sub-second loads", "Contact or quote form", "On-page SEO setup"]),
 ("Multi-page website", 999, "Delivered in 5–7 days", True,
  ["Up to 5 custom pages", "Local SEO and schema markup", "Custom quote and intake forms", "Google Maps and multi-location support", "30 days post-launch support"]),
 ("Business website pro", 1499, "Delivered in 7–10 days", False,
  ["Up to 10 custom pages", "Blog and case-study engine", "Google Analytics 4 event tracking", "Advanced technical SEO", "CRM integration and lead routing"]),
 ("E-commerce website", 1999, "Timeline set in your plan", False,
  ["Online store with cart and checkout", "Product catalog setup", "Payments and shipping configuration", "Product and store SEO", "Everything in Business pro"]),
]
ADDONS = [("AI chatbot", 299), ("SEO keyword sprint", 249), ("Google Business Profile setup", 99), ("Online booking system", 249)]

def tiers():
    out = '<div class="tiers">'
    for name, price, when, pick, feats in PACKAGES:
        slug = name.lower().replace(" ", "-")
        out += (f'<div class="tier{" pick" if pick else ""}">' + ('<span class="tag">Most popular</span>' if pick else '') +
                f'<h3>{name}</h3><div class="price">${price:,}</div><div class="when">{when}</div><ul>' +
                "".join(f"<li>{I['check']}<span>{f}</span></li>" for f in feats) +
                f'</ul><a class="btn {"btn-primary" if pick else "btn-ghost"}" href="/free-growth-plan/?package={name.replace(" ", "%20")}&amp;estimate={price}">Choose {name.lower()}</a></div>')
    return out + '</div>'

def estimator():
    pk = "".join(f'<label class="opt"><input type="radio" name="pkg" value="{p}" data-label="{n}"{" checked" if pick else ""}><span>{n}</span><b>${p:,}</b></label>'
                 for n, p, _, pick, _ in PACKAGES)
    ad = "".join(f'<label class="opt"><input type="checkbox" name="addon" value="{p}" data-label="{n}"><span>{n}</span><b>+${p}</b></label>' for n, p in ADDONS)
    return f'''<div class="est" data-est>
  <form class="est-form" onsubmit="return false">
    <fieldset><legend>Choose your website</legend>{pk}</fieldset>
    <fieldset style="margin-bottom:0"><legend>Add growth extras</legend>{ad}</fieldset>
  </form>
  <div class="est-sum" aria-live="polite">
    <span class="muted">Estimated investment</span>
    <div class="est-total" data-total>$999</div>
    <p class="muted"><span data-pkgname>Multi-page website</span>. Pay <strong data-deposit>$499.50</strong> to start and the rest when you approve the finished site.</p>
    <a class="btn btn-primary" data-lock href="/free-growth-plan/">Get a plan for this scope</a>
  </div>
</div>'''

HOME_FAQ = [
 ("How much does a website cost with Impex Studios?",
  "Websites start at $499 for a landing page, $999 for a 5-page site, $1,499 for a 10-page business site with a blog, and $1,999 for an online store. Every price is fixed in writing before we start. See <a href=\"/pricing/\">full pricing</a>."),
 ("Do you work with businesses outside Toronto?",
  "Yes. We’re based in Toronto and work with businesses across Canada and the United States, from solo owners to larger teams with multiple locations. Everything runs remotely, with calls scheduled in your time zone."),
 ("What is an AI phone agent?",
  "An AI phone agent (or AI receptionist) answers your business line in a natural voice, handles common questions, books appointments into your calendar, and sends the details to your CRM. It works 24/7 and can hand off to a person whenever you want."),
 ("Will my site show up in ChatGPT and Google AI Overviews?",
  "We build for it. Clean structure, schema markup, clear answers to the questions customers ask, and consistent business information across the web all make it easier for AI search tools to understand and recommend you. No one can guarantee placement, and anyone who does is guessing."),
 ("How long does it take?",
  "Landing pages take 1–2 days, multi-page sites about 5–7 days, and larger builds 7–10 days. AI automation and SEO timelines depend on scope and are written into your plan."),
 ("Do I own the website?",
  "Yes. You own 100% of the code, design, content and accounts. If you ever leave, you take everything with you."),
]

# ================= PAGES =================

def home():
    body = f'''<section class="hero"><div class="wrap hero-grid">
  <div>
    <h1>Get found. Get the call. Never miss it again.</h1>
    <p class="lede">Impex Studios is a digital marketing and AI automation agency for businesses across Canada and the US. We build fast websites, get you ranked on Google and in AI search, and set up AI phone agents that book customers around the clock.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/free-growth-plan/">Get my free growth plan</a><a class="btn btn-ghost" href="/pricing/">See pricing</a></div>
    <div class="hero-meta"><span>{I["pin"]}Toronto, serving Canada &amp; the US</span><span>{I["clock"]}Plan in one business day</span><span>{I["key"]}Websites from $499</span></div>
  </div>
  {CALL_DEMO}
</div></section>

<section class="section-tight band"><div class="wrap">{PROMISES}</div></section>

<section class="section" id="services"><div class="wrap">
  <div class="section-head"><h2>Everything that turns a search into a paying customer</h2>
  <p class="lede">Most businesses lose customers in the gaps: a slow site, a missing map listing, a call nobody answered. We close those gaps with one team.</p></div>
  {svc_rows()}
</div></section>

<section class="section paper"><div class="wrap">
  <div class="section-head"><h2>How a project runs</h2><p class="lede">Clear steps, a fixed price, and a launch date you can plan around.</p></div>
  {STEPS}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>What are unanswered calls costing you?</h2>
  <p class="lede">Move the sliders to match your business. Most owners are surprised.</p></div>
  {CALC}
</div></section>

<section class="section paper"><div class="wrap split">
  <div><h2>Built for small shops and growing teams alike</h2>
  <p class="lede">A one-location contractor and a multi-region brand need different things. Your plan is sized to where you are now, with room to grow.</p></div>
  <div class="industries">
    <span>Home services &amp; trades</span><span>Real estate</span><span>Clinics &amp; wellness</span><span>Restaurants &amp; hospitality</span>
    <span>Law &amp; accounting</span><span>Automotive</span><span>Salons &amp; beauty</span><span>E-commerce</span><span>B2B &amp; SaaS</span><span>Tech &amp; startups</span>
  </div>
</div></section>

<!-- CASE STUDIES: top agencies win on proof. Add 3 real projects here once you have client sign-off.
<section class="section"><div class="wrap"><div class="section-head"><h2>Recent work</h2></div>
  Client name · industry · city — one sentence on the problem — 1–2 real numbers (e.g. "+38% quote requests in 60 days")
</div></section> -->

<section class="section"><div class="wrap">
  <div class="section-head"><h2>Pricing you can see before you call</h2>
  <p class="lede">Fixed project prices. Monthly SEO, social and automation work is quoted in your growth plan.</p></div>
  {tiers()}
</div></section>

<section class="section paper"><div class="wrap">
  <div class="section-head"><h2>Questions owners ask us</h2></div>
  {faq_html(HOME_FAQ)}
</div></section>

{cta_band()}'''
    page("/", "Digital Marketing & AI Automation Agency | Canada & US | Impex Studios",
         "Toronto-based agency building fast websites, SEO and AI search visibility, AI phone agents and automation for businesses across Canada and the US. Websites from $499.",
         body, [faq_schema(HOME_FAQ)])

# ---------- service pages ----------
SVC = {
 "web-design": dict(
   name="Web design & development", t="Web Design & Development Agency | Canada & US | Impex Studios",
   d="Custom, fast, mobile-first websites for businesses in Canada and the US. Landing pages from $499, full sites from $999. Fixed pricing, launch in days.",
   h1="Websites that load fast and turn visitors into customers",
   lede="Custom-designed, hand-built websites for businesses across Canada and the US. No bloated templates, no plugin chains that break on update, and a launch date in writing.",
   inc=[("Custom design for your brand", "Layouts built around how your customers decide, not a template someone else is also using."),
        ("Mobile-first and fast", "Built to pass Google’s Core Web Vitals so pages feel instant on any phone."),
        ("Lead capture that works", "Quote forms, booking, click-to-call and chat placed where people are ready to act."),
        ("SEO built in from day one", "Clean headings, schema markup, sitemaps and metadata on every page."),
        ("Accessible by default", "Designed toward WCAG 2.1 AA, which supports AODA in Ontario and ADA expectations in the US."),
        ("Analytics and tracking", "GA4, conversion events and call tracking so you know which pages earn leads.")],
   why=[("Faster launches", "Landing pages in 1–2 days and full sites in about a week, because senior people do the work."),
        ("Clear ownership", "You get the code, domain and accounts. No lock-in, no hostage hosting."),
        ("Room to grow", "Add a blog, store, booking or AI chatbot later without rebuilding.")],
   faq=[("What platform do you build on?", "It depends on what you need to manage. We hand-code for speed, use WordPress when you want to edit content yourself, and connect tools like Supabase or GoHighLevel for portals and CRM. We recommend the right fit in your growth plan."),
        ("Can you redesign my existing website?", "Yes. We keep what’s working, set up redirects so you don’t lose Google rankings, and rebuild the rest."),
        ("Do you write the content?", "We write conversion-focused copy from a short intake call and your existing material. You approve every word before launch."),
        ("Where is my site hosted?", "We usually deploy on Cloudflare for speed and security. If you already have hosting you like, we can use it.")]),
 "seo": dict(
   name="SEO, local SEO & AI search optimization", t="SEO & AI Search Optimization Agency | Canada & US | Impex Studios",
   d="Rank on Google, win the local map pack, and get recommended in ChatGPT, Perplexity and Google AI Overviews. SEO for businesses across Canada and the US.",
   h1="Show up where customers search, including AI answers",
   lede="Search no longer ends at ten blue links. We get your business ranking on Google, visible in the map pack, and easy for ChatGPT, Perplexity, Gemini and Google’s AI Overviews to understand and recommend.",
   inc=[("Technical SEO audit and fixes", "Speed, crawlability, indexing, redirects and site structure, fixed rather than just reported."),
        ("Local SEO and Google Business Profile", "Categories, services, photos, reviews strategy and consistent listings across directories."),
        ("Keyword research and content plan", "The searches your buyers use, mapped to pages that answer them better than competitors."),
        ("Schema markup and entity data", "Structured data that tells search engines and AI tools exactly who you are and what you do."),
        ("AI search optimization (GEO)", "Clear answer-style content, FAQs and citations that make your business easy for AI assistants to recommend."),
        ("Reporting tied to leads", "Monthly reports on calls, forms and bookings from search, not just rankings.")],
   why=[("City and region pages done right", "Useful location pages for every market you serve in Canada and the US, not thin copies."),
        ("No black-hat shortcuts", "No bought links or keyword stuffing. Nothing that puts your domain at risk."),
        ("Honest timelines", "Local fixes can move in weeks. Competitive rankings take months, and we’ll say so up front.")],
   faq=[("How long does SEO take to work?", "Technical and Google Business Profile fixes often show movement in a few weeks. Competitive organic rankings usually take three to six months of consistent work."),
        ("What is GEO or AI search optimization?", "Generative engine optimization is making your business easy for AI assistants like ChatGPT, Perplexity and Google AI Overviews to find, understand and cite, using structured data, clear answers and consistent information across the web."),
        ("Can you guarantee first place on Google?", "No honest agency can. We guarantee the work, the reporting, and a clear plan for what we’ll do each month."),
        ("Do you do SEO for multiple locations?", "Yes. We handle multi-location and multi-city SEO across Canadian provinces and US states, including separate Google Business Profiles per location.")]),
 "ai-automation": dict(
   name="AI phone agents, chatbots & workflow automation", t="AI Phone Agents, Chatbots & Automation Agency | Canada & US | Impex Studios",
   d="AI receptionists that answer every call and book appointments, website chatbots that qualify leads, and n8n/Make workflow automation for businesses in Canada and the US.",
   h1="AI that answers, books and follows up for you",
   lede="We build AI phone agents, chatbots and automated workflows on the tools you already use, so every call gets answered, every lead gets a reply, and your team stops copying data between apps.",
   inc=[("AI phone agents", "A natural-sounding receptionist on your number that answers questions, books appointments and takes messages 24/7."),
        ("Website and SMS chatbots", "Trained on your services and pricing to answer questions and capture qualified leads."),
        ("CRM and calendar automation", "New leads land in your CRM, get tagged, and receive an instant reply and reminders."),
        ("Workflow automation", "n8n and Make workflows that connect forms, email, spreadsheets, invoicing and your CRM."),
        ("Follow-up sequences", "Text and email follow-ups for quotes, missed calls and reviews, sent with proper consent."),
        ("Human handoff and monitoring", "Clear rules for when a call goes to a person, plus logs so you can review every conversation.")],
   why=[("Built on proven platforms", "Vapi for voice, GoHighLevel, n8n, Make, Airtable and Supabase. No black-box software you can’t leave."),
        ("Consent and privacy in mind", "Call disclosures and opt-ins designed with CASL and PIPEDA in Canada and TCPA in the US in mind."),
        ("Start small", "Begin with one agent or one workflow, measure it, then expand.")],
   faq=[("Will callers know they’re talking to AI?", "We recommend a short disclosure at the start of each call. It builds trust and is expected under many privacy and telemarketing rules. The agent sounds natural and can transfer to a person any time."),
        ("What does an AI phone agent cost?", "It depends on call volume and integrations. You’ll get a fixed setup price and a clear monthly estimate in your growth plan. A website chatbot can be added to any site package for $299."),
        ("Can it book into my calendar?", "Yes. We connect Google Calendar, Outlook, GoHighLevel and most booking tools, and the agent only offers times you’re actually available."),
        ("Which tools do you automate?", "Common ones include GoHighLevel, HubSpot, Google Workspace, Microsoft 365, Airtable, QuickBooks, Stripe, Slack and most apps with an API.")]),
 "social-media": dict(
   name="Social media marketing", t="Social Media Marketing Agency | Canada & US | Impex Studios",
   d="Social media management, content creation and paid social for businesses in Canada and the US. Consistent, on-brand posts that build trust and drive leads.",
   h1="Social media that keeps you top of mind",
   lede="Planned, designed and published for you. We create on-brand content for Instagram, Facebook, LinkedIn and TikTok that builds trust with your audience and sends people back to your website.",
   inc=[("Content strategy and calendar", "A monthly plan built around your offers, seasons and what your audience engages with."),
        ("Post and carousel design", "Custom graphics from designers with years of Adobe Creative Suite experience."),
        ("Short-form video", "Reels and short videos edited for each platform."),
        ("Captions and hashtags", "Written in your voice, with clear calls to action."),
        ("Community management", "Replies to comments and messages so no lead goes cold."),
        ("Paid social campaigns", "Targeted Meta and LinkedIn ads tied to landing pages and tracked to leads.")],
   why=[("Connected to your website", "Every campaign points somewhere that converts, with tracking in place."),
        ("Consistent, not sporadic", "A steady publishing rhythm beats bursts of activity followed by silence."),
        ("Reported in plain English", "What grew, what drove leads, and what we’ll change next month.")],
   faq=[("Which platforms do you manage?", "Instagram, Facebook, LinkedIn and TikTok are the most common. We recommend the platforms where your customers actually spend time."),
        ("Do I need to provide photos?", "Real photos of your team and work perform best, and we’ll guide you on what to capture. We fill gaps with design and licensed imagery."),
        ("How much does social media management cost?", "Monthly pricing depends on platforms and posting volume. You’ll see a fixed monthly price in your growth plan."),
        ("Can you run ads too?", "Yes. We set up and manage paid campaigns on Meta and LinkedIn with landing pages and conversion tracking.")]),
}

def service(slug):
    s = SVC[slug]; path = f"/services/{slug}/"
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], None)]
    why = "".join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in s["why"])
    body = f'''{page_hero(trail, s["h1"], s["lede"])}
<section class="section"><div class="wrap split">
  <div><h2>What’s included</h2><p class="lede">Everything is scoped in your growth plan with a fixed price before any work starts.</p>
  {'<div style="margin-top:28px">'+CALL_DEMO+'</div>' if slug=="ai-automation" else ''}</div>
  {checks(s["inc"])}
</div></section>
{'<section class="section band"><div class="wrap"><div class="section-head"><h2>What are unanswered calls costing you?</h2></div>'+CALC+'</div></section>' if slug=="ai-automation" else ''}
<section class="section paper"><div class="wrap"><div class="section-head"><h2>Why businesses choose us</h2></div>
  <div class="feature-grid">{why}</div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><h2>How it works</h2></div>{STEPS}</div></section>
<section class="section paper"><div class="wrap"><div class="section-head"><h2>Frequently asked questions</h2></div>{faq_html(s["faq"])}</div></section>
{cta_band()}'''
    svc_schema = {"@type": "Service", "@id": SITE + path + "#service", "name": s["name"], "serviceType": s["name"],
                  "provider": {"@id": SITE + "/#org"}, "description": s["d"],
                  "areaServed": [{"@type": "Country", "name": "Canada"}, {"@type": "Country", "name": "United States"}]}
    page(path, s["t"], s["d"], body, [svc_schema, faq_schema(s["faq"])], trail)

def services_hub():
    trail = [("Home", "/"), ("Services", None)]
    body = f'''{page_hero(trail, "Digital marketing and AI automation services", "One team for your website, search visibility, social presence and the automation that keeps leads from slipping through. Pick one service or combine them.")}
<section class="section"><div class="wrap">{svc_rows()}</div></section>
<section class="section paper"><div class="wrap"><div class="section-head"><h2>How a project runs</h2></div>{STEPS}</div></section>
{cta_band()}'''
    page("/services/", "Services: Web Design, SEO, AI Automation & Social | Impex Studios",
         "Web design, SEO and AI search optimization, AI phone agents, chatbots, workflow automation and social media marketing for businesses across Canada and the US.", body, [], trail)

def pricing():
    trail = [("Home", "/"), ("Pricing", None)]
    faq = [("Are these prices final?", "Yes. Your growth plan lists the exact scope and a fixed price. If you ask for something outside that scope, we quote it separately before doing it."),
           ("How does payment work?", "50% to start your project and 50% when you approve the finished site on staging. Nothing goes live until you’re happy."),
           ("What about monthly services?", "SEO, social media, AI phone agents and automation are quoted monthly in your growth plan based on scope. No long lock-in contracts."),
           ("Is hosting included?", "We deploy on fast, secure hosting and walk you through the options. Most small sites run on low-cost or free hosting tiers."),
           ("Do you offer payment plans?", "Ask us. For larger builds we can split payments across milestones.")]
    body = f'''{page_hero(trail, "Simple, fixed pricing", "Know what you’ll pay before we start. Every project is custom, delivered on a fixed timeline, and paid 50% up front and 50% on approval.", ctas=False)}
<section class="section"><div class="wrap">{tiers()}</div></section>
<section class="section band"><div class="wrap"><div class="section-head"><h2>Estimate your project</h2><p class="lede">Pick a website and any extras to see your total.</p></div>{estimator()}</div></section>
<section class="section"><div class="wrap split">
  <div><h2>Monthly growth services</h2><p class="lede">Ongoing work is priced to your goals and quoted in your free growth plan.</p>
  <div class="btn-row"><a class="btn btn-primary" href="/free-growth-plan/">Get my free growth plan</a></div></div>
  {checks([("SEO and AI search", "Technical fixes, content, local SEO and monthly lead reporting."),
           ("AI phone agents", "Setup plus a monthly plan based on call volume."),
           ("Automation and CRM", "Workflows built once, with optional monitoring and changes."),
           ("Social media management", "Content, publishing and community management by platform.")])}
</div></section>
<section class="section paper" id="faq"><div class="wrap"><div class="section-head"><h2>Pricing questions</h2></div>{faq_html(faq)}</div></section>
{cta_band()}'''
    offers = {"@type": "OfferCatalog", "name": "Website packages", "itemListElement": [
        {"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "CAD", "seller": {"@id": SITE + "/#org"}} for n, p, *_ in PACKAGES]}
    page("/pricing/", "Website & Marketing Pricing | From $499 | Impex Studios",
         "Transparent, fixed pricing: landing pages from $499, 5-page websites $999, business sites $1,499, e-commerce $1,999. 50/50 payment, launch in days.",
         body, [offers, faq_schema(faq)], trail)

def about():
    trail = [("Home", "/"), ("About", None)]
    body = f'''{page_hero(trail, "A small studio with senior-level standards", "Impex Studios is a Toronto-based digital marketing and AI automation agency. We work with businesses across Canada and the US that want a partner who builds, explains, and stays accountable.")}
<section class="section"><div class="wrap split">
  <div><h2>Why we exist</h2>
  <p class="lede">Too many business owners pay for websites that look fine and do nothing, and for marketing reports full of numbers that never become customers.</p>
  <p class="muted">We started Impex Studios to do it differently: one team that connects design, search, social and automation, with fixed prices and plain-English reporting. We use the same AI tools reshaping our industry to move faster, and pass that speed on to you.</p>
  <!-- FOUNDER: add your photo, name and 2–3 lines here. A real face is one of the strongest trust signals an agency site can have. --></div>
  {checks([("Senior people on every project", "No hand-offs to juniors you’ve never met."),
           ("Fixed scope, fixed price", "The quote is the invoice."),
           ("You own everything", "Code, content, domain and accounts."),
           ("No bloat", "Lightweight builds that stay fast and don’t break on updates."),
           ("Measured on results", "Leads, calls and bookings, not impressions.")])}
</div></section>
<section class="section paper"><div class="wrap"><div class="section-head"><h2>The tools we build with</h2><p class="lede">Proven platforms you can keep using even if you stop working with us.</p></div>
<div class="industries"><span>WordPress</span><span>Supabase</span><span>Cloudflare</span><span>n8n</span><span>Make</span><span>Vapi</span><span>GoHighLevel</span><span>Airtable</span><span>Google Analytics 4</span><span>Adobe Creative Suite</span></div></div></section>
{cta_band()}'''
    page("/about/", "About Impex Studios | Toronto Digital Marketing & AI Agency",
         "Impex Studios is a Toronto-based digital marketing and AI automation agency serving businesses across Canada and the US with fixed pricing and senior-led work.", body, [], trail)

def lead_form(kind, full=True):
    services = ["Website", "SEO / AI search", "AI phone agent", "Chatbot", "Automation", "Social media"]
    sizes = ["Just me", "2–10", "11–50", "51–200", "200+"]
    pills = lambda name, opts, typ="checkbox": '<div class="pills">' + "".join(
        f'<label><input type="{typ}" name="{name}" value="{o}"><span>{o}</span></label>' for o in opts) + '</div>'
    extra = f'''
  <div><label for="website">Current website <span class="opt-l">(optional)</span></label><input id="website" name="website" type="url" placeholder="https://"></div>
  <div><label for="country">Where is your business?</label><select id="country" name="country" required><option value="">Choose one</option><option>Canada</option><option>United States</option><option>Both</option><option>Other</option></select></div>
  <fieldset class="full"><legend>Team size</legend>{pills("size", sizes, "radio")}</fieldset>
  <fieldset class="full"><legend>What do you need help with?</legend>{pills("services", services)}</fieldset>
  <div class="full"><label for="budget">Budget range <span class="opt-l">(optional)</span></label><select id="budget" name="budget"><option value="">Not sure yet</option><option>Under $1,000</option><option>$1,000–$3,000</option><option>$3,000–$10,000</option><option>$10,000+</option><option>Monthly retainer</option></select></div>''' if full else ""
    return f'''<form class="form" action="/api/contact" method="post" data-lead="{kind}">
  <input type="hidden" name="form" value="{kind}">
  <div class="hp" aria-hidden="true"><label for="company_url">Leave this empty</label><input id="company_url" name="company_url" tabindex="-1" autocomplete="off"></div>
  <div><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
  <div><label for="business">Business name</label><input id="business" name="business" type="text" autocomplete="organization" required></div>
  <div><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
  <div><label for="phone">Phone <span class="opt-l">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>{extra}
  <div class="full"><label for="message">{"What would you like to achieve in the next 12 months?" if full else "How can we help?"}</label><textarea id="message" name="message" required></textarea></div>
  <div class="full"><button class="btn btn-primary" type="submit">{"Send me my growth plan" if full else "Send message"}</button>
  <p class="small muted" style="margin-top:12px">We reply within one business day. We’ll only use your details to respond. See our <a href="/privacy/">privacy policy</a>.</p></div>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>'''

def growth_plan():
    trail = [("Home", "/"), ("Free growth plan", None)]
    body = f'''{page_hero(trail, "Get your free growth plan", "Tell us about your business. Within one business day you’ll get a written plan with what we’d fix, what we’d build, and fixed pricing. No pressure, no obligation.", ctas=False)}
<section class="section"><div class="wrap split">
  <div><h2>What you’ll get</h2>
  {checks([("A review of your current site and search presence", "Speed, mobile experience, Google Business Profile and how AI search sees you."),
           ("Clear recommendations", "What to fix first and what will move leads the most."),
           ("Fixed pricing options", "Exact scope and price for each recommendation."),
           ("A realistic timeline", "When you can expect launch and results.")])}
  <p class="muted small" style="margin-top:20px">Prefer to talk? Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p></div>
  <div class="panel">{lead_form("growth-plan")}</div>
</div></section>'''
    page("/free-growth-plan/", "Free Growth Plan & Website Audit | Impex Studios",
         "Get a free written growth plan for your business within one business day: website and SEO review, recommendations and fixed pricing. Canada and US.", body, [], trail)

def contact():
    trail = [("Home", "/"), ("Contact", None)]
    body = f'''{page_hero(trail, "Let’s talk about your business", "Call, text, email or send a message. You’ll hear back from a real person within one business day.", ctas=False)}
<section class="section"><div class="wrap split">
  <div><ul class="contact-list">
    <li><strong>Call or text</strong><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
    <li><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><strong>Hours</strong><span>Mon–Fri, 9 am–6 pm ET</span></li>
    <li><strong>Based in</strong><span>Toronto, Ontario</span></li>
    <li><strong>Serving</strong><span>Canada and the United States</span></li></ul></div>
  <div class="panel">{lead_form("contact", full=False)}</div>
</div></section>'''
    page("/contact/", "Contact Impex Studios | Toronto Digital Marketing Agency",
         f"Contact Impex Studios. Call or text {PHONE} or email {EMAIL}. Serving businesses across Canada and the US.", body, [], trail)

def market(slug):
    ca = slug == "canada"
    path = f"/{slug}/"
    trail = [("Home", "/"), ("Canada" if ca else "United States", None)]
    if ca:
        h1 = "Digital marketing and AI automation for Canadian businesses"
        lede = "From Toronto to Vancouver, Calgary to Halifax, we help Canadian businesses get found online, win more calls and automate the busywork, with pricing in plain dollars and a team in your time zone."
        pts = [("Local SEO for Canadian cities", "Google Business Profile, city pages and directory listings for every market you serve, from the GTA to the rest of Canada."),
               ("Privacy-aware lead capture", "Forms and data handling designed with PIPEDA and provincial privacy rules in mind."),
               ("CASL-conscious email and SMS", "Automations built around consent, clear identification and easy unsubscribe."),
               ("Accessible websites", "Designed toward WCAG 2.1 AA, the standard behind Ontario’s AODA requirements."),
               ("Bilingual-ready builds", "Site structure that can support English and French pages when you need them."),
               ("Eastern-time support", "Calls and updates during Canadian business hours.")]
        cities = ["Toronto", "Mississauga", "Brampton", "Vaughan", "Markham", "Oakville", "Hamilton", "Ottawa", "Montréal", "Vancouver", "Calgary", "Edmonton", "Winnipeg", "Halifax"]
        t = "Digital Marketing & AI Automation Agency in Canada | Impex Studios"
        d = "Toronto-based agency helping Canadian businesses with web design, local SEO, AI search, AI phone agents and automation. Built with PIPEDA, CASL and AODA in mind."
    else:
        h1 = "Digital marketing and AI automation for US businesses"
        lede = "We help US businesses in every state get found on Google and in AI search, answer every call with AI receptionists, and automate follow-up, with fixed pricing and hours that overlap your day."
        pts = [("Multi-state local SEO", "Google Business Profiles, location pages and citations for every city and state you serve."),
               ("Accessible websites", "Designed toward WCAG 2.1 AA to support ADA accessibility expectations."),
               ("Consent-aware calling and SMS", "AI calls and text follow-ups set up with TCPA consent requirements in mind."),
               ("Privacy-aware forms", "Data collection designed with CCPA and state privacy laws in mind."),
               ("Coverage across time zones", "AI agents answer 24/7 from Eastern to Pacific time."),
               ("Overlapping hours", "We’re on Eastern time, so your morning calls get same-day answers.")]
        cities = ["New York", "Buffalo", "Boston", "Chicago", "Detroit", "Miami", "Atlanta", "Dallas", "Houston", "Phoenix", "Denver", "Los Angeles", "Seattle", "Philadelphia"]
        t = "Digital Marketing & AI Automation Agency for US Businesses | Impex Studios"
        d = "Web design, SEO and AI search optimization, AI phone agents and automation for small and growing businesses across the United States. Fixed pricing, fast launches."
    body = f'''{page_hero(trail, h1, lede)}
<section class="section"><div class="wrap split">
  <div><h2>Built for the {"Canadian" if ca else "US"} market</h2><p class="lede">The marketing fundamentals are the same everywhere. The details that protect you and win local customers are not.</p></div>
  {checks(pts)}
</div></section>
<section class="section band"><div class="wrap"><div class="section-head"><h2>Our services</h2></div>{svc_rows()}</div></section>
<section class="section"><div class="wrap split">
  <div><h2>Where we work</h2><p class="lede">We work remotely with businesses {"across every province and territory" if ca else "in all 50 states"}. Some of the markets we serve:</p></div>
  <div class="industries">{"".join(f"<span>{c}</span>" for c in cities)}</div>
</div></section>
{cta_band()}'''
    page(path, t, d, body, [], trail)

def privacy():
    trail = [("Home", "/"), ("Privacy", None)]
    body = f'''{page_hero(trail, "Privacy policy", "How Impex Studios collects, uses and protects your information.", ctas=False)}
<section class="section"><div class="wrap prose">
<p><em>Last updated: October 26, 2026</em></p>
<h2>What we collect</h2><p>When you contact us or request a growth plan, we collect the details you submit: your name, business name, email, phone number, website and message. Our site may also use privacy-friendly analytics to understand which pages are visited.</p>
<h2>How we use it</h2><p>We use your information only to respond to you, prepare your growth plan or proposal, and deliver services you’ve agreed to. We do not sell your information. We will only send you marketing messages if you’ve given consent, and you can unsubscribe at any time.</p>
<h2>Who we share it with</h2><p>We use trusted service providers to run our website, forms, email and CRM. They process data on our behalf and only as needed to provide those services. Some providers may store data outside Canada.</p>
<h2>Your choices</h2><p>You can ask to see, correct or delete the personal information we hold about you by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>Questions about privacy? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
</div></section>'''
    page("/privacy/", "Privacy Policy | Impex Studios", "How Impex Studios collects, uses and protects personal information submitted through impexstudios.com.", body, [], trail)

def thanks():
    body = f'''<section class="page-hero" style="border:0"><div class="wrap"><h1>Thanks, we’ve got it.</h1>
<p class="lede">You’ll hear from us within one business day. If it’s urgent, call or text <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
<div class="btn-row"><a class="btn btn-ghost" href="/">Back to home</a><a class="btn btn-ghost" href="/pricing/">See pricing</a></div></div></section>'''
    page("/thanks/", "Thank you | Impex Studios", "Your message has been sent to Impex Studios.", body, [], noindex=True)

def notfound():
    body = '''<section class="page-hero" style="border:0"><div class="wrap"><h1>This page doesn’t exist.</h1>
<p class="lede">It may have moved when we redesigned the site. Try one of these instead.</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Go to home</a><a class="btn btn-ghost" href="/services/">Services</a><a class="btn btn-ghost" href="/pricing/">Pricing</a><a class="btn btn-ghost" href="/contact/">Contact</a></div></div></section>'''
    page("/404.html", "Page not found | Impex Studios", "The page you’re looking for doesn’t exist.", body, [], noindex=True)

# ---------- static files ----------
def statics():
    src = os.path.dirname(os.path.abspath(__file__))
    shutil.copytree(os.path.join(src, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True)
    w = lambda p, s: open(os.path.join(OUT, p), "w", encoding="utf-8").write(s)
    w("favicon.svg", LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in SITEMAP)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    w("llms.txt", f"""# Impex Studios

> Toronto-based digital marketing and AI automation agency serving small to large businesses across Canada and the United States.

Contact: {PHONE} · {EMAIL} · Mon–Fri 9am–6pm ET

## Services
- [Web design & development]({SITE}/services/web-design/): custom, fast websites. Landing page $499, 5-page site $999, 10-page business site $1,499, e-commerce $1,999. Fixed pricing, 50/50 payment.
- [SEO, local SEO & AI search]({SITE}/services/seo/): technical SEO, Google Business Profile, schema, content, generative engine optimization.
- [AI phone agents & automation]({SITE}/services/ai-automation/): AI receptionists, chatbots, CRM and n8n/Make workflow automation.
- [Social media marketing]({SITE}/services/social-media/): content, design, short-form video, community management, paid social.

## Key pages
- [Pricing]({SITE}/pricing/)
- [Free growth plan]({SITE}/free-growth-plan/)
- [Canada]({SITE}/canada/) · [United States]({SITE}/usa/)
- [About]({SITE}/about/) · [Contact]({SITE}/contact/)
""")
    # Keep old URLs' rankings: 301 the previous .html pages to the new clean URLs
    w("_redirects", """/index.html      /                 301
/about.html      /about/           301
/services.html   /services/        301
/portfolio.html  /services/        301
/pricing.html    /pricing/         301
/faq.html        /pricing/#faq     301
/contact.html    /contact/         301
/usa             /usa/             301
/us/             /usa/             301
/audit           /free-growth-plan/ 301
""")
    w("_headers", """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
""")

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    home(); services_hub()
    for s in SVC: service(s)
    pricing(); about(); growth_plan(); contact(); market("canada"); market("usa"); privacy(); thanks(); notfound()
    statics()
    print("Built", len(SITEMAP), "indexable pages into", OUT)
