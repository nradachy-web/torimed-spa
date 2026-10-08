"""Everything the site says: services and prices, the home menu, and one entry per service page.

Written in Tori's voice (first person). Every fact has a source, listed in README.md:
prices and appointment lengths are her own rows in the Vagaro booking data, descriptions come
from her listings and her Instagram captions. Do not add a claim here that she has not made.
"""

SITE = {
    "url": "https://torimed.ca",
    "name": "ToriMed Spa",
    "asset_version": "8",
}

IG = "https://www.instagram.com/torimed.spa/"
IG_DM = "https://ig.me/m/torimed.spa"
WAX_PREP_REEL = "https://www.instagram.com/torimed.spa/reel/DdM8sfKRjlB/"
KOREAN_REEL = "https://www.instagram.com/torimed.spa/reel/DcM_YIFMqN2/"

# id: name, price (CAD), minutes to set aside, optional note. "time": False hides the time where the name already states it.
CATALOG = {
    "brazilian": {"name": "Brazilian wax", "price": 70, "min": 30},
    "brazilian-male": {"name": "Male anatomy Brazilian", "price": 90, "min": 45},
    "bikini": {"name": "Bikini wax", "price": 30, "min": 15, "note": "Bikini line."},
    "full-leg": {"name": "Full leg wax", "price": 72, "min": 30},
    "half-leg": {"name": "Half leg wax", "price": 35, "min": 15, "note": "Lower legs."},
    "underarm": {"name": "Underarm wax", "price": 20, "min": 15},
    "full-arm": {"name": "Full arm wax", "price": 50, "min": 30},
    "half-arm": {"name": "Half arm wax", "price": 25, "min": 30, "note": "Elbow to wrist."},
    "back": {"name": "Back wax", "price": 58, "min": 30},
    "chest": {"name": "Chest wax", "price": 52, "min": 45},
    "full-face": {"name": "Full face wax", "price": 50, "min": 30, "note": "Brows, lip, chin, cheeks and sideburns."},
    "brow-wax": {"name": "Brow wax", "price": 29, "min": 15},
    "lip": {"name": "Lip wax", "price": 15, "min": 15},
    "chin": {"name": "Chin wax", "price": 20, "min": 15},
    "nose": {"name": "Nose wax", "price": 20, "min": 15},
    "sideburn": {"name": "Sideburn wax", "price": 15, "min": 15},
    "brow-lam": {"name": "Brow lamination", "price": 95, "min": 45, "note": "Lamination, tint and wax in one visit."},
    "brow-tint-wax": {"name": "Brow tint and wax", "price": 54, "min": 30, "note": "Tint for depth, then mapping and wax for a clean shape."},
    "brow-lam-lash-lift": {"name": "Brow lamination and lash lift", "price": 209, "min": 105, "note": "Both in one appointment."},
    "lash-lift-tint": {"name": "Lash lift and tint", "price": 100, "min": 60, "note": "Curls your natural lashes upward and tints them black."},
    "korean-lash-lift": {"name": "Korean lash lift", "price": 150, "min": 75, "note": "A gentler lift with a natural-looking curl."},
    "facial-30": {"name": "30 minute facial", "price": 50, "min": 45, "time": False},
    "facial-60": {"name": "60 minute facial", "price": 105, "min": 75, "time": False},
    "dermaplaning": {"name": "Dermaplaning facial", "price": 130, "min": 75, "note": "Removes dead skin and peach fuzz for a smooth finish."},
    "microchanneling": {"name": "Microchanneling", "price": 300, "min": 75, "note": "I use it for fine lines, wrinkles, scarring and acne."},
    "mani-express": {"name": "Express manicure", "price": 35, "min": 45},
    "mani-classic": {"name": "Classic manicure", "price": 42, "min": 45},
    "mani-gel-express": {"name": "Express gel manicure", "price": 55, "min": 75},
    "mani-gel-classic": {"name": "Classic gel manicure", "price": 62, "min": 75, "note": "Shaping, cuticle care, gel polish and a hand massage."},
    "gel-removal": {"name": "Gel polish removal", "price": 20, "min": 15},
    "pedi-express": {"name": "Express pedicure", "price": 45, "min": 75},
    "pedi-classic": {"name": "Classic pedicure", "price": 55, "min": 90},
    "pedi-gel-express": {"name": "Express gel pedicure", "price": 55, "min": 75},
    "pedi-gel-classic": {"name": "Classic gel pedicure", "price": 65, "min": 90, "note": "Foot and nail care, sea salt scrub, gel polish and a foot massage."},
}

