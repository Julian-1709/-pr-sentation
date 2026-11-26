// Baut die Folien "Motiv: Vater-Sohn-Beziehung" (Kafka, Die Verwandlung)
// Aufruf: NODE_PATH=<dir mit node_modules> node build_deck.js <applyTheme-Pfad>
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.argv[2]);

const A = (f) => path.join(__dirname, "assets", f);
// Zeilenangaben (von textgrundlage.py berechnet)
const Z = JSON.parse(require("fs").readFileSync(path.join(__dirname, "zeilen.json"), "utf8"));
const zref = (k) => { if (!Z[k]) throw new Error("Keine Zeilenangabe für: " + k); return Z[k]; };
const OUT = path.join(__dirname, "Vater-Sohn-Beziehung.pptx");

const THEME = {
  name: "Kafka Sepia",
  headFontFace: "Cambria",
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
// Hintergrund wie bei den anderen Folien: Titelbild gleichmäßig beige verblasst, ohne Rand und Kasten.
const BG = { path: A("bg_titelbild_blass.jpg") };
const MUTED = C.accent5;
// Erste Folie: Titelbild in Originalfarben, Text an der Stelle von "Franz Kafka / Die Verwandlung"
pres.defineSlideMaster({
  title: "Kapitel",
  background: { path: A("bg_titelbild.jpg") },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 3.55, y: 1.12, w: 5.0, h: 0.45, align: "center", fontSize: 22, color: C.text1, charSpacing: 4, fontFace: "Georgia" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 3.2, y: 1.72, w: 5.7, h: 1.9, align: "center", valign: "middle", fontSize: 44, color: C.text1, fontFace: "Georgia", lineSpacingMultiple: 0.9 }, text: "" } },
    { placeholder: { options: { name: "sub", type: "body", x: 3.75, y: 3.78, w: 4.6, h: 0.5, align: "center", fontSize: 15, italic: true, color: C.text1 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Inhalt",
  background: BG,
  slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.25, fontSize: 9, color: MUTED, align: "right" },
  objects: [
    { text: { text: "Franz Kafka: Die Verwandlung – Motiv: Vater-Sohn-Beziehung", options: { x: 0.5, y: 5.2, w: 6, h: 0.25, fontSize: 9, color: MUTED, margin: 0 } } },
    { placeholder: { options: { name: "kicker", type: "body", x: 0.6, y: 0.28, w: 8.8, h: 0.25, align: "left", fontSize: 9, bold: true, color: MUTED, charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.55, w: 8.8, h: 0.6, align: "left", fontSize: 28, bold: true, color: C.text1, margin: 0 }, text: "" } },
  ],
});

// ---------- Helfer ----------
const txt = (s, text, o) => s.addText(text, { isTextBox: true, color: C.text1, fontSize: 14, valign: "top", ...o });
const rule = (s, x, y, w, name) => s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: C.text1, width: 0.75 }, objectName: name });

// Zeilen grob schätzen, damit Kästen zum Text passen
const lines = (str, cpl) => str.split("\n").reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0);

// Linke Spalte: Analysepunkte (fett + Erklärung)
const LX = 0.6, LW = 4.35;
function points(s, items, y0 = 1.3) {
  let y = y0;
  items.forEach(([h, d, a], i) => {
    const ref = a ? " (" + zref(a.anchor).replace(/ /g, "\u00A0") + ")" : "";
    const hh = 0.3, dh = lines(d + ref, 45) * 0.24 + 0.05;
    txt(s, [
      { text: h, options: { bold: true, fontSize: 15, color: C.accent1, fontFace: THEME.headFontFace, breakLine: true } },
      { text: d, options: { fontSize: 14 } },
      ...(ref ? [{ text: ref, options: { fontSize: 11, color: MUTED } }] : []),
    ], { x: LX, y, w: LW, h: hh + dh, margin: 0, paraSpaceAfter: 2, objectName: `Punkt ${i + 1}` });
    y += hh + dh + 0.22;
  });
  return y;
}

