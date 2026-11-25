// Baut die Folien "Motiv: Vater-Sohn-Beziehung" (Kafka, Die Verwandlung)
// Aufruf: NODE_PATH=<dir mit node_modules> node build_deck.js <applyTheme-Pfad>
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.argv[2]);

const A = (f) => path.join(__dirname, "assets", f);
const OUT = path.join(__dirname, "Vater-Sohn-Beziehung.pptx");

const THEME = {
  name: "Kafka Sepia",
  headFontFace: "Georgia",
  bodyFontFace: "Cambria",
  colors: {
    dk1: "1E1812", lt1: "FFFFFF", dk2: "4A3F33", lt2: "EDE5D3",
    accent1: "6B1F1A", accent2: "8C7A5E", accent3: "3B3128", accent4: "A89880",
    accent5: "5C4B3A", accent6: "B3A58C", hlink: "6B1F1A", folHlink: "4A3F33",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625
pres.title = "Die Verwandlung – Motiv: Vater-Sohn-Beziehung";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- Layouts ----------
pres.defineSlideMaster({
  title: "Kapitel",
  background: { path: A("bg_kapitel.jpg") },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 1.5, y: 1.2, w: 7, h: 0.45, align: "center", fontSize: 18, color: C.text1, charSpacing: 4 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 1.85, w: 9, h: 1.5, align: "center", fontSize: 40, bold: true, color: C.text1, fontFace: THEME.headFontFace }, text: "" } },
    { placeholder: { options: { name: "sub", type: "body", x: 1.5, y: 3.55, w: 7, h: 0.6, align: "center", fontSize: 16, italic: true, color: C.text2 }, text: "" } },
  ],
});
for (const [name, bg] of [["Inhalt links", "bg_hell_links.jpg"], ["Inhalt rechts", "bg_hell_rechts.jpg"], ["Inhalt Rahmen", "bg_hell_rahmen.jpg"], ["Schluss", "bg_tuer.jpg"]]) {
  pres.defineSlideMaster({
    title: name,
    background: { path: A(bg) },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 8.8, h: 0.8, align: "left", fontSize: 32, bold: true, color: C.text1, fontFace: THEME.headFontFace, margin: 0 }, text: "" } },
    ],
  });
}

// ---------- Helfer ----------
const card = (s, x, y, w, h, name, transp = 22) =>
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, objectName: name,
    fill: { color: C.background2, transparency: transp },
    line: { color: C.accent2, width: 0.75 },
    shadow: { type: "outer", color: "1E1812", opacity: 0.25, blur: 6, offset: 2, angle: 90 },
  });
const txt = (s, text, o) => s.addText(text, { isTextBox: true, color: C.text1, fontSize: 15, valign: "top", ...o });
const rule = (s, x, y, w, name) => s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: C.text1, width: 0.75 }, objectName: name });

// ===== Folie 1: Kapitel =====
pres.addSection({ title: "Vater-Sohn-Beziehung" });
let s = pres.addSlide({ masterName: "Kapitel", sectionTitle: "Vater-Sohn-Beziehung" });
s.addText("Motiv", { placeholder: "kicker" });
s.addText("Vater-Sohn-Beziehung", { placeholder: "title" });
s.addText("Macht, Schuld und Ohnmacht in „Die Verwandlung“", { placeholder: "sub" });
rule(s, 3.6, 1.72, 2.8, "Linie oben");
rule(s, 3.6, 3.42, 2.8, "Linie unten");
s.addNotes(
`(ca. 30 Sek.)
Ich beschäftige mich mit einem der wichtigsten Motive der Erzählung: der Beziehung zwischen Gregor Samsa und seinem Vater.
Man kann „Die Verwandlung“ nämlich nicht nur als Geschichte über einen Mann lesen, der zum Käfer wird – sondern auch als Geschichte über einen Machtkampf in der Familie. Und dieser Machtkampf hat sehr viel mit Kafkas eigenem Leben zu tun.`);

