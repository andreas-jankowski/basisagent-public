# Das Prinzip

Alle Entscheidungen in diesem Template folgen aus einer einzigen Unterscheidung.

## Zwei Arten von Tokenkosten

**Einmalkosten** entstehen beim Laden: eine Datei lesen, einen Skill aufrufen, eine Spec öffnen. Das zahlst du, wenn du es brauchst. Unproblematisch.

**Dauerkosten** entstehen bei *jedem einzelnen Zug*. Dazu gehören:

- die Systemprompt
- die Schemata **aller** verfügbaren Werkzeuge — auch der MCP-Server
- Name und Beschreibung **aller** installierten Skills, benutzt oder nicht
- alles in `AGENTS.md` bzw. `CLAUDE.md` und in importierten Dateien

Bei einer Sitzung mit 60 Zügen wird eine Zeile in `AGENTS.md` sechzigmal bezahlt. Eine installierte, nie aufgerufene Skill-Beschreibung ebenfalls.

**Wiederholkosten** sind der Sonderfall, den man leicht für Einmalkosten hält. Was du einmal lädst — eine gelesene Datei, eine Werkzeugausgabe, ein Suchergebnis —, steht danach *für den Rest der Sitzung* im Verlauf und wird bei jeder folgenden Anfrage erneut gelesen. Über den Zwischenspeicher kostet das etwa ein Zehntel des Einzelpreises (auf Opus 5.5 ein Zwanzigstel), aber es kostet bei jedem Zug erneut.

Daraus folgt eine Rechnung, die den Umgang mit ganzen Sitzungen bestimmt: Ein Token aus Zug 20 einer 100-Zug-Sitzung wird achtzigmal wiedergelesen. **Der Verbrauch wächst quadratisch mit der Sitzungslänge.** Dieselbe Arbeit auf zwei Sitzungen geteilt kostet die Hälfte, zweimal geteilt ein Drittel.

Gemessen an 49 Sitzungen mit 4.780 Anfragen: rund 60 % des Gesamtaufwands ist wiedergelesener Kontext, im Schnitt 252k Token je Anfrage. Und rund drei Viertel davon ist Maschinenverkehr — Werkzeugaufrufe und deren Ausgaben. Nicht das Denken kostet, nicht das Schreiben: das Mitschleppen.

## Nicht jeder Token kostet gleich

Die Kostenarten oben zählen Token. Was ein Token *kostet*, ist damit noch nicht gesagt — und es spreizt weit. Bezogen auf frische Eingabe als 1,0:

| | Faktor |
|---|---|
| Cache gelesen | **0,1x** · Opus 5.5: 0,05x · Fable 5.1: 0,025x |
| frische Eingabe | 1,0x |
| Cache geschrieben | 1,25x (5-Min-Haltedauer) · 2,0x (1 Std.) |
| **Ausgabe** | **5,0x** |

Herstellerangabe, kein Messwert: Opus 5 kostet $5 je Mio. Eingabe gegen $25 je Mio. Ausgabe, und die Doku nennt *„Cache reads cost ~0.1x base input price. Cache writes cost 1.25x for 5-minute TTL, 2x for 1-hour TTL."* (`code.claude.com/docs` → prompt caching, abgerufen 25.08.2026). Opus 5.5 kostet $4 gegen $20, und dort liest der Cache zu 0,05x statt 0,1x (`platform.claude.com` → „Pricing", abgerufen 24.09.2026).

**Der Faktor 5 hängt nicht am Modell.** Er gilt in der ganzen aktuellen Familie: Fable 5.1 und Fable 5 $10/$50, Opus 5.5 $4/$20, Opus 5 $5/$25, Sonnet 5 $2/$10, Haiku 4.5 $1/$5 (Stand 24.09.2026; Sonnet 5 stand hier bis dahin mit $3/$15, die zum 01.09. angekündigte Erhöhung ist entfallen). Ein Modellwechsel verschiebt die absoluten Kosten, nicht diese Rangfolge — die Rangfolge gilt also unabhängig davon, womit ein Projekt arbeitet. **Der Cache-Lesefaktor dagegen hängt seit Opus 5.5 und Fable 5.1 am Modell:** 0,05x und 0,025x statt 0,1x. Die Rangfolge bleibt, die Spreizung wächst.

Daraus folgt ein Satz, der in den vier Regeln unten nicht vorkommt, weil sie alle auf Dateien und Sitzungen zielen: **Ein gesparter Ausgabetoken wiegt fünfzig gesparte Cache-Lese-Token — auf Opus 5.5 hundert, auf Fable 5.1 zweihundert.** Und die Spreizung ist genau umgekehrt zur Menge — Ausgabe entsteht einmal je Zug, Kontext wird in jedem Zug erneut gelesen. Der Posten mit dem kleinsten Volumen trägt damit den höchsten Preis je Token. Wie groß sein Anteil am Aufwand tatsächlich ist, steht in `core/belege/` — gemessen mit 0,1x, also für Opus 5 und früher. Seit 24.09.2026 gewichtet das Werkzeug je Modell (`feedback/offene-punkte.md`, Punkt 42).

