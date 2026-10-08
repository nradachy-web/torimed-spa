# ToriMed Spa

One-page site for Tori Kruse (ToriMed Spa), a medical aesthetician inside The Beauty Collective, 191 Main Street, Fredericton, NB. Built to replace the Vagaro link in her Instagram bio. Domain: torimed.ca.

Plain HTML, CSS and JavaScript. No build step: edit the files and push.

## Where things are

- `index.html`: all copy, the service menu and prices.
- `assets/styles.css`: styles. Brand colours are black and pink (pink sampled from her logo).
- `assets/main.js`: menu tabs, the "your visit" picker and the booking request form. Settings are in `SITE` at the top.
- `scripts/build_images.py`: cuts and encodes the photos from `_source/ig` (not in git).

## Where the facts came from (read October 8, 2026)

- Services, prices and appointment lengths: Tori's own rows in the Vagaro booking data for The Beauty Collective (provider id 251016366), not the venue-wide "starting at" prices.
- Bio, specialties, "since 2021": her Vagaro staff bio and The Beauty Collective's April 23, 2026 Instagram post introducing her.
- How long results last, the $95 lamination bundle, 2027 wedding dates: her own Instagram captions.
- Client review: Emily M., Vagaro, April 20, 2026, quoted word for word. The second quote is from The Beauty Collective's introduction post.
- Photos and logo: her Instagram (@torimed.spa). The hero portrait has extra blank wall added above her head; nothing else is altered.
- Parking and the 24 hour cancellation policy: The Beauty Collective's Vagaro listing.

## Launch status

Live at https://torimed.ca since October 8, 2026 (GitHub Pages, custom domain set in `CNAME`, DNS at Namecheap: four A records plus a `www` CNAME).

Still open:

1. Tori confirms prices, the cancellation policy and that her clients are fine with their photos on the site.
2. Booking delivery: set `SITE.formKey` in `assets/main.js` to a Web3Forms key that sends to Tori, then prove it with a real submission. Until then the form copies the request for an Instagram message.
