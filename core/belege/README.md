# Belege

Hier liegt die **Messgrundlage** für die Kostenaussagen des Templates —
nicht Ablauf, nicht Vorlage. Nichts hiervon wird in ein Zielprojekt
eingerichtet, nichts davon wird beim Einrichten gelesen.

Übernommen am 23.08.2026 aus Werkzeugprojekt A, das danach
aufgelöst wurde. Ohne diese Dateien stünden die Zahlen in
`core/prinzip.md` und `core/skills/uebergabe/SKILL.md` ohne Beleg da —
und `AGENTS.md:13` verbietet genau das.

## Was hier liegt

| Datei | Was sie ist |
|---|---|
| `kontext-messung.md` | Die abgeschlossene Übergabe der Messaufgabe: Befunde, Entscheidungen, verworfene Wege. Der eigentliche Beleg |
| `kontextbericht.py` | Das Werkzeug, das die Zahlen erzeugt. Läuft ohne Modell, liest nur `~/.claude/projects/` |
| `uebergabe-in-anderes-projekt.md` | Installationsanleitung für bestehende Projekte — die ausführliche Fassung neben `../skills/uebergabe/ADDON.md` |
| `claude-code-kurzanleitung.html` | „Der Claude-Code-Arbeitszyklus" — dieselbe Sache für den Endnutzer statt für den Agenten |

## Die Zahlen in einem Absatz

Gemessen über 49 Sitzungen und 4.780 Anfragen: Rund **60 % des
Gesamtaufwands ist wiedergelesener Kontext**. Der Verbrauch wächst
**quadratisch** mit der Sitzungslänge — dieselbe Arbeit auf zwei Sitzungen
geteilt kostet die Hälfte. Beim Beenden verliert man zu **drei Vierteln**
Maschinenverkehr, der noch auf der Platte liegt. Nicht wiederbeschaffbar
sind Entscheidungen und Begründungen. Das ist die Rechnung hinter der
vierten Kostenart in `prinzip.md` und hinter dem ganzen Übergabeverfahren.

## Eine Falle in der Protokollstruktur

Gefunden am 24.08.2026 beim Messen der Verfahrenstreue, festgehalten hier,
weil sie jede künftige Auswertung betrifft:

**`/clear` steht in Zeile 3 der *neuen* Protokolldatei.** Es eröffnet die
Folgesitzung, es beendet nicht die alte. Wer innerhalb einer Datei fragt
„folgt auf X ein `/clear`", misst eine Unmöglichkeit — und bekommt eine
perfekte, sinnlose Zahl: im konkreten Fall „0 von 13 Übergaben von `/clear`
gefolgt" und „25 von 25 `/clear` ohne Übergabe". Beides Artefakt.