// ===== Folie 2: Biografischer Hintergrund =====
s = pres.addSlide({ masterName: "Inhalt rechts", sectionTitle: "Vater-Sohn-Beziehung" });
s.addText("Kafka und sein Vater", { placeholder: "title" });
const facts = [
  ["Hermann Kafka", "erfolgreicher Kaufmann in Prag – laut, kräftig, dominant"],
  ["Franz Kafka", "sensibel, unsicher, fühlt sich vom Vater nie anerkannt"],
  ["„Brief an den Vater“ (1919)", "über 100 Seiten Abrechnung – nie abgeschickt"],
];
facts.forEach(([h, d], i) => {
  const y = 1.45 + i * 1.18;
  s.addText(String(i + 1), { isTextBox: true, x: 0.6, y, w: 0.55, h: 0.55, fontSize: 30, bold: true, color: C.accent1, fontFace: THEME.headFontFace, margin: 0, valign: "top", objectName: `Nummer ${i + 1}` });
  txt(s, [
    { text: h, options: { bold: true, fontSize: 17, breakLine: true } },
    { text: d, options: { fontSize: 14, color: C.text2 } },
  ], { x: 1.2, y: y - 0.02, w: 3.6, h: 1.0, margin: 0, objectName: `Fakt ${i + 1}` });
});
card(s, 5.25, 1.4, 4.15, 3.25, "Briefkarte", 15);
txt(s, "„Mein Schreiben handelte von Dir, ich klagte dort ja nur, was ich an Deiner Brust nicht klagen konnte.“",
  { x: 5.5, y: 1.6, w: 3.65, h: 2.2, fontSize: 18, italic: true, fontFace: THEME.headFontFace, objectName: "Zitat Brief" });
txt(s, "— Franz Kafka, Brief an den Vater", { x: 5.5, y: 3.95, w: 3.65, h: 0.45, fontSize: 12, color: C.text2, objectName: "Quelle Brief" });
s.addNotes(
`(ca. 1 Min.)
Um das Motiv zu verstehen, muss man Kafkas Biografie kennen. Sein Vater Hermann Kafka war ein erfolgreicher, selbstbewusster Kaufmann – körperlich groß, laut und sehr dominant. Franz dagegen war sensibel und unsicher und hatte sein Leben lang das Gefühl, den Erwartungen seines Vaters nicht zu genügen.
1919 schrieb Kafka einen über hundert Seiten langen „Brief an den Vater“, in dem er mit ihm abrechnet. Abgeschickt hat er ihn nie.
In diesem Brief steht der Satz: „Mein Schreiben handelte von Dir, ich klagte dort ja nur, was ich an Deiner Brust nicht klagen konnte.“ Kafka sagt also selbst: Seine Texte drehen sich um den Vater. „Die Verwandlung“, geschrieben 1912, ist dafür ein Paradebeispiel.`);

// ===== Folie 3: Vor der Verwandlung – Rollentausch =====
s = pres.addSlide({ masterName: "Inhalt links", sectionTitle: "Vater-Sohn-Beziehung" });
s.addText("Vorher: Rollentausch", { placeholder: "title" });
const cols = [
  ["Gregor", "der Ernährer", ["arbeitet als Handlungsreisender", "bezahlt die Schulden des Vaters", "finanziert die ganze Familie"]],
  ["Der Vater", "der Versager", ["Geschäft vor fünf Jahren pleite", "alt, schwerfällig, untätig", "lässt sich vom Sohn versorgen"]],
];
cols.forEach(([h, sub, items], i) => {
  const x = 2.75 + i * 3.45;
  card(s, x, 1.45, 3.15, 3.0, `Karte ${h}`);
  txt(s, h, { x: x + 0.25, y: 1.6, w: 2.65, h: 0.5, fontSize: 22, bold: true, fontFace: THEME.headFontFace, objectName: `Kopf ${h}` });
  txt(s, sub, { x: x + 0.25, y: 2.08, w: 2.65, h: 0.4, fontSize: 15, italic: true, color: C.accent1, objectName: `Rolle ${h}` });
  txt(s, items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < items.length - 1 } })),
    { x: x + 0.25, y: 2.6, w: 2.7, h: 1.7, fontSize: 14, paraSpaceAfter: 6, objectName: `Liste ${h}` });
});
txt(s, "Der Sohn hat die Rolle des Vaters übernommen – doch Dank bekommt er dafür nicht.",
  { x: 2.75, y: 4.6, w: 6.6, h: 0.5, fontSize: 15, italic: true, bold: true, color: C.text1, objectName: "Fazit Rollentausch" });
s.addNotes(
`(ca. 1 Min.)
Schon vor der Verwandlung ist das Verhältnis in der Familie Samsa auf den Kopf gestellt. Das Geschäft des Vaters ist vor fünf Jahren zusammengebrochen. Seitdem ist Gregor der Ernährer: Er arbeitet als Handlungsreisender in einem Job, den er hasst, und bezahlt damit die Schulden seines Vaters bei seinem Chef ab.
Der Vater dagegen wirkt alt und schwerfällig, er sitzt zu Hause, liest Zeitung und lässt sich versorgen.
Gregor hat also die Rolle des Familienoberhaupts übernommen. Aber – und das ist wichtig – er bekommt dafür keine echte Anerkennung. Das Geld wird selbstverständlich genommen, „eine besondere Wärme wollte sich nicht mehr ergeben“, heißt es im Text.`);

