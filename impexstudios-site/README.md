# impexstudios.com

Static website for Impex Studios. Plain HTML/CSS/JS, no framework, hosted on Cloudflare Pages.

## Folder layout

```
build.py            Page generator: all copy, pricing, FAQs and SEO schema live here
assets/             Source CSS, JS and images (copied into public/ on build)
functions/api/      Cloudflare Pages Function that handles the contact forms
public/             The built website (this is what Cloudflare serves)
```

## Editing the site

1. Change copy, prices or FAQs in `build.py` (styles in `assets/css/site.css`).
2. Run `python3 build.py` (Python 3.9+, no packages needed).
3. Commit and push. Cloudflare redeploys automatically.

## First deploy

1. Create a new GitHub repo and push this folder to it:
   ```
   git init && git add . && git commit -m "New Impex Studios site"
   git branch -M main
   git remote add origin https://github.com/<you>/impexstudios.git
   git push -u origin main
   ```
2. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick the repo.
3. Build settings:
   - Framework preset: None
   - Build command: `python3 build.py`
   - Build output directory: `public`
4. Settings → Variables and Secrets → add `WEBHOOK_URL` = your n8n / Make / GoHighLevel webhook URL.
   Every form submission is POSTed there as JSON (name, business, email, phone, services, budget, message, page, detected country).
5. Custom domains → add `impexstudios.com` and `www.impexstudios.com`.
   Point the domain at Cloudflare Pages only after the new build looks right on the `*.pages.dev` preview URL.

## After launch

- Google Search Console: verify the domain, submit `https://impexstudios.com/sitemap.xml`, and request indexing of the home page.
- Bing Webmaster Tools: import from Search Console (Bing also feeds ChatGPT search).
- Analytics: turn on Cloudflare Web Analytics, or paste a GA4 snippet where `build.py` says "Analytics".
- Test a form submission end to end before announcing the new site.

## SEO built in

- Unique titles, descriptions and canonical URLs on every page
- Schema.org: ProfessionalService/Organization (area served: Canada + US), Service, FAQPage, BreadcrumbList, OfferCatalog
- `sitemap.xml`, `robots.txt`, `llms.txt` (for AI search tools)
- `_redirects`: 301s from the old `.html` URLs so existing Google rankings carry over
- `_headers`: security headers and long-term asset caching
- Canada and US landing pages, plus a page per service
