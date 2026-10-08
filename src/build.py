#!/usr/bin/env python3
"""Build the ToriMed Spa site.

    python3 src/build.py

Writes index.html, one folder per service page and sitemap.xml at the repo root.
Copy and prices live in src/content.py; shared markup lives in src/templates.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import BOOKING_FAQS, CATALOG, CATEGORIES, HOME_FAQS, IG_DM, PAGES, SHARED_FAQS, SITE  # noqa: E402

IMAGES = json.load(open(os.path.join(HERE, "images.json")))
V = SITE["asset_version"]
URL = SITE["url"]


def tpl(name):
    return open(os.path.join(HERE, "templates", name), encoding="utf-8").read()


def fill(text, **values):
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{(\w+)\}\}", text)
    if left:
        raise SystemExit("unfilled placeholders: " + ", ".join(sorted(set(left))))
    return text


def minutes_label(minutes):
    hours, mins = divmod(minutes, 60)
    if not hours:
        return f"{mins} min"
    return f"{hours} h" + (f" {mins} min" if mins else "")


def picture(name, sizes, alt, lazy=True, indent="        "):
    """A <picture> with AVIF first and WebP as the fallback, from the image manifest."""
    info = IMAGES[name]
    avif = ", ".join(f"/assets/img/{name}-{w}.avif {w}w" for w in info["widths"])
    webp = ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w in info["widths"])
    loading = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (
        f"{indent}<picture>\n"
        f'{indent}  <source type="image/avif" srcset="{avif}" sizes="{sizes}">\n'
        f'{indent}  <img src="/assets/img/{name}-{info["w"]}.webp" srcset="{webp}" sizes="{sizes}" '
        f'width="{info["w"]}" height="{info["h"]}" alt="{alt}"{loading} decoding="async">\n'
        f"{indent}</picture>"
    )


def service_row(sid):
    s = CATALOG[sid]
    note = f'<span class="svc__note">{s["note"]}</span>' if s.get("note") else ""
    time = f'<span class="svc__time">{minutes_label(s["min"])}</span>' if s.get("time", True) else ""
    return (
        f'              <li class="svc" data-id="{sid}"><span class="svc__text"><span class="svc__name">{s["name"]}</span>{note}</span>'
        f'<span class="svc__meta"><span class="svc__price">${s["price"]}</span>{time}</span></li>'
    )


def price_groups(groups):
    out = []
    for heading, ids in groups:
        rows = "\n".join(service_row(i) for i in ids)
        out.append(
            f'          <div class="menu__group">\n            <h4>{heading}</h4>\n            <ul class="svcs">\n{rows}\n            </ul>\n          </div>'
        )
    return "\n".join(out)


def pills(links):
    if not links:
        return ""
    items = "".join(f'<a class="pill" href="{href}">{label}</a>' for label, href in links)
    return f'\n          <p class="menu__links"><span class="menu__links-label">Read more</span>{items}</p>'


def header(current=""):
    services = "\n".join(f'          <a href="/{p["slug"]}/">{p["nav"]}</a>' for p in PAGES)
    html = fill(tpl("header.html"), services=services)
    if current:
        html = html.replace(f'href="{current}"', f'href="{current}" aria-current="page"')
    return html


def footer():
    services = "\n".join(f'      <a href="/{p["slug"]}/">{p["nav"]}</a>' for p in PAGES)
    return fill(tpl("footer.html"), services=services)


def faq_block(items):
    out = []
    for q, a in items:
        out.append(
            f'        <details>\n          <summary>{q}</summary>\n          <div class="faq__a"><p>{a}</p></div>\n        </details>'
        )
    return "\n".join(out)


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def quote_band(q):
    return (
        '<section class="band band--blush review" aria-label="In their words">\n'
        '  <div class="wrap review__in review__in--single">\n    <figure>\n      <blockquote>\n'
        f'        <p>“{q["quote"]}”</p>\n      </blockquote>\n      <figcaption>\n'
        f'        <span class="review__who">{q["who"]}</span>\n        <span>{q["detail"]}</span>\n'
        "      </figcaption>\n    </figure>\n  </div>\n</section>\n"
    )


BOOK_DEFAULTS = {
    "book_heading": "Book an appointment",
    "book_lede": "Send your request and I will confirm your time.",
    "when_legend": "When suits you?",
    "day_label": "Preferred day",
    "notes_label": "Anything I should know?",
    "opening": "Hi Tori, I would like to book an appointment.",
    "sent": "I will reply to confirm your appointment time.",
    "book_tag": "h2",
    "book_class": "",
}
BOOK_LINK = 'href="/book/" data-scroll="#book"'
STEPS = [
    ("Choose your services", "Add them from the price list. You see the time and the total before you send anything."),
    ("Tell me when you are free", "Pick a day and the time of day that suits you."),
    ("Get your confirmation", "I reply to confirm your appointment time."),
]


def book_form(menu_anchor, overrides=None):
    values = dict(BOOK_DEFAULTS, menu_anchor=menu_anchor)
    values.update(overrides or {})
    return fill(tpl("book.html"), **values)


def catalog_json():
    slim = {k: {"name": v["name"], "price": v["price"], "min": v["min"]} for k, v in CATALOG.items()}
    return json.dumps(slim, ensure_ascii=False, separators=(",", ":"))


def page(meta, main, preloads, jsonld, body_attrs=""):
    return fill(
        tpl("base.html"),
        title=meta["title"],
        description=meta["description"],
        canonical=meta["canonical"],
        og_title=meta.get("og_title", meta["title"]),
        og_image=meta["og_image"],
        preloads=preloads,
        jsonld=json.dumps(jsonld, ensure_ascii=False, indent=2),
        body_attrs=body_attrs,
        header=header(meta.get("path", "")),
        main=main,
        footer=footer(),
        dock=tpl("dock.html"),
        catalog=catalog_json(),
        v=V,
    )


# ---------------------------------------------------------------- home page

def home_menu():
    tabs, panels = [], []
    for i, c in enumerate(CATEGORIES):
        selected = "true" if i == 0 else "false"
        tabindex = "" if i == 0 else ' tabindex="-1"'
        desc = f'<span class="cat__desc">{c["desc"]}</span>' if c["desc"] else ""
        tabs.append(
            f'      <button class="cat" type="button" role="tab" id="tab-{c["id"]}" aria-controls="panel-{c["id"]}" aria-selected="{selected}"{tabindex}>\n'
            + picture(c["img"], "(min-width: 900px) 290px, 46vw", "")
            + f'\n        <span class="cat__body"><span class="cat__name">{c["name"]}</span><span class="cat__from">{desc}{c["from"]}</span></span>\n      </button>'
        )
        panels.append(
            f'      <div class="menu__panel" role="tabpanel" id="panel-{c["id"]}" aria-labelledby="tab-{c["id"]}" tabindex="0">\n'
            f'        <div class="menu__intro">\n          <h3>{c["name"]}</h3>\n          <p>{c["intro"]}</p>{pills(c["links"])}\n        </div>\n'
            f'        <div class="menu__cols">\n{price_groups(c["groups"])}\n        </div>\n      </div>'
        )
    return "\n".join(tabs), "\n\n".join(panels)


def business_jsonld():
    offers = [
        {"@type": "Offer", "price": str(s["price"]), "priceCurrency": "CAD", "itemOffered": {"@type": "Service", "name": s["name"]}}
        for s in CATALOG.values()
    ]
    return {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "@id": URL + "/#business",
        "name": "ToriMed Spa",
        "url": URL + "/",
        "image": URL + "/assets/img/og.jpg",
        "description": "Waxing, brow lamination, lash lifts, facials, microchanneling and gel nails by medical aesthetician Tori Kruse in Fredericton, New Brunswick.",
        "priceRange": "$15 to $300",
        "currenciesAccepted": "CAD",
        "address": {
            "@type": "PostalAddress", "streetAddress": "191 Main Street", "addressLocality": "Fredericton",
            "addressRegion": "NB", "postalCode": "E3A 1E1", "addressCountry": "CA",
        },
        "areaServed": "Fredericton, New Brunswick",
        "sameAs": ["https://www.instagram.com/torimed.spa/"],
        "founder": {"@type": "Person", "name": "Tori Kruse", "jobTitle": "Medical aesthetician"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services and prices", "itemListElement": offers},
    }


def build_home():
    tabs, panels = home_menu()
    main = "\n".join([
        tpl("home_hero.html"),
        tpl("home_feature.html"),
        fill(tpl("home_services.html"), tabs=tabs, panels=panels),
        tpl("home_results.html"),
        tpl("home_about.html"),
        tpl("home_review.html"),
        fill(tpl("home_how.html"), faqs=faq_block(HOME_FAQS)),
        book_form("#services"),
    ])
    preloads = (
        '<link rel="preload" as="image" type="image/avif" media="(max-width: 899px)" imagesrcset="/assets/img/hero-m-520.avif 520w, /assets/img/hero-m-800.avif 800w" imagesizes="100vw" fetchpriority="high">\n'
        '<link rel="preload" as="image" type="image/avif" media="(min-width: 900px)" imagesrcset="/assets/img/hero-760.avif 760w, /assets/img/hero-1160.avif 1160w" imagesizes="56vw" fetchpriority="high">'
    )
    meta = {
        "title": "ToriMed Spa | Waxing, brows, lashes and skin in Fredericton, NB",
        "og_title": "ToriMed Spa | Waxing, brows, lashes and skin in Fredericton",
        "description": "I’m Tori Kruse, a medical aesthetician in Fredericton. Waxing is my specialty, and I also do brow lamination, lash lifts, facials, microchanneling and gel nails. See every price and book an appointment.",
        "canonical": URL + "/",
        "og_image": URL + "/assets/img/og.jpg",
    }
    return page(meta, main, preloads, business_jsonld())


# ---------------------------------------------------------------- service pages

def service_hero(p):
    hero = p["hero"]
    info = IMAGES[hero["img"]]
    facts = "\n".join(f'        <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p["facts"])
    add = f' data-add="{p["primary"]}"' if p["primary"] else ""
    second_label = p.get("second_cta") or ("See results" if p["results"] else "See prices")
    second_href = "#results" if p["results"] else "#prices"
    second = f'<a class="btn btn--ghost" href="{second_href}" data-scroll="{second_href}">{second_label}</a>'
    return (
        f'<section class="hero hero--service" style="--focus: {hero["focus"]}">\n  <div class="hero__photo">\n'
        + picture(hero["img"], "(min-width: 900px) 56vw, 100vw", hero["alt"], lazy=False, indent="    ")
        + '\n  </div>\n  <div class="wrap hero__in">\n    <div class="hero__copy">\n'
        '      <a class="crumb" href="/services/">All services</a>\n'
        f'      <h1 class="hero__title">{p["h1"]}</h1>\n'
        f'      <p class="hero__lede">{p["lede"]}</p>\n'
        f'      <dl class="facts">\n{facts}\n      </dl>\n'
        f'      <div class="hero__actions">\n        <a class="btn btn--blush" {BOOK_LINK}{add}>{p["cta"]}</a>\n        {second}\n      </div>\n'
        "    </div>\n  </div>\n</section>\n"
    ), info


def service_about(p):
    about = p["about"]
    paras = "\n".join(f"      <p>{t}</p>" for t in about["paras"])
    aside = about["aside"]
    if aside["type"] == "checks":
        items = "\n".join(f"        <li>{t}</li>" for t in aside["items"])
        card = f'    <aside class="card">\n      <h3 class="card__title">{aside["heading"]}</h3>\n      <ul class="checks">\n{items}\n      </ul>\n    </aside>'
    else:
        card = (
            f'    <aside class="card">\n      <h3 class="card__title">{aside["heading"]}</h3>\n      <p>{aside["text"]}</p>\n'
            f'      <a class="btn btn--coal btn--block" href="{IG_DM}" target="_blank" rel="noopener">Message @torimed.spa</a>\n    </aside>'
        )
    return (
        '<section class="band band--petal" id="about">\n  <div class="wrap split">\n    <div class="split__text">\n'
        f'      <h2>{about["heading"]}</h2>\n{paras}\n    </div>\n{card}\n  </div>\n</section>\n'
    )


def service_results(p):
    return results_block(p["results"]) if p["results"] else ""


def results_block(r, sid="results"):
    pairs = []
    for pr in r["pairs"]:
        pairs.append(
            '      <figure class="pair">\n        <div class="pair__shots">\n          <div class="pair__shot">\n'
            + picture(pr["before"], "(min-width: 900px) 600px, 92vw", pr["alt_before"], indent="            ")
            + '\n            <span class="tag">Before</span>\n          </div>\n          <div class="pair__shot">\n'
            + picture(pr["after"], "(min-width: 900px) 600px, 92vw", pr["alt_after"], indent="            ")
            + '\n            <span class="tag tag--after">After</span>\n          </div>\n        </div>\n'
            f'        <figcaption>{pr["caption"]}</figcaption>\n      </figure>'
        )
    pairs_html = ""
    if pairs:
        cls = "pairs pairs--single" if len(pairs) == 1 else "pairs"
        pairs_html = f'    <div class="{cls}">\n' + "\n".join(pairs) + "\n    </div>\n"
    tiles = []
    wide = r.get("wide")
    sizes = "(min-width: 900px) 600px, 92vw" if wide else "(min-width: 900px) 290px, 44vw"
    for img, alt, caption in r["tiles"]:
        cap = f"\n        <p>{caption}</p>" if caption else ""
        tiles.append('      <li class="tile">\n' + picture(img, sizes, alt) + cap + "\n      </li>")
    tiles_html = ""
    if tiles:
        cls = "tiles tiles--first" if not pairs else "tiles"
        if wide:
            cls += " tiles--wide"
        tiles_html = f'    <ul class="{cls}">\n' + "\n".join(tiles) + "\n    </ul>\n"
    more = ""
    if r.get("more"):
        label, href = r["more"]
        more = f'    <p class="results__more"><a href="{href}" target="_blank" rel="noopener">{label}</a></p>\n'
    if r.get("links"):
        items = "".join(f'<a class="btn btn--ghost btn--sm" href="{href}">{label}</a>' for label, href in r["links"])
        more += f'    <p class="results__links">{items}</p>\n'
    return (
        f'<section class="band band--coal" id="{sid}">\n  <div class="wrap">\n    <div class="band__head">\n'
        f'      <h2>{r["heading"]}</h2>\n      <p>{r["intro"]}</p>\n    </div>\n{pairs_html}{tiles_html}{more}  </div>\n</section>\n'
    )


def service_prices(p):
    pr = p["prices"]
    if not pr:
        return ""
    return (
        '<section class="band band--petal" id="prices">\n  <div class="wrap">\n    <div class="menu">\n      <div class="menu__panel">\n'
        f'        <div class="menu__intro">\n          <h2 class="menu__title">{pr["heading"]}</h2>\n          <p>{pr["intro"]}</p>{pills(pr["links"])}\n        </div>\n'
        f'        <div class="menu__cols">\n{price_groups(pr["groups"])}\n        </div>\n      </div>\n    </div>\n'
        '    <p class="menu__foot">Prices are in Canadian dollars. Times show how long to set aside. I confirm the final price with your appointment.</p>\n'
        "  </div>\n</section>\n"
    )


def steps_and_questions(faqs, steps=STEPS, heading="How booking works", cta="Book an appointment", link=BOOK_LINK):
    items = "\n".join(
        f"        <li>\n          <h3>{title}</h3>\n          <p>{text}</p>\n        </li>" for title, text in steps
    )
    return fill(tpl("service_how.html"), faqs=faq_block(faqs), steps=items, steps_heading=heading, steps_cta=cta, steps_link=link)


def service_questions(p):
    shared = [f for f in SHARED_FAQS if f[0] not in p.get("skip_shared", [])]
    faqs = p["faqs"] + shared
    html = steps_and_questions(
        faqs, p.get("steps", STEPS), p.get("steps_heading", "How booking works"), p.get("steps_cta", "Book an appointment"),
    )
    return html, faqs


def service_jsonld(p, faqs):
    graph = [
        {
            "@type": "Service",
            "@id": f'{URL}/{p["slug"]}/#service',
            "name": p["h1"],
            "description": p["description"],
            "url": f'{URL}/{p["slug"]}/',
            "provider": {"@id": URL + "/#business"},
            "areaServed": "Fredericton, New Brunswick",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ToriMed Spa", "item": URL + "/"},
                {"@type": "ListItem", "position": 2, "name": p["h1"], "item": f'{URL}/{p["slug"]}/'},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs
            ],
        },
    ]
    if p["primary"]:
        s = CATALOG[p["primary"]]
        graph[0]["offers"] = {"@type": "Offer", "price": str(s["price"]), "priceCurrency": "CAD"}
    return {"@context": "https://schema.org", "@graph": graph}


def build_service(p):
    hero_html, info = service_hero(p)
    questions_html, faqs = service_questions(p)
    main = "\n".join(filter(None, [
        hero_html,
        service_about(p),
        service_results(p),
        quote_band(p["quote"]),
        service_prices(p),
        questions_html,
        book_form("#prices" if p["prices"] else "", p.get("book")),
    ]))
    name = p["hero"]["img"]
    srcset = ", ".join(f"/assets/img/{name}-{w}.avif {w}w" for w in info["widths"])
    preloads = f'<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset}" imagesizes="(min-width: 900px) 56vw, 100vw" fetchpriority="high">'
    meta = {
        "title": p["title"],
        "description": p["description"],
        "canonical": f'{URL}/{p["slug"]}/',
        "og_image": f'{URL}/assets/img/og-{p["slug"]}.jpg',
        "path": f'/{p["slug"]}/',
    }
    attrs = f' data-preselect="{p["primary"]}"' if p["primary"] else ""
    if p.get("service_type"):
        attrs += f' data-service-type="{p["service_type"]}"'
    return page(meta, main, preloads, service_jsonld(p, faqs), attrs)


# ---------------------------------------------------------------- book, services, results, about, questions

MAPS = "https://www.google.com/maps/search/?api=1&amp;query=The+Beauty+Collective%2C+191+Main+Street%2C+Fredericton%2C+NB+E3A+1E1"
BY_SLUG = {p["slug"]: p for p in PAGES}


def pagehead(h1, lede):
    return f'<section class="pagehead">\n  <div class="wrap">\n    <h1>{h1}</h1>\n    <p>{lede}</p>\n  </div>\n</section>\n'


def cta_band():
    return (
        '<section class="cta" aria-labelledby="cta-title">\n  <div class="wrap cta__in">\n'
        '    <h2 id="cta-title">Ready to book?</h2>\n'
        "    <p>Pick your services, tell me when you are free, and I will confirm your time.</p>\n"
        '    <div class="cta__actions">\n      <a class="btn btn--coal" href="/book/">Book an appointment</a>\n'
        '      <a class="btn btn--line" href="/services/">See services and prices</a>\n    </div>\n  </div>\n</section>\n'
    )


def simple_meta(path, title, description):
    return {"title": title, "description": description, "canonical": URL + path, "og_image": URL + "/assets/img/og.jpg", "path": path}


def simple_jsonld(name, path, faqs=None):
    graph = [
        {"@type": "WebPage", "@id": URL + path, "name": name, "url": URL + path, "about": {"@id": URL + "/#business"}},
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ToriMed Spa", "item": URL + "/"},
                {"@type": "ListItem", "position": 2, "name": name, "item": URL + path},
            ],
        },
    ]
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs],
        })
    return {"@context": "https://schema.org", "@graph": graph}


def build_book():
    faqs = BOOKING_FAQS + SHARED_FAQS
    main = "\n".join([
        book_form("", {"book_tag": "h1", "book_class": " book--page"}),
        steps_and_questions(faqs, cta="See services and prices", link='href="/services/"'),
    ])
    meta = simple_meta(
        "/book/", "Book an appointment | ToriMed Spa",
        "Send a booking request to Tori Kruse at ToriMed Spa in Fredericton. Choose your services, pick a day, and get your appointment time confirmed.",
    )
    return page(meta, main, "", simple_jsonld("Book an appointment", "/book/", faqs))


def build_services():
    panels = []
    for c in CATEGORIES:
        panels.append(
            f'      <div class="menu__panel" id="{c["id"]}">\n'
            f'        <div class="menu__intro">\n          <h2>{c["name"]}</h2>\n          <p>{c["intro"]}</p>{pills(c["links"])}\n        </div>\n'
            f'        <div class="menu__cols">\n{price_groups(c["groups"])}\n        </div>\n      </div>'
        )
    makeup = BY_SLUG["makeup"]
    panels.append(
        '      <div class="menu__panel" id="makeup">\n        <div class="menu__intro menu__intro--plain">\n'
        f'          <h2>{makeup["h1"]}</h2>\n          <p>{makeup["lede"]} Priced by quote.</p>'
        + pills([(makeup["nav"], "/makeup/")]) + "\n        </div>\n      </div>"
    )
    main = "\n".join([
        pagehead("Services and prices", "Every service and every price. Add what you want, then send it to me as one booking request."),
        '<section class="band band--petal" id="services">\n  <div class="wrap">\n    <div class="menu menu--all">\n'
        + "\n\n".join(panels)
        + '\n    </div>\n    <p class="menu__foot">Prices are in Canadian dollars. Times show how long to set aside. I confirm the final price with your appointment.</p>\n  </div>\n</section>\n',
        book_form("#services"),
    ])
    meta = simple_meta(
        "/services/", "Services and prices | ToriMed Spa, Fredericton",
        "Every service and price at ToriMed Spa in Fredericton: waxing from $15, brow lamination $95, lash lifts from $100, facials, microchanneling, manicures and pedicures.",
    )
    return page(meta, main, "", simple_jsonld("Services and prices", "/services/"))


def build_results():
    lash, korean, brows, nails, makeup = (
        BY_SLUG[k]["results"] for k in ("lash-lift-and-tint", "korean-lash-lift", "brow-lamination", "manicures-and-pedicures", "makeup")
    )
    groups = [
        ("lashes", {
            "heading": "Lash lifts", "intro": "My clients’ own lashes, before and after. No extensions.",
            "pairs": [lash["pairs"][0], korean["pairs"][0]], "tiles": [],
            "links": [("About the lash lift and tint", "/lash-lift-and-tint/"), ("About the Korean lash lift", "/korean-lash-lift/")],
        }),
        ("brows", {
            "heading": "Brow lamination", "intro": "Lamination, tint and wax in one visit.",
            "pairs": [], "tiles": brows["tiles"], "links": [("About brow lamination", "/brow-lamination/")],
        }),
        ("nails", {
            "heading": "Nails", "intro": "Gel overlay and hand-painted nail art.",
            "pairs": [], "tiles": nails["tiles"], "links": [("About manicures and pedicures", "/manicures-and-pedicures/")],
        }),
        ("makeup", {
            "heading": "Wedding makeup", "intro": makeup["intro"],
            "pairs": [], "wide": True, "tiles": makeup["tiles"][:2], "links": [("About wedding and event makeup", "/makeup/")],
        }),
    ]
    main = "\n".join(
        [pagehead("My work", "Every photo here is one of my own clients, from my Instagram.")]
        + [results_block(r, sid) for sid, r in groups]
        + [cta_band()]
    )
    meta = simple_meta(
        "/results/", "Results: lash lifts, brows, nails and makeup | ToriMed Spa",
        "Real before and after photos from ToriMed Spa in Fredericton: lash lifts, Korean lash lifts, brow lamination, gel nails and wedding makeup by Tori Kruse.",
    )
    return page(meta, main, "", simple_jsonld("My work", "/results/"))


def build_about():
    find_me = (
        '<section class="band band--petal" id="find-me">\n  <div class="wrap">\n    <div class="band__head">\n      <h2>Where to find me</h2>\n    </div>\n'
        '    <div class="cards">\n      <div class="card">\n        <h3 class="card__title">ToriMed Spa</h3>\n'
        "        <address>Inside The Beauty Collective<br>191 Main Street<br>Fredericton, NB E3A 1E1</address>\n        <p>Free parking.</p>\n"
        f'        <a class="btn btn--coal btn--block" href="{MAPS}" target="_blank" rel="noopener">Get directions</a>\n      </div>\n'
        '      <div class="card">\n        <h3 class="card__title">Rather message?</h3>\n        <p>Ask me anything before you book.</p>\n'
        f'        <a class="btn btn--coal btn--block" href="{IG_DM}" target="_blank" rel="noopener">Message @torimed.spa</a>\n      </div>\n    </div>\n  </div>\n</section>\n'
    )
    main = "\n".join([
        pagehead("About me", "Medical aesthetician in Fredericton. Waxing is my specialty."),
        tpl("home_about.html"),
        tpl("home_review.html"),
        find_me,
        cta_band(),
    ])
    meta = simple_meta(
        "/about/", "About Tori Kruse, medical aesthetician | ToriMed Spa",
        "Tori Kruse has been an aesthetician since 2021 and specializes in waxing. Meet her, see her treatment room at The Beauty Collective in Fredericton, and read what clients say.",
    )
    return page(meta, main, "", simple_jsonld("About me", "/about/"))


def build_questions():
    wax, braz = BY_SLUG["waxing"]["faqs"], BY_SLUG["brazilian-wax"]["faqs"]
    waxing = [(q, a.replace(", and the review on this page is from a first wax", "")) for q, a in wax] + [braz[2]]
    groups = [("Booking and visiting", BOOKING_FAQS + SHARED_FAQS, None, None), ("Waxing", waxing, "/waxing/", "waxing")]
    for slug in ("korean-lash-lift", "lash-lift-and-tint", "brow-lamination", "facials", "microchanneling", "manicures-and-pedicures", "makeup"):
        nav = BY_SLUG[slug]["nav"]
        groups.append((nav, BY_SLUG[slug]["faqs"], f"/{slug}/", nav if nav.startswith("Korean") else nav[0].lower() + nav[1:]))
    blocks, every = [], []
    for name, faqs, href, label in groups:
        more = f'\n      <p class="faqgroup__more"><a href="{href}">More about {label}</a></p>' if href else ""
        blocks.append(f'    <div class="faqgroup">\n      <h2>{name}</h2>\n      <div class="faq">\n{faq_block(faqs)}\n      </div>{more}\n    </div>')
        every += faqs
    main = "\n".join([
        pagehead("Questions", "Booking, waxing, lashes, brows, skin, nails and makeup. If yours is not here, message me on Instagram."),
        '<section class="band band--white" id="questions">\n  <div class="wrap faqgroups">\n' + "\n".join(blocks) + "\n  </div>\n</section>\n",
        cta_band(),
    ])
    meta = simple_meta(
        "/questions/", "Questions and answers | ToriMed Spa, Fredericton",
        "Answers about booking, waxing, lash lifts, brow lamination, facials, microchanneling, nails and wedding makeup at ToriMed Spa in Fredericton.",
    )
    return page(meta, main, "", simple_jsonld("Questions", "/questions/", every))


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    for bad in (chr(0x2014), chr(0x2013)):
        if bad in text:
            raise SystemExit(f"{path}: contains a dash character that the house style forbids")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote", path, f"({len(text) // 1024} KB)")


def main():
    write("index.html", build_home())
    urls = [URL + "/"]
    for slug, build in (("book", build_book), ("services", build_services), ("results", build_results), ("about", build_about), ("questions", build_questions)):
        write(f"{slug}/index.html", build())
        urls.append(f"{URL}/{slug}/")
    for p in PAGES:
        write(f'{p["slug"]}/index.html', build_service(p))
        urls.append(f'{URL}/{p["slug"]}/')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sitemap)


if __name__ == "__main__":
    main()