// ===== Folie 4: Drei Konfrontationen =====
s = pres.addSlide({ masterName: "Inhalt Rahmen", sectionTitle: "Vater-Sohn-Beziehung" });
s.addText("Drei Konfrontationen", { placeholder: "title" });
const parts = [
  ["I", "Der Stock", "Der Vater treibt Gregor mit Stock und Zeitung zurück ins Zimmer – „Zischlaute ausstoßend wie ein Wilder“. Gregor verletzt sich an der Tür."],
  ["II", "Die Äpfel", "Der Vater bombardiert Gregor mit Äpfeln. Einer bleibt im Rücken stecken – eine Wunde, die nie verheilt."],
  ["III", "Das Urteil", "Grete fordert: „Wir müssen versuchen, es loszuwerden.“ Der Vater stimmt zu. Gregor stirbt in derselben Nacht."],
];
parts.forEach(([n, h, d], i) => {
  const x = 0.6 + i * 3.0;
  card(s, x, 1.4, 2.75, 3.25, `Karte Teil ${n}`);
  txt(s, n, { x: x + 0.25, y: 1.5, w: 2.25, h: 0.8, fontSize: 40, bold: true, color: C.accent1, fontFace: THEME.headFontFace, objectName: `Teil ${n}` });
  txt(s, h, { x: x + 0.25, y: 2.3, w: 2.25, h: 0.45, fontSize: 19, bold: true, fontFace: THEME.headFontFace, objectName: `Titel Teil ${n}` });
  txt(s, d, { x: x + 0.25, y: 2.8, w: 2.3, h: 1.8, fontSize: 14, objectName: `Text Teil ${n}` });
});
s.addNotes(
`(ca. 1,5 Min.)
Die Erzählung hat drei Teile – und in jedem Teil kommt es zu einer Konfrontation zwischen Vater und Sohn. Die Gewalt steigert sich dabei.
Im ersten Teil treibt der Vater Gregor mit einem Stock und einer Zeitung zurück in sein Zimmer. Er stößt dabei „Zischlaute aus wie ein Wilder“. Gregor bleibt in der Tür stecken und verletzt sich.
Im zweiten Teil kommt die bekannteste Szene: Der Vater bewirft Gregor mit Äpfeln. Ein Apfel dringt in Gregors Rücken ein und bleibt dort stecken. Diese Wunde entzündet sich und heilt nie wieder – der Apfel ist also eine Art Waffe, die Gregor langsam tötet. Viele Interpreten sehen darin eine Anspielung auf den Sündenfall: Schuld und Strafe.
Im dritten Teil fällt das endgültige Urteil. Die Schwester sagt: „Wir müssen versuchen, es loszuwerden“, und der Vater stimmt zu. In derselben Nacht stirbt Gregor.`);

