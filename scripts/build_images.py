"""Cut and encode the site photos from the originals in _source/ig.

Run from anywhere:  python3 -I scripts/build_images.py <source_dir> <out_dir>
Every photo is Tori's own, taken from her Instagram posts (see docs/SOURCES.md).
"""
import os
import sys
from PIL import Image, ImageFilter

src_dir, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)

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
}

# Stacked before and after posts, split on the white divider (pixel rows measured on the originals).
PIXEL_JOBS = {
    "ba-lash-before": ("lashlift-0.jpg", (13, 13, 2566, 1605), [900, 520]),
    "ba-lash-after": ("lashlift-0.jpg", (13, 1618, 2566, 3212), [900, 520]),
    "ba-combo-before": ("lashbrow-combo-1.jpg", (10, 0, 2400, 1593), [900, 520]),
    "ba-combo-after": ("lashbrow-combo-1.jpg", (10, 1603, 2400, 3052), [900, 520]),
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
    im = Image.open(os.path.join(src_dir, f)).convert("RGB")
    W, H = im.size
    im = im.crop((round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H)))
    save_all(im, name, widths)

for name, (f, box, widths) in PIXEL_JOBS.items():
    im = Image.open(os.path.join(src_dir, f)).convert("RGB").crop(box)
    save_all(im, name, widths)

# Hero portrait: the original crops tight to the top of her hair, so give it headroom for the header.
portrait = Image.open(os.path.join(src_dir, "intro-0.jpg")).convert("RGB")
save_all(extend_top(portrait, 0.12), "hero", [1160, 760])
W, H = portrait.size
save_all(extend_top(portrait.crop((round(0.10 * W), 0, round(0.90 * W), H)), 0.15), "hero-m", [800, 520])

logo = Image.open(os.path.join(src_dir, "logo-150.jpg")).convert("RGB")
logo.save(os.path.join(out_dir, "logo-150.webp"), quality=90, method=6)
logo.save(os.path.join(out_dir, "logo-150.png"))
print("logo ok")