Und sie ist der einzige Hebel ohne Gegenrechnung. Jeder andere hat einen Preis: Die Regeldatei zu kürzen kostet Regeltreue, die Sitzung zu teilen kostet die Übergabe, weniger Werkzeugaufrufe kosten Gründlichkeit. **Kürzer zu antworten kostet nichts außer Disziplin** — solange nicht die Begründung wegfällt, die den Wert trägt.

## Vier Regeln, die daraus folgen

1. **`AGENTS.md` bleibt unter 100 Zeilen.** Harte Grenze. Jede Zeile muss sich rechtfertigen. Ausführliches gehört in Dateien, die nur bei Bedarf geladen werden — der Projektkontext, `CONTEXT.md`.

   **Zeilen sind ein Näherungswert, nicht die Größe selbst.** Dieselben Inhalte ergeben 39 Zeilen oder 55, je nachdem wie umgebrochen wird, bei praktisch gleichem Verbrauch — wer die Grenze durch lange Einzelzeilen einhält, hat nichts gespart. Was zählt, sind Zeichen: Größenordnung 4.500 für die Regeldatei, bei deutschem Text grob drei Zeichen je Token. Die Zeilenzahl bleibt, weil sie beim Schreiben ohne Werkzeug im Kopf mitläuft; gemessen wird in Phase 9 beides.

   **Von den beiden Zahlen bindet die Zeichenzahl.** Bei der beobachteten Dichte der Vorlagen — grob 45 Zeichen je Zeile, weil viele Zeilen kurz sind — entsprechen 100 Zeilen etwa 4.500 Zeichen, liegen also innerhalb der Größenordnung. Wer die Zeilengrenze künftig weiter anhebt, muss vorher die Zeichen nachrechnen; sonst wächst die Regeldatei über das, was das Prinzip trägt.

   **Woher die 100 kommt.** Die Claude-Code-Doku nennt als Obergrenze: „Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." (`code.claude.com/docs/en/memory`, Abschnitt „Write effective instructions", abgerufen 24.08.2026). Die 100 liegt bewusst darunter — die Hälfte des Zulässigen als Reserve für Projekte, die einen ausführlicheren Rahmen brauchen. Erreicht eine Regeldatei die 100, ist das kein Anlass, zur Doku-Obergrenze aufzurücken, sondern der Anlass, Kategorie B in den Projektkontext zu verschieben.

2. **Nur installieren, was tatsächlich benutzt wird.** Ein Skill-Repo komplett zu klonen heißt, für jede Beschreibung darin dauerhaft zu zahlen. Dasselbe gilt für MCP-Server: jeder bringt seine Werkzeugschemata in jeden Zug.

3. **Was immer gelten soll, gehört in die Regeldatei — nicht in ein Paket.** Ein Skill, dessen Inhalt permanent gilt, kostet doppelt: Beschreibung in jedem Zug *plus* Rumpf beim Laden. Für Sätze, die man direkt hinschreiben kann.

   Die Umkehrung gilt genauso: Was **nur beim Auslösen** gilt, gehört nicht in die Regeldatei. Ein Skill mit `disable-model-invocation: true` steht laut Doku mit *keiner* Zeile im Kontext, bis der Nutzer ihn aufruft — Beschreibung eingeschlossen. Das ist der billigste Ort für ein Verfahren: Dauerkosten null, dafür kein Selbstaufruf durch das Modell. In die Regeldatei kommt dann nur der Auslöser, der auf den Namen zeigt.

4. **Lange Sitzungen teilen.** Der Hebel gegen Wiederholkosten. Nach fertiger Aufgabe und vor jeder längeren Pause: den Stand nach `uebergabe/` schreiben, sichern, `/clear`. Nicht `/compact` — das Zusammenfassen kostet eine Modellanfrage bei größtem Kontext und entscheidet ohne dich, was wegfällt.

   **Das Teilen hat selbst einen Preis, und die Rechnung oben enthält ihn nicht.** Die Übergabe kostet rund ein Fünftel der Sitzung, in der sie läuft — und zwar an der teuersten Stelle, bei maximalem Kontext. Wer spät schneidet, spart mehr *und* zahlt mehr. Dazu kommt: Der Schnitt setzt einmal zurück, er verhindert das Wachsen nicht. Wer danach genauso lange weiterarbeitet, holt den Vorteil wieder ein. Die Mechanik „geteilt kostet die Hälfte" bleibt richtig — sie ist nur nicht die ganze Rechnung, und gemessen fällt der Vorteil deutlich kleiner aus als sie erwarten lässt.

   **Deshalb steht die Empfehlung nicht auf dem Sparen.** Was beim `/clear` verlorengeht, ist zu drei Vierteln Material, das noch auf der Platte liegt und gezielt nachlesbar ist. Nicht wiederbeschaffbar sind Entscheidungen, Begründungen und verworfene Wege — genau das, was die Übergabe festhält. Ist die Aufgabe nach dem Schnitt fertig, spart die Übergabe **gar nichts** und ist trotzdem richtig geschrieben. **Der Fehler ist nie `/clear`, sondern `/clear` ohne Übergabe.**

