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

from content import CATALOG, CATEGORIES, IG_DM, PAGES, SHARED_FAQS, SITE  # noqa: E402

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


def header():
    services = "\n".join(f'          <a href="/{p["slug"]}/">{p["nav"]}</a>' for p in PAGES)
    return fill(tpl("header.html"), services=services)


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
        header=header(),
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
        tpl("home_how.html"),
        fill(tpl("book.html"), menu_anchor="#services"),
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
    second = '<a class="btn btn--ghost" href="#results">See results</a>' if p["results"] else '<a class="btn btn--ghost" href="#prices">See prices</a>'
    return (
        f'<section class="hero hero--service" style="--focus: {hero["focus"]}">\n  <div class="hero__photo">\n'
        + picture(hero["img"], "(min-width: 900px) 56vw, 100vw", hero["alt"], lazy=False, indent="    ")
        + '\n  </div>\n  <div class="wrap hero__in">\n    <div class="hero__copy">\n'
        '      <a class="crumb" href="/#services">All services</a>\n'
        f'      <h1 class="hero__title">{p["h1"]}</h1>\n'
        f'      <p class="hero__lede">{p["lede"]}</p>\n'
        f'      <dl class="facts">\n{facts}\n      </dl>\n'
        f'      <div class="hero__actions">\n        <a class="btn btn--blush" href="#book"{add}>{p["cta"]}</a>\n        {second}\n      </div>\n'
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
    r = p["results"]
    if not r:
        return ""
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
    for img, alt, caption in r["tiles"]:
        cap = f"\n        <p>{caption}</p>" if caption else ""
        tiles.append('      <li class="tile">\n' + picture(img, "(min-width: 900px) 290px, 44vw", alt) + cap + "\n      </li>")
    tiles_html = ""
    if tiles:
        cls = "tiles tiles--first" if not pairs else "tiles"
        tiles_html = f'    <ul class="{cls}">\n' + "\n".join(tiles) + "\n    </ul>\n"
    more = ""
    if r.get("more"):
        label, href = r["more"]
        more = f'    <p class="results__more"><a href="{href}" target="_blank" rel="noopener">{label}</a></p>\n'
    return (
        '<section class="band band--coal" id="results">\n  <div class="wrap">\n    <div class="band__head">\n'
        f'      <h2>{r["heading"]}</h2>\n      <p>{r["intro"]}</p>\n    </div>\n{pairs_html}{tiles_html}{more}  </div>\n</section>\n'
    )


def service_prices(p):
    pr = p["prices"]
    return (
        '<section class="band band--petal" id="prices">\n  <div class="wrap">\n    <div class="menu">\n      <div class="menu__panel">\n'
        f'        <div class="menu__intro">\n          <h2 class="menu__title">{pr["heading"]}</h2>\n          <p>{pr["intro"]}</p>{pills(pr["links"])}\n        </div>\n'
        f'        <div class="menu__cols">\n{price_groups(pr["groups"])}\n        </div>\n      </div>\n    </div>\n'
        '    <p class="menu__foot">Prices are in Canadian dollars. Times show how long to set aside. I confirm the final price with your appointment.</p>\n'
        "  </div>\n</section>\n"
    )


def service_questions(p):
    faqs = p["faqs"] + SHARED_FAQS
    return fill(tpl("service_how.html"), faqs=faq_block(faqs)), faqs


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
        fill(tpl("book.html"), menu_anchor="#prices"),
    ]))
    name = p["hero"]["img"]
    srcset = ", ".join(f"/assets/img/{name}-{w}.avif {w}w" for w in info["widths"])
    preloads = f'<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset}" imagesizes="(min-width: 900px) 56vw, 100vw" fetchpriority="high">'
    meta = {
        "title": p["title"],
        "description": p["description"],
        "canonical": f'{URL}/{p["slug"]}/',
        "og_image": f'{URL}/assets/img/og-{p["slug"]}.jpg',
    }
    attrs = f' data-preselect="{p["primary"]}"' if p["primary"] else ""
    return page(meta, main, preloads, service_jsonld(p, faqs), attrs)


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    for bad in ("—", "–"):
        if bad in text:
            raise SystemExit(f"{path}: contains a dash character that the house style forbids")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote", path, f"({len(text) // 1024} KB)")


def main():
    write("index.html", build_home())
    urls = [URL + "/"]
    for p in PAGES:
        write(f'{p["slug"]}/index.html', build_service(p))
        urls.append(f'{URL}/{p["slug"]}/')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sitemap)


if __name__ == "__main__":
    main()
