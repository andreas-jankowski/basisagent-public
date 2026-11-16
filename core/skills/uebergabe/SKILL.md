---
name: uebergabe
description: Schreibt den Aufgabenstand nach uebergabe/ fort, sichert ihn und empfiehlt /clear. Nutze bei "übergabe", "aufgabe fertig", "vor der pause", "kontext voll".
disable-model-invocation: true
---

# Übergabe

Der Stand einer Aufgabe kommt auf die Platte, damit die Sitzung enden kann.

Zwei Betriebsarten, erkennbar am Aufruf:

| Aufruf | Betriebsart |
|---|---|
| `/uebergabe` oder mit freiem Text | **Schreiben** — der Normalfall |
| `/uebergabe einrichten` | **Einrichten** — einmalig je Projekt |

---

## Warum überhaupt

Kontext, der einmal geladen ist, wird bei **jeder** folgenden Anfrage erneut
gelesen und erneut bezahlt — beim Zwischenspeicher zu etwa einem Zehntel des
Einzelpreises. Ein Token aus Zug 20 einer 100-Zug-Sitzung wird 80-mal
wiedergelesen. Der Verbrauch wächst damit **quadratisch** mit der
Sitzungslänge: dieselbe Arbeit auf zwei Sitzungen geteilt kostet die Hälfte,
zweimal geteilt ein Drittel.

Beim Beenden verliert man rund drei Viertel Maschinenverkehr — Werkzeugaufrufe
und deren Ausgaben, die noch auf der Platte liegen und gezielt nachlesbar
sind. Nicht wiederbeschaffbar sind Entscheidungen, Begründungen und verworfene
Wege. **Der Fehler ist nie `/clear`, sondern `/clear` ohne Übergabe.**

Deshalb nicht `/compact`: das Zusammenfassen kostet eine Modellanfrage bei
größtem Kontext und entscheidet ohne dich, was wegfällt.

---

## Betriebsart 1 — Schreiben

**1. Datei bestimmen.** Eine Datei je Aufgabe: `uebergabe/<aufgabe>.md`,
Name in Kleinschreibung mit Bindestrichen. Fehlt `uebergabe/`, wechsle zu
Betriebsart 2.

**2. Schneiden oder fortschreiben — entschieden wird das hier, vor dem
Schreiben.** Gibt es die Datei schon, prüfe zuerst, ob sie den neuen
Abschnitt noch aufnimmt. Zwei Anzeichen, jedes für sich genügt:

- **ab etwa 8.000 Zeichen** (~2.300 Token) — die laufende Datei wird zu
  Sitzungsbeginn gelesen und läuft ab Zug 1 mit, dem teuersten Platz;
- **beim dritten `## Fortschreibung`** — dann ist die Aufgabe meist eine
  andere geworden als die, die oben im „Ziel" steht.

Der Schnitt: sag es dem Nutzer, erklär die Aufgabe für beendet, verschieb
die Datei nach `uebergabe/erledigt/` und leg die neue an — **in die**
schreibst du diese Sitzung, mit einem Verweis auf die alte im Abschnitt
„Stand". Sonst wird sie fortgeschrieben.

**Ziel erreicht? Dann abschließen** — nach Schritt 6, nicht stattdessen.
Maßstab ist der Satz unter „Ziel", nicht die Liste der offenen Fragen. Geh
jede verbliebene Frage einzeln durch: Sie wandert ins Projekt
(Systemdoku, Projektdokument, eigene neue Übergabe), oder der Nutzer lässt
sie ausdrücklich fallen. Danach die Datei nach `uebergabe/erledigt/` — wo
das Projekt Verschieben freigabepflichtig macht, mit Freigabe. Ohne diesen
Schritt bleibt eine erledigte Übergabe liegen, weil sie der einzige Ort
ihrer Reste ist: gezählt 31 offene in einem Projekt, die meisten nur mit
Fragen *blockiert nicht*.

**Vor jedem Verschieben nach `erledigt/` — beim Schnitt wie beim
Abschluss — prüfen, ob der Name dort frei ist.** Ist er belegt, bekommt die
verschobene Datei die nächste freie Nummer (`<aufgabe>-2.md`, `-3` …); nie
überschreiben. Belegt in einem Projekt: Ein `mv` ersetzte die Erstfassung
derselben Aufgabe, zurück nur über Git.

Hier und nicht am Schluss, weil der Schnitt nur vorher folgenlos ist:
danach hieße er, den eben geschriebenen Abschnitt wieder auszubauen, und die
Nachfolgedatei wäre eine zusätzliche Bitte nach getaner Arbeit — die dann
ausbleibt und den Faden mit in den Ordner nimmt, in dem nicht mehr gelesen
wird.

**Nicht verdichten, nicht löschen, nicht zusammenfassen.** Der Wert einer
alten Übergabe liegt in den verworfenen Wegen — genau dem, was eine
Zusammenfassung streicht. Eine abgeschlossene Datei kostet nichts, weil
niemand sie mehr öffnet. Das Aufräumen ist ein Schnitt, kein Kürzen.

**3. Fortschreiben statt umschreiben.** Was dasteht, bleibt stehen. Neues
kommt als Abschnitt `## Fortschreibung <Datum> — <Stichwort>` ans Ende,
danach wird „Nächster Schritt" ersetzt. Ein späterer Leser muss sehen, was
wann galt.

**4. Zuerst das System nachziehen, dann hier schreiben.** Was die Sitzung
erarbeitet hat, gehört ins Projekt: der Zustand in die Doku des Systems,
wiederkehrende Arbeit in ein Runbook, eine festgehaltene Messung in einen
Bericht. Das gilt auch für Nebenertrag — eine Recherche über Fassungen,
Module oder Bezugswege ist Sachwissen über das System, nicht Sitzungsverlauf.
Genau der fällt sonst durch, weil er zu keiner Aufgabe gehört und deshalb im
Sitzungstext landet.