## Der zweite Hebel: früh anhalten

`edit` auf `ask` zu setzen ist nicht nur eine Sicherheitsmaßnahme, sondern eine Tokenmaßnahme.

Ein Agent, der in die falsche Richtung läuft, produziert Ausgabe, die du korrigieren lässt. Die Korrekturrunde kostet mehr als die Unterbrechung. **Früh anhalten ist billiger als spät reparieren.**

Deshalb steht der Berechtigungsschritt in Phase 1, vor allem anderen.

## Der dritte Hebel: die Aufwandstufe

Neu seit 0.17.0. Die aktuellen Modelle kennen eine Stufe für den Aufwand —
`low`, `medium`, `high`, `xhigh`, `max`, Voreinstellung `high`, auf Opus 5.5
`medium`. Sie wirkt auf
**alle** Ausgabetoken: den Text, das Denken und die Werkzeugaufrufe. Niedrige
Stufen führen laut Hersteller zu weniger und knapperen Aufrufen, höhere zu
mehr Aufrufen und ausführlicheren Erklärungen.

Damit ist sie der einzige Regler, der die drei Kostenarten oben gemeinsam
bewegt: weniger Werkzeugaufrufe heißt weniger Maschinenverkehr, und der ist
nach der Messung oben **drei Viertel** des wiedergelesenen Kontexts.

**Zwei Dinge, die sie nicht tut.** Erstens kürzt sie die sichtbare Antwort
nicht — auf Opus 5 ausdrücklich nicht verlässlich; dafür ist die Zeile in der
Regeldatei da. Zweitens ist sie keine Obergrenze, sondern ein Verhaltenssignal:
Bei schweren Aufgaben denkt das Modell auch auf `low`, nur weniger.

**Die Stufennamen sind je Modell nicht gleich viel wert.** Opus 5.5 auf
`medium` erreicht oder übertrifft laut Hersteller Opus 5 auf `high`; `xhigh`
und `max` sollen dort nur laufen, wo ein Qualitätsgewinn gemessen ist. Eine
Stufe, die zum alten Modell passte, wird beim Modellwechsel neu gewählt, nicht
übernommen. Claude Code tut das teils von selbst: Ein früher gesetztes
`effortLevel` gilt für Opus 5.5 ausdrücklich nicht — wer umsteigt, läuft ohne
eigene Wahl auf `medium`.

**Sie zu wechseln ist nicht überall umsonst.** Ein geänderter Wert auf oberster
Ebene erhält den Zwischenspeicher nicht; die Doku rät, die Stufe am Anfang zu
wählen und in einer Sitzung, die auf Cache-Treffer setzt, konstant zu lassen.
Claude Code zeigt beim Wechseln mitten in der Arbeit dann eine Cache-Warnung.
Gemessen kostet eine Anfrage nach kaltem Cache das **6,5-Fache**
(`core/belege/`). Daraus folgt kein Verbot, sondern ein Zeitpunkt: **am
Sitzungsanfang wählen** — also dort, wo Regel 4 ohnehin schneidet.

**Ausnahme seit Opus 5.5.** Die Schnittstelle kennt einen Wechsel je Nachricht
(Beta), der den Zwischenspeicher erhält. Claude Code nutzt ihn auf Opus 5.5 und
Fable 5.1 über Abo oder API-Schlüssel und wechselt dort ohne Rückfrage — nicht
über Bedrock, Google Cloud, das Claude-Apps-Gateway, mit
`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` oder bei HIPAA-Konfiguration. Die
Schnittstelle kann den Wechsel auch auf Opus 5; Claude Code nennt ihn dafür
nicht. **Auf diesen beiden Modellen wird die Stufe vom Regler je Sitzung zum
Regler je Aufgabe:** niedrig zum Nachschlagen, höher für die Bewertung, in
derselben Sitzung. Für alle übrigen bleibt der Sitzungsanfang.

**Die Stufe gehört nicht ins Template**, so wenig wie das Modell
(`core/verworfen.md`). Was ins Template gehört, ist der Auftrag an den Agenten,
sie vorzuschlagen und zu begründen. Die Wahl trifft der Nutzer.

