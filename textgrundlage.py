"""Zeilennummerierte Textgrundlage für "Die Verwandlung" + Zeilenangaben für alle Zitate.

1. Liest den gemeinfreien Originaltext (Projekt Gutenberg Nr. 22367, Fassung von 1915).
2. Bricht ihn in feste Zeilen um und nummeriert sie durchgehend (Z. 1 bis Ende).
3. Schreibt daraus "Textgrundlage_Die_Verwandlung_mit_Zeilen.pdf" (Zeilen exakt wie gezählt).
4. Sucht jedes Zitat/jeden Ankersatz aus build_deck.js im Text und schreibt die
   Zeilenangaben nach zeilen.json, z. B. "Z. 123", "Z. 123 f.", "Z. 123 ff.".

Aufruf: python3 textgrundlage.py
"""
import json
import re
import textwrap
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).parent
SRC = ROOT / "quelle" / "die_verwandlung_original.txt"
PDF = ROOT / "Textgrundlage_Die_Verwandlung_mit_Zeilen.pdf"
WIDTH = 64  # Zeichen pro Zeile (ähnlich einer Schulausgabe)

# ---------- 1. Absätze lesen ----------
raw = SRC.read_text(encoding="utf-8")
blocks = [re.sub(r"\s+", " ", b).strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
# Gedankenstriche typografisch setzen (nur Darstellung; die Suche ignoriert den Unterschied)
blocks = [re.sub(r" - ", " – ", b) for b in blocks]

# ---------- 2. Zeilen bilden ----------
rows = []  # (art, text, zeilennummer|None, teil)
teil = ""
n = 0
for b in blocks:
    if b in ("I.", "II.", "III."):
        teil = b.rstrip(".")
        rows.append(("teil", b, None, teil))
        continue
    if b.startswith("Franz Kafka") or b == "DIE VERWANDLUNG":
        continue
    for line in textwrap.wrap(b, WIDTH, break_long_words=False, break_on_hyphens=False):
        n += 1
        rows.append(("text", line, n, teil))
    rows.append(("absatz", "", None, teil))
TOTAL = n

# ---------- 3. PDF ----------
FONTS = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif", FONTS + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SerifB", FONTS + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SerifI", FONTS + "LiberationSerif-Italic.ttf"))

PW, PH = A4
LEFT, TOP, BOTTOM = 32 * mm, PH - 22 * mm, 20 * mm
LH = 14.2  # Zeilenabstand in pt

c = canvas.Canvas(str(PDF), pagesize=A4)
c.setTitle("Franz Kafka: Die Verwandlung – zeilennummerierte Textgrundlage")
page = 1


def footer():
    c.setFont("Serif", 8.5)
    c.setFillGray(0.35)
    c.drawString(LEFT, 11 * mm, "Franz Kafka: Die Verwandlung (1915) – zeilennummerierte Textgrundlage")
    c.drawRightString(PW - 22 * mm, 11 * mm, f"S. {page}")
    c.setFillGray(0)


y = TOP
c.setFont("SerifB", 17)
c.drawString(LEFT, y, "Franz Kafka: Die Verwandlung")
y -= 18
c.setFont("SerifI", 9.5)
for t in (
    "Text der Erstausgabe 1915 (gemeinfrei), nach Projekt Gutenberg, E-Book Nr. 22367.",
    f"Zeilen durchgehend nummeriert (Z. 1–{TOTAL}); alle Zeilenangaben der Präsentation beziehen sich auf diese Fassung.",
):
    c.drawString(LEFT, y, t)
    y -= 12
y -= 14

for art, text, num, _ in rows:
    need = 30 if art == "teil" else LH
    if y - need < BOTTOM:
        footer()
        c.showPage()
        page += 1
        y = TOP
    if art == "teil":
        y -= 8
        c.setFont("SerifB", 13)
        c.drawCentredString(LEFT + (PW - LEFT - 22 * mm) / 2, y, text)
        y -= 22
    elif art == "absatz":
        y -= 3
    else:
        c.setFont("Serif", 11)
        c.drawString(LEFT, y, text)
        if num % 5 == 0 or num == 1:
            c.setFont("Serif", 8)
            c.setFillGray(0.4)
            c.drawRightString(LEFT - 5 * mm, y + 0.5, str(num))
            c.setFillGray(0)
        y -= LH
footer()
c.save()

# ---------- 4. Zeilenangaben berechnen ----------
def norm(s):
    s = s.replace("„", "").replace("“", "").replace("–", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:!?«])", r"\1", s)
    return s.strip()


# durchgehender Text mit Zeichen->Zeile-Zuordnung
flat, owner = [], []
for art, text, num, _ in rows:
    if art != "text":
        continue
    piece = norm(text) + " "
    flat.append(piece)
    owner.extend([num] * len(piece))
flat = "".join(flat)


def find(seg, start=0):
    seg = norm(seg).strip(" ,")
    for cand in (seg, seg[:1].upper() + seg[1:], seg[:1].lower() + seg[1:]):
        i = flat.find(cand, start)
        if i >= 0:
            return i, i + len(cand) - 1
    raise SystemExit(f"NICHT GEFUNDEN: {seg[:80]}")


def span(text):
    """Zeilenbereich eines Zitats; »[…]« und »“ – „« trennen Teilstücke."""
    parts = [p for p in re.split(r"\[…\]|“ – „", text) if norm(p).strip(" ,")]
    a, e = find(parts[0])
    pos = e
    for p in parts[1:]:
        _, pos = find(p, pos)
    return owner[a], owner[pos]


def fmt(z1, z2):
    if z2 == z1:
        return f"Z. {z1}"
    if z2 == z1 + 1:
        return f"Z. {z1} f."
    return f"Z. {z1} ff."


js = (ROOT / "build_deck.js").read_text(encoding="utf-8")
out = {}
for t in re.findall(r'\{ t: "(.*?)", ref: "Buch"', js):
    out[t] = fmt(*span(t))
for a in re.findall(r'anchor: "(.*?)"', js):
    out[a] = "vgl. " + fmt(*span(a))
(ROOT / "zeilen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{TOTAL} Zeilen, {page} Seiten -> {PDF.name}; {len(out)} Angaben -> zeilen.json")