BODY_WAX = ["brazilian", "brazilian-male", "bikini", "full-leg", "half-leg", "underarm", "full-arm", "half-arm", "back", "chest"]
FACE_WAX = ["full-face", "brow-wax", "lip", "chin", "nose", "sideburn"]
MANICURES = ["mani-express", "mani-classic", "mani-gel-express", "mani-gel-classic", "gel-removal"]
PEDICURES = ["pedi-express", "pedi-classic", "pedi-gel-express", "pedi-gel-classic"]

# The four tabs on the home page menu.
CATEGORIES = [
    {
        "id": "wax", "name": "Waxing", "img": "cat-wax", "desc": "My specialty. ", "from": "From $15",
        "intro": "Full body and face. Waxing is my specialty, and I keep every appointment fast.",
        "groups": [("Body", BODY_WAX), ("Face", FACE_WAX)],
        "links": [("Brazilian wax", "/brazilian-wax/"), ("All about waxing", "/waxing/")],
    },
    {
        "id": "brows", "name": "Brows and lashes", "img": "cat-lashes", "desc": "Lamination and lifts. ", "from": "From $54",
        "intro": "Brow lamination lasts 4 to 6 weeks. A Korean lash lift lasts 6 to 8.",
        "groups": [("Brows", ["brow-lam", "brow-tint-wax", "brow-lam-lash-lift"]), ("Lashes", ["lash-lift-tint", "korean-lash-lift"])],
        "links": [("Korean lash lift", "/korean-lash-lift/"), ("Lash lift and tint", "/lash-lift-and-tint/"), ("Brow lamination", "/brow-lamination/")],
    },
    {
        "id": "skin", "name": "Skin", "img": "cat-skin", "desc": "Facials and microchanneling. ", "from": "From $50",
        "intro": "Facials, dermaplaning and microchanneling in my treatment room.",
        "groups": [("Facials", ["facial-30", "facial-60", "dermaplaning"]), ("Advanced", ["microchanneling"])],
        "links": [("Facials", "/facials/"), ("Microchanneling", "/microchanneling/")],
    },
    {
        "id": "nails", "name": "Nails", "img": "cat-nails", "desc": "", "from": "Manicures from $35",
        "intro": "Gel and classic, hands and feet. For gel overlay or nail art, mention it in your request.",
        "groups": [("Manicures", MANICURES), ("Pedicures", PEDICURES)],
        "links": [("Manicures and pedicures", "/manicures-and-pedicures/")],
    },
]

EMILY = {
    "quote": "I got a wax for the first time today and Tori’s room along with Tori herself made my first time super comfortable.",
    "who": "Emily M.",
    "detail": "First-time waxing client. Reviewed on Vagaro, April 2026.",
}
COLLECTIVE = {
    "quote": "She brings incredible talent and the best energy everyday, we truly can’t get enough of her. Be sure to prebook your appointments, she’s a busy girl!",
    "who": "The Beauty Collective",
    "detail": "Welcoming me to the studio, April 2026.",
}

# Appended to the questions on every service page.
SHARED_FAQS = [
    ("Where are you located?", "I’m inside The Beauty Collective at 191 Main Street, Fredericton, NB E3A 1E1. Parking is free."),
    ("What if I need to cancel?", "Please give at least 24 hours’ notice to cancel or reschedule. Later cancellations may be charged 50% of the appointment price."),
]

ASK = {
    "type": "ask",
    "heading": "Not sure what to book?",
    "text": "Message me on Instagram and I will help you choose.",
}