// Rechte Spalte: Zitate aus dem Buch. hi = wichtig (rot hinterlegt)
const QX = 5.2, QW = 4.25, QBOTTOM = 5.08;
function quotes(s, list, y0 = 1.25) {
  list = list.map((q) => ({ ...q, ref: q.ref === "Buch" ? zref(q.t) : q.ref }));
  // größte Schrift wählen (12,5 → 11 pt), bei der alle Zitate in die Spalte passen
  const nb = (r) => "\u00A0(" + r.replace(/ /g, "\u00A0") + ")";
  const height = (t, ref, fs) => lines(t + nb(ref), 62 * 11 / fs) * 0.19 * fs / 11 + 0.27;
  let fs = 12.5;
  while (fs > 10.5 && list.reduce((sum, q) => sum + height(q.t, q.ref, fs) + 0.09, y0) - 0.09 > QBOTTOM) fs -= 0.5;
  let y = y0;
  list.forEach(({ t, ref, hi }, i) => {
    const h = height(t, ref, fs);
    s.addShape(pres.shapes.RECTANGLE, {
      x: QX, y, w: QW, h, objectName: `${hi ? "Wichtiges " : ""}Zitat ${i + 1}`,
      fill: hi ? { color: C.accent1, transparency: 0 } : { color: C.background1, transparency: 40 },
      line: hi ? { type: "none" } : { color: C.accent2, width: 0.5 },
    });
    s.addText([
      { text: t, options: { italic: true } },
      { text: nb(ref), options: { fontSize: fs - 1.5, italic: false, bold: true } },
    ], {
      isTextBox: true, x: QX + 0.1, y: y + 0.02, w: QW - 0.2, h: h - 0.04, valign: "middle", margin: 2,
      fontSize: fs, fontFace: THEME.bodyFontFace, color: hi ? C.background2 : C.text1, objectName: `Zitattext ${i + 1}`,
    });
    y += h + 0.09;
  });
  if (y - 0.09 > QBOTTOM) console.warn("WARNUNG: Zitate zu hoch", (y - 0.09).toFixed(2));
}
let nContent = 0;
const content = (title) => {
  const s = pres.addSlide({ masterName: "Inhalt", sectionTitle: SEC });
  s.addText(`MOTIV: VATER-SOHN-BEZIEHUNG · FOLIE ${++nContent} VON 7`, { placeholder: "kicker" });
  s.addText(title, { placeholder: "title" });
  return s;
};
const SEC = "Vater-Sohn-Beziehung";

// ===== Folie 1: Kapitel =====
pres.addSection({ title: SEC });
let s = pres.addSlide({ masterName: "Kapitel", sectionTitle: SEC });
s.addText("Motiv", { placeholder: "kicker" });
s.addText("Vater-Sohn-\nBeziehung", { placeholder: "title" });
s.addText("Macht, Schuld und Ohnmacht in „Die Verwandlung“", { placeholder: "sub" });
rule(s, 4.53, 1.62, 2.54, "Linie oben");
rule(s, 4.53, 3.68, 2.54, "Linie unten");
s.addNotes(
`[ca. 30 Sek.]
Mein Teil ist das Motiv der Vater-Sohn-Beziehung.
Man kann „Die Verwandlung“ nicht nur als Geschichte über einen Mann lesen, der zum Käfer wird, sondern auch als Machtkampf zwischen Vater und Sohn. Ich konzentriere mich auf vier Stationen: die Ausgangslage, die erste Begegnung, den Apfelwurf und Gregors Tod. Zum Schluss ziehe ich ein Fazit.

HINWEIS: Rot hinterlegte Zitate auf den Folien = im Vortrag vorlesen. Die anderen stehen als Beleg auf der Folie, müssen aber nicht gesagt werden.`);