*(Herstellerangaben, `platform.claude.com` → „Effort" und „Prompting Claude
Opus 5", `code.claude.com/docs` → „Model configuration", abgerufen
21.09.2026; Opus 5.5 und der Wechsel je Nachricht: `platform.claude.com` →
„Effort", „Prompting Claude Opus 5.5", `code.claude.com/docs` → „Model
configuration", „How Claude Code uses prompt caching", abgerufen 24.09.2026.
Keine eigene Messung.)*

## Der vierte Hebel: nicht delegieren, was man selbst erledigt

Ein Subagent ist eine zweite Sitzung. Er hat seinen eigenen Systemprompt, seine
eigenen Werkzeugschemata, seinen eigenen Verlauf — und sein Ergebnis kommt in
die Hauptsitzung zurück, wo es ab da in **jedem** Zug mitgelesen wird. Er
verlagert Kontext also nicht, er erzeugt zusätzlichen und legt das Ergebnis
obendrauf.

Das rechnet sich, wo die Arbeit wirklich unabhängig ist und das Zwischenmaterial
groß gegenüber dem Ergebnis: eine breite Suche über viele Dateien, deren
Ausgaben sonst alle im Hauptverlauf lägen. Es rechnet sich nicht bei allem, was
in einer Handvoll Aufrufe selbst erledigt ist — und nicht zum Gegenprüfen der
eigenen Arbeit.

**Einmal gemessen, und die Messung schränkt den Satz davor ein** (Journal
2026-09-23, Textprojekt J, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`). Eine Recherche über acht Firmen ging aus einer
Sitzung mit rund 290k Kontext an vier Subagenten. Die Arbeit war unabhängig,
die Berichtstexte hatten mehrere hunderttausend Zeichen, es war also genau der
Fall, für den der Satz gilt. Je Firma kostete das **rund das Doppelte** eines
vergleichbaren Durchgangs in der Hauptsitzung. Ganz gleichwertig ist der
Vergleich nicht, denn die Subagenten prüften gründlicher. Der Grund: Die
Subagenten holten die Rohtexte in den eigenen Verlauf, im Mittel 137k Kontext
je Anfrage gegen 169k in der Hauptsitzung. Der frische Kontext, der den
Vorteil ausmachen sollte, war nach wenigen Zügen keiner mehr.

Zwei Folgerungen, beide aus dieser einen Messung. **Ein Subagent spart nur,
wenn sein Auftrag seinen Kontext klein hält:** Zwischenmaterial in Dateien, nur
das Ergebnis zurück. Und **aus einer langen Sitzung ist der billigere Weg meist
nicht der Subagent**, sondern Übergabe, `/clear` und die Arbeit in der frischen
Sitzung (Regel 4). Überschlagen kostet das etwa die Hälfte, gemessen ist es
nicht.

**Der Anlass für diesen Abschnitt ist modellabhängig.** Claude Opus 5 delegiert
nach Herstellerangabe bereitwilliger als seine Vorgänger. Die Voreinstellungen
sind dabei großzügig: drei Ebenen Verschachtelung, zwanzig gleichzeitige
Subagenten. Das Template setzt sie in der Berechtigungsvorlage auf eine Ebene
und fünf gleichzeitige herunter (→ `claudecode/adapter.md`). Eine Anweisung im
Prompt steuert nur; die beiden Umgebungsvariablen greifen.

**Seit 0.23.0 sperrt die Vorlage Subagenten und Workflows ganz** —
Nutzerentscheidung vom 2026-10-12: zu langsam, zu teuer. Die Grenzen oben
gelten erst, wenn der Nutzer sie bei der Einrichtung oder später erlaubt.

**Tiefe und Anzahl sind nicht die Länge.** Ein einzelner Rechercheagent lief am
2026-10-07 22 Minuten mit 49 Abrufen, berichtet sind Läufe über 40 Minuten —
innerhalb beider Grenzen. Die Länge begrenzt nur eine Agentendefinition mit
`maxTurns`, die Kosten je Schritt das Modell darin. Wie viel das sein darf,
fragt die Einrichtung den Nutzer (→ Adapter, „Rechercheagenten").

*(Herstellerangaben, `code.claude.com/docs` → Agent SDK, „Cap subagent depth,
concurrency, and spend", abgerufen 21.09.2026. Keine eigene Messung.)*

## Was daraus nicht folgt

Sparsamkeit ist kein Selbstzweck. Wenn ein Projekt eine ausführliche Architekturbeschreibung braucht, bekommt es sie — nur eben an einem Ort, der nicht in jedem Zug mitläuft.

Und: **Eine explizite Anforderung schlägt Minimalismus.** Wenn die Spec eine Kante verlangt, wird sie gebaut, auch wenn sie sich wegkürzen ließe.