PAGES = [
    {
        "slug": "korean-lash-lift",
        "nav": "Korean lash lift",
        "title": "Korean lash lift in Fredericton | ToriMed Spa",
        "description": "A gentler lash lift with a natural-looking curl that lasts 6 to 8 weeks. $150 with Tori Kruse at ToriMed Spa in Fredericton. See real results and book.",
        "h1": "Korean lash lift",
        "lede": "A gentler lift that curls your own lashes into a soft, natural shape. No extensions, and it lasts 6 to 8 weeks.",
        "primary": "korean-lash-lift",
        "cta": "Book a Korean lash lift",
        "facts": [("Price", "$150"), ("Appointment", "1 h 15 min"), ("Lasts", "6 to 8 weeks")],
        "hero": {"img": "svc-korean", "alt": "Close view of a client’s lifted lashes and laminated brow after a Korean lash lift", "focus": "42% 46%"},
        "about": {
            "heading": "What a Korean lash lift is",
            "paras": [
                "A Korean lash lift is a gentler alternative to a traditional lash lift. It curls your natural lashes upward into a soft, natural-looking shape, so your eyes look brighter and more open.",
                "It is made to be kind to your lashes, helping keep them healthy while the lift holds. The result is low maintenance and lasts 6 to 8 weeks.",
            ],
            "aside": {"type": "checks", "heading": "It suits you if", "items": [
                "You want a natural-looking curl",
                "You want to look after your own lashes",
                "You want low maintenance lashes for weeks",
                "You do not want extensions",
            ]},
        },
        "results": {
            "heading": "Real results",
            "intro": "One of my own clients, before and after the same appointment.",
            "pairs": [{
                "before": "ba-combo-before", "after": "ba-combo-after",
                "alt_before": "Client’s brows and lashes before a Korean lash lift and brow lamination",
                "alt_after": "The same client with lifted lashes and laminated brows",
                "caption": "<strong>Korean lash lift with brow lamination.</strong> My favourite combination. The lift lasts about 8 weeks and the lamination 4 to 6.",
            }],
            "tiles": [],
            "more": ("Watch a Korean lash lift before and after on Instagram", KOREAN_REEL),
        },
        "quote": COLLECTIVE,
        "prices": {
            "heading": "Price and add-ons",
            "intro": "Add what you want and send it as one booking request. You see the total before you send anything.",
            "groups": [("Korean lash lift", ["korean-lash-lift"]), ("Goes well with", ["brow-lam", "brow-tint-wax"])],
            "links": [("Lash lift and tint, the classic option", "/lash-lift-and-tint/"), ("Brow lamination", "/brow-lamination/")],
        },
        "faqs": [
            ("How long does a Korean lash lift last?", "6 to 8 weeks."),
            ("How is it different from a regular lash lift?", "It is a gentler alternative to a traditional lash lift, with a natural-looking curl, and it helps keep your natural lashes healthy. I also offer a classic <a href=\"/lash-lift-and-tint/\">lash lift and tint</a> for $100."),
            ("Are they my real lashes?", "Yes. A lash lift works on your own natural lashes. There are no extensions."),
            ("How long is the appointment?", "Set aside 1 hour 15 minutes."),
            ("Can I have my brows done in the same visit?", "Yes. A Korean lash lift with brow lamination is my favourite combination. Brow lamination is $95 and takes 45 minutes. Add both to your booking request."),
        ],
    },
    {
        "slug": "lash-lift-and-tint",
        "nav": "Lash lift and tint",
        "title": "Lash lift and tint in Fredericton | ToriMed Spa",
        "description": "Your own lashes curled upward and tinted black for a longer, fuller look without mascara. $100 with Tori Kruse at ToriMed Spa in Fredericton.",
        "h1": "Lash lift and tint",
        "lede": "Your own lashes, curled upward and tinted black for a longer, fuller look without mascara.",
        "primary": "lash-lift-tint",
        "cta": "Book a lash lift and tint",
        "facts": [("Price", "$100"), ("Appointment", "1 hour"), ("Includes", "Black tint")],
        "hero": {"img": "svc-lashlift", "alt": "Close view of a client’s eye with lifted, curled lashes after a lash lift", "focus": "50% 50%"},
        "about": {
            "heading": "What a lash lift and tint does",
            "paras": [
                "A lash lift curls your natural lashes upward, and the black tint darkens them, so they look longer and fuller.",
                "The results are long lasting, and you get defined lashes without needing mascara. It makes getting ready in the morning a lot quicker.",
            ],
            "aside": {"type": "checks", "heading": "It suits you if", "items": [
                "You want longer, fuller looking lashes",
                "You want to skip mascara",
                "You want your own lashes, not extensions",
            ]},
        },
        "results": {
            "heading": "Real results",
            "intro": "My own clients, before and after.",
            "pairs": [
                {
                    "before": "ba-lash-before", "after": "ba-lash-after",
                    "alt_before": "Client’s natural lashes before a lash lift",
                    "alt_after": "The same client’s lashes lifted and curled after a lash lift",
                    "caption": "<strong>Lash lift.</strong> My client’s own lashes, lifted and curled. No extensions.",
                },
                {
                    "before": "ba-lash2-before", "after": "ba-lash2-after",
                    "alt_before": "A second view of a client’s natural lashes before a lash lift",
                    "alt_after": "A second view of lifted, curled lashes after a lash lift",
                    "caption": "<strong>Lash lift.</strong> Before and after.",
                },
            ],
            "tiles": [],
            "more": ("More lash lifts on Instagram @torimed.spa", IG),
        },
        "quote": COLLECTIVE,
        "prices": {
            "heading": "Price and add-ons",
            "intro": "Add what you want and send it as one booking request. You see the total before you send anything.",
            "groups": [("Lash lift and tint", ["lash-lift-tint"]), ("Goes well with", ["brow-lam-lash-lift", "brow-lam"])],
            "links": [("Korean lash lift, the gentler option", "/korean-lash-lift/"), ("Brow lamination", "/brow-lamination/")],
        },
        "faqs": [
            ("Does it include a tint?", "Yes. A black tint is included in the $100."),
            ("Are they my real lashes?", "Yes. A lash lift works on your own natural lashes. There are no extensions."),
            ("How long is the appointment?", "Set aside 1 hour."),
            ("What is the difference between this and a Korean lash lift?", "The <a href=\"/korean-lash-lift/\">Korean lash lift</a> is a gentler alternative with a natural-looking curl. It lasts 6 to 8 weeks and is $150."),
            ("Can I add brow lamination?", "Yes. Brow lamination and a lash lift together are $209, in one appointment of 1 hour 45 minutes."),
        ],
    },
    {
        "slug": "brow-lamination",
        "nav": "Brow lamination",
        "title": "Brow lamination in Fredericton | ToriMed Spa",
        "description": "Fuller, lifted brows that stay put. Lamination, tint and wax for $95, lasting 4 to 6 weeks, with Tori Kruse at ToriMed Spa in Fredericton.",
        "h1": "Brow lamination",
        "lede": "Fuller, lifted brows that stay put. Lamination, tint and wax in one visit, lasting 4 to 6 weeks.",
        "primary": "brow-lam",
        "cta": "Book a brow lamination",
        "facts": [("Price", "$95"), ("Appointment", "45 min"), ("Lasts", "4 to 6 weeks")],
        "hero": {"img": "svc-browlam", "alt": "Close view of a client’s full, brushed-up brow after lamination", "focus": "50% 45%"},
        "about": {
            "heading": "What brow lamination does",
            "paras": [
                "Brow lamination sets your brow hairs into a full, feathery shape that stays put. It is a three step treatment that relaxes the hairs, hides sparse areas and creates volume.",
                "At my appointments it comes with a tint and a wax, all for $95, so you leave with brows that are shaped, defined and easy to style every day.",
            ],
            "aside": {"type": "checks", "heading": "It suits you if", "items": [
                "Your brow hairs grow downward",
                "Your brows are unruly or coarse",
                "You have sparse areas you want to look fuller",
                "You want to spend less time styling them",
            ]},
        },
        "results": {
            "heading": "Real results",
            "intro": "Brow lamination on my own clients.",
            "pairs": [],
            "tiles": [
                ("g-brows", "A client’s brow after lamination, brushed up and defined", ""),
                ("g-brows-2", "Close view of a laminated brow with a clean waxed shape", ""),
                ("g-brows-3", "A client’s laminated and tinted brow seen from the side", ""),
                ("g-brows-4", "Close view of a full laminated brow", ""),
            ],
            "more": ("See how to style laminated brows on Instagram @torimed.spa", IG),
        },
        "quote": COLLECTIVE,
        "prices": {
            "heading": "Brow prices",
            "intro": "Add what you want and send it as one booking request. You see the total before you send anything.",
            "groups": [("Brows", ["brow-lam", "brow-lam-lash-lift", "brow-tint-wax", "brow-wax"]), ("Goes well with", ["korean-lash-lift", "lash-lift-tint"])],
            "links": [("Korean lash lift", "/korean-lash-lift/"), ("Lash lift and tint", "/lash-lift-and-tint/")],
        },
        "faqs": [
            ("How long does brow lamination last?", "4 to 6 weeks."),
            ("What is included?", "Lamination, a tint and a wax, all for $95."),
            ("How long is the appointment?", "Set aside 45 minutes."),
            ("Can I style my brows different ways afterwards?", "Yes. Laminated brows can be brushed into different looks. I post styling examples on <a href=\"" + IG + "\" target=\"_blank\" rel=\"noopener\">my Instagram</a>."),
            ("Can I get my lashes done in the same visit?", "Yes. Brow lamination and a lash lift together are $209. You can also add a <a href=\"/korean-lash-lift/\">Korean lash lift</a>, which is my favourite combination."),
        ],
    },
    {
        "slug": "brazilian-wax",
        "nav": "Brazilian wax",
        "title": "Brazilian wax in Fredericton | ToriMed Spa",
        "description": "Quick, comfortable Brazilian waxing with Tori Kruse, a waxing specialist in Fredericton. $70, about 30 minutes. First-time clients welcome.",
        "h1": "Brazilian wax",
        "lede": "Quick, comfortable Brazilian waxing in my own treatment room. First-time clients are welcome.",
        "primary": "brazilian",
        "cta": "Book a Brazilian wax",
        "facts": [("Brazilian", "$70"), ("Male anatomy", "$90"), ("Bikini line", "$30")],
        "hero": {"img": "room", "alt": "My treatment room: wax warmers on the counter, white cabinets and a treatment bed", "focus": "78% 60%"},
        "about": {
            "heading": "Waxing is my specialty",
            "paras": [
                "I have been an aesthetician since 2021, and waxing is what I specialize in. I keep every appointment fast and efficient, and a Brazilian is booked for 30 minutes.",
                "If this is your first one, that is completely fine. Message me on Instagram with any question before you book.",
            ],
            "aside": {"type": "checks", "heading": "Good to know", "items": [
                "A 30 minute appointment",
                "First-time clients welcome",
                "Male anatomy Brazilian available",
                "Free parking at 191 Main Street",
            ]},
        },
        "results": None,
        "quote": EMILY,
        "prices": {
            "heading": "Brazilian and bikini prices",
            "intro": "Add what you want and send it as one booking request. You see the total before you send anything.",
            "groups": [("Brazilian and bikini", ["brazilian", "brazilian-male", "bikini"]), ("Add to your visit", ["underarm", "full-leg", "half-leg"])],
            "links": [("All waxing prices", "/waxing/")],
        },
        "faqs": [
            ("I have never had a Brazilian before. Is that okay?", "Yes. First-time clients are welcome, and the review on this page is from a first wax. Message me on Instagram with any question before you book."),
            ("How should I prepare?", "I made a short video on exactly this. <a href=\"" + WAX_PREP_REEL + "\" target=\"_blank\" rel=\"noopener\">Watch “How to prepare for your waxing appointment” on Instagram.</a>"),
            ("How long does it take?", "A Brazilian is a 30 minute appointment. A male anatomy Brazilian is 45 minutes."),
            ("Do you wax men?", "Yes. A male anatomy Brazilian is $90, and I also do back and chest waxing."),
        ],
    },
    {
        "slug": "waxing",
        "nav": "Waxing",
        "title": "Waxing in Fredericton, body and face | ToriMed Spa",
        "description": "Full body and face waxing with Tori Kruse, a waxing specialist in Fredericton. Every price listed, from $15. First-time clients and men welcome.",
        "h1": "Waxing",
        "lede": "Full body and face waxing, done fast. Waxing is my specialty.",
        "primary": None,
        "cta": "Book a wax",
        "facts": [("From", "$15"), ("Appointments", "15 to 45 min"), ("Aesthetician since", "2021")],
        "hero": {"img": "hero", "alt": "Tori Kruse, medical aesthetician and owner of ToriMed Spa", "focus": "50% 0"},
        "about": {
            "heading": "Fast, comfortable waxing",
            "paras": [
                "Waxing is my specialty. I do full body and face waxing, and I keep every appointment fast and efficient.",
                "Every price is listed below, so you know the cost before you book. Add as many areas as you like and send them as one request.",
            ],
            "aside": {"type": "checks", "heading": "What I wax", "items": [
                "Body: legs, arms, underarms, back, chest, bikini and Brazilian",
                "Face: brows, lip, chin, nose, sideburns or full face",
                "First-time clients welcome",
                "Men welcome",
            ]},
        },
        "results": None,
        "quote": EMILY,
        "prices": {
            "heading": "Waxing prices",
            "intro": "Add each area you want and send them as one booking request. You see the total and the time before you send anything.",
            "groups": [("Body", BODY_WAX), ("Face", FACE_WAX)],
            "links": [("More about Brazilian waxing", "/brazilian-wax/")],
        },
        "faqs": [
            ("How should I prepare for a wax?", "I made a short video on exactly this. <a href=\"" + WAX_PREP_REEL + "\" target=\"_blank\" rel=\"noopener\">Watch “How to prepare for your waxing appointment” on Instagram.</a>"),
            ("I have never been waxed before. Is that okay?", "Yes. First-time clients are welcome, and the review on this page is from a first wax. Message me on Instagram with any question before you book."),
            ("Do you wax men?", "Yes. My menu includes back, chest and male anatomy Brazilian waxing."),
            ("Can I book more than one area?", "Yes. Add each area from the price list and send them as one request."),
        ],
    },
    {
        "slug": "facials",
        "nav": "Facials",
        "title": "Facials and dermaplaning in Fredericton | ToriMed Spa",
        "description": "30 and 60 minute facials and dermaplaning with Tori Kruse, a medical aesthetician in Fredericton. From $50. See prices and book.",
        "h1": "Facials",
        "lede": "A facial in my treatment room, in 30 or 60 minutes, with dermaplaning when you want an extra smooth finish.",
        "primary": None,
        "cta": "Book a facial",
        "facts": [("30 minutes", "$50"), ("60 minutes", "$105"), ("Dermaplaning", "$130")],
        "hero": {"img": "room", "alt": "My treatment room: a round mirror with pink flowers, white cabinets and a treatment bed", "focus": "22% 40%"},
        "about": {
            "heading": "Choose your facial",
            "paras": [
                "I offer a 30 minute facial for $50 and a 60 minute facial for $105.",
                "The dermaplaning facial is $130. Dermaplaning removes dead skin and peach fuzz from the surface of your face, which leaves your skin smooth.",
            ],
            "aside": ASK,
        },
        "results": None,
        "quote": COLLECTIVE,
        "prices": {
            "heading": "Facial prices",
            "intro": "Add what you want and send it as one booking request. You see the total before you send anything.",
            "groups": [("Facials", ["facial-30", "facial-60", "dermaplaning"]), ("Advanced", ["microchanneling"])],
            "links": [("More about microchanneling", "/microchanneling/")],
        },
        "faqs": [
            ("Which facial should I book?", "If you are not sure, message me on Instagram and I will help you choose."),
            ("What is dermaplaning?", "Dermaplaning removes dead skin and peach fuzz from the surface of your face, which leaves your skin smooth."),
            ("How long are the appointments?", "Set aside 45 minutes for the 30 minute facial, and 1 hour 15 minutes for the 60 minute facial or the dermaplaning facial."),
        ],
    },
    {
        "slug": "microchanneling",
        "nav": "Microchanneling",
        "title": "Microchanneling in Fredericton | ToriMed Spa",
        "description": "Microchanneling with Tori Kruse, a medical aesthetician in Fredericton, for fine lines, wrinkles, scarring and acne. $300. See details and book.",
        "h1": "Microchanneling",
        "lede": "A skin treatment I use for fine lines, wrinkles, scarring and acne.",
        "primary": "microchanneling",
        "cta": "Book microchanneling",
        "facts": [("Price", "$300"), ("Appointment", "1 h 15 min")],
        "hero": {"img": "room", "alt": "My treatment room: a round mirror with pink flowers, white cabinets and a treatment bed", "focus": "30% 50%"},
        "about": {
            "heading": "What microchanneling is",
            "paras": [
                "Microchanneling makes very fine channels in the surface of the skin, which prompts the skin to renew itself.",
                "I use it to work on fine lines, wrinkles, scarring and acne.",
            ],
            "aside": {"type": "ask", "heading": "Not sure it is right for you?", "text": "Message me on Instagram first and we can talk it through."},
        },
        "results": None,
        "quote": COLLECTIVE,
        "prices": {
            "heading": "Price",
            "intro": "Add it to your visit and send your booking request. You see the total before you send anything.",
            "groups": [("Microchanneling", ["microchanneling"]), ("Facials", ["facial-30", "facial-60", "dermaplaning"])],
            "links": [("More about facials", "/facials/")],
        },
        "faqs": [
            ("What do you use microchanneling for?", "Fine lines, wrinkles, scarring and acne."),
            ("How long is the appointment?", "Set aside 1 hour 15 minutes."),
            ("Is it right for my skin?", "Message me on Instagram before you book and we can talk it through."),
        ],
    },
    {
        "slug": "manicures-and-pedicures",
        "nav": "Manicures and pedicures",
        "title": "Gel manicures and pedicures in Fredericton | ToriMed Spa",
        "description": "Gel and classic manicures and pedicures with Tori Kruse at ToriMed Spa in Fredericton, plus gel overlay and hand-painted nail art. Manicures from $35.",
        "h1": "Manicures and pedicures",
        "lede": "Gel and classic manicures and pedicures, with gel overlay and hand-painted nail art by request.",
        "primary": None,
        "cta": "Book your nails",
        "facts": [("Manicures", "From $35"), ("Pedicures", "From $45"), ("Nail art", "By request")],
        "hero": {"img": "svc-nails", "alt": "A client’s hands with blue cat eye gel nails", "focus": "50% 45%"},
        "about": {
            "heading": "Hands and feet",
            "paras": [
                "I do express and classic manicures and pedicures, with regular polish or gel.",
                "A classic gel manicure includes shaping, cuticle care, gel polish and a hand massage. A classic gel pedicure includes foot and nail care, a sea salt scrub, gel polish and a foot massage.",
                "I also do gel overlay and hand-painted nail art. Mention it in your request and I will confirm the price.",
            ],
            "aside": {"type": "checks", "heading": "Gel overlay is a good choice if", "items": [
                "Your nails keep breaking with gel polish alone",
                "Your nails are not as strong as you would like",
                "You want more stability",
            ]},
        },
        "results": {
            "heading": "Recent sets",
            "intro": "Gel overlay and nail art on my own clients.",
            "pairs": [],
            "tiles": [
                ("g-cat-eye", "Blue cat eye gel nails with a marble look", "Cat eye gel overlay"),
                ("cat-nails", "A second view of blue cat eye gel nails", "Cat eye gel overlay"),
                ("g-nail-art", "Purple and black gel nails with hand-painted ghosts and stars", "Hand-painted nail art"),
                ("g-nail-art-2", "Close view of two nails painted with stars, a moon and ghosts", "Hand-painted nail art"),
            ],
            "more": ("More nails on Instagram @torimed.spa", IG),
        },
        "quote": COLLECTIVE,
        "prices": {
            "heading": "Nail prices",
            "intro": "Add what you want and send it as one booking request. You see the total before you send anything.",
            "groups": [("Manicures", MANICURES), ("Pedicures", PEDICURES)],
            "links": [],
        },
        "faqs": [
            ("What is a gel overlay, and is it for me?", "Gel overlay is a good choice if your nails keep breaking with gel polish alone, if your nails are not as strong as you would like, or if you just want more stability."),
            ("How much is gel overlay or nail art?", "Mention it in your booking request and I will confirm the price."),
            ("Can I book a manicure and a pedicure together?", "Yes. Add both and send them as one request."),
            ("Do you remove gel polish?", "Yes. Gel polish removal is $20."),
        ],
    },
    {
        "slug": "makeup",
        "nav": "Wedding and event makeup",
        "title": "Bridal and event makeup in Fredericton | ToriMed Spa",
        "description": "Professional makeup for brides, bridal parties and events with Tori Kruse in Fredericton. 2027 wedding dates open. Send your date for availability and a price.",
        "h1": "Wedding and event makeup",
        "lede": "Professional makeup for brides, bridal parties and events. I still have 2027 wedding dates open.",
        "primary": None,
        "service_type": "Wedding makeup",
        "cta": "Ask about your date",
        "second_cta": "See my work",
        "facts": [("Weddings", "2027 dates open"), ("Bridal parties", "Welcome"), ("Pricing", "By quote")],
        "hero": {"img": "svc-makeup", "alt": "Tori applying a bride’s makeup, seen through a ring light", "focus": "62% 40%"},
        "about": {
            "heading": "Makeup for your big day",
            "paras": [
                "It is always such an honour, and so much fun, to be part of your big day. I do makeup for brides and their bridal parties, and for other events too.",
                "Every wedding and event is different, so I price each one individually. Send me your date and a few details, and I will reply with my availability and a price.",
            ],
            "aside": {"type": "checks", "heading": "To get a price, tell me", "items": [
                "Your date",
                "Where you are getting ready",
                "How many people need makeup",
                "The look you have in mind",
            ]},
        },
        "results": {
            "heading": "Recent work",
            "intro": "A wedding from October 2026. I did the makeup for this bride and her bridal party, working alongside another artist.",
            "pairs": [],
            "wide": True,
            "tiles": [
                ("g-wed-bride", "The bride outdoors in her veil, smiling, with her makeup finished", "The bride"),
                ("g-wed-robes", "The bride and her bridal party in robes with their makeup done", "Her bridal party, ready"),
                ("g-wed-work", "Tori applying the bride’s makeup beside a ring light", "Makeup in progress"),
                ("g-wed-party", "The bride and five bridesmaids outdoors, holding her bouquet together", "The whole party"),
            ],
            "more": ("More of my work on Instagram @torimed.spa", IG),
        },
        "quote": COLLECTIVE,
        "prices": None,
        "steps_heading": "How it works",
        "steps": [
            ("Send me your date", "Tell me when it is and where you are getting ready."),
            ("Tell me about your group", "How many people need makeup, and the look you have in mind."),
            ("Get my reply", "I reply with my availability and a price."),
        ],
        "steps_cta": "Ask about your date",
        "skip_shared": ["Where are you located?", "What if I need to cancel?"],
        "book": {
            "book_heading": "Ask about your date",
            "book_lede": "Send your date and a few details, and I will reply with my availability and a price.",
            "when_legend": "When is it?",
            "day_label": "Event date",
            "notes_label": "Where you are getting ready, how many people, and the look you want",
            "opening": "Hi Tori, I would like to ask about makeup for my date.",
        },
        "faqs": [
            ("Do you do makeup for the whole bridal party?", "Yes. I do makeup for brides and their bridal parties."),
            ("Do you have dates open?", "I still have openings for 2027. Send me your date and I will let you know."),
            ("Do you do makeup for events that are not weddings?", "Yes. Send me the date and tell me what the event is."),
            ("How much does it cost?", "Every wedding and event is different, so I price each one individually. Send me your date, where you are getting ready and how many people need makeup, and I will reply with a price."),
        ],
    },
]