// ===== Folie 2: Ausgangslage =====
s = content("Ausgangslage: Der Sohn als Ernährer");
points(s, [
  ["Rollentausch", "Nach dem Bankrott des Vaters ernährt Gregor die ganze Familie und zahlt die Schulden des Vaters ab.", { anchor: "Schuld der Eltern an ihn abzuzahlen" }],
  ["Pflicht statt Anerkennung", "Die Familie nimmt das Geld selbstverständlich an – echte Dankbarkeit oder Nähe gibt es nicht mehr.", { anchor: "Man hatte sich eben daran gewöhnt, sowohl die Familie, als auch Gregor, man nahm das Geld dankbar an, er lieferte es gern ab, aber eine besondere Wärme wollte sich nicht mehr ergeben." }],
  ["Der Vater verschweigt Geld", "Heimlich hat der Vater ein kleines Vermögen behalten. Gregor hätte früher kündigen können – und freut sich trotzdem.", { anchor: "daß trotz allen Unglücks ein allerdings ganz kleines Vermögen aus der alten Zeit noch vorhanden war" }],
]);
quotes(s, [
  { t: "„Wenn ich mich nicht wegen meiner Eltern zurückhielte, ich hätte längst gekündigt“", ref: "Buch", hi: true },
  { t: "„habe ich einmal das Geld beisammen, um die Schuld der Eltern an ihn abzuzahlen – es dürfte noch fünf bis sechs Jahre dauern –, mache ich die Sache unbedingt.“", ref: "Buch" },
  { t: "„man nahm das Geld dankbar an, er lieferte es gern ab, aber eine besondere Wärme wollte sich nicht mehr ergeben.“", ref: "Buch", hi: true },
  { t: "„daß trotz allen Unglücks ein allerdings ganz kleines Vermögen aus der alten Zeit noch vorhanden war“", ref: "Buch" },
  { t: "„Gregor, hinter seiner Türe, nickte eifrig, erfreut über diese unerwartete Vorsicht und Sparsamkeit.“", ref: "Buch" },
]);
s.addNotes(
`[ca. 1 Min.]
Schon vor der Verwandlung ist die Familie auf den Kopf gestellt. Das Geschäft des Vaters ist vor fünf Jahren zusammengebrochen. Seitdem ist Gregor der Ernährer: Er arbeitet als Handlungsreisender und zahlt die Schulden seines Vaters bei seinem Chef ab.
Gleich am Anfang denkt er: ROT VORLESEN → „Wenn ich mich nicht wegen meiner Eltern zurückhielte, ich hätte längst gekündigt.“ Er opfert sich für die Eltern.
Aber Dank bekommt er dafür nicht. Im zweiten Teil heißt es: ROT VORLESEN → „man nahm das Geld dankbar an, er lieferte es gern ab, aber eine besondere Wärme wollte sich nicht mehr ergeben.“ Gregor ist für die Familie nur noch der, der das Geld bringt.
Später erfährt Gregor, dass der Vater heimlich ein kleines Vermögen behalten hatte. Statt wütend zu sein, nickt er nur „eifrig“. Er kritisiert den Vater nie, nicht einmal in Gedanken.`);

// ===== Folie 3: Erste Konfrontation =====
s = content("Teil I: Der Vater als Gegner");
points(s, [
  ["Drohung von Anfang an", "Schon beim ersten Klopfen benutzt der Vater die Faust – noch bevor er Gregor überhaupt gesehen hat.", { anchor: "schon klopfte an der einen Seitentür der Vater, schwach, aber schon mit der Faust." }],
  ["Hass und Hilflosigkeit", "Beim Anblick des Käfers zeigt er Feindseligkeit und weint zugleich. Er ist überfordert, reagiert aber mit Aggression.", { anchor: "Der Vater ballte mit feindseligem Ausdruck die Faust, als wolle er Gregor in sein Zimmer zurückstoßen, sah sich dann unsicher im Wohnzimmer um, beschattete dann mit den Händen die Augen und weinte, daß sich seine mächtige Brust schüttelte." }],
  ["Gewalt statt Gespräch", "Mit Stock und Zeitung treibt er Gregor zurück. Den brutalen Stoß empfindet Gregor sogar als „erlösend“.", { anchor: "packte er mit der Rechten den Stock des Prokuristen" }],
]);
quotes(s, [
  { t: "„schon klopfte an der einen Seitentür der Vater, schwach, aber schon mit der Faust.“", ref: "Buch" },
  { t: "„Der Vater ballte mit feindseligem Ausdruck die Faust, als wolle er Gregor in sein Zimmer zurückstoßen, […] und weinte, daß sich seine mächtige Brust schüttelte.“", ref: "Buch", hi: true },
  { t: "„packte er mit der Rechten den Stock des Prokuristen […], holte mit der Linken eine große Zeitung vom Tisch“", ref: "Buch" },
  { t: "„Unerbittlich drängte der Vater und stieß Zischlaute aus, wie ein Wilder.“", ref: "Buch", hi: true },
  { t: "„da gab ihm der Vater von hinten einen jetzt wahrhaftig erlösenden starken Stoß, und er flog, heftig blutend, weit in sein Zimmer hinein.“", ref: "Buch" },
]);
s.addNotes(
`[ca. 1 Min. 15 Sek.]
Schon als Gregor nicht aufsteht, klopft der Vater „schwach, aber schon mit der Faust“.
Als er Gregor dann sieht, reagiert er so: ROT VORLESEN → „Der Vater ballte mit feindseligem Ausdruck die Faust, als wolle er Gregor in sein Zimmer zurückstoßen, sah sich dann unsicher im Wohnzimmer um, beschattete dann mit den Händen die Augen und weinte, daß sich seine mächtige Brust schüttelte.“
Der Vater ist gleichzeitig feindselig und verzweifelt – er zeigt seine Überforderung durch Aggression.
Mit Stock und Zeitung treibt er Gregor zurück ins Zimmer. ROT VORLESEN → „Unerbittlich drängte der Vater und stieß Zischlaute aus, wie ein Wilder.“ Der Vater wird hier selbst wie ein Tier beschrieben, nicht Gregor.
Den Stoß, nach dem Gregor „heftig blutend“ ins Zimmer fliegt, empfindet er sogar als „erlösend“ – so sehr hat er gelernt, sich zu unterwerfen.`);

