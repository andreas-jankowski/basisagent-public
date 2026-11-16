> **Übernommen aus Werkzeugprojekt A am 23.08.2026.**
> Dies ist die abgeschlossene Übergabe jener Aufgabe und damit der Beleg für
> die Kostenart **Wiederholkosten** in `core/prinzip.md` sowie für die Zahlen,
> mit denen `core/skills/uebergabe/SKILL.md` argumentiert. Sie wird **nicht**
> fortgeschrieben — sie ist ein Beleg, keine laufende Aufgabe.
>
> Die Pfade in den Belegen zeigen auf das damalige Projekt. Übersetzung:
>
> | dort | hier |
> |---|---|
> | `werkzeug/kontextbericht.py` | `core/belege/kontextbericht.py` |
> | `werkzeug/gegenprobe-usage.py` | dieselbe Datei, Betriebsart `gegenprobe` |
> | `uebergabe/statusline.md` | **nicht übernommen**, siehe `README.md` |

<!--
REGELN — gelten für jede Aktualisierung dieser Datei:
1. Belege als pfad:zeile. Keine Zitate, keine Dateiinhalte, keine
   vollständigen Fehlerausgaben.
2. Hinein gehört nur, was sich NICHT aus dem Repository zurückholen
   lässt: Entscheidung, Begründung, verworfene Alternative, offene Frage.
3. "Nächster Schritt": genau einer, ohne Nachdenken beginnbar.
4. Nichts umschreiben, was schon dasteht. Nur ergänzen und den Stand
   fortschreiben.
5. Aussagen über Werkzeugverhalten tragen ihren Beleg oder das Wort
   "ungeprüft". Sonst gehören sie unter "Offene Fragen".
-->

# Auswertung: Kontextkosten im Nachhinein sichtbar machen — Stand 23.08.2026

## Ziel
Ein Bericht, der ohne Modell und ohne Kontextkosten sagt, wohin der
Verbrauch geht, welche Sitzungen entgleist sind und **wer** den Kontext
gefüllt hat. Fertig, wenn er aus den Sitzungsprotokollen läuft und die
Zahlen gegen eine Stichprobe stimmen.

## Stand
Läuft. `werkzeug/kontextbericht.py`, aufgerufen mit `--tage N`, `--projekt X`,
`--brocken N`. Erste Auswertung über 49 Sitzungen und 4780 Anfragen liegt vor
und hat die Projektfrage beantwortet — siehe „Befunde".

Diese Aufgabe ist der Ersatz für die Statusline. Warum die nicht ging, steht
in `uebergabe/statusline.md`.

## Befunde aus der ersten Auswertung
Alle Zahlen aus `~/.claude/projects/*/*.jsonl`, Feld `message.usage`.

- **Rund 60 % des Aufwands ist wiedergelesener Kontext.** 1206M Token
  Cache-Lesen gegen 6,4M Ausgabe und 51k frische Eingabe. Nicht das Denken
  kostet, nicht das Schreiben — das Mitschleppen.
- **Im Schnitt 252k Token je Anfrage, 78 % aller Anfragen über 100k.**
- **Daraus die Faustregel:** Ein Token in Zug 20 einer 100-Zug-Sitzung wird
  80-mal wiedergelesen, kostet bei Faktor 0,1 also das Achtfache seines
  Einzelpreises. Der Verbrauch wächst **quadratisch** mit der Sitzungslänge.
  Eine in der Mitte geteilte Sitzung kostet die Hälfte, zweimal geteilt ein
  Drittel — bei gleicher Arbeit. Das ist die Rechnung, die `/clear`
  begründet, und sie stammt aus eigenen Daten, nicht aus einer Empfehlung.
- **Woraus der Kontext besteht:** 42 % Werkzeug-Ausgaben, 31 %
  Werkzeug-Aufrufe, 10 % Claude-Text, 10 % Nutzereingaben, 7 % Anhänge.
  **73 % ist Maschinenverkehr.** `Read` allein stellt 55 % aller
  Werkzeugausgaben.
- **Damit ist die Frage „was verliere ich beim `/clear`" beantwortet:**
  zu drei Vierteln Material, das noch auf der Platte liegt und gezielt
  nachlesbar ist. Nicht wiederbeschaffbar sind Entscheidungen und
  Begründungen — genau das, was `uebergabe/` festhält. Der Fehler ist nie
  `/clear`, sondern `/clear` ohne Übergabe.

## Belege
- `werkzeug/kontextbericht.py:26-32` — Preisfaktoren mit Doku-Zitat im
  Kommentar: Cache lesen 0,1×, schreiben 1,25× (5 Min.) bzw. 2× (1 Std.),
  Ausgabe 5× bei Opus
- Doku-Beleg dafür: code.claude.com/docs, Prompt Caching, Abschnitt
  „Economics"
- Herkunftsanalyse ist eine **Schätzung** (Zeichen ÷ 4), im Bericht so
  gekennzeichnet. Die Verbrauchszahlen darüber sind es nicht — die kommen
  aus `message.usage`