Wer Sitzungsgrenzen auswerten will, muss die Dateien je Projekt zeitlich
verketten. Für die Frage, ob eine Sitzung nach einer Handlung endete, ist
die **relative Position** in der Datei der brauchbare Indikator — nachgeprüft
an drei Sitzungen: `/clear` bei Zeile 3, `/uebergabe` bei 216 von 226 und
605 von 646. Seit Oktober 2026 rutscht `/clear` durch neue Kopfzeilen bis
Zeile 20 (Abschnitt „Wiederholung am 2026-10-29").

Zwei weitere Fallen, gefunden am selben Tag beim Bilanzieren der Schnitte —
beide haben eine zu gute Zahl erzeugt, die erst beim Nachrechnen fiel:

- **Der Kontextstand einer Anfrage ist `input + cache_read + cache_creation`.**
  Wer `cache_creation` weglässt, misst bei einer **frischen** Sitzung fast
  null, weil dort der Cache erst geschrieben wird. Der Startstand nach
  `/clear` erschien so als 0 statt als rund 24k, und jede darauf gebaute
  Ersparnis war zu hoch.
- **Eine Folgesitzung wächst über den Schnittpunkt hinaus.** In vier von
  sechs gemessenen Fällen war ihr Endstand höher als der der geschnittenen
  Sitzung. Eine Ersparnis pauschal als `(Ende_A − Start_B)` je Anfrage zu
  rechnen, unterstellt einen Vorteil, der ab diesem Punkt nicht mehr
  existiert; richtig ist `max(0, Ende_A − Ctx_i)` je einzelne Anfrage.

Die beiden Fehler zusammen ergaben Faktor 3,2x statt der korrigierten 1,4x.

## Die Aufrufseite, und warum sie im Bericht fehlte

Bis zum 25.08.2026 schlüsselte `kontextbericht.py` nur die Werkzeug**ausgaben**
nach Werkzeug auf. Das ist knapp die Hälfte des Werkzeugverkehrs — die
Aufrufseite, also die Parameter, die ein Aufruf mitbringt, lag als eine
Summenzeile daneben und wurde keinem Werkzeug zugerechnet. Die Rangfolge
verschiebt sich dadurch erheblich: `Write` und `Edit` bringen ihren Inhalt im
Aufruf mit und haben eine winzige Ausgabe („File updated"). Nach Ausgaben
allein führt `Read` mit über der Hälfte; **beide Seiten gezählt, sind `Write`
und `Edit` zusammen so groß wie `Read`.**

Der Bericht kann das seit 25.08.2026 selbst — Spalten `Aufrufe`, `Median`,
`Ausgaben`, `zusammen`. Der Median gehört dazu, weil er die verwertbare
Entscheidung trägt: Wer eine Datei in zehn `Edit`-Aufrufen schreibt, zahlt
zehnmal den geänderten Abschnitt; wer sie in einem `Write` anlegt, einmal den
ganzen Text. Welches billiger ist, hängt am Verhältnis.

**Geprüft gegen den naheliegenden Verdacht**, der Befund sei ein Artefakt der
Woche, in der ausführliche Journal- und Übergabedateien geschrieben wurden —
genau die erzeugen große `Write`-Aufrufe. Verhältnis `Write`+`Edit` zu `Read`,
je Kalenderwoche über sechs Wochen:

| Woche | Read | Write | Edit | W+E / Read | Aufrufseite |
|---|---|---|---|---|---|
| KW30 | 18k | 7k | 8k | 0,87 | 30 % |
| KW31 | 60k | 42k | 22k | 1,07 | 34 % |
| KW32 | 65k | 10k | 31k | 0,64 | 35 % |
| KW33 | 275k | 139k | 119k | 0,94 | 41 % |
| KW34 | 716k | 443k | 317k | 1,06 | 44 % |
| KW35 | 144k | 60k | 57k | 0,82 | 36 % |

KW34 ist die verdächtige Woche. Sie liegt mitten im Feld, und KW31 erreicht
dasselbe Verhältnis ohne eine einzige Übergabedatei. **Der Vorbehalt ist
widerlegt**, das Verhältnis ist über sechs Wochen stabil zwischen 0,64 und
1,07. Der Anteil der Aufrufseite steigt allerdings von 30 % auf 44 % — die
`Write`-Aufrufe werden größer (Median 583 auf 787 Token), nicht nur
zahlreicher. Erhoben mit denselben Zählregeln wie oben, einzelne Anfragen
nach eigenem Zeitstempel gefiltert, nicht ganze Sitzungen.

Am 23.08.2026 gegen eine **unabhängige Quelle** geprüft: Claude Code zeigt
in `/status` inzwischen selbst einen Verbrauchsanteil hoher Kontexte, aus
derselben Datenquelle. Die Nachrechnung traf die angezeigte Zahl auf gut
einen Prozentpunkt — und zeigte, dass die Anzeige **nach Aufwand** gewichtet,
nicht nach Anzahl der Anfragen. Nachzuvollziehen mit
`python kontextbericht.py gegenprobe`.

## Was der Schnitt wirklich spart — 35 verkettete Schnitte

Am 24.08.2026 an sechs Schnitten bilanziert, Ergebnis 1,4x. Die Klärbedingung
war *„zwanzig verkettete Schnitte"*; am 25.08.2026 lagen **35** vor, in 25
Projekten. Methode unverändert: Sitzung A endet bei X Kontext, jede Anfrage
der Folgesitzung B hätte ohne Schnitt X mitgeschleppt statt ihres eigenen
Stands, Ersparnis je Anfrage `max(0, Ende_A − Ctx_i)`. Kosten des Schnitts =
Aufwand der letzten zwölf Anfragen von A.

| | 24.08. (6 Schnitte) | 25.08. (35 Schnitte) |
|---|---|---|
| Faktor gesamt | 1,4x | **2,25x** |
| **Median je Schnitt** | 1,7x | **0,64x** |
| Fehlschläge (unter 1,0x) | 2 von 6 | **22 von 35** |
| Spanne | 0,6x–2,8x | 0,02x–7,46x |
| Ende B höher als Ende A | 4 von 6 | 17 von 35 |

**Das Gesamtergebnis wird besser, das typische deutlich schlechter.** Der
mittlere Schnitt kostet mehr als er spart; in 63 % der Fälle ist er ein
Verlust. Die Summe tragen wenige sehr große: drei Schnitte bei 735k, 657k und
540k Kontext bringen zusammen mehr als die anderen 32 zusammen.

**Die Vermutung vom 24.08. ist bestätigt: der Kontextstand beim Schnitt ist
die Trennlinie.** Oberhalb von etwa 275k zahlt sich der Schnitt fast immer
aus, unterhalb von etwa 200k fast nie — bei Endständen von 49k bis 68k liegt
der Faktor zwischen 0,02 und 0,19. **Diese Größenordnung steht bewusst nicht
im Template**: Die tragende Annahme der Bilanz ist unbewiesen, nämlich dass
Sitzung B dieselbe Arbeit ist, die ohne Schnitt in A weitergelaufen wäre.
Plausibel bei einer Übergabe, nicht belegt — und keine Zahl von Schnitten
kann das belegen.

### Ein dritter Messfehler, gefunden wie die anderen: die Zahl war zu gut

Die erste Fassung dieser Wiederholung ergab **22,5x**. Sechzehnmal der Wert
vom 24.08. — und damit sofort verdächtig. Die Ursache:

**Die gesparten Token wären mitgeschleppter Kontext gewesen, also
Cache-Lesungen zu 0,1x.** Wer sie **roh** gegen die Kosten stellt, die in
Aufwandseinheiten gerechnet sind, vergleicht ungewichtete gegen gewichtete
Token und überschätzt um genau den Faktor 10. Korrekt ist
`gespart_tokens × 0,1`.

Gegengeprüft am einzigen Schnittpaar, das in beiden Messungen vorkommt
(344k → 240k): 18,9k Ersparnis je Anfrage gegen 19,6k am 24.08. — dieselbe
Methode, nur mehr Fälle. Ohne diese Gegenprobe wäre der Gewichtungsfehler
nicht von einer echten Abweichung zu unterscheiden gewesen.

Damit sind es **drei** Messfehler in dieser Auswertungsreihe, die alle nur
auffielen, weil das Ergebnis zu gut war: fehlendes `cache_creation`, die
pauschale Ersparnis (beide 24.08.) und die fehlende Gewichtung (25.08.).
Die Arbeitsregel gilt unverändert und hat sich zum dritten Mal bezahlt.

### Und trägt die Übergabe selbst dazu bei? Nein — der Zeitpunkt tut es

Gemessen am 2026-08-28 über die fünf Tage 23.–27.08. (46 Sitzungen, 4.915
Anfragen). Die Bilanz oben mischt Schnitte mit und ohne Übergabe. Getrennt
ausgewertet — Methode unverändert, zusätzlich je Schnitt geprüft, ob in der
**zweiten Hälfte** von Sitzung A ein `/uebergabe` steht:

| | mit Übergabe | ohne |
|---|---|---|
| Schnitte | 18 | 17 |
| Faktor gesamt | 2,41x | 3,68x |
| **Median je Schnitt** | **1,33x** | **0,45x** |
| Fehlschläge (unter 1,0x) | 6 von 18 | 11 von 17 |
| netto | +15,1M Aufwandseinheiten | +16,0M |
| **Kontext bei Schnitt, Median** | **281k** | **122k** |

Die Paarung ist belegt und nicht unterstellt: **18 von 18** Folgesitzungen
der Übergabeschnitte beginnen mit `/clear` in Zeile ≤5 (ohne Übergabe: 15
von 17). Das ist zugleich die Gegenprobe auf die Falle am Anfang dieser
Datei — `/clear` eröffnet die neue Datei, es beendet nicht die alte.

**Der Vorsprung im Median ist ein Artefakt des Kontextstands.** Beide
Mediane liegen auf verschiedenen Seiten der Trennlinie von ~275k. Auf den
Kontextstand kontrolliert:

| Kontext bei Schnitt | n mit | Median mit | n ohne | Median ohne | Kosten mit | Kosten ohne |
|---|---|---|---|---|---|---|
| 0–150k | 2 | 0,43x | 12 | 0,24x | 242k | 216k |
| 150–275k | 7 | 0,72x | 1 | 1,48x | 478k | 453k |
| >275k | 9 | 3,18x | 4 | 5,66x | 705k | 870k |

In keinem Band ist die Übergabe vorn; in den beiden oberen ist sie hinten.
**Die Bänder tragen die Aussage aber nur in eine Richtung** — auf der
Gegenseite stehen n=1 und n=4, und die vier sind die Extremschnitte bei
536k, 735k und 766k, die auch den Gesamtfaktor 3,68x allein tragen.
Belastbar ist deshalb nur die negative Aussage: **Es gibt keinen Hinweis,
dass die Übergabe für sich genommen Aufwand spart.** Dass sie schadet, sagen
diese Zahlen nicht.

**Was tatsächlich wirkt, ist der Auslöser.** Übergaben fallen im Median bei
281k Kontext, also oberhalb der Trennlinie; Schnitte ohne bei 122k, also
darunter. Alle sechs Fehlschläge mit Übergabe liegen unter 275k (109k bis
240k), die drei größten Gewinne bei 482k, 495k und 516k. Die Regel „Pause
über einer Stunde" trifft in der Praxis die richtigen Momente, ohne den
Kontextstand je zu nennen.

**Die Kostenseite bestätigt `core/prinzip.md:61` unabhängig.** Dort steht,
die Übergabe koste rund ein Fünftel der Sitzung und werde mit dem
Kontextstand teurer. Gemessen steigt der Aufwand der letzten zwölf Anfragen
von 242k über 478k auf 705k je Band — dieselbe Richtung, aus anderer Quelle.

**Und damit bestätigt diese Messung `core/prinzip.md:63`, statt es zu
widerlegen.** Dort steht seit jeher: *„Deshalb steht die Empfehlung nicht auf
dem Sparen … Ist die Aufgabe nach dem Schnitt fertig, spart die Übergabe gar
nichts und ist trotzdem richtig geschrieben."* Das war ein Argument; jetzt
ist es gemessen. Der Ertrag der Übergabe liegt auf der vierten Kostenart —
Entscheidungen und Begründungen, die sonst verloren gehen — nicht auf dem
Kontext.

**Der tragende Vorbehalt gilt hier stärker als oben, nicht schwächer.** Die
Annahme, Sitzung B sei dieselbe Arbeit, die sonst in A weitergelaufen wäre,
bleibt unbewiesen. Bei einem Übergabeschnitt ist sie am plausibelsten — die
Übergabe stellt genau diese Fortsetzung her. Der Vergleich mit/ohne
begünstigt die Übergabeseite also systematisch, und sie gewinnt trotzdem
nicht.

**Seit 2026-10-29 Betriebsart `bilanz`** (Abschnitt „Wiederholung am
2026-10-29"). Bis dahin galt: **Nachbaubar aus `kontextbericht.py`,** aber nicht als Betriebsart darin
enthalten. Was fehlt: Sitzungen je Projekt nach `erste`/`letzte` verketten,
überlappende Paare verwerfen, je Paar `max(0, Ende_A − Ctx_i) × 0,1` gegen
den Aufwand der letzten zwölf Anfragen von A, Gruppierung nach der
Fundstelle von `/uebergabe`. Ob das eine dritte Betriebsart werden soll,
stand als **Punkt 26** offen — ein zweites Skript wäre nach dem Abschnitt
„Warum hier Code liegt" das Falsche. **Am 2026-09-01 entschieden: dritte
Betriebsart.** Der Grund steht im nächsten Abschnitt.

### Wiederholung am 2026-09-01 — derselbe Befund, besser besetzt

Fenster 28.08.–01.09., drei Arbeitstage, 40 Sitzungen, 4.321 Anfragen, 28
verkettete Schnitte in 10 Projekten, 11 davon mit Übergabe. Methode
unverändert.

| | mit Übergabe | ohne |
|---|---|---|
| Schnitte | 11 | 17 |
| Faktor gesamt | 2,73x | 3,68x |
| **Median je Schnitt** | **1,39x** | **0,51x** |
| Fehlschläge (unter 1,0x) | 4 von 11 | 11 von 17 |
| **Kontext bei Schnitt, Median** | **293k** | **153k** |

Auf den Kontextstand kontrolliert:

| Kontext bei Schnitt | n mit | Median mit | n ohne | Median ohne |
|---|---|---|---|---|
| 0–150k | 0 | — | 8 | 0,13x |
| 150–275k | 5 | **0,85x** | 3 | 0,98x |
| >275k | 6 | **3,60x** | 6 | 4,26x |

**Im oberen Band stehen jetzt sechs gegen sechs**, am 2026-08-28 waren es
neun gegen vier. Der Vergleich ist damit belastbarer als in der Vorrunde, und
das Ergebnis ist dasselbe: In keinem vergleichbaren Band ist die Übergabe
vorn. **Der Befund „der Zeitpunkt wirkt, nicht das Verfahren" ist bestätigt.**
Paarung geprüft: 11 von 11 Folgesitzungen der Übergabeschnitte beginnen mit
`/clear` in Zeile ≤5.

**Die Nutzungsrate ist gesunken** — 39 % der Schnitte tragen eine Übergabe,
in der Vorrunde 55 %. Das ist keine Aussage über das Verfahren, sondern über
seine Anwendung, und es berührt Punkt 25.

#### Der vierte Messfehler, und warum er die Vorrunde nicht beschädigt

Die erste Fassung dieses Nachbaus ergab für die Übergabe **3,79x statt
2,73x** — wieder zu gut, wieder deshalb geprüft. Ursache: Der Detektor suchte
`/uebergabe` im Klartext und zählte damit **7 von 18** Sitzungen mit, in denen
bloß *über* den Skill geredet wurde. Im Basisagenten selbst ist das der
Normalfall. Belastbar wurde die Zahl erst mit `<command-name>/uebergabe` plus
dem Skill-Werkzeugaufruf; die beiden größten Gewinne des Fensters (10,93x und
10,50x) wanderten dabei von „mit" nach „ohne".

**Gegengeprüft, ob die Vorrunde denselben Fehler trug** — beide Detektoren
über das alte Fenster gerechnet:

| Bandbesetzung (mit/ohne) | 0–150k | 150–275k | >275k |
|---|---|---|---|
| Messung vom 2026-08-28 | 2 / 12 | 7 / 1 | 9 / 4 |
| Nachbau, strenger Detektor | 2 / 12 | 7 / 0 | 8 / 2 |
| Nachbau, laxer Detektor | 7 / 7 | 7 / 0 | 9 / 1 |

Die Vorrunde deckt sich mit dem **strengen** Detektor. **Sie bleibt gültig.**

#### Warum die Prosa nicht reicht — Punkt 26, entschieden

Dieselbe Gegenprobe zeigt aber, dass der Nachbau die Vorrunde **nicht exakt
reproduziert**: 31 statt 35 Schnitte, rund 11 % weniger, bei 44 statt 46
Sitzungen. Woran es liegt, ist aus der Beschreibung nicht entscheidbar — sie
nennt das Fenster, aber nicht, ob nach Tagesdatum oder stundengenau gefiltert
wird und ob eine Sitzung nach ihrem ersten oder letzten Zeitstempel
hineinfällt. Dazu die Detektorfalle, die in der Prosa gar nicht vorkommt.

**Zwei unabhängige Gründe, beide erst durch das Nachbauen sichtbar.** Damit
ist die Prüffrage aus Punkt 26 beantwortet: Eine dritte Betriebsart `bilanz`
gehört in `kontextbericht.py`. **Auflage** aus demselben Punkt: Die Kopfhilfe
muss die dritte Filterlogik so ausdrücklich nennen wie die beiden bestehenden
— verkettete Paare, Sitzung nach letztem Zeitstempel —, und der strenge
Detektor gehört mit Begründung in den Code, nicht in diese Datei.

### Wiederholung am 2026-10-29 — jetzt als Betriebsart, über 30 Tage

Seit diesem Tag steht die Bilanz im Werkzeug:
`python kontextbericht.py [--tage N] bilanz`. Filterlogik, Detektor und
Kostenansatz stehen mit Begründung im Code. Fenster 29.09.–29.10.,
204 Schnitte in 14 Projekten, 20 überlappende Paare verworfen, alles auf
Opus 5.5 (Cache lesen 0,05x).

| | mit Übergabe | ohne |
|---|---|---|
| Schnitte | 121 | 83 |
| Faktor gesamt | 1,24x | 0,47x |
| **Median je Schnitt** | **0,77x** | **0,19x** |
| Fehlschläge (unter 1,0x) | 76 von 121 | 74 von 83 |
| netto | +7,1M | −7,3M |
| **Kontext bei Schnitt, Median** | **195k** | **103k** |
| B beginnt mit `/clear` | 115 von 121 | 58 von 83 |

| Kontext bei Schnitt | n mit | Median mit | n ohne | Median ohne |
|---|---|---|---|---|
| 0–150k | 43 | 0,20x | 64 | 0,11x |
| 150–275k | 39 | 0,79x | 16 | 0,91x |
| >275k | 39 | 1,71x | 3 | 1,51x |

**Der Befund hält zum dritten Mal:** Bandkontrolliert ist die Übergabe
nicht durchgehend vorn. Der Abstand im Gesamtmedian kommt aus dem
Kontextstand. Im oberen Band steht sie allerdings fast allein: Schnitte
ohne Übergabe über 275k kommen kaum noch vor (3).

**Die Trennlinie liegt wie bisher bei 200k bis 275k.** In feineren Bändern
liegt der Median bei 0,60x für 150–200k, 1,04x für 200–250k und 1,46x für
250–300k. Unter 200k lohnen sich 6 von 138 Schnitten, ab 250k 40 von 51.
Die Faktoren liegen niedriger als im August. Das passt zum halbierten
Cache-Lesefaktor, ist aber nicht getrennt nachgerechnet.

**Die Nutzungsrate ist gestiegen: 59 % der Schnitte tragen eine Übergabe**,
nach 55 % und 39 % in den Vorrunden. Vergleichbar nur mit Vorbehalt:
30 Tage statt drei bis fünf, andere Projektmischung.

**Zwei Dinge, die jede künftige Auswertung betreffen:**

- **Das Protokollformat hat neue Kopfzeilen** (`type=mode`, `cost-state`,
  `bridge-session` und andere). `/clear` steht deshalb nicht mehr in
  Zeile 3, sondern meist in Zeile 6 bis 20. Mit der alten Prüfung „Zeile
  ≤5" wären es 60 statt 115 gepaarte Übergabeschnitte gewesen. Die
  Betriebsart zählt deshalb `/clear` vor der ersten Anfrage. Neu sind auch
  Zeilen `type=api-request-blob`, die den Befehlstext als Kopie tragen. Der
  Detektor schließt sie aus.
- **Die Rohdaten halten nur 7 Tage.** Claude Code löscht Protokolle nach
  `cleanupPeriodDays`, Standard 30 Tage (code.claude.com/docs,
  „Data usage", abgerufen 2026-10-29). Der Nutzer hat am 2026-10-29 aus
  Datenschutzgründen 7 Tage eingestellt. **Jede Messung muss ihre Zahlen
  deshalb hier festhalten.** Ein Verweis auf die Protokolle ist nach einer
  Woche wertlos. Diese Wiederholung lief auf dem letzten 30-Tage-Bestand.

**Nicht mehr prüfbar:** ob die Betriebsart die 35 Schnitte vom 2026-08-28
oder die 31 des Nachbaus reproduziert. Die Protokolle dieses Fensters sind
gelöscht.

## Warum die Stunde die richtige Schwelle ist

Gemessen am 25.08.2026 über 63 Sitzungen und 5.794 Anfragen. Die Empfehlung
*„Pause über einer Stunde: `/uebergabe`, dann `/clear`"* stand bis dahin auf
der Cache-Haltedauer als **Ableitung**. Sie ist jetzt gemessen — je Anfrage
die Pause seit der vorigen Anfrage **derselben** Sitzung, dagegen der Anteil,
der neu geschrieben statt gelesen wurde:

| Pause davor | Anfragen | Schreibanteil | Aufwand je Anfrage |
|---|---|---|---|
| < 1 min | 4.305 | 0,9 % | 28k |
| 1–5 min | 1.133 | 2,2 % | 34k |
| 5–20 min | 262 | 4,5 % | 46k |
| 20–60 min | 59 | 9,4 % | 74k |
| **1–4 Std** | 22 | **91,5 %** | **481k** |
| > 4 Std | 13 | 91,5 % | 558k |

Der Sprung liegt exakt auf der Haltedauer, nicht daneben: **Faktor 6,5 im
Aufwand je Anfrage**, Schreibanteil von 9 % auf 92 %. Diese 35 Anfragen sind
0,6 % aller Anfragen und tragen 9 % des Cache-Aufwands. Die erste Anfrage
einer Sitzung ist ausgenommen — dort ist trivialerweise nichts im Cache.

**Wechsel oder echte Pause — der Test, der die Aussage trägt.** Aus dem
Sprung folgt noch nicht, dass paralleles Arbeiten schuld ist; eine
Mittagspause kostet dasselbe, und die hätte serielles Arbeiten auch nicht
vermieden. Unterscheidbar ist es, indem man für jede Lücke prüft, ob
**währenddessen in einem anderen Projekt** Verkehr war:

| Art | Pausen | neu geschrieben | Mehrkosten |
|---|---|---|---|
| Wechsel (parallel gearbeitet) | 22 | 5,5M | 10,5M |
| Pause (nirgends Verkehr) | 13 | 3,4M | 6,4M |

**Diese 10,5M sind zu hoch, und der Grund gehört dazu:** Eine Lücke von 64
Stunden wird zwangsläufig als „Wechsel" gezählt, weil irgendwann irgendwo
gearbeitet wurde — der Cache wäre aber nach einer Stunde ohnehin verfallen.
Vermeidbar sind nur die *kurzen* Wechsel. Nach Länge aufgeschlüsselt:

| Pausenlänge | Wechsel | neu geschrieben | echte Pausen |
|---|---|---|---|
| 1–2 Std | 9 | 2,4M | 7 |
| 2–4 Std | 5 | 1,1M | 1 |
| 4–12 Std | 1 | 52k | 2 |
| > 12 Std | 7 | 2,0M | 3 |

**Klar vermeidbar: 14 Wechsel unter 4 Stunden, 3,5M neu geschrieben, 6,7M
Aufwandseinheiten Mehrkosten** — rund 3,5 % des gesamten Cache-Aufwands.
Der sichtbare Wiederholtäter war ein Hin und Her zwischen zwei Projekten im
Abstand von 1,1 bis 1,4 Stunden, dreimal, gut 1,1M neu geschrieben.

**Die verwertbare Regel ist deshalb nicht „eins nach dem anderen".** Es ist
eine Rechnung: *Anzahl der Projekte, durch die du rotierst, × Zeit je
Projekt muss unter einer Stunde bleiben.* Zwei Projekte im 20-Minuten-Wechsel
bleiben beide warm und kosten nichts extra. Fünf Projekte im
20-Minuten-Wechsel lassen jedes einzelne verfallen. Teuer ist nicht das
Verlassen einer Sitzung, sondern das **Zurückkommen** — und eine Sitzung, die
mit `/clear` beendet wurde, kostet gar nichts mehr.

Deshalb steht seit 0.13.0 im Auslöserblock der Regeldatei: *„Ein Wechsel in
ein anderes Projekt ist so eine Pause."* Es ist der Fall, den man nicht
bemerkt, weil man selbst durchgehend arbeitet.

## Warum hier Code liegt, obwohl der Basisagent keiner hat

`AGENTS.md:7` nennt das Projekt ein Textprojekt ohne Code, und
`core/verworfen.md` hat **Skriptordner verworfen**. Beides gilt weiter und
wird hier nicht aufgeweicht:

- Die Verwerfung betraf Skriptordner **in Zielprojekten**, mit
  Ausführfreigabe per Muster — der Sicherheitsvorbehalt dort bleibt
  vollständig gültig. Hier wird nichts eingerichtet und nichts freigegeben.
- Ihre Revisionsbedingung gibt die Form vor: *„nicht als Ordner …, sondern
  als **eine Datei** mit dem gemeinsamen Kern"*. Deshalb ist es genau eine
  Datei. Sie war ursprünglich zwei; beim Übernehmen zusammengeführt, geprüft
  durch Ausgabevergleich beider Betriebsarten vor und nach dem Zusammenlegen.

**So wird eine Änderung am Werkzeug gegengeprüft.** Alte Fassung
(`git show HEAD:core/belege/kontextbericht.py`) und neue auf einer
**eingefrorenen Kopie** der Protokolle laufen lassen, sonst wächst die
laufende Sitzung zwischen den beiden Läufen. `wurzel_finden()` folgt `~`: Es
genügt, `USERPROFILE` (Windows) und `HOME` auf ein Verzeichnis zu setzen, das
`.claude/projects/<projekt>/*.jsonl` als Kopie enthält. Danach jede
Abweichung unabhängig aus den Rohdaten nachrechnen. Zuletzt so geprüft am
2026-09-24 (Faktor je Modell, `feedback/offene-punkte.md`, Punkt 42).

Wächst das hier auf mehrere Skripte an, ist das der Anlass, die Verwerfung
neu zu lesen — nicht der Anlass, einen `tools/`-Ordner anzulegen.

## Was bewusst nicht übernommen wurde

Das Herkunftsprojekt hat vor der Messung versucht, den Kontextverbrauch
**live anzuzeigen** — Statusline und Hook-Hinweise. Das trug nicht und wurde
zurückgestellt; die Befunddatei ist mit dem Projekt weggefallen. Der Kern
in zwei Sätzen, damit es niemand ungeprüft erneut plant:

- Ein Schwellenwert-Hinweis über `PostToolUse` ist **nicht gratis baubar**:
  die eine Ausgabeform sieht niemand, die dokumentierte kostet Kontext.
- Die Statusline war in der VS-Code-Extension **nicht sichtbar**. Der
  entscheidende Gegenversuch im echten Terminal wurde nie gemacht — das ist
  ein Verdacht, kein Befund.

Wer das aufgreifen will, fängt bei diesem Versuch an. Ein Eintrag in
`core/verworfen.md` mit Revisionsbedingung wäre der richtige Ort dafür —
er steht noch aus, weil ein einzelnes Projekt dafür nach `AGENTS.md:17`
nicht reicht.