// ===== Folie 4: Verwandlung des Vaters =====
s = content("Teil II: Die Verwandlung des Vaters");
points(s, [
  ["Vorher: schwach", "Früher lag der Vater müde im Bett oder empfing Gregor im Schlafrock – kaum fähig aufzustehen.", { anchor: "Der gleiche Mann, der müde im Bett vergraben lag" }],
  ["Nachher: Autorität", "Jetzt arbeitet er als Bankdiener, steht aufrecht in Uniform. Aus Gregors Perspektive wirkt er riesig.", { anchor: "Nun aber war er recht gut aufgerichtet" }],
  ["Macht als Wippe", "Je schwächer Gregor wird, desto stärker wird der Vater. Er legt die Uniform nicht einmal zu Hause ab.", { anchor: "Mit einer Art Eigensinn weigerte sich der Vater, auch zu Hause seine Dieneruniform abzulegen" }],
]);
quotes(s, [
  { t: "„war das noch der Vater? Der gleiche Mann, der müde im Bett vergraben lag, wenn früher Gregor zu einer Geschäftsreise ausgerückt war; der ihn an Abenden der Heimkehr im Schlafrock im Lehnstuhl empfangen hatte“", ref: "Buch", hi: true },
  { t: "„Nun aber war er recht gut aufgerichtet; in eine straffe blaue Uniform mit Goldknöpfen gekleidet, wie sie Diener der Bankinstitute tragen“", ref: "Buch", hi: true },
  { t: "„Gregor staunte über die Riesengröße seiner Stiefelsohlen.“", ref: "Buch" },
  { t: "„Mit einer Art Eigensinn weigerte sich der Vater, auch zu Hause seine Dieneruniform abzulegen“", ref: "Buch" },
]);
s.addNotes(
`[ca. 1 Min. 15 Sek.]
Im zweiten Teil verwandelt sich auch der Vater. ROT VORLESEN → „war das noch der Vater? Der gleiche Mann, der müde im Bett vergraben lag, wenn früher Gregor zu einer Geschäftsreise ausgerückt war; der ihn an Abenden der Heimkehr im Schlafrock im Lehnstuhl empfangen hatte.“
Und jetzt? ROT VORLESEN → „Nun aber war er recht gut aufgerichtet; in eine straffe blaue Uniform mit Goldknöpfen gekleidet, wie sie Diener der Bankinstitute tragen.“
Schlafrock gegen Uniform, liegen gegen aufrecht stehen. Gregor am Boden „staunte über die Riesengröße seiner Stiefelsohlen“.
Wie bei einer Wippe: Je schwächer Gregor, desto stärker der Vater. Ironisch ist: Es ist eine Dieneruniform – draußen ist er Diener, zu Hause Herrscher.`);

