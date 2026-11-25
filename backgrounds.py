"""Erzeugt die Sepia-Hintergründe im Stil der Titelfolie (Wand, Fensterlicht, Korn, Vignette)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
rng = np.random.default_rng(1915)


def blur(arr, r):
    img = Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))
    return np.asarray(img.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255


def noise(r):
    """Glattes Rauschen der Größenordnung r Pixel (float, ohne Bänder)."""
    sw, sh = max(2, int(W / r)), max(2, int(H / r))
    small = Image.fromarray(rng.normal(0, 1, (sh, sw)).astype(np.float32), mode="F")
    a = np.asarray(small.resize((W, H), Image.BICUBIC), np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def scratches():
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    for _ in range(140):
        x, y = rng.integers(0, W), rng.integers(0, H)
        l = rng.integers(20, 160)
        dx = rng.normal(0, 0.3)
        d.line([(x, y), (x + dx * l, y + l)], fill=int(rng.integers(60, 200)), width=1)
    a = np.asarray(img.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    return a * np.where(rng.random() > 0.5, 1, -1)


def mask_from(draw_fn, r):
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m))
    return np.asarray(m.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255


def base_wall(cx=0.55, cy=0.45, bright=1.0):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x / W - cx) * 1.25) ** 2 + ((y / H - cy) * 1.0) ** 2)
    lum = np.clip(1.0 - d * 0.95, 0, 1) ** 1.2 * 0.62 * bright + 0.20
    # Fleckige Wand (niederfrequentes Rauschen)
    lum = lum + noise(70) * 0.024 + noise(18) * 0.011 + noise(4) * 0.006
    lum = lum + scratches() * 0.04
    return lum


def window_light(lum, side="left", strength=0.16):
    def draw(d):
        # zwei schräge Fensterflügel mit Sprossen, wie das Licht auf der Titelfolie
        x0 = 60 if side == "left" else W - 60 - 520
        for col in range(2):
            for row in range(3):
                bx = x0 + col * 250
                by = 40 + row * 240
                skew = 110
                if side == "left":
                    poly = [(bx, by), (bx + 210, by + 40), (bx + 210 + skew * 0.2, by + 250), (bx + skew * 0.2, by + 210)]
                else:
                    poly = [(bx + 210, by), (bx, by + 40), (bx - skew * 0.2, by + 250), (bx + 210 - skew * 0.2, by + 210)]
                d.polygon(poly, fill=255)
    m = mask_from(draw, 9)
    fade = np.linspace(1, 0, H, dtype=np.float32)[:, None] ** 0.8
    return lum + m * strength * fade


def vignette(lum, k=0.9):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x / W - 0.5) * 2) ** 2 + ((y / H - 0.5) * 2) ** 2) / np.sqrt(2)
    return lum * (1 - k * np.clip(d - 0.35, 0, 1) ** 1.4)


def floor(lum, top=0.83):
    y = np.arange(H, dtype=np.float32)[:, None] / H
    f = np.clip((y - top) * 30, 0, 1)
    planks = np.zeros((H, W), np.float32)
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    yt = int(top * H)
    for i in range(-20, 30):
        xb = W / 2 + i * 160
        xt = W / 2 + i * 60
        d.line([(xt, yt), (xb, H)], fill=255, width=3)
    planks = np.asarray(img.filter(ImageFilter.GaussianBlur(1.5)), np.float32) / 255
    floor_lum = 0.30 + (y - top) * -0.6 - planks * 0.08
    return lum * (1 - f) + floor_lum * f


def grain(lum, amt=0.03):
    return lum + rng.normal(0, 1, (H, W)).astype(np.float32) * amt + noise(1.2) * 0.02


def frame_on_wall(lum, x, y, w, h):
    def outer(d):
        d.rectangle([x, y, x + w, y + h], fill=255)
    def inner(d):
        d.rectangle([x + 18, y + 18, x + w - 18, y + h - 18], fill=255)
    lum = lum - mask_from(outer, 2) * 0.32 + mask_from(inner, 2) * 0.18
    shadow = mask_from(lambda d: d.rectangle([x + 10, y + 14, x + w + 12, y + h + 16], fill=255), 10)
    return lum - shadow * 0.08


def apple(lum, cx, cy, r, darkness=0.85):
    def draw(d):
        d.ellipse([cx - r, cy - r * 0.9, cx + r * 0.15, cy + r * 0.95], fill=255)
        d.ellipse([cx - r * 0.15, cy - r * 0.9, cx + r, cy + r * 0.95], fill=255)
        d.ellipse([cx - r * 0.8, cy - r * 0.55, cx + r * 0.8, cy + r], fill=255)
        d.line([(cx, cy - r * 0.7), (cx + r * 0.12, cy - r * 1.25)], fill=255, width=max(4, r // 9))
        d.ellipse([cx + r * 0.12, cy - r * 1.3, cx + r * 0.62, cy - r * 1.05], fill=255)
    m = mask_from(draw, 2)
    sh = mask_from(lambda d: d.ellipse([cx - r * 1.3, cy + r * 0.75, cx + r * 1.5, cy + r * 1.15], fill=255), 14)
    lum = lum - sh * 0.25
    hl = mask_from(lambda d: d.ellipse([cx - r * 0.6, cy - r * 0.55, cx - r * 0.2, cy - r * 0.05], fill=255), 10)
    return lum * (1 - m * darkness) + hl * m * 0.07


def door(lum, x, y, w, h, gap=26):
    # dunkle Tür, Lichtspalt an der Seite
    frame = mask_from(lambda d: d.rectangle([x - 26, y - 26, x + w + 26, H], fill=255), 2)
    body = mask_from(lambda d: d.rectangle([x, y, x + w, H], fill=255), 2)
    lum = lum * (1 - frame * 0.55)
    lum = lum * (1 - body * 0.35)
    for py in (0.08, 0.52):
        p = mask_from(lambda d, py=py: d.rectangle([x + 40, y + h * py, x + w - 40, y + h * py + h * 0.36], width=6, outline=255), 2)
        lum = lum - p * 0.1
    knob = mask_from(lambda d: d.ellipse([x + 30, y + h * 0.5, x + 58, y + h * 0.5 + 28], fill=255), 2)
    lum = lum - knob * 0.25
    slit = mask_from(lambda d: d.rectangle([x + w, y, x + w + gap, H], fill=255), 3)
    glow = mask_from(lambda d: d.polygon([(x + w, H), (x + w + gap, H), (x + w + 520, H + 200), (x + w - 60, H + 200)], fill=255), 40)
    lum = lum * (1 - slit) + slit * 0.95
    beam = mask_from(lambda d: d.polygon([(x + w, int(H * 0.84)), (x + w + gap, int(H * 0.84)), (x + w + 600, H), (x + w - 40, H)], fill=255), 25)
    return lum + beam * 0.35 + glow * 0.1


def to_sepia(lum, path):
    lum = np.clip(lum, 0, 1)
    # Sepia-Tonung: dunkel = warmes Braun, hell = Pergament
    dark = np.array([28, 22, 16], np.float32)
    mid = np.array([150, 136, 112], np.float32)
    light = np.array([238, 230, 212], np.float32)
    l = lum[..., None]
    rgb = np.where(l < 0.5, dark + (mid - dark) * (l / 0.5), mid + (light - mid) * ((l - 0.5) / 0.5))
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(path, quality=88)


def make(name, fn):
    lum = fn()
    lum = grain(lum)
    to_sepia(lum, f"{OUT}/{name}.jpg")
    print("wrote", name)


# 1) Kapitelfolie: Fensterlicht links, Boden, Apfel auf dem Boden (Leitsymbol)
make("bg_kapitel", lambda: vignette(apple(floor(window_light(base_wall(0.55, 0.42), "left", 0.2)), 1610, 975, 52), 0.95))
# 2) Inhaltsfolie hell: Fensterlicht links, Bilderrahmen
make("bg_hell_links", lambda: vignette(window_light(base_wall(0.55, 0.5, 1.12), "left", 0.13), 0.8))
# 3) Inhaltsfolie hell: Fensterlicht rechts
make("bg_hell_rechts", lambda: vignette(window_light(base_wall(0.45, 0.5, 1.12), "right", 0.13), 0.8))
# 4) Inhaltsfolie ruhig, mit kleinem Rahmen oben rechts
make("bg_hell_rahmen", lambda: vignette(frame_on_wall(base_wall(0.5, 0.5, 1.12), 1680, 70, 150, 190), 0.8))
# 5) Schlussfolie: Tür mit Lichtspalt (Gregors Zimmertür)
make("bg_tuer", lambda: vignette(door(floor(base_wall(0.4, 0.45), 0.88), 1430, 150, 330, 800), 0.95))
