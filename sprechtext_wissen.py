"""Erzeugt zwei PDFs für das Referat (Motiv Vater-Sohn-Beziehung):

  - Sprechtext_Vater-Sohn-Beziehung.pdf : ausformulierter Sprechtext je Folie (ca. 7 Min.)
  - Wissen_Die_Verwandlung.pdf          : Hintergrundwissen zur ganzen Erzählung

Seiten-/Zeilenangaben (S. …, Z. …) beziehen sich auf Textgrundlage_Die_Verwandlung_mit_Zeilen.pdf.
Aufruf: python3 sprechtext_wissen.py
"""
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

# ---------------------------------------------------------------- Sprechtext
# [[...]] = rot markiertes Zitat zum Vorlesen; **...** = Schlüsselwort fett
SPRECH = [
    ("Folie 1 – Vater-Sohn-Beziehung", "ca. 20 Sek.", [
        "Ich stelle euch das **Motiv der Vater-Sohn-Beziehung** vor – ein Thema, das sich durch alle drei Teile der Erzählung zieht.",
        "Meine These lautet: „Die Verwandlung“ ist nicht nur die Geschichte eines Mannes, der zum Käfer wird, sondern auch ein **Machtkampf zwischen Vater und Sohn**.",
        "Ich zeige euch erst die Ausgangslage, dann die Konfrontationen aus den drei Teilen und am Ende mein Fazit.",
    ]),
    ("Folie 2 – Ausgangslage: Der Sohn als Ernährer", "ca. 50 Sek.", [
        "Schon vor der Verwandlung steht die Familie auf dem Kopf: Das Geschäft des Vaters ist pleite, und **Gregor ist der Ernährer**. Er zahlt die Schulden des Vaters ab und bleibt in seinem verhassten Job nur wegen seiner Eltern.",
        "Aber wird Gregor dafür geschätzt? Im Text heißt es:",
        "[[„man nahm das Geld dankbar an, er lieferte es gern ab, aber eine besondere Wärme wollte sich nicht mehr ergeben.“ (S. 18, Z. 33 ff.)]]",
        "Aus Dankbarkeit ist **Gewohnheit** geworden – Gregor ist nur noch die Geldquelle.",
        "Später erfährt Gregor, dass der Vater **heimlich ein kleines Vermögen** behalten hatte – Gregor hätte früher kündigen können. Trotzdem nickt er nur „eifrig“. Er kritisiert den Vater nicht einmal in Gedanken.",
    ]),
    ("Folie 3 – Teil I: Der Vater als Gegner", "ca. 1 Min.", [
        "Schon am ersten Morgen klopft der Vater „schwach, aber schon **mit der Faust**“ – eine Drohung, bevor er überhaupt weiß, was los ist.",
        "Als er Gregor dann sieht, ballt er „mit feindseligem Ausdruck die Faust“ – und weint im nächsten Moment. Der Vater ist **überfordert, reagiert aber mit Aggression**.",
        "Mit Stock und Zeitung treibt er Gregor zurück ins Zimmer:",
        "[[„Unerbittlich drängte der Vater und stieß Zischlaute aus, wie ein Wilder.“ (S. 13, Z. 3 f.)]]",
        "Eigentlich ist Gregor das Tier – aber hier wird **der Vater wie ein Tier** beschrieben.",
        "Den Stoß, nach dem Gregor „heftig blutend“ ins Zimmer fliegt, empfindet er sogar als „**erlösend**“ – so sehr hat er gelernt, sich unterzuordnen.",
    ]),
    ("Folie 4 – Teil II: Die Verwandlung des Vaters", "ca. 1 Min.", [
        "Im zweiten Teil verwandelt sich **auch der Vater**. Früher lag er müde im Bett oder saß im Schlafrock im Lehnstuhl. Jetzt heißt es:",
        "[[„Nun aber war er recht gut aufgerichtet; in eine straffe blaue Uniform mit Goldknöpfen gekleidet, wie sie Diener der Bankinstitute tragen“ (S. 26, Z. 30 ff.)]]",
        "**Schlafrock gegen Uniform**, Liegen gegen aufrechtes Stehen. Gregor am Boden „staunte über die Riesengröße seiner Stiefelsohlen“ – er sieht den Vater von unten, übermächtig.",
        "Wie bei einer **Wippe**: Je schwächer Gregor, desto stärker der Vater. Ironisch ist: Es ist eine **Diener**uniform – draußen ist er Diener, zu Hause Herrscher.",
    ]),
    ("Folie 5 – Teil II: Der Apfelwurf", "ca. 1 Min.", [
        "Diese Stärke zeigt der Vater beim Apfelwurf. Die Mutter ist ohnmächtig, und der Vater urteilt sofort, ohne nachzufragen: „Ich habe es ja erwartet.“ Dann heißt es:",
        "[[„der Vater hatte sich entschlossen, ihn zu bombardieren.“ (S. 27, Z. 18 f.)]]",
        "Zwei Wörter sind wichtig: „**entschlossen**“ zeigt, dass es eine Entscheidung ist und kein Reflex. Und „**bombardieren**“ ist Kriegssprache – der Vater behandelt seinen Sohn wie einen Feind.",
        "Ein Apfel bleibt in Gregors Rücken stecken, verfault und schwächt ihn **bis zu seinem Tod**. Die Mutter muss sogar um Gregors Leben bitten.",
        "Der Apfel erinnert an den **Sündenfall** – Schuld und Strafe. Gregor wird für eine Schuld bestraft, die er nicht hat. Der Vater ist damit mitschuldig an seinem Tod.",
    ]),
    ("Folie 6 – Teil III: Das Urteil", "ca. 1 Min.", [
        "Im dritten Teil fällt das Urteil. Nach dem Geigenabend sagt die Schwester: „wir müssen versuchen, es loszuwerden.“ Gregor ist nur noch „**es**“. Der Vater antwortet: „Sie hat tausendmal Recht.“",
        "Gregor wehrt sich nicht, denkt „mit Rührung und Liebe“ an die Familie und stirbt in derselben Nacht. Und der Vater?",
        "[[„»Nun,« sagte Herr Samsa, »jetzt können wir Gott danken.«“ (S. 38, Z. 41)]]",
        "**Kein Wort der Trauer.** Auffällig: Ab Gregors Tod heißt er im Text nur noch „**Herr Samsa**“, nie mehr „der Vater“ – die Vaterrolle ist ausgelöscht. Danach wirft er die Zimmerherren raus und ist wieder Herr im Haus.",
    ]),
    ("Folie 7 – Fazit", "ca. 50 Sek.", [
        "Mein Fazit: Gregor opfert sich **ohne Anerkennung**. Der Vater wird mit jeder Konfrontation **stärker und gewalttätiger**, Gregor schwächer. Und am Ende ist Gregor nur noch eine **Pflicht**, die man „zu dulden, nichts als zu dulden“ hat.",
        "Ganz am Ende, als Gregor tot ist, sagt der Vater:",
        "[[„»Also kommt doch her. Laßt schon endlich die alten Sachen. Und nehmt auch ein wenig Rücksicht auf mich.«“ (S. 40, Z. 37 f.)]]",
        "„Rücksicht auf **mich**“ – der Sohn ist kaum tot, und der Vater stellt sich wieder in den Mittelpunkt.",
        "Die Vater-Sohn-Beziehung zeigt also, wie ein Sohn an der **Härte und fehlenden Anerkennung seines Vaters zerbricht**. Vielen Dank fürs Zuhören!",
    ]),
    ("Folie 8 – Quellen", "nur zeigen", [
        "Folie kurz zeigen, nichts vorlesen.",
    ]),
]