// ===== Folie 5: Apfelwurf =====
s = content("Teil II: Der Apfelwurf");
points(s, [
  ["Vorurteil", "Der Vater fragt nicht nach, sondern unterstellt Gregor sofort eine Gewalttat.", { anchor: "»Ich habe es ja erwartet«, sagte der Vater, »ich habe es euch ja immer gesagt, aber ihr Frauen wollt nicht hören.«" }],
  ["Geplanter Angriff", "Er füllt sich die Taschen und „bombardiert“ den Sohn – es ist kein Ausrutscher, sondern ein Entschluss.", { anchor: "Aus der Obstschale auf der Kredenz hatte er sich die Taschen gefüllt und warf nun, ohne vorläufig scharf zu zielen, Apfel für Apfel." }],
  ["Die tödliche Wunde", "Der Apfel bleibt im Rücken stecken, verfault und schwächt Gregor bis zum Tod. Der Vater ist damit mitverantwortlich.", { anchor: "Den verfaulten Apfel in seinem Rücken und die entzündete Umgebung" }],
]);
quotes(s, [
  { t: "„»Ich habe es ja erwartet«, sagte der Vater, »ich habe es euch ja immer gesagt, aber ihr Frauen wollt nicht hören.«“", ref: "Buch" },
  { t: "„der Vater hatte sich entschlossen, ihn zu bombardieren.“", ref: "Buch", hi: true },
  { t: "„Ein ihm sofort nachfliegender drang dagegen förmlich in Gregors Rücken ein“", ref: "Buch", hi: true },
  { t: "„der Apfel blieb, da ihn niemand zu entfernen wagte, als sichtbares Andenken im Fleische sitzen“", ref: "Buch", hi: true },
  { t: "„Den verfaulten Apfel in seinem Rücken und die entzündete Umgebung […] spürte er schon kaum.“", ref: "Buch" },
]);
s.addNotes(
`[ca. 1 Min. 15 Sek.]
Der Höhepunkt der Gewalt ist der Apfelwurf. Der Vater denkt sofort das Schlimmste: „Ich habe es ja erwartet.“ Er fragt nicht nach.
Dann heißt es: ROT VORLESEN → „der Vater hatte sich entschlossen, ihn zu bombardieren.“ Das Wort „entschlossen“ ist wichtig: Es ist kein Reflex, sondern eine Entscheidung.
ROT VORLESEN → „Ein ihm sofort nachfliegender drang dagegen förmlich in Gregors Rücken ein.“
Und dieser Apfel bleibt dort. ROT VORLESEN → „der Apfel blieb, da ihn niemand zu entfernen wagte, als sichtbares Andenken im Fleische sitzen.“ Der Apfel verfault und schwächt Gregor bis zum Tod.
Der Apfel erinnert an den Sündenfall – Schuld und Strafe. Der Vater bestraft den Sohn für eine Schuld, die er nicht hat, und ist damit am Tod mitschuldig.`);

// ===== Folie 6: Urteil und Tod =====
s = content("Teil III: Das Urteil");
points(s, [
  ["Der Vater stimmt zu", "Die Schwester fordert, „es“ loszuwerden. Der Vater gibt ihr sofort recht – Gregor ist für ihn kein Sohn mehr.", { anchor: "»Sie hat tausendmal Recht,« sagte der Vater für sich." }],
  ["Gregor unterwirft sich", "Bis zuletzt denkt Gregor voller Liebe an die Familie und akzeptiert, dass er verschwinden muss.", { anchor: "An seine Familie dachte er mit Rührung und Liebe zurück." }],
  ["Erleichterung", "Nach Gregors Tod dankt der Vater Gott, wirft die Zimmerherren hinaus und ist wieder Herr im Haus.", { anchor: "»Verlassen Sie sofort meine Wohnung!« sagte Herr Samsa" }],
]);
quotes(s, [
  { t: "„wir müssen versuchen, es loszuwerden.“ – „»Sie hat tausendmal Recht,« sagte der Vater für sich.“", ref: "Buch", hi: true },
  { t: "„»Wenn er uns verstünde,« sagte der Vater halb fragend“", ref: "Buch" },
  { t: "„An seine Familie dachte er mit Rührung und Liebe zurück. Seine Meinung darüber, daß er verschwinden müsse, war womöglich noch entschiedener, als die seiner Schwester.“", ref: "Buch", hi: true },
  { t: "„»Nun,« sagte Herr Samsa, »jetzt können wir Gott danken.«“", ref: "Buch", hi: true },
  { t: "„»Verlassen Sie sofort meine Wohnung!« sagte Herr Samsa“", ref: "Buch" },
]);
s.addNotes(
`[ca. 1 Min. 15 Sek.]
Im dritten Teil fällt das Urteil. Nach dem Geigenabend sagt die Schwester: „wir müssen versuchen, es loszuwerden.“ Und der Vater? ROT VORLESEN → „Sie hat tausendmal Recht, sagte der Vater für sich.“ Für ihn ist Gregor nur noch „es“.
Und Gregor wehrt sich nicht. In seiner letzten Nacht heißt es: ROT VORLESEN → „An seine Familie dachte er mit Rührung und Liebe zurück. Seine Meinung darüber, daß er verschwinden müsse, war womöglich noch entschiedener, als die seiner Schwester.“ Gregor übernimmt das Urteil über sich selbst – völlige Unterwerfung.
Als Gregor tot ist, sagt der Vater: ROT VORLESEN → „Nun, jetzt können wir Gott danken.“ Kein Wort der Trauer. Danach wirft er die Zimmerherren hinaus: „Verlassen Sie sofort meine Wohnung!“ Der Vater ist wieder das Oberhaupt der Familie.`);

