"""Cut and encode the site photos from the originals in _source/ig.

Run from anywhere:  python3 -I scripts/build_images.py <source_dir> <out_dir> [name ...]
With names after the two folders, only the cuts whose name starts with one of them are made
(for example "g-mu" "ba-brow"), so adding photos does not re-encode the rest.
Every photo is Tori's own: from her Instagram posts, or texted by her (see README.md).
"""
import os
import sys
from PIL import Image, ImageFilter, ImageOps

src_dir, out_dir = sys.argv[1], sys.argv[2]
only = sys.argv[3:]
os.makedirs(out_dir, exist_ok=True)


def wanted(name):
    return not only or any(name.startswith(prefix) for prefix in only)


# name: (source file, crop box as fractions x0 y0 x1 y1, output widths)
JOBS = {
    "room": ("intro-1.jpg", (0, 0, 1, 1), [1200, 760]),
    "cat-wax": ("intro-1.jpg", (0.44, 0.30, 1.0, 1.0), [800, 480]),
    "cat-skin": ("intro-1.jpg", (0.0, 0.08, 0.56, 0.78), [800, 480]),
    "cat-lashes": ("lashbrow-combo-0.jpg", (0.02, 0.02, 0.96, 0.98), [800, 480]),
    "cat-nails": ("nails-cateye-1.jpg", (0.10, 0, 0.90, 1), [800, 480]),
    "g-brows": ("browlam-a-1.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    "g-nail-art": ("nails-halloween-0.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    "g-cat-eye": ("nails-cateye-0.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    "g-bridal": ("bridal-0.jpg", (0.20, 0, 0.833, 1), [540, 400]),
    # Service page heroes and extra result tiles.
    "svc-korean": ("lashbrow-combo-0.jpg", (0.02, 0.02, 0.96, 0.98), [1200, 760]),
    "svc-browlam": ("browlam-b-0.jpg", (0.08, 0, 0.92, 1), [1200, 760]),
    "svc-nails": ("nails-cateye-1.jpg", (0.08, 0, 0.92, 1), [1200, 760]),
    "g-brows-2": ("browlam-a-0.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    "g-brows-3": ("browlam-b-1.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    "g-brows-4": ("browlam-b-0.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    "g-nail-art-2": ("nails-halloween-1.jpg", (0.10, 0, 0.90, 1), [640, 400]),
    # Wedding makeup. The originals are small (about 850 px wide), so these stay at full size.
    "svc-makeup": ("bridal-0.jpg", (0, 0, 1, 1), [853, 600]),
    "g-wed-bride": ("wedding-2.jpg", (0, 0, 1, 1), [1080, 600]),
    "g-wed-robes": ("wedding-10.jpg", (0, 0, 1, 1), [853, 600]),
    "g-wed-work": ("wedding-3.jpg", (0, 0, 1, 1), [853, 600]),
    "g-wed-party": ("wedding-11.jpg", (0, 0, 1, 1), [853, 600]),
}

# Stacked before and after posts, split on the white divider (pixel rows measured on the originals).
PIXEL_JOBS = {
    "ba-lash-before": ("lashlift-0.jpg", (13, 13, 2566, 1605), [900, 520]),
    "ba-lash-after": ("lashlift-0.jpg", (13, 1618, 2566, 3212), [900, 520]),
    "ba-combo-before": ("lashbrow-combo-1.jpg", (10, 0, 2400, 1593), [900, 520]),
    "ba-combo-after": ("lashbrow-combo-1.jpg", (10, 1603, 2400, 3052), [900, 520]),
    "ba-lash2-before": ("lashlift-1.jpg", (22, 22, 2556, 1600), [900, 520]),
    "ba-lash2-after": ("lashlift-1.jpg", (22, 1623, 2556, 3202), [900, 520]),
    "svc-lashlift": ("lashlift-0.jpg", (425, 1618, 1725, 3212), [1200, 760]),
}


# Photos Tori texted on October 13, 2026, kept beside the Instagram folder.
texted_dir = os.path.join(src_dir, "..", "tori-2026-10-13")

# name: (source file, centre x, centre y, width as a fraction of the photo, quarter turns, output widths).
# Each is cut to 4:5 around the face or the hands, which also keeps the room behind out of the frame.
FOCUS_JOBS = {
    # Makeup. "a" is eyes open, "b" is the second view of the same client.
    "g-mu-bride": ("c-IMG_1547.jpg", 0.50, 0.50, 1.00, 0, [1200, 760]),
    "g-bride": ("c-IMG_1547.jpg", 0.50, 0.44, 0.62, 0, [640, 400]),
    "g-mu-1a": ("a-IMG_1626.jpg", 0.50, 0.42, 0.62, 0, [640, 400]),
    "g-mu-1b": ("a-IMG_1624.jpg", 0.47, 0.44, 0.66, 0, [640, 400]),
    "g-mu-2a": ("c-IMG_1198.jpg", 0.56, 0.42, 0.56, 0, [640, 400]),
    "g-mu-2b": ("c-IMG_1201.jpg", 0.50, 0.44, 0.62, 0, [640, 400]),
    "g-mu-3a": ("c-IMG_1220.jpg", 0.50, 0.46, 0.62, 0, [640, 400]),
    "g-mu-3b": ("c-IMG_1223.jpg", 0.50, 0.50, 0.60, 0, [640, 400]),
    "g-mu-4a": ("c-IMG_1188.jpg", 0.59, 0.42, 0.52, 0, [640, 400]),
    "g-mu-4b": ("c-IMG_1184.jpg", 0.52, 0.45, 0.37, 0, [640, 400]),
    # The client was lying down, so this one is turned upright.
    "g-brows-5": ("b-IMG_1560.jpg", 0.50, 0.50, 0.94, 3, [640, 400]),
    "g-nails-shimmer": ("b-IMG_1562.jpg", 0.60, 0.50, 0.80, 0, [640, 400]),
    "g-nails-pink": ("b-IMG_1564.jpg", 0.55, 0.50, 0.80, 0, [640, 400]),
}

# Her stacked before and after photos, split on the white divider and trimmed to 8:5.
TEXTED_PIXEL_JOBS = {
    "ba-browlash-before": ("b-IMG_1558.jpg", (8, 8, 2572, 1607), [900, 520]),
    "ba-browlash-after": ("b-IMG_1558.jpg", (8, 1617, 2572, 3217), [900, 520]),
    "ba-browlash2-before": ("b-IMG_1559.jpg", (15, 15, 2565, 1604), [900, 520]),
    "ba-browlash2-after": ("b-IMG_1559.jpg", (15, 1620, 2565, 3210), [900, 520]),
    "ba-korean-before": ("b-IMG_1561.jpg", (70, 0, 988, 574), [900, 520]),
    "ba-korean-after": ("b-IMG_1561.jpg", (70, 588, 988, 1158), [900, 520]),
    "ba-browlam-before": ("b-IMG_1563.jpg", (67, 0, 984, 574), [900, 520]),
    "ba-browlam-after": ("b-IMG_1563.jpg", (67, 587, 984, 1164), [900, 520]),
}


def extend_top(im, frac):
    """Add headroom above the portrait by continuing its plain studio backdrop upward."""
    extra = round(im.height * frac)
    strip = im.crop((0, 0, im.width, 10)).resize((im.width, extra), Image.BILINEAR)
    strip = strip.filter(ImageFilter.GaussianBlur(14))
    out = Image.new("RGB", (im.width, im.height + extra))
    out.paste(strip, (0, 0))
    out.paste(im, (0, extra))
    # Soften the join so the new wall and the photo read as one surface.
    seam = out.crop((0, extra - 24, im.width, extra + 8)).filter(ImageFilter.GaussianBlur(6))
    mask = Image.linear_gradient("L").resize((im.width, 32)).point(lambda v: 255 - v)
    out.paste(seam, (0, extra - 24), mask)
    return out


def save_all(im, name, widths):
    for w in widths:
        if w > im.width:
            w = im.width
        h = round(im.height * w / im.width)
        out = im.resize((w, h), Image.LANCZOS)
        base = os.path.join(out_dir, f"{name}-{w}")
        out.save(base + ".avif", quality=56, speed=3)
        out.save(base + ".webp", quality=76, method=6)
        print(f"{name}-{w}: {w}x{h}  avif {os.path.getsize(base + '.avif') // 1024}K  webp {os.path.getsize(base + '.webp') // 1024}K")


for name, (f, box, widths) in JOBS.items():
    if not wanted(name):
        continue
    im = Image.open(os.path.join(src_dir, f)).convert("RGB")
    W, H = im.size
    im = im.crop((round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H)))
    save_all(im, name, widths)

for name, (f, box, widths) in PIXEL_JOBS.items():
    if not wanted(name):
        continue
    im = Image.open(os.path.join(src_dir, f)).convert("RGB").crop(box)
    save_all(im, name, widths)

for name, (f, cx, cy, frac, turns, widths) in FOCUS_JOBS.items():
    if not wanted(name):
        continue
    im = ImageOps.exif_transpose(Image.open(os.path.join(texted_dir, f))).convert("RGB")
    if turns:
        im = im.rotate(90 * turns, expand=True)
    W, H = im.size
    ch = min(frac * W * 1.25, H)
    cw = ch / 1.25
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    save_all(im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))), name, widths)

