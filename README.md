# Lawfinity Solicitors — static Jekyll rebuild

This repository contains the GitHub Pages rebuild of the Lawfinity Solicitors website.

## Design
The site uses the **Yacht Club** palette:
- `#F2F0EF` — paper
- `#BBBCBC` — stone
- `#245F73` — teal
- `#733E24` — rust

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
5. Confirm GitHub Pages and the production domain/DNS are configured.

Firm details used in the build:
- Lawfinity Solicitors Limited
- 71–75 Shelton Street, Covent Garden, London WC2H 9JQ
- 07950 789563
- info@lawfinitysolicitors.com
- SRA no. 8008876
- Company no. 15588850
