"""Schneidet die Titelfolie aus dem Screenshot aus und entfernt den Titeltext (Inpainting),
damit das Bild als Hintergrund für jede Folie dienen kann."""
import sys
import cv2
import numpy as np

src, out = sys.argv[1], sys.argv[2]
img = cv2.imread(src)
crop = img[312:988, 30:1254]                      # nur die Folie, ohne Rahmen/Ecken
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(gray)
# einzelne Textzeilen (x0, x1, y0, y1) – Kafkas Gesicht (x>900, y<300) bleibt unberührt
boxes = [
    (545, 885, 135, 205),   # "Franz Kafka" + Linie
    (610, 800, 215, 312),   # "Die"
    (418, 1045, 312, 418),  # "Verwandlung"
    (545, 865, 430, 450),   # untere Linie
    (950, 1045, 410, 445),  # Unterlänge vom "g"
]
for x0, x1, y0, y1 in boxes:
    region = gray[y0:y1, x0:x1]
    mask[y0:y1, x0:x1] = np.maximum(mask[y0:y1, x0:x1], (region < 125).astype(np.uint8) * 255)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
clean = cv2.inpaint(crop, mask, 9, cv2.INPAINT_TELEA)
# Sanft nachglätten, damit keine Flecken bleiben
blurred = cv2.GaussianBlur(clean, (0, 0), 6)
soft = cv2.GaussianBlur(mask, (0, 0), 6).astype(np.float32)[..., None] / 255
clean = (clean * (1 - soft) + blurred * soft).astype(np.uint8)
# etwas Korn darüber, wie im Original
noise = np.random.default_rng(1).normal(0, 5, clean.shape)
clean = np.clip(clean + noise * soft, 0, 255).astype(np.uint8)
clean = cv2.resize(clean, (1920, 1060), interpolation=cv2.INTER_LANCZOS4)
clean = cv2.copyMakeBorder(clean, 10, 10, 0, 0, cv2.BORDER_REFLECT)  # auf 1920x1080
cv2.imwrite(out, clean, [cv2.IMWRITE_JPEG_QUALITY, 92])
cv2.imwrite(out.replace(".jpg", "_mask.png"), mask)

# Variante mit beigem Rand: Bildränder laufen weich in Beige aus (wie bei den anderen Folien)
H, W = clean.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def fade(dist, inner=35, width=240):                          # 0 am Rand -> 1 im Bild
    t = np.clip((dist - inner) / width, 0, 1)
    return t * t * (3 - 2 * t)
alpha = 1 - fade(np.minimum(xx, W - 1 - xx)) * fade(np.minimum(yy, H - 1 - yy))  # weiche, runde Ecken
beige = np.array([196, 214, 228], np.float32)                  # BGR ≈ #E4D6C4
rand = clean.astype(np.float32) * (1 - alpha[..., None]) + beige * alpha[..., None]
rand = np.clip(rand + np.random.default_rng(2).normal(0, 3, rand.shape) * alpha[..., None], 0, 255).astype(np.uint8)
cv2.imwrite(out.replace(".jpg", "_rand.jpg"), rand, [cv2.IMWRITE_JPEG_QUALITY, 92])