Eine Übergabe in `erledigt/` wird nicht mehr geöffnet. Das ist ihr Zweck
(Schritt 2) und zugleich die Falle: **was dort als einziger Ort steht, ist
verloren.** Prüfe deshalb vor dem Schreiben, welches Projektdokument den
Ertrag aufnimmt, und zieh es nach — erst was dort keinen Platz hat, kommt
hierher.

**Dasselbe gilt für den Arbeitsordner der Sitzung** (in Claude Code: der
Scratchpad). Er ist kein Ablageort; sein Pfad gehört zur Sitzung, eine
spätere findet ihn nur durch Zufall. Ordne vor dem Schreiben jede Datei darin
ein: was Wert hat — Code, Belege, Sicherungen — ins Projekt, den Rest dem
Nutzer als löschbar nennen. Eine Übergabe verweist nie auf ihn. Darf
Fremdsoftware oder Herstellerdoku nicht ins Repository, braucht das Projekt
dafür einen benannten Ort außerhalb; fehlt er, frag danach.

**Was hierher gehört.** Nur, was sich **nicht** aus dem Repository
zurückholen lässt:

- **Entscheidungen mit Grund** — und die verworfene Alternative, mit Grund.
  Ohne sie wird sie beim nächsten Mal erneut geprüft.
- **Offene Fragen**, je mit dem Vermerk *blockiert* oder *blockiert nicht*.
  Bei *blockiert nicht* dazu, wohin die Frage beim Abschluss geht.
- **Belege** als `pfad:zeile` oder URL. Keine Zitate, keine Dateiinhalte,
  keine vollständigen Fehlerausgaben — das ist genau der Maschinenverkehr,
  der ohnehin wiederbeschaffbar ist.
- **Genau ein nächster Schritt**, so konkret, dass er ohne Nachdenken
  begonnen werden kann.

Was der Code, die Versionshistorie oder die Regeldatei schon sagt, gehört
nicht hinein.

**5. Aussagen über Werkzeugverhalten** tragen ihren Beleg oder das Wort
„ungeprüft". Sonst gehören sie unter „Offene Fragen". Eine Vermutung, die als
Befund gelesen wird, kostet später mehr als die fehlende Zeile.

**6. Sichern.** Nach dem projekteigenen Weg — im Zweifel fragen, nicht raten.
`uebergabe/` gehört in die Versionshistorie. Führt das Projekt keine, sag
es: dann ist die Datei ungesichert.

**7. Ergebnis nennen und `/clear` empfehlen.** Nenne den Dateipfad und den
nächsten Schritt in einer Zeile, dann: neue Sitzung mit `/clear`, dort zuerst
diese Datei lesen. Du kannst `/clear` nicht selbst auslösen — vorschlagen
genügt.

---

## Betriebsart 2 — Einrichten

Einmalig je Projekt, drei Schritte:

1. Ordner `uebergabe/` anlegen, darin `_vorlage.md` mit dem Aufbau unten.
2. Sicherstellen, dass `uebergabe/` **nicht** ignoriert wird — im Gegensatz
   zu einem Wegwerfordner wie `.tmp/`.
3. In die Regeldatei (`AGENTS.md` bzw. `CLAUDE.md`) den Auslöser aufnehmen —
   drei Zeilen, mehr nicht:

```markdown
## Übergabe
- Neue Aufgabe oder Pause über einer Stunde: `/uebergabe` vorschlagen,
  danach `/clear`. Nicht `/compact`. Ein Wechsel in ein anderes Projekt
  ist so eine Pause.
- Stand je Aufgabe: `uebergabe/<aufgabe>.md`.
```

Der Auslöser muss in der Regeldatei stehen, weil er **immer** gilt. Das
Verfahren selbst darf es nicht: dieser Skill trägt
`disable-model-invocation: true` und liegt deshalb erst im Kontext, wenn du
ihn aufrufst.

**Warum die Stunde und warum der Projektwechsel dazugehört.** Die Schwelle
ist keine runde Zahl, sondern die Haltedauer des Prompt-Caches. Solange eine
Sitzung darin liegt, kostet ihr mitgeschleppter Kontext ein Zehntel; danach
muss er neu geschrieben werden und kostet das Doppelte — Faktor 20 auf
denselben Text. Gemessen über 63 Sitzungen: Eine Anfrage nach einer Pause
von über einer Stunde kostet **6,5-mal** so viel wie eine knapp darunter
(481k gegen 74k Aufwandseinheiten), und der Schreibanteil springt von 9 %
auf 92 %. Wer zwischen mehreren Projekten wechselt, hat subjektiv **keine**
Pause und lässt trotzdem jede liegengelassene Sitzung verfallen. Deshalb
steht der Wechsel im Auslöser: Er ist der Fall, den man nicht bemerkt.
Belege in `core/belege/README.md`.

### Aufbau von `_vorlage.md`

```markdown
# <Aufgabe> — Stand <Datum>

## Ziel
Ein Satz. Was gilt als fertig.

## Stand
Was läuft, was nicht. Zwei bis fünf Zeilen.

## Belege
- pfad/zu/datei:42           ← wo es sitzt
- <URL oder Versuchsausgabe> ← woher die Aussage kommt

## Entscheidungen
- <Entscheidung> — weil <Grund>. Verworfen: <Alternative>, weil <Grund>.

## Offene Fragen
- <Frage> — blockiert / blockiert nicht → beim Abschluss nach: <Ort>

## Nächster Schritt
Genau einer. So konkret, dass du ihn ohne Nachdenken beginnen kannst.
```