# ---------------------------------------------------------------- Wissen
WISSEN = [
    ("Steckbrief", [
        ("Autor", "Franz Kafka (1883–1924), deutschsprachiger Schriftsteller aus Prag, im Hauptberuf Jurist bei einer Versicherung. Er starb 1924 an Tuberkulose."),
        ("Werk", "„Die Verwandlung“, eine Erzählung (oft auch als Novelle bezeichnet: Im Mittelpunkt steht eine „unerhörte Begebenheit“, die Verwandlung)."),
        ("Entstehung", "Geschrieben Ende 1912, veröffentlicht 1915."),
        ("Epoche", "Literarische Moderne. Kafka ist keiner Epoche eindeutig zuzuordnen, steht aber dem Expressionismus nahe (Themen wie Entfremdung, Angst, Identitätsverlust)."),
        ("Aufbau", "Drei Teile (I, II, III). Teil I und II enden jeweils mit Gewalt des Vaters, Teil III mit Gregors Tod und dem Ausflug der Familie."),
        ("Ort", "Die Wohnung der Familie Samsa in einer Stadt, vor allem Gregors Zimmer."),
        ("Zeit", "Wenige Monate: Weihnachten ist schon „vorüber“ (S. 34, Z. 29), Gregor stirbt „Ende März“ (S. 39, Z. 5)."),
        ("Erster Satz", "„Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.“ (S. 1, Z. 1)"),
    ]),
    ("Inhalt in Kürze", [
        ("Teil I", "Gregor wacht als Käfer auf und verpasst seinen Zug. Die Familie klopft, der Prokurist kommt in die Wohnung. Als Gregor die Tür öffnet, flieht der Prokurist entsetzt. Der Vater treibt Gregor mit Stock und Zeitung zurück ins Zimmer. Gregor verletzt sich in der Tür."),
        ("Teil II", "Grete versorgt Gregor mit Essen, die Milch, früher sein Lieblingsgetränk, schmeckt ihm nicht mehr (S. 14, Z. 23 f.). Der Vater erklärt die Finanzen, dabei kommt das heimliche Vermögen heraus. Gregor kriecht an Wänden und Decke. Mutter und Grete räumen sein Zimmer aus, Gregor klammert sich an das Bild der Dame im Pelz. Die Mutter wird ohnmächtig, der Vater bewirft Gregor mit Äpfeln."),
        ("Teil III", "Die Apfelwunde schwächt Gregor. Die Familie arbeitet jetzt: der Vater als Bankdiener, die Mutter näht Wäsche, Grete wird Verkäuferin (S. 28, Z. 19 f.). Drei Zimmerherren ziehen ein. Beim Geigenspiel von Grete kriecht Gregor hervor, die Zimmerherren kündigen. Grete fordert, „es“ loszuwerden, der Vater stimmt zu. Gregor stirbt in der Nacht. Die Familie macht einen Ausflug ins Grüne und plant eine kleinere Wohnung und einen Mann für Grete."),
    ]),
    ("Figuren", [
        ("Gregor Samsa", "Handlungsreisender für Tuchwaren, Ernährer der Familie, pflichtbewusst und unterwürfig. Er verwandelt sich in ein „Ungeziefer“, denkt aber weiter wie ein Mensch."),
        ("Der Vater (Herr Samsa)", "Früher Geschäftsmann, nach dem Bankrott träge. Nach der Verwandlung wird er Bankdiener in Uniform, autoritär und gewalttätig (Stock, Apfelwurf). Nach Gregors Tod heißt er im Text nur noch „Herr Samsa“."),
        ("Die Mutter", "Liebt Gregor, ist aber schwach (Asthma) und fällt beim Anblick Gregors in Ohnmacht. Sie bittet den Vater um Schonung von Gregors Leben."),
        ("Grete", "Die 17-jährige Schwester. Anfangs versorgt sie Gregor als Einzige, später fordert gerade sie, „es“ loszuwerden. Am Ende blüht sie auf. Gregor wollte sie heimlich aufs Konservatorium schicken (S. 18, Z. 40)."),
        ("Prokurist", "Gregors Vorgesetzter. Er steht für die harte Arbeitswelt und flieht beim Anblick Gregors."),
        ("Zimmerherren", "Drei Untermieter mit Vollbärten (S. 31, Z. 45 f.). Die Familie ordnet sich ihnen unter, bis der Vater sie hinauswirft."),
        ("Bedienerin", "Eine „alte Witwe“ (S. 31, Z. 7 f.), die keine Angst vor Gregor hat. Sie entdeckt seine Leiche und „entsorgt“ ihn."),
    ]),
    ("Wichtige Motive und Symbole", [
        ("Verwandlung / Ungeziefer", "Gregor wird zu etwas „Unnützem“. So wird sichtbar, wie die Familie ihn eigentlich sieht: Er zählt nur, solange er nützlich ist. Kafka wollte nicht, dass das Insekt auf dem Buchumschlag abgebildet wird. Es soll unbestimmt bleiben."),
        ("Vater-Sohn-Beziehung", "Dein Thema: Machtkampf, Gewalt, Schuld, Unterwerfung (siehe Sprechtext)."),
        ("Isolation und Entfremdung", "Gregor ist im Zimmer eingesperrt, niemand versteht ihn („Das war eine Tierstimme“, S. 8, Z. 38 f.). Er ist schon vor der Verwandlung einsam (Reisen, keine echten Freunde)."),
        ("Arbeit und Geld", "Der Mensch als Funktion: Gregors Wert hängt an seinem Einkommen. Als er nicht mehr arbeiten kann, ist er „wertlos“."),
        ("Tür und Zimmer", "Die Tür trennt Gregor von der Familie. Sie wird geöffnet, zugeschlagen oder abgeschlossen, je nachdem, wie die Familie zu ihm steht. Das Zimmer wird erst Rückzugsort, dann Abstellkammer, dann Gefängnis."),
        ("Der Apfel", "Waffe des Vaters und Symbol für Schuld und Strafe (Sündenfall). Er bleibt als „sichtbares Andenken“ im Rücken stecken und verfault."),
        ("Die Uniform", "Zeichen von Macht und Ordnung. Früher hing Gregor als Leutnant in Uniform an der Wand (S. 10, Z. 28 f.), jetzt trägt der Vater Uniform. Die Macht hat gewechselt."),
        ("Musik / Geige", "Gretes Geigenspiel berührt Gregor tief: „War er ein Tier, da ihn Musik so ergriff?“ (S. 34, Z. 13 f.). Es zeigt seine Menschlichkeit, löst aber das Ende aus."),
        ("Essen", "Gregor verliert den Appetit auf Menschliches und am Ende auf alles. Sein Verhungern zeigt den seelischen und körperlichen Verfall."),
        ("Das Bild der Dame im Pelz", "Gregor klammert sich daran, als das Zimmer ausgeräumt wird (S. 1, Z. 17 f.). Es ist das Letzte, was ihn mit seinem menschlichen Leben verbindet."),
        ("Licht / Frühling am Ende", "Gregor stirbt bei Tagesanbruch, danach scheint die Sonne, die Familie fährt ins Grüne und Grete „dehnt ihren jungen Körper“ (S. 41, Z. 13 f.). Für die Familie ist es ein Neubeginn, für Gregor bitter."),
    ]),
    ("Erzählweise und Sprache", [
        ("Erzähler", "Er-Erzähler mit personaler Perspektive: Wir erleben fast alles durch Gregors Augen. Nach seinem Tod wechselt der Blick zur Familie."),
        ("Sachlicher Stil", "Das Unglaubliche wird nüchtern und ohne Erklärung erzählt, wie etwas Alltägliches. Gerade das wirkt verstörend."),
        ("Groteske und Ironie", "Komik und Grauen gleichzeitig: Gregor sorgt sich als Käfer zuerst um seinen Zug und seinen Job."),
        ("Kafkaesk", "Das Wort beschreibt eine ausweglose, rätselhafte, bedrückende Situation, die nüchtern hingenommen wird. Es ist nach Kafka benannt."),
    ]),
    ("Deutungsansätze (gut für Diskussionsfragen)", [
        ("Biografisch", "Kafka hatte selbst einen dominanten Vater. In seinem „Brief an den Vater“ (1919, nie übergeben) schreibt er: „Mein Schreiben handelte von Dir“. Außerdem erzählt er dort, dass der Vater einen Freund von ihm „mit Ungeziefer“ verglichen hat."),
        ("Psychologisch", "Die Verwandlung als Bild für Schuldgefühle, Minderwertigkeit und den Konflikt mit dem Vater."),
        ("Sozialkritisch", "Kritik an einer Arbeitswelt, in der der Mensch nur als Arbeitskraft zählt. Gregor ist „entfremdet“ von sich selbst."),
        ("Existenzialistisch", "Der Mensch in einer sinnlosen, unerklärlichen Welt. Die Verwandlung wird nie erklärt, Gregor muss sie einfach hinnehmen."),
        ("Religiös", "Der Apfel erinnert an den Sündenfall, Gregor kann man als Opfer sehen, das für die Familie „stirbt“. Nach seinem Tod bekreuzigen sich alle."),
    ]),
    ("Typische Fragen zur ganzen Geschichte", [
        ("Warum verwandelt sich Gregor?", "Der Text erklärt es nie. Das ist Absicht. Man kann es deuten: als Bild für Gregors Gefühl, nutzlos und „Ungeziefer“ zu sein, oder als Folge seines Lebens, das nur aus Pflicht und Arbeit bestand."),
        ("Warum gerade ein Käfer / Ungeziefer?", "Ungeziefer ist lästig, eklig und „unnütz“. Das ist genau das, was Gregor für die Familie wird, sobald er kein Geld mehr bringt."),
        ("Wer ist schuld an Gregors Tod?", "Mehrere: der Vater (Apfelwunde, Gewalt), die Familie (Vernachlässigung, Urteil), aber auch Gregor selbst, der sich aufgibt. Eine differenzierte Antwort ist am besten."),
        ("Wie verändert sich die Familie?", "Sie wird selbstständig: Alle arbeiten, der Vater wird wieder stark, Grete erwachsen. Gregors „Opfer“ macht die Familie lebendig. Das ist bittere Ironie."),
        ("Warum wehrt sich Gregor nie?", "Er hat Pflicht und Unterordnung verinnerlicht. Selbst Gewalt empfindet er als „erlösend“, und am Ende stimmt er seinem eigenen Verschwinden zu."),
        ("Ist das Ende hoffnungsvoll?", "Für die Familie ja (Frühling, Sonne, Zukunftspläne), für Gregor nein. Diese Gegensätzlichkeit ist typisch für Kafka."),
    ]),
    ("Wichtige Begriffe", [
        ("Motiv", "Ein inhaltliches Element, das in einem Werk immer wiederkehrt, z. B. die Vater-Sohn-Beziehung."),
        ("Symbol", "Ein Gegenstand mit tieferer Bedeutung, z. B. der Apfel für Schuld und Strafe."),
        ("Novelle", "Kürzere Erzählung um ein unerhörtes Ereignis mit Wendepunkt."),
        ("Personales Erzählen", "Der Erzähler erzählt in der Er-Form, aber aus der Sicht einer Figur."),
        ("Groteske", "Verbindung von Komischem und Grauenhaftem."),
    ]),
]