- Claudes Denkschritte stehen nicht im Klartext im Protokoll und fehlen
  daher in der Herkunftsanalyse. Geprüft: das Feld `thinking` ist leer und
  trägt nur eine Signatur

## Entscheidungen
- **Auswerten statt anzeigen** — weil die Live-Anzeige in der
  VS-Code-Extension nicht läuft (siehe `statusline.md`) und weil der Bericht
  mehr kann: er nennt den Verursacher, nicht nur die Größe. Verworfen:
  weiter am Anzeigekanal suchen, weil beide verbliebenen Kandidaten
  (`systemMessage`, `terminalSequence`) entweder tot oder ungeprüft sind.
- **Python statt PowerShell** — obwohl `AGENTS.md` PowerShell 5.1 als
  Zielsystem nennt. Grund: zeilenweises JSON über hunderte Megabyte. Python
  ist auf dem Rechner vorhanden und wurde im Betrieb getestet. Wenn das
  stört, ist es zu ändern, bevor mehr darauf aufbaut.
- **Neuer Ordner `werkzeug/`** — `AGENTS.md` kennt bisher nur `doku/`,
  `uebergabe/`, `.tmp/`. Der Ordner gehört in die Versionshistorie. Sollte
  in `AGENTS.md` nachgetragen werden.
- **Der Bericht gibt keine Inhalte aus**, nur Größen, Werkzeugnamen und
  gekürzte Ziele. Sonst würde ein Werkzeug gegen Kontextverbrauch selbst
  Kontext fluten.

## Offene Fragen
- **Die Schätzung Zeichen ÷ 4 ist nicht geprüft** — blockiert nicht, die
  relativen Anteile tragen. Für absolute Zahlen wäre `count_tokens` nötig,
  und das kostet eine API-Anfrage je Messung.
- **Bei `--tage` steckte ein stiller Fehler**: der Filter griff auf die
  Sitzungsliste, nicht auf die Herkunftsanalyse — beide Läufe lieferten
  dieselben Prozentzahlen. Behoben (`kontextbericht.py:88-92,141-143`) und
  per Gegenprobe geprüft: 7 Tage 1,2M gegen alle 1,9M. **Lehre: jeder
  weitere Filter braucht dieselbe Gegenprobe**, sonst liefert das Werkzeug
  genau die stille Falschzahl, gegen die `AGENTS.md` schreibt.
- **Der 1-Stunden-Cache verdoppelt den Schreibfaktor**, das Skript rechnet
  fest mit 1,25×. In den Protokollen taucht `ephemeral_1h_input_tokens`
  auf — das Feld liegt also vor, wird aber nicht ausgewertet. Der Aufwand
  für „Cache geschrieben" ist dadurch eher zu niedrig angesetzt.

## Fortschreibung 23.08.2026 — Schreibfaktor nachgezogen
Erledigt (`kontextbericht.py:30-32,146-158,203-205`). Befund, der die
Schätzung vorher deutlich verzerrt hat: **Das gesamte Cache-Schreiben läuft
mit 1-Stunden-Haltedauer** — 26,2M Token gegen 0 bei 5 Minuten. Der Faktor
ist also durchgehend 2,0 und nicht 1,25.

Folge für die Zahlen: „Cache geschrieben" steigt von 33M auf 52,5M Aufwand,
sein Anteil von 17,7 % auf 25,4 %. Der Anteil des Wiederlesens sinkt
entsprechend von 65 % auf 59 % — die Aussage bleibt, die Größenordnung
verschiebt sich. Was ohne Angabe käme, wird getrennt ausgewiesen und mit
1,25 gezählt; aktuell ist dieser Posten null.

## Fortschreibung 23.08.2026 — Claude Code wertet inzwischen selbst aus
Der Nutzer zeigte den `/status`-Bildschirm. Unter „What's contributing to
your limits usage?" steht dort eine Auswertung, die es beim Projektstart
nicht gab, mit der Fußnote „Approximate, based on local sessions on this
machine". **Das ist dieselbe Datenquelle, aus der `kontextbericht.py`
rechnet.** Die Zeile im Wortlaut, weil sie der Prüfgegenstand ist:
`86% of your usage was at >150k context`.

**Gegenprobe gemacht, und sie beantwortet, wie die Zahl zu lesen ist.**
Über dieselben 24 Stunden aus den eigenen Protokollen:

| Schwelle | Anteil der Anfragen | Anteil des Aufwands |
|---|---|---|
| >100k | 77,0 % | 90,5 % |
| >150k | **64,6 %** | **83,7 %** |
| >200k | 58,2 % | 78,9 % |

Nur die aufwandsgewichtete Spalte trifft die 86 %; die Anfragenzahl liegt
21 Punkte daneben. **Befund: Die eingebaute Anzeige gewichtet nach
Verbrauch, nicht nach Anzahl.** Wer sie als „86 % meiner Anfragen" liest,
liegt falsch.

