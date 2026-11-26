"""Vorbereitung für das Referat: Hintergrund, Sprechtext in Stichpunkten und mögliche Lehrerfragen je Folie.

Erzeugt:
  - Vorbereitung_Vater-Sohn-Beziehung.pdf  (zum Lernen, gut lesbar auf dem Handy)
  - Vorbereitung_Vater-Sohn-Beziehung.html (Zwischenstufe für das PDF)
  - notizen.json                           (Stichpunkte für die Notizen der Folien, liest build_deck.js)

Alle Seiten-/Zeilenangaben beziehen sich auf Textgrundlage_Die_Verwandlung_mit_Zeilen.pdf.
Aufruf: python3 vorbereitung.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
ROT = "🔴 VORLESEN:"

GRUNDWISSEN = [
    "<b>Franz Kafka</b> (1883–1924), deutschsprachiger Schriftsteller aus Prag, im Hauptberuf Jurist bei einer Versicherung.",
    "<b>„Die Verwandlung“</b> ist eine Erzählung. Geschrieben Ende 1912, veröffentlicht 1915.",
    "<b>Aufbau:</b> drei Teile (I, II, III). Teil I und Teil II enden jeweils mit Gewalt des Vaters (der Stoß in Teil I, der Apfelwurf in Teil II). In Teil III stirbt Gregor.",
    "<b>Figuren:</b> Gregor Samsa (Handlungsreisender für Tuchwaren, S. 1, Z. 13), der Vater (Herr Samsa), die Mutter, die Schwester Grete (17 Jahre), der Prokurist (Gregors Vorgesetzter), drei Zimmerherren, die Bedienerin.",
    "<b>Erzähler:</b> Er-Erzähler, der fast nur aus Gregors Sicht erzählt (personales Erzählen). Wir sehen den Vater also immer durch Gregors Augen. Nach Gregors Tod wechselt die Sicht zur Familie.",
    "<b>Motiv</b> = ein Thema bzw. inhaltliches Element, das sich durch das ganze Werk zieht und immer wieder auftaucht. Die Vater-Sohn-Beziehung taucht in allen drei Teilen an den entscheidenden Stellen auf.",
    "<b>Erster Satz</b> (S. 1, Z. 1): „Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.“",
]

TIPPS = [
    "Nicht ablesen, sondern die Stichpunkte als Gedächtnisstütze nutzen. Nur die roten Zitate liest du wörtlich vor.",
    "Vor jedem roten Zitat kurz Pause machen, langsam vorlesen, danach wieder Blickkontakt mit der Klasse.",
    "Bei jedem Zitat auf die Folie zeigen: „Hier rechts im Kasten seht ihr …“",
    "Die Überleitungssätze (→) laut sagen. Sie verbinden die Folien und lassen den Vortrag flüssig wirken.",
    "Wenn du eine Frage nicht sicher beantworten kannst: „Das ist eine gute Frage – ich würde sagen …“ und dann mit einer Textstelle begründen.",
]

FOLIEN = [
    {
        "titel": "Folie 1 – Vater-Sohn-Beziehung (Titel)",
        "zeit": "ca. 30 Sek.",
        "hintergrund": [
            "Du stellst ein <b>Motiv</b> vor, also kein einzelnes Kapitel, sondern etwas, das sich durch die ganze Erzählung zieht.",
            "Deine Hauptthese: Die Erzählung ist nicht nur die Geschichte eines Käfers, sondern ein <b>Machtkampf zwischen Vater und Sohn</b>.",
            "Stark für die Einleitung: Die ersten beiden Teile enden jeweils mit einer Gewalttat des Vaters.",
        ],
        "sprechtext": [
            "„Ich stelle euch das Motiv der Vater-Sohn-Beziehung vor.“",
            "Ein Motiv ist ein Thema, das immer wieder auftaucht. Und der Vater taucht in jedem Teil genau an den entscheidenden Stellen auf.",
            "These: „Die Verwandlung ist nicht nur die Geschichte von einem Mann, der zum Käfer wird, sondern ein Machtkampf zwischen Vater und Sohn.“",
            "Ablauf ankündigen: erst die Ausgangslage, dann die Konfrontationen aus Teil I, II und III, zum Schluss mein Fazit.",
            "→ Überleitung: „Fangen wir damit an, wie die Familie vor der Verwandlung aussah.“",
        ],
        "fragen": [
            ("Was ist ein Motiv?",
             "Ein Motiv ist ein inhaltliches Element, das in einem Werk immer wiederkehrt und eine Bedeutung trägt. Hier: das Verhältnis von Vater und Sohn, das in allen drei Teilen vorkommt."),
            ("Warum ist gerade dieses Motiv so wichtig?",
             "Weil die Höhepunkte der Erzählung Vater-Szenen sind: Teil I endet mit dem Stoß des Vaters, Teil II mit dem Apfelwurf, in Teil III stimmt der Vater dem Urteil zu und Gregor stirbt."),
        ],
    },
    {
        "titel": "Folie 2 – Ausgangslage: Der Sohn als Ernährer",
        "zeit": "ca. 1 Min.",
        "hintergrund": [
            "Das Geschäft des Vaters ist vor fünf Jahren zusammengebrochen (S. 18, Z. 9 f.).",
            "Gregor hat daraufhin „mit ganz besonderem Feuer“ gearbeitet und ist Reisender geworden. Am Anfang war die Familie „erstaunt und beglückt“, es „waren schöne Zeiten“ (S. 18, Z. 27 ff.).",
            "Er bezahlt die Schulden des Vaters bei seinem Chef und will in fünf bis sechs Jahren kündigen (S. 2, Z. 18 ff.).",
            "Später erfährt Gregor, dass der Vater heimlich ein kleines Vermögen behalten hat (S. 19, Z. 12 f.). Mit dem Geld wäre der Tag, an dem Gregor kündigen könnte, „weit näher gewesen“ (S. 19, Z. 22 ff.). Trotzdem denkt Gregor, es sei „zweifellos besser so“ (S. 19, Z. 24 f.).",
        ],
        "sprechtext": [
            "Vor der Verwandlung ist die Familie schon auf den Kopf gestellt: Der Vater ist pleite, der Sohn ernährt alle.",
            "Gregor zahlt die Schulden des Vaters ab. Er hasst seinen Job und bleibt nur wegen der Eltern (auf das erste Zitat zeigen, nicht vorlesen).",
            "Frage an die Klasse stellen: „Wird er dafür geschätzt?“",
            f"{ROT} „man nahm das Geld dankbar an, er lieferte es gern ab, aber eine besondere Wärme wollte sich nicht mehr ergeben.“ (S. 18, Z. 33 ff.)",
            "Deuten: Aus Dankbarkeit ist Gewohnheit geworden. Gregor ist nur noch die Geldquelle.",
            "Dann das versteckte Vermögen: Der Vater hat Geld zurückgehalten, Gregor hätte früher aufhören können. Aber Gregor nickt nur „eifrig“, er kritisiert den Vater nicht einmal in Gedanken.",
            "Merksatz: „Gregor hat die Rolle des Vaters übernommen, aber nicht dessen Respekt.“",
            "→ Überleitung: „Und wie reagiert der Vater, als Gregor verwandelt ist?“",
        ],
        "fragen": [
            ("Warum ist es wichtig, dass der Vater Geld versteckt hat?",
             "Es zeigt, dass der Vater Gregor arbeiten lässt, obwohl es nicht ganz nötig wäre. Gregor hätte früher frei sein können (S. 19, Z. 22 ff.). Gregor nimmt den Vater trotzdem in Schutz („zweifellos besser so“, S. 19, Z. 24 f.). Das zeigt, wie unterwürfig er ist."),
            ("Warum kündigt Gregor nicht einfach?",
             "Aus Pflichtgefühl. Er will die Schulden der Eltern abbezahlen (S. 2, Z. 18 ff.) und denkt: „Wenn ich mich nicht wegen meiner Eltern zurückhielte, ich hätte längst gekündigt“ (S. 2, Z. 10 ff.)."),
            ("War das Verhältnis immer so kalt?",
             "Nein. Am Anfang war die Familie „erstaunt und beglückt“ und es waren „schöne Zeiten“ (S. 18, Z. 27 ff.). Erst mit der Zeit wurde es Gewohnheit."),
        ],
    },
    {
        "titel": "Folie 3 – Teil I: Der Vater als Gegner",
        "zeit": "ca. 1 Min. 15 Sek.",
        "hintergrund": [
            "Handlung: Gregor wacht als Käfer auf und verpasst seinen Zug. Der Prokurist kommt in die Wohnung. Gregor öffnet die Tür, der Prokurist flieht entsetzt.",
            "Der Vater treibt Gregor mit dem Stock des Prokuristen und einer Zeitung zurück in sein Zimmer. Gregor bleibt in der Tür stecken, wird verletzt und landet blutend im Zimmer. Damit endet Teil I.",
            "Wichtig: Der Vater wird hier selbst tierhaft beschrieben („Zischlaute … wie ein Wilder“), nicht Gregor.",
        ],
        "sprechtext": [
            "Schon am ersten Morgen klopft der Vater „schwach, aber schon mit der Faust“, also eine Drohung, bevor er überhaupt weiß, was los ist.",
            "Als er Gregor sieht: Er ballt die Faust und weint gleichzeitig. Er ist überfordert, reagiert aber mit Aggression.",
            "Der Prokurist flieht, der Vater nimmt Stock und Zeitung.",
            f"{ROT} „Unerbittlich drängte der Vater und stieß Zischlaute aus, wie ein Wilder.“ (S. 13, Z. 3 f.)",
            "Deuten: Eigentlich ist Gregor das Tier, aber hier wird der Vater wie ein Tier beschrieben.",
            "Zum Schluss der Stoß: Gregor fliegt „heftig blutend“ ins Zimmer und empfindet das sogar als „erlösend“. So sehr hat er gelernt, sich zu unterwerfen.",
            "→ Überleitung: „Im zweiten Teil verwandelt sich dann auch der Vater selbst.“",
        ],
        "fragen": [
            ("Warum weint der Vater?",
             "Er ist geschockt und überfordert, Gregor ist ihm also nicht völlig egal. Aber statt zu helfen, wählt er Gewalt. Das zeigt die zwei Seiten des Vaters."),
            ("Warum empfindet Gregor den Stoß als „erlösend“?",
             "Er steckt in der Tür fest und kommt nur durch den Stoß frei. Gleichzeitig ist es bitter: Gewalt vom Vater erlebt er als Hilfe. Das zeigt, wie sehr er sich dem Vater unterordnet."),
            ("Warum ist der Vater so wütend?",
             "Der Prokurist ist Gregors Vorgesetzter. Wenn Gregor seine Stelle verliert, ist die Existenz der Familie in Gefahr, denn Gregor zahlt die Schulden des Vaters ab."),
        ],
    },
    {
        "titel": "Folie 4 – Teil II: Die Verwandlung des Vaters",
        "zeit": "ca. 1 Min. 15 Sek.",
        "hintergrund": [
            "Nach Gregors Verwandlung nimmt der Vater eine Stelle als Bankdiener an. Er holt z. B. „den kleinen Bankbeamten das Frühstück“ (S. 29, Z. 34 f.).",
            "Früher lag der Vater müde im Bett und empfing Gregor im Schlafrock (S. 26, Z. 18 ff.). Jetzt steht er aufrecht in Uniform (S. 26, Z. 30 ff.).",
            "Parallele: Im Wohnzimmer hängt ein Foto von Gregor als Leutnant in Uniform (S. 10, Z. 28 f.). Früher stand Gregor für Stärke und Uniform, jetzt der Vater.",
            "Er zieht die Dieneruniform nicht einmal zu Hause aus (S. 28, Z. 27 f.).",
        ],
        "sprechtext": [
            "Im zweiten Teil verwandelt sich auch der Vater. Gregor fragt sich: „war das noch der Vater?“",
            "Früher: müde im Bett, im Schlafrock im Lehnstuhl, kaum fähig aufzustehen.",
            f"{ROT} „Nun aber war er recht gut aufgerichtet; in eine straffe blaue Uniform mit Goldknöpfen gekleidet, wie sie Diener der Bankinstitute tragen“ (S. 26, Z. 30 ff.)",
            "Gegensätze betonen: Schlafrock gegen Uniform, liegen gegen aufrecht stehen.",
            "Gregor am Boden „staunte über die Riesengröße seiner Stiefelsohlen“: Er sieht den Vater von unten, riesig und übermächtig.",
            "Bild einer Wippe: Je schwächer Gregor, desto stärker der Vater.",
            "Ironie: Es ist eine DIENER-Uniform. Draußen ist er nur Diener, zu Hause spielt er den Herrscher.",
            "→ Überleitung: „Und diese neue Stärke zeigt er im Apfelwurf.“",
        ],
        "fragen": [
            ("Was bedeutet die Uniform?",
             "Autorität, Ordnung und Macht. Weil es aber eine Dieneruniform ist, ist sie auch ironisch: Der Vater ist draußen ganz unten und braucht die Uniform, um zu Hause Macht zu zeigen. Er legt sie nicht einmal zu Hause ab (S. 28, Z. 27 f.)."),
            ("War der Vater vorher wirklich so schwach?",
             "Vielleicht nicht. Er kann plötzlich wieder arbeiten und hatte heimlich Geld (S. 19, Z. 12 f.). Möglich ist, dass er sich bequem von Gregor versorgen ließ. Außerdem sehen wir alles aus Gregors Sicht, und Gregor hat den Vater vielleicht schwächer wahrgenommen."),
            ("Warum ist die Erzählperspektive hier wichtig?",
             "Weil wir den Vater nur durch Gregors Augen sehen. Die „Riesengröße seiner Stiefelsohlen“ ist Gregors Blick von unten. Der Vater wirkt so groß, weil Gregor so klein geworden ist."),
        ],
    },
    {
        "titel": "Folie 5 – Teil II: Der Apfelwurf",
        "zeit": "ca. 1 Min. 15 Sek.",
        "hintergrund": [
            "Handlung: Mutter und Grete räumen Gregors Zimmer aus. Gregor klammert sich an ein Bild, die Mutter wird ohnmächtig. Gregor läuft ins Wohnzimmer, da kommt der Vater nach Hause.",
            "Der Vater glaubt sofort, Gregor habe eine Gewalttat begangen: „Ich habe es ja erwartet“ (S. 25, Z. 46 ff.).",
            "Er füllt sich die Taschen mit Äpfeln und wirft. Einer bleibt in Gregors Rücken stecken (S. 27, Z. 24 ff.), niemand traut sich, ihn zu entfernen (S. 27, Z. 41 f.).",
            "Die Mutter muss den Vater „um Schonung von Gregors Leben“ bitten (S. 27, Z. 38 f.). Damit endet Teil II.",
            "Der Apfel verfault und entzündet sich. Kurz vor seinem Tod spürt Gregor ihn „schon kaum“ (S. 37, Z. 47 ff.).",
        ],
        "sprechtext": [
            "Kurz die Situation: Die Mutter ist ohnmächtig, Gregor ist im Wohnzimmer, der Vater kommt nach Hause.",
            "Der Vater fragt nicht nach, er urteilt sofort: „Ich habe es ja erwartet.“",
            f"{ROT} „der Vater hatte sich entschlossen, ihn zu bombardieren.“ (S. 27, Z. 18 f.)",
            "Zwei Wörter betonen: „entschlossen“ heißt, es ist eine Entscheidung und kein Reflex. „Bombardieren“ ist Kriegssprache.",
            "Ein Apfel dringt in Gregors Rücken ein und bleibt stecken. Er verfault und schwächt Gregor bis zum Tod.",
            "Die Mutter muss um Gregors Leben bitten. So ernst ist die Gewalt.",
            "Symbol: Der Apfel erinnert an den Sündenfall (Schuld und Strafe). Gregor wird für eine Schuld bestraft, die er gar nicht hat.",
            "Fazit der Folie: Der Vater ist am Tod seines Sohnes mitschuldig.",
            "→ Überleitung: „Im dritten Teil fällt dann das endgültige Urteil.“",
        ],
        "fragen": [
            ("Warum gerade Äpfel?",
             "Äpfel sind ein Alltagsgegenstand aus der Obstschale, die Gewalt kommt also mitten aus dem Familienalltag. Symbolisch erinnert der Apfel an den Sündenfall in der Bibel: Schuld und Strafe."),
            ("Ist der Vater schuld an Gregors Tod?",
             "Mitschuldig: Die Apfelwunde schwächt Gregor bis zum Ende (S. 37, Z. 47 ff.). Aber auch die ganze Familie gibt ihn auf, und Gregor selbst will am Ende verschwinden. Am besten antwortest du differenziert: Hauptverantwortlich für die Verletzung ist der Vater, für den Tod die ganze Situation."),
            ("Warum entfernt niemand den Apfel?",
             "Aus Ekel und Angst vor Gregor. Im Text steht: „da ihn niemand zu entfernen wagte“ (S. 27, Z. 41 f.). Die Familie hält Abstand, statt zu helfen."),
        ],
    },
    {
        "titel": "Folie 6 – Teil III: Das Urteil",
        "zeit": "ca. 1 Min. 15 Sek.",
        "hintergrund": [
            "Handlung: Die Familie hat drei Zimmerherren aufgenommen. Grete spielt Geige, Gregor kommt aus seinem Zimmer, die Zimmerherren sehen ihn und kündigen.",
            "Grete nennt Gregor ein „Untier“ und sagt: „wir müssen versuchen, es loszuwerden“ (S. 35, Z. 48 ff.). Der Vater: „Sie hat tausendmal Recht“ (S. 36, Z. 3).",
            "Kurz denkt der Vater noch: „Wenn er uns verstünde“ (S. 36, Z. 26), gibt den Gedanken aber auf.",
            "Gregor stirbt in derselben Nacht gegen drei Uhr morgens (S. 38, Z. 4 f.), Ende März.",
            "<b>Wichtige Beobachtung:</b> Nach Gregors Tod wird der Vater im Text kein einziges Mal mehr „der Vater“ genannt, nur noch „Herr Samsa“. Vorher heißt er fast immer „der Vater“.",
        ],
        "sprechtext": [
            "Nach dem Geigenabend fordert Grete, „es“ loszuwerden. Sie nennt Gregor nicht mal mehr beim Namen.",
            "Der Vater gibt ihr sofort recht: „Sie hat tausendmal Recht.“ Für ihn ist Gregor nur noch „es“.",
            "Gregor wehrt sich nicht. In seiner letzten Nacht denkt er „mit Rührung und Liebe“ an seine Familie und ist selbst überzeugt, dass er verschwinden muss.",
            f"{ROT} „»Nun,« sagte Herr Samsa, »jetzt können wir Gott danken.«“ (S. 38, Z. 41)",
            "Deuten: Kein Wort der Trauer, nur Erleichterung.",
            "Beobachtung nennen: Ab Gregors Tod heißt er nur noch „Herr Samsa“, nie mehr „der Vater“. Er ist nicht mehr Gregors Vater, die Beziehung ist ausgelöscht.",
            "Er wirft die Zimmerherren raus („Verlassen Sie sofort meine Wohnung!“) und ist wieder Herr im Haus.",
            "→ Überleitung: „Damit komme ich zu meinem Fazit.“",
        ],
        "fragen": [
            ("Warum fordert Grete das und nicht der Vater?",
             "Grete hat Gregor am längsten versorgt und ist am Ende erschöpft. Entscheidend ist aber, dass der Vater sofort zustimmt. Erst damit ist das Urteil endgültig."),
            ("Woran stirbt Gregor?",
             "Körperlich an der Schwäche: die entzündete Apfelwunde und dass er kaum noch isst. Seelisch, weil er das Urteil der Familie annimmt. Er „verschwindet“ genau so, wie die Familie es will."),
            ("Was bedeutet es, dass er nach dem Tod „Herr Samsa“ heißt?",
             "Die Vaterrolle ist vorbei. Er hat keinen Sohn mehr, und der Text zeigt das durch den Namenswechsel. Außerdem wechselt die Erzählperspektive: Gregor ist tot, also wird nicht mehr aus seiner Sicht erzählt."),
        ],
    },
    {
        "titel": "Folie 7 – Fazit",
        "zeit": "ca. 1 Min.",
        "hintergrund": [
            "Nach Gregors Tod macht die Familie einen Ausflug mit der Straßenbahn („Elektrische“) ins Grüne (S. 40, Z. 42 f.).",
            "Sie planen die Zukunft, die Eltern wollen für Grete „einen braven Mann“ suchen (S. 41, Z. 11).",
            "Die Familie blüht ohne Gregor auf. Das Ende wirkt für die Familie hell, für Gregor ist es tragisch.",
        ],
        "sprechtext": [
            "Drei Punkte zusammenfassen: Gregor opfert sich ohne Anerkennung. Der Vater wird mit jeder Konfrontation stärker und gewalttätiger. Am Ende ist Gregor nur noch eine Pflicht.",
            "Das Familienpflicht-Zitat kurz nennen: man müsse „dulden, nichts als zu dulden“. Das ist Pflicht und keine Liebe.",
            f"{ROT} „»Also kommt doch her. Laßt schon endlich die alten Sachen. Und nehmt auch ein wenig Rücksicht auf mich.«“ (S. 40, Z. 37 f.)",
            "Deuten: „Rücksicht auf MICH“. Der Sohn ist kaum tot, und der Vater stellt sich selbst in den Mittelpunkt.",
            "Schluss: Die Familie fährt ins Grüne und plant die Zukunft. Ohne Gregor geht es ihnen besser.",
            "Kernsatz vorlesen: „Die Verwandlung zeigt, wie ein Sohn an der Härte und fehlenden Anerkennung seines Vaters zerbricht.“",
            "„Vielen Dank fürs Zuhören! Habt ihr Fragen?“",
        ],
        "fragen": [
            ("Ist das Ende positiv oder negativ?",
             "Beides. Für die Familie ist es ein Neuanfang (Frühling, Ausflug, Zukunftspläne). Für Gregor ist es tragisch, denn er musste sterben, damit es der Familie besser geht. Genau diese Bitterkeit macht das Ende so stark."),
            ("Hat sich der Vater am Ende verändert?",
             "Nein, er ist wieder das Familienoberhaupt. Er wirft die Zimmerherren raus und verlangt „Rücksicht auf mich“. Die Macht ist vom Sohn zum Vater zurückgewandert."),
            ("Hat das etwas mit Kafkas eigenem Leben zu tun? (steht nicht auf den Folien, aber gut zu wissen)",
             "Ja. Kafkas Vater Hermann war dominant und körperlich stark. 1919 schrieb Kafka den „Brief an den Vater“, den er nie übergab. Darin steht: „Mein Schreiben handelte von Dir“ und dass der Vater einen Freund von Kafka „mit Ungeziefer“ verglichen hat."),
        ],
    },
    {
        "titel": "Folie 8 – Quellen",
        "zeit": "nur zeigen",
        "hintergrund": [
            "Die Seiten- und Zeilenangaben (S. …, Z. …) beziehen sich auf die zeilennummerierte Textgrundlage (Textgrundlage_Die_Verwandlung_mit_Zeilen.pdf), nicht auf eure Schulausgabe.",
            "Der Text ist die Fassung von 1915 nach Projekt Gutenberg (E-Book Nr. 22367). Deshalb steht dort die alte Rechtschreibung („daß“).",
        ],
        "sprechtext": [
            "Folie nur kurz zeigen, nichts vorlesen.",
        ],
        "fragen": [
            ("Warum stimmen die Seitenzahlen nicht mit meinem Buch überein?",
             "„Ich habe den Originaltext von 1915 verwendet. Die Angaben beziehen sich auf diese Textfassung, die ich in den Quellen angegeben habe.“"),
            ("Warum steht „daß“ statt „dass“?",
             "Weil der Originaltext von 1915 zitiert wird, also in der damaligen Rechtschreibung."),
        ],
    },
]


def esc_keep_tags(s):
    # Texte enthalten nur <b>…</b> als Auszeichnung; alles andere escapen
    return html.escape(s).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")


def li(items):
    out = []
    for it in items:
        cls = ' class="rot"' if it.startswith(ROT) else (' class="ueber"' if it.startswith("→") else "")
        out.append(f"<li{cls}>{esc_keep_tags(it)}</li>")
    return "<ul>" + "".join(out) + "</ul>"


parts = [
    "<h1>Vorbereitung: Motiv Vater-Sohn-Beziehung</h1>",
    "<p class='sub'>Franz Kafka: Die Verwandlung – Julian Sickinger · Seiten-/Zeilenangaben nach der nummerierten Textgrundlage</p>",
    "<h2>Grundwissen (sollte man sicher können)</h2>", li(GRUNDWISSEN),
    "<h2>Tipps für den Vortrag</h2>", li(TIPPS),
]
for f in FOLIEN:
    parts.append(f"<section><h2>{html.escape(f['titel'])} <span class='zeit'>{html.escape(f['zeit'])}</span></h2>")
    parts.append("<h3>Das musst du verstehen</h3>" + li(f["hintergrund"]))
    parts.append("<h3>Sprechtext in Stichpunkten</h3>" + li(f["sprechtext"]))
    parts.append("<h3>Mögliche Fragen der Lehrerin</h3>")
    for q, a in f["fragen"]:
        parts.append(f"<div class='qa'><p class='q'>❓ {html.escape(q)}</p><p class='a'>{esc_keep_tags(a)}</p></div>")
    parts.append("</section>")

CSS = """
@page { size: A4; margin: 16mm 15mm; }
body { font-family: 'DejaVu Serif', Georgia, serif; color: #1E1812; font-size: 10.3pt; line-height: 1.38; }
h1 { font-size: 21pt; margin: 0 0 2pt; color: #1E1812; }
.sub { color: #5C4B3A; margin: 0 0 12pt; font-size: 9.5pt; }
h2 { font-size: 14.5pt; color: #6B1F1A; margin: 16pt 0 4pt; border-bottom: 1px solid #C9BBA3; padding-bottom: 3pt; }
h3 { font-size: 11.5pt; margin: 9pt 0 3pt; color: #3B3128; }
.zeit { font-size: 9.5pt; color: #5C4B3A; font-weight: normal; float: right; margin-top: 4pt; }
ul { margin: 0 0 4pt 0; padding-left: 16pt; }
li { margin: 2pt 0; }
li.rot { color: #6B1F1A; font-weight: bold; }
li.ueber { color: #5C4B3A; font-style: italic; }
.qa { background: #F3EEE4; border: 1px solid #DDD2BF; padding: 5pt 8pt; margin: 5pt 0; break-inside: avoid; }
.q { font-weight: bold; margin: 0 0 2pt; }
.a { margin: 0; }
section { break-before: page; }
"""
doc = f"<!doctype html><html lang='de'><head><meta charset='utf-8'><title>Vorbereitung Vater-Sohn-Beziehung</title><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
HTML = ROOT / "Vorbereitung_Vater-Sohn-Beziehung.html"
HTML.write_text(doc, encoding="utf-8")

# Notizen für die Folien: Sprechtext-Stichpunkte
notes = {}
for i, f in enumerate(FOLIEN, 1):
    notes[str(i)] = f"[{f['zeit']}]\n" + "\n".join("• " + it.replace("<b>", "").replace("</b>", "") for it in f["sprechtext"])
(ROOT / "notizen.json").write_text(json.dumps(notes, ensure_ascii=False, indent=1), encoding="utf-8")

# PDF über Chromium (Node-Playwright ist vorinstalliert)
import subprocess  # noqa: E402

js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(process.argv[1]);
  await p.pdf({ path: process.argv[2], format: 'A4', printBackground: true,
    margin: { top: '16mm', bottom: '16mm', left: '15mm', right: '15mm' } });
  await b.close();
})();
"""
subprocess.run(["node", "-e", js, HTML.resolve().as_uri(), str(ROOT / "Vorbereitung_Vater-Sohn-Beziehung.pdf")], check=True)
print("Vorbereitung erstellt")