for name, (f, box, widths) in TEXTED_PIXEL_JOBS.items():
    if not wanted(name):
        continue
    im = ImageOps.exif_transpose(Image.open(os.path.join(texted_dir, f))).convert("RGB").crop(box)
    save_all(im, name, widths)

# Hero portrait: the original crops tight to the top of her hair, so give it headroom for the header.
if wanted("hero"):
    portrait = Image.open(os.path.join(src_dir, "intro-0.jpg")).convert("RGB")
    save_all(extend_top(portrait, 0.12), "hero", [1160, 760])
    W, H = portrait.size
    save_all(extend_top(portrait.crop((round(0.10 * W), 0, round(0.90 * W), H)), 0.15), "hero-m", [800, 520])

if wanted("logo"):
    logo = Image.open(os.path.join(src_dir, "logo-150.jpg")).convert("RGB")
    logo.save(os.path.join(out_dir, "logo-150.webp"), quality=90, method=6)
    logo.save(os.path.join(out_dir, "logo-150.png"))
    print("logo ok")

# Manifest of every cut (widths and the size of the largest), read by src/build.py.
import json
import re
manifest = {}
for f in sorted(os.listdir(out_dir)):
    m = re.match(r"(.+)-(\d+)\.webp$", f)
    if not m or m.group(1) == "logo":
        continue
    name, w = m.group(1), int(m.group(2))
    entry = manifest.setdefault(name, {"widths": [], "w": 0, "h": 0})
    entry["widths"].append(w)
    if w > entry["w"]:
        with Image.open(os.path.join(out_dir, f)) as im:
            entry["w"], entry["h"] = im.size
for entry in manifest.values():
    entry["widths"].sort()
manifest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "images.json")
with open(manifest_path, "w") as fh:
    json.dump(manifest, fh, indent=1, sort_keys=True)
print("manifest:", len(manifest), "images")