CSS = """
@page { size: A4; margin: 15mm 15mm; }
body { font-family: 'DejaVu Serif', Georgia, serif; color: #1E1812; font-size: 10.8pt; line-height: 1.5; }
h1 { font-size: 20pt; margin: 0 0 2pt; }
.sub { color: #5C4B3A; margin: 0 0 12pt; font-size: 9.5pt; }
h2 { font-size: 13.5pt; color: #6B1F1A; margin: 14pt 0 5pt; border-bottom: 1px solid #C9BBA3; padding-bottom: 3pt; break-after: avoid; }
.zeit { float: right; font-size: 9.5pt; color: #5C4B3A; font-weight: normal; margin-top: 3pt; }
p { margin: 0 0 6pt; }
p.rot { color: #6B1F1A; font-weight: bold; font-style: italic; background: #F6EEEA; border-left: 3px solid #6B1F1A; padding: 4pt 8pt; }
.hinweis { background: #F3EEE4; border: 1px solid #DDD2BF; padding: 6pt 9pt; font-size: 9.8pt; margin-bottom: 10pt; }
dl { margin: 0; }
dt { font-weight: bold; margin-top: 5pt; color: #3B3128; }
dd { margin: 0 0 2pt 12pt; }
.folie { break-inside: avoid-page; }
"""