// ===== Folie 5: Machtwechsel =====
s = pres.addSlide({ masterName: "Inhalt rechts", sectionTitle: "Vater-Sohn-Beziehung" });
s.addText("Machtwechsel", { placeholder: "title" });
s.addChart(pres.charts.LINE, [
  { name: "Vater", labels: ["Vorher", "Teil I", "Teil II", "Teil III"], values: [1, 2.5, 4, 5] },
  { name: "Gregor", labels: ["Vorher", "Teil I", "Teil II", "Teil III"], values: [5, 3, 1.8, 0.2] },
], {
  x: 0.5, y: 1.3, w: 5.0, h: 3.6, objectName: "Diagramm Macht",
  chartColors: ["6B1F1A", "4A3F33"], lineSize: 3, lineDataSymbol: "circle", lineDataSymbolSize: 9,
  showLegend: true, legendPos: "b", legendFontSize: 13, legendColor: "1E1812", legendFontFace: "+mn-lt",
  valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 5.5, valGridLine: { style: "none" },
  catAxisLabelColor: "1E1812", catAxisLabelFontSize: 13, catAxisLabelFontFace: "+mn-lt", catGridLine: { style: "none" },
  catAxisLineShow: true, catAxisLineColor: "4A3F33",
  showTitle: true, title: "Macht in der Familie (symbolisch)", titleFontSize: 13, titleColor: "4A3F33", titleFontFace: "+mn-lt",
});
card(s, 5.8, 1.6, 3.6, 2.75, "Karte Zitat Vater", 15);
txt(s, [
  { text: "Der Vater danach:", options: { bold: true, fontSize: 16, breakLine: true } },
  { text: " ", options: { fontSize: 6, breakLine: true } },
  { text: "„recht gut aufgerichtet; in eine straffe blaue Uniform mit Goldknöpfen gekleidet“", options: { italic: true, fontSize: 15, breakLine: true } },
  { text: " ", options: { fontSize: 8, breakLine: true } },
  { text: "Gregor „staunte über die Riesengröße seiner Stiefelsohlen“.", options: { italic: true, fontSize: 15 } },
], { x: 6.05, y: 1.75, w: 3.15, h: 2.5, objectName: "Zitate Vater" });
s.addNotes(
`(ca. 1,5 Min.)
Das Spannende ist: Je schwächer Gregor wird, desto stärker wird der Vater. Das Diagramm zeigt das symbolisch.
Vorher war der Vater müde und träge, er lag im Schlafrock auf dem Sofa. Nach der Verwandlung nimmt er wieder eine Arbeit als Bankdiener an – und plötzlich steht er da, „recht gut aufgerichtet, in eine straffe blaue Uniform mit Goldknöpfen gekleidet“. Gregor, der jetzt auf dem Boden kriecht, „staunte über die Riesengröße seiner Stiefelsohlen“. Das zeigt sehr bildlich, wie klein Gregor gegenüber dem Vater geworden ist.
Die Macht wandert also zurück: Der Vater wird wieder Familienoberhaupt, und Gregor verliert erst seine Stellung, dann seine Gesundheit und schließlich sein Leben.`);

// ===== Folie 6: Deutung & Fazit =====
s = pres.addSlide({ masterName: "Schluss", sectionTitle: "Vater-Sohn-Beziehung" });
s.addText("Deutung", { placeholder: "title" });
const points = [
  ["Ungeziefer", "So fühlte sich Kafka vor seinem Vater: klein, wertlos, unerwünscht."],
  ["Schuld", "Gregor wehrt sich nie – er sucht die Schuld bei sich selbst."],
  ["Erlösung?", "Nach Gregors Tod: „Nun können wir Gott danken.“ Die Familie blüht auf."],
];
points.forEach(([h, d], i) => {
  const y = 1.3 + i * 1.0;
  card(s, 0.6, y, 6.9, 0.85, `Karte ${h}`);
  txt(s, h, { x: 0.85, y: y + 0.05, w: 1.75, h: 0.75, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1, valign: "middle", objectName: `Kopf ${h}` });
  txt(s, d, { x: 2.65, y: y + 0.05, w: 4.7, h: 0.75, fontSize: 14, valign: "middle", objectName: `Text ${h}` });
});
s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 4.35, w: 6.9, h: 0.75, objectName: "Karte Kernaussage", fill: { color: C.accent1, transparency: 8 }, line: { type: "none" } });
txt(s, "„Die Verwandlung“ zeigt, wie ein Sohn an der fehlenden Liebe seines Vaters zerbricht.",
  { x: 0.85, y: 4.35, w: 6.5, h: 0.75, valign: "middle", color: C.background2, fontSize: 15, italic: true, bold: true, fontFace: THEME.headFontFace, objectName: "Kernaussage" });
s.addNotes(
`(ca. 1,5 Min.)
Wie kann man das deuten?
Erstens: Das Ungeziefer ist ein Bild dafür, wie Kafka sich vor seinem Vater gefühlt hat – klein, wertlos und unerwünscht. Im „Brief an den Vater“ beschreibt er genau dieses Gefühl, schon durch die „bloße Körperlichkeit“ des Vaters niedergedrückt zu sein.
Zweitens: Schuld. Gregor wehrt sich kein einziges Mal gegen den Vater. Selbst als er verletzt wird, sucht er die Schuld bei sich und denkt „mit Rührung und Liebe“ an seine Familie zurück.
Drittens: Nach Gregors Tod sagt der Vater: „Nun können wir Gott danken.“ Die Familie macht einen Ausflug, schmiedet Pläne und blüht regelrecht auf. Gregors Tod wirkt wie eine Erlösung – für die Familie, nicht für ihn.
Mein Fazit: Die Vater-Sohn-Beziehung ist der Kern der Erzählung. „Die Verwandlung“ zeigt, wie ein Sohn an der fehlenden Liebe und Anerkennung seines Vaters zerbricht – und genau das war Kafkas eigene Lebenserfahrung.
Vielen Dank!`);

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