// ===== Folie 7: Fazit =====
s = content("Fazit");
points(s, [
  ["Opfer ohne Anerkennung", "Gregor trägt die Familie und die Schulden des Vaters – doch er bleibt für sie nur der Geldverdiener.", { anchor: "eine besondere Wärme wollte sich nicht mehr ergeben" }],
  ["Gewalt und Machtwechsel", "Mit jeder Konfrontation wird der Vater stärker und gewalttätiger, Gregor schwächer – bis zur tödlichen Wunde.", { anchor: "der Vater hatte sich entschlossen, ihn zu bombardieren." }],
  ["Familie als Pflicht", "Gregor wird nur noch geduldet. Am Ende stellt sich der Vater wieder selbst in den Mittelpunkt.", { anchor: "Gebot der Familienpflicht" }],
]);
quotes(s, [
  { t: "„dem gegenüber es das Gebot der Familienpflicht war, den Widerwillen hinunterzuschlucken und zu dulden, nichts als zu dulden.“", ref: "Buch" },
  { t: "„»Also kommt doch her. Laßt schon endlich die alten Sachen. Und nehmt auch ein wenig Rücksicht auf mich.«“", ref: "Buch", hi: true },
]);
s.addShape(pres.shapes.RECTANGLE, { x: QX, y: 3.55, w: QW, h: 1.3, objectName: "Kernaussage Kasten", fill: { color: C.accent1, transparency: 0 }, line: { type: "none" } });
txt(s, "Die Verwandlung zeigt, wie ein Sohn an der Härte und fehlenden Anerkennung seines Vaters zerbricht.", {
  x: QX + 0.2, y: 3.55, w: QW - 0.4, h: 1.3, valign: "middle", fontSize: 16, bold: true, italic: true, color: C.background2, objectName: "Kernaussage",
});
s.addNotes(
`[ca. 1 Min.]
Zum Schluss mein Fazit in drei Punkten.
Erstens: Gregor opfert sich für seine Familie und trägt sogar die Schulden des Vaters. Anerkennung bekommt er dafür nicht, er ist nur noch der, der das Geld bringt.
Zweitens: Mit jeder Konfrontation wird der Vater stärker und gewalttätiger, während Gregor immer schwächer wird – bis zur tödlichen Wunde durch den Apfel.
Drittens: Gregor ist für die Familie nur noch eine Pflicht. Im Text heißt es, man müsse „den Widerwillen hinunterzuschlucken und zu dulden, nichts als zu dulden“. Und ganz am Ende, nach Gregors Tod, sagt der Vater: ROT VORLESEN → „Also kommt doch her. Laßt schon endlich die alten Sachen. Und nehmt auch ein wenig Rücksicht auf mich.“ Der Sohn ist vergessen, und der Vater stellt sich selbst wieder in den Mittelpunkt.
Die Vater-Sohn-Beziehung zeigt also, wie ein Sohn an der Härte und fehlenden Anerkennung seines Vaters zerbricht. Vielen Dank!`);

// ===== Folie 8: Quellen (wird selbst ausgefüllt) =====
s = content("Quellen");
s.addNotes("Quellen bitte selbst eintragen. Tipp: Die Zeilenangaben (Z.) beziehen sich auf die zeilennummerierte Textgrundlage (Textgrundlage_Die_Verwandlung_mit_Zeilen.pdf) – Text der Erstausgabe 1915 nach Projekt Gutenberg, E-Book Nr. 22367.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
