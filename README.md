<div align="center">

**🇺🇸 English** · [🇧🇷 Português](README.pt-BR.md)

<a href="https://nlspaint.com"><img src="assets/og-image.jpg" alt="NLS Paint" width="100%"></a>

# NLS Paint

**A first web presence for a residential and commercial painting company in Massachusetts and Rhode Island, built to get estimate requests from the phone.**

[![Live site](https://img.shields.io/badge/live-nlspaint.com-0B2A5B?style=for-the-badge&logo=googlechrome&logoColor=white)](https://nlspaint.com)
[![Status](https://img.shields.io/badge/status-coming%20soon%20page-D2202F?style=for-the-badge)](https://nlspaint.com)

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

[**🌐 Visit the site**](https://nlspaint.com) · [About](#-about) · [Screenshots](#-screenshots) · [Features](#-features) · [Run locally](#-run-locally)

</div>

---

## 📌 About

NLS Paint is a painting company based in Woonsocket, RI, serving homes and businesses within about 70 miles of Milford, MA. It had no presence on the web. The goals are to **get estimate requests from the phone** and to **show up on Google for local searches**.

This first release is a "coming soon" page that already works for the business: it presents the brand, shows where the company works and what it does, and gets the visitor to call or text in one tap.

| | |
|---|---|
| **Client** | NLS Paint, residential and commercial painting in MA and RI |
| **Audience** | Homeowners and businesses in MA and RI, mostly on their phones |
| **My role** | Client interview, web identity, design, development, SEO and deploy |
| **Year** | 2026 |
| **Site** | [nlspaint.com](https://nlspaint.com) |

## 📸 Screenshots

<div align="center">
  <img src=".github/screenshots/desktop.png" alt="NLS Paint on desktop" width="68%">
  &nbsp;
  <img src=".github/screenshots/mobile.png" alt="NLS Paint on a phone" width="24%">
  <br><sub>The page on desktop and on a phone (390 px)</sub>
</div>

## ✨ Features

- **Animations that paint.** Three red, white and red brush strokes cross the top like the logo, and an SVG paint roller paints the wall live to reveal "NLS PAINT · coming soon". Pure CSS, no library.
- **Mobile first, built to convert.** One-tap **Call** (`tel:`) and **Send a text** (`sms:`) with the message pre-written, plus a **Copy number** button with a fallback for browsers that block the clipboard.
- **Local SEO from day one.** Title and description with service, towns and phone, canonical URL, Open Graph and Twitter Card with a custom 1200×630 image, and full favicon set.
- **Accessible and fast.** Respects `prefers-reduced-motion`, visible focus states, ARIA labels, and a logo in WebP with declared dimensions so nothing jumps. The whole page is one ~15 KB file with no build step.
- **Brand palette from the logo:** navy `#0B2A5B`, red `#D2202F` and paper `#F4F6FA`, with Barlow Condensed italics for headings, like brush strokes.

## 🚀 Run locally

**No install:** open `index.html` in a browser.

**With Docker**, same as production:

```bash
docker build -t nlspaint .
```

```bash
docker run --rm -p 8080:80 nlspaint
```

Then open `http://localhost:8080`.

## 🗺️ Roadmap

- [x] "Coming soon" page with contact, service area and services
- [x] Docker + Nginx deploy with a custom domain
- [ ] Full home page with a gallery of real projects and before/after photos
- [ ] A page for each of the 6 services
- [ ] Project pages with photos and the town of each job
- [ ] Town pages created only from real projects
- [ ] `HousePainter` (LocalBusiness), `FAQPage` and `BreadcrumbList` structured data

---

<div align="center">

**Wanderson Oliveira** · Websites & AI solutions that bring businesses more customers

[![derson.cloud](https://img.shields.io/badge/derson.cloud-2563EB?style=flat-square&logo=googlechrome&logoColor=white)](https://derson.cloud)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:wanderson1873@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/wanderson1873/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat-square&logo=whatsapp&logoColor=white)](https://wa.me/17816664150)

<sub>© 2026 NLS Paint. All rights reserved. Source shown as a portfolio sample.</sub>

</div>