def inline(s):
    s = html.escape(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def to_pdf(html_text, html_path, pdf_path):
    html_path.write_text(html_text, encoding="utf-8")
    js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(process.argv[1]);
  await p.pdf({ path: process.argv[2], format: 'A4', printBackground: true,
    margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' } });
  await b.close();
})();
"""
    subprocess.run(["node", "-e", js, html_path.resolve().as_uri(), str(pdf_path)], check=True)


# Sprechtext
words = 0
body = ["<h1>Sprechtext: Motiv Vater-Sohn-Beziehung</h1>",
        "<p class='sub'>Franz Kafka: Die Verwandlung – Julian Sickinger · Dauer ca. 6–6½ Minuten</p>",
        "<div class='hinweis'><b>So benutzt du den Text:</b> Die <span style='color:#6B1F1A;font-weight:bold'>roten Zitate</span> liest du wörtlich vor, langsam und mit kurzer Pause davor. Den Rest kannst du frei mit eigenen Worten sagen. Die <b>fetten Wörter</b> sind die Kernbegriffe, die du betonen solltest. Seiten- und Zeilenangaben beziehen sich auf die nummerierte Textgrundlage.</div>"]
for titel, zeit, absaetze in SPRECH:
    body.append(f"<div class='folie'><h2>{html.escape(titel)} <span class='zeit'>{html.escape(zeit)}</span></h2>")
    for a in absaetze:
        words += len(re.sub(r"\(S\. [^)]*\)", "", a).split())
        if a.startswith("[["):
            body.append(f"<p class='rot'>🔴 {inline(a[2:-2])}</p>")
        else:
            body.append(f"<p>{inline(a)}</p>")
    body.append("</div>")
minutes = f"{words / 115:.1f}–{words / 105:.1f}"
body.insert(2, f"<p class='sub'>Umfang: ca. {words} Wörter ≈ {minutes} Minuten mit Pausen vor den Zitaten</p>")
doc = f"<!doctype html><html lang='de'><head><meta charset='utf-8'><title>Sprechtext</title><style>{CSS}</style></head><body>{''.join(body)}</body></html>"
to_pdf(doc, ROOT / "Sprechtext_Vater-Sohn-Beziehung.html", ROOT / "Sprechtext_Vater-Sohn-Beziehung.pdf")

# Wissen
body = ["<h1>Wissen: Die Verwandlung</h1>",
        "<p class='sub'>Alles Wichtige zur Erzählung, zu Figuren, Motiven und Deutungen · Angaben (S., Z.) nach der nummerierten Textgrundlage</p>"]
for titel, eintraege in WISSEN:
    body.append(f"<h2>{html.escape(titel)}</h2><dl>")
    for k, v in eintraege:
        body.append(f"<dt>{inline(k)}</dt><dd>{inline(v)}</dd>")
    body.append("</dl>")
doc = f"<!doctype html><html lang='de'><head><meta charset='utf-8'><title>Wissen</title><style>{CSS}</style></head><body>{''.join(body)}</body></html>"
to_pdf(doc, ROOT / "Wissen_Die_Verwandlung.html", ROOT / "Wissen_Die_Verwandlung.pdf")
print(f"Sprechtext: {words} Wörter ≈ {minutes} Min.")
