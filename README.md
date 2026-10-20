# Lawfinity Solicitors — static Jekyll rebuild

This repository contains the GitHub Pages rebuild of the Lawfinity Solicitors website.

## Preview
The current GitHub Pages preview is:

https://tamimtasdik-bit.github.io/Tamim-Profile/

The preview uses `baseurl: /Tamim-Profile` so assets and internal links work correctly on the project Pages URL. Before connecting the production domain, change `url` to `https://lawfinitysolicitors.com`, set `baseurl` to an empty string, and replace the preview-only `robots.txt`.

## Design
The site uses a formal **Midnight Navy / Warm Ivory / Antique Brass** palette:
- `#172638` — midnight navy (header/footer)
- `#29465A` — navy slate (buttons and links)
- `#F8F6F1` — warm ivory (page background)
- `#EDE9E0` — soft limestone (editorial sections)
- `#806341` — antique brass (small accents)

The original supplied Lady Justice logo is retained.
## Structure
- Shared Jekyll header/footer
- 8 private immigration service hubs
- 35 service detail routes
- Corporate Immigration and Commissioner for Oaths routes
- Blog archive preserving all 28 supplied article URLs
- About and Contact pages
- Seven policy routes
- SRA digital badge in the footer
- Mobile responsive navigation
- GitHub Pages deployment workflow

## Before production launch
1. Replace `REPLACE_WITH_FORM_ID` in `contact/index.md` with the firm's Formspree form ID.
2. Replace the policy migration notices with the firm's approved policy texts.
3. Replace each blog archive migration notice with the approved original article body.
4. Review all newly drafted service-page copy for legal/marketing approval.
5. Switch Jekyll from the project preview base URL to the production domain.
6. Update `robots.txt` so search engines can crawl the production site.
7. Confirm production DNS and GitHub Pages custom-domain settings.

Firm details used in the build:
- Lawfinity Solicitors Limited
- 71–75 Shelton Street, Covent Garden, London WC2H 9JQ
- 07950 789563
- info@lawfinitysolicitors.com
- SRA no. 8008876
- Company no. 15588850


## AI-generated homepage photography
The homepage now uses two AI-generated, people-free images stored locally:
- `assets/images/ai-lawfinity-hero.webp` — elegant Westminster-inspired legal office
- `assets/images/ai-lawfinity-library.webp` — unoccupied law library and consultation space

These are **conceptual illustrations**, not photographs of Lawfinity Solicitors' actual offices, lawyers or clientele. Public captions make this distinction clear.