**Zweiter Befund, der das Werkzeug betrifft:** Damit ist
`kontextbericht.py` erstmals gegen eine **unabhängige Quelle** validiert.
Bisher standen die Preisfaktoren nur auf einem Doku-Zitat (siehe „Belege"
oben). Dass die eigene Rechnung die Anthropic-Zahl auf gut einen Punkt
trifft, ist ein Beleg für die Faktoren — kein Beweis, dass dieselbe Formel
läuft.

## Entscheidungen aus dieser Fortschreibung
- **Das Projekt wird nicht überflüssig.** Der Bildschirm sagt, *dass* es
  teuer ist — eine Zahl plus die Empfehlung `/compact`/`/clear`. Der
  Bericht sagt, *woran*: Aufteilung Cache/Ausgabe, 73 % Maschinenverkehr,
  `Read` als größter Posten, Sitzungsausreißer, größte Einzelbrocken.
  Nichts davon steht im Bildschirm. Umgekehrt kann der Bericht die Limits
  und die Skills-Aufschlüsselung nicht.
- **Eigenes Skript statt Umbau von `kontextbericht.py`** — weil der
  Zeitfilter dort ganze **Sitzungen** nach ihrem letzten Zeitstempel
  auswählt, die Gegenprobe aber einzelne **Anfragen** nach ihrem eigenen
  braucht. Eine Sitzung, die vor 30 Stunden begann und vor zwei endete,
  gehört nicht als Ganzes in ein 24-Stunden-Fenster. Verworfen: `--stunden`
  in `kontextbericht.py` nachrüsten, weil dort beide Filterarten
  nebeneinander stünden und man die falsche erwischt.

## Belege dieser Fortschreibung
- `werkzeug/gegenprobe-usage.py` — rechnet die Anzeige nach, beide
  Gewichtungen nebeneinander, Schwelle und Fenster als Parameter
- Filter-Gegenprobe bestanden (die Lehre aus „Offene Fragen" oben):
  24 h → 534 Anfragen / 83,7 %, 6 h → 320 Anfragen / 58,0 %
- Modelle im Fenster geprüft: 1093 Zeilen `claude-opus-5`, 2 `<synthetic>`.
  Der Ausgabefaktor 5,0× trägt also. `<synthetic>` sind lokal erzeugte
  Nachrichten mit `usage`-Feld, aber keine bezahlte Anfrage — im Skript
  ausgeschlossen (`gegenprobe-usage.py:71-74`)

## Offene Fragen dieser Fortschreibung
- **Was zählt „% of usage" bei Skills?** Der Bildschirm weist `/uebergabe`
  mit 3 % aus — erstmals ein Preisschild für das eigene Werkzeug. Ob das
  die Anfrage meint, die die Skill lädt, oder alle Anfragen, solange sie im
  Kontext liegt, geht aus der Anzeige nicht hervor. **Ungeprüft.** Solange
  das offen ist, lässt sich nicht sagen, ob die Skill 3 % *kostet* oder ob
  3 % der Arbeit *durch sie liefen*. Blockiert nicht, ist aber die
  interessanteste Zahl im Bildschirm.
- **Die Zahl driftet.** Zwei Läufe im Abstand von Minuten ergaben 84,6 %
  und 83,7 %, weil das 24-Stunden-Fenster mitwandert und die laufende
  Sitzung selbst Anfragen erzeugt. Die Übereinstimmung mit den 86 % gilt
  für den Moment des Screenshots, nicht als feste Zahl. Blockiert nicht,
  gehört aber an jede Wiederholung der Messung.
- **Zwei Parser für dasselbe Format.** `kontextbericht.py` und
  `gegenprobe-usage.py` lesen beide `message.usage` mit eigenem Code. Ändert
  Anthropic das Format, muss man an zwei Stellen reparieren — und merkt es
  vielleicht nur an einer. Blockiert nicht, wäre aber der Anlass für ein
  gemeinsames Lesemodul, sobald ein drittes Skript dazukommt.

## Abschluss 23.08.2026 — Aufgabe erledigt, Datei geschnitten
Das Ziel oben ist erreicht: Der Bericht läuft aus den Sitzungsprotokollen,
ohne Modell und ohne Kontextkosten, und die Zahlen stimmen gegen eine
Stichprobe — sogar gegen eine unabhängige, siehe Fortschreibung oben.

Geschnitten, nicht gekürzt, bei 10.412 Zeichen. Grund: Die laufende
Übergabe wird zu Sitzungsbeginn gelesen und ab Zug 1 mitgeschleppt, also am
teuersten Platz. Die verbliebene offene Frage — was „% of usage" bei Skills
zählt — ist eine eigene, kleine Aufgabe und steht in
`uebergabe/skills-anteil.md`. Diese Datei bleibt vollständig: Ihr Wert liegt
in den verworfenen Wegen und im stillen `--tage`-Fehler, genau dem, was eine
Zusammenfassung streichen würde.

## Nächster Schritt
Keiner. Aufgabe erledigt. Weiter in `uebergabe/skills-anteil.md`.
