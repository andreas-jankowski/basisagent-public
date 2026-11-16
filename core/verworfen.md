# Was bewusst nicht drin ist

Negativentscheidungen mit Begründung. Wird nie geladen — nur gelesen, wenn jemand fragt „warum eigentlich nicht X?".

**Der Zweck dieser Datei:** Eine Entscheidung gegen etwas ist in sechs Monaten nicht mehr erkennbar. Ohne diese Notizen wird dieselbe Frage erneut aufgeworfen und erneut recherchiert. Jeder Eintrag nennt deshalb eine **Revisionsbedingung** — den beobachtbaren Umstand, unter dem die Entscheidung neu zu treffen wäre.

---

## karpathy

Vier Prinzipien: Annahmen offenlegen, Simplicity First, chirurgische Änderungen, zielgetriebenes Arbeiten. Kanonisch eine immer aktive Regeldatei, kein aufgabengetriggerter Skill.

**Nicht installiert, aber inhaltlich übernommen.** Ein Skill, dessen Inhalt immer gelten soll, ist ein Widerspruch: Du zahlst die Beschreibung in jedem Zug *und* den Rumpf beim Laden — für Sätze, die direkt in `AGENTS.md` stehen können.

In `core/profil/code/AGENTS.md.tpl` sind sie enthalten: „Bei mehrdeutiger Anforderung nachfragen" ist *Think Before Coding*, „nur ändern was die Aufgabe verlangt" ist *Surgical Changes*, der Nachher-Block ist *Goal-Driven Execution*.

Zur Einordnung ein Kommentar aus der Community zum Repo: Es sei ein Menü, kein Template — der schnellste Weg, es falsch zu benutzen, sei, das Ganze an jedes Projekt anzuhängen und für erledigt zu halten.

**Revisionsbedingung:** keine. Der Inhalt ist übernommen; das Paket selbst brächte nichts hinzu.

---

## ponytail

Hier ist die Sache ernster zu nehmen als bei karpathy. ponytail zwingt den Agenten vor der ersten Zeile durch eine Leiter: Muss das überhaupt existieren? Gibt es das schon im Codebase? Das trifft das Überbau-Problem **direkt**. Gemessene Codereduktion nahe 54 % im Test des Autors.

**Trotzdem nicht installiert, aus drei Gründen:**

1. Es bringt bei Sitzungsbeginn ein Regelwerk ein, dessen Umfang du nicht steuerst. Bei einer Einrichtung, die auf Tokensparsamkeit ausgelegt ist, ist ein unbekannt großer Dauerblock die falsche Wahl.
2. Sein Kernverhalten sind zwei Sätze, die in der Vorlage stehen: „Prüfe, ob die Funktion schon existiert" und „Einfachste Lösung, die die Anforderung erfüllt".
3. Die Messung ist selbstberichtet, n=4, ein einziges Repo, auf einem schwachen Modell.

**Revisionsbedingung:** Wenn nach zwei Wochen mit den Zeilen aus der Vorlage weiterhin beobachtet wird, dass der Agent überbaut. Dann ponytail auf Stufe `full` — **nicht** `ultra` — und in `AGENTS.md` bleibt die Zeile *„Eine explizite Anforderung schlägt Minimalismus"* stehen. Ohne sie streicht ponytail Kanten weg, die in der Spec stehen.

---

## oh-my-openagent

Der Todo Enforcer ist dafür gebaut, dass der Agent nicht stehenbleibt und fragt — das Gegenteil dessen, was diese Einrichtung erreichen will. Dazu Hooks bei jedem Prompt und parallele Subagenten.

**Revisionsbedingung:** Wenn sich das Ziel umkehrt — also wenn der Agent zu oft fragt statt zu selten. Bei der aktuellen Zielsetzung die falsche Richtung.

---

## GSD Core

Sauberere Architektur als oh-my-openagent, aber ebenfalls Subagenten in parallelen Wellen. Die eigene Dokumentation nennt Recherche, Planung und Ausführung als je eigene Roundtrips. Nicht billiger, nur besser steuerbar.

**Revisionsbedingung:** Wenn Steuerbarkeit wichtiger wird als Tokenkosten — etwa bei deutlich größeren Änderungen, als sie derzeit anfallen.

---

## edit-guard / Hashline

Verhindert, dass Dateien auf veraltetem Stand überschrieben werden.

**Revisionsbedingung:** Wenn dauerhaft auf günstigen Modellen gearbeitet wird *und* beobachtet wird, dass Dateien auf veraltetem Stand überschrieben werden. Vorher ist es Vorsorge gegen ein Problem, das nicht auftritt.

---

## LSP in OpenCode

OpenCode empfiehlt selbst, in vielen Projekten stattdessen den Agenten Lint- und Typecheck-CLIs direkt ausführen zu lassen — Language Server geraten aus dem Takt, belegen Speicher und verlangsamen Abläufe. Die Befehle stehen in `AGENTS.md`.

**Revisionsbedingung:** Wenn der Agent wiederholt Typfehler übersieht, die ein Language Server sofort gezeigt hätte. Dann `"lsp": true` — vorher prüfen, ob die installierte Version eine LSP-Laufzeit mitbringt.

---

## Modellempfehlungen

Ursprünglich enthielt das Template eine Aufteilung „teures Modell für Planung, günstiges für Ausführung" und ein `model:`-Feld in den Rollenvorlagen.

**Entfernt auf Wunsch des Nutzers.** Die Modellwahl wird situativ getroffen und gehört nicht in eine Einrichtung, die einmal läuft. Die Rollenvorlagen erben stattdessen das Modell der Sitzung.

**Revisionsbedingung:** keine. Das ist eine Nutzerentscheidung, keine technische.

**Nachtrag 2026-10-07, ebenfalls Nutzerentscheidung:** Für die Rechercheagenten
aus Phase 1 wird das Modell **gefragt** — es ist der größte Kostenhebel eines
Subagenten, und der Nutzer will ihn selbst einstellen, einmal bei der
Einrichtung und später je Aufgabe. Empfohlen wird weiterhin nicht: Die Stufen
im Adapter sind eine Auswahl, kein Rat. Für alle anderen Rollen gilt der
Eintrag oben unverändert.

---

## Skriptordner für wiederverwendbare Aufrufe

Die Idee: Was der Agent an Code schreibt, um etwas zu zählen, zu suchen, zu messen oder abzurufen, landet in einem Projektunterordner — `tools/`, `scripts/` — statt jedes Mal neu geschrieben zu werden. Klingt zwingend, besonders bei Infrastrukturarbeit.

**Gemessen und verworfen am 2026-08-21** in Infrastrukturprojekt A, drei Verläufe, 5,8 MB vollständig geparst:

| Größe | Wert |
|---|---|
| Ausführende Aufrufe | 335 (324 PowerShell, 10 Bash, 1 Skriptdatei) |
| davon mehrzeilig oder mit Pipeline | 334 |
| Median-Länge | 1.175 Zeichen |
| Gruppen nach Zweck | 303 |
| **davon einmalig** | **276** |
| größte wortgleiche Gruppe | 3 Vorkommen |

Die Gegenprobe an den drei manuell konsolidierten Themen ist in zwei von drei Fällen negativ, und zwar aus unterschiedlichen Gründen — beide sind der eigentliche Grund für diese Entscheidung:

1. **Veränderliche Werte.** Bei der Reindex-Gruppe hingen 7 von 8 Aufrufen an Indexnamen mit Zeitstempel, Session-IDs oder Messfenstern. Ein Skript vom 18.08. hätte am 21.08. auf einen Index gezeigt, den es nicht mehr gab — der Fall „liefert still eine falsche Zahl", der schlechter ist als kein Skript.
2. **Keine Wiederfindbarkeit.** Bei der Heap-Gruppe war „Heap" eine Wortgruppe, kein Zweck: Position von `-Xmx`, Circuit-Breaker-Schwellen und Prozesszuordnung an drei verschiedenen Tagen. Der Agent hat ausdrücklich bestätigt, er hätte am dritten Tag nicht nach dem Skript vom ersten gesucht. Ein Ordner, in den niemand sieht, spart nichts.

**Der verwertbare Rest ist klein und anders geformt.** Die einzige teilweise tragfähige Gruppe hatte einen gemeinsamen Kern von **vier Zeilen** — drei Zählabfragen — bei einer Median-Aufruflänge von 23 Zeilen. Wiederkehrend ist also nicht der Aufruf, sondern die **Messgröße**. Vier Zeilen gehören in die Projektdatei, nicht in einen ausführbaren Ordner: kein Schreib- plus Ausführrecht auf dasselbe Verzeichnis, keine Pflege, und man kann sie ansehen statt ihnen zu vertrauen. Als offener Journaleintrag geführt. *(Nachtrag 2026-10-22: Der Eintrag ist seit 2026-09-01 entschieden — die Frage nach Kennzahlen bestätigt, die Ablage im Dokument für Kennzahlen über viele Systeme widerlegt, Rest Punkt 30 in `feedback/offene-punkte.md`. Er liegt seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`.)*

**Der Sicherheitsvorbehalt bleibt gültig, auch wenn er hier nicht der Grund war.** Schreibrecht und Ausführrecht auf dasselbe Verzeichnis sind zusammen eine selbstgebaute Interpreter-Freigabe: Wer beliebige Skripte anlegen *und* per Muster ausführen darf, umgeht jede `deny`-Regel, weil die Prüfung den Aufruf sieht und nicht, was darin passiert. Das ist Falle 7 im Adapter, nur selbst gebaut. Wäre die Messung positiv ausgefallen, wäre das die nächste zu klärende Frage gewesen.

**Revisionsbedingung:** Ein Projekt, in dem eine nach Zweck gruppierte Aufrufklasse **mehr als fünf** Vorkommen erreicht *und* die Gegenprobe (a) — unverändert beim zweiten Mal korrekt — positiv ausfällt. Dann nicht als Ordner mit Ausführfreigabe einrichten, sondern als eine Datei mit dem gemeinsamen Kern, Ausführung je Datei freigegeben, nie per Muster.

---

## OpenCode als Zweitwerkzeug

Bis 0.26.0 hat das Template jede Einrichtung für zwei Werkzeuge ausgelegt: eigener Adapter, eigene Startdatei, Phase 7 „Zweitwerkzeug anbinden", OpenCode-Pfade in Bestandsaufnahme und Skillsuche. **OpenCode ist in keiner einzigen Einrichtung eingesetzt worden** (`feedback/offene-punkte.md`, Punkt 15, durchgehend seit v0.3.0).

Der Preis war nicht nur Pflege. Fünf offene Punkte hingen allein daran, dass für OpenCode nichts gemessen werden konnte (9, 28, 33, 48, 49 teilweise), und Punkt 28 hielt zwei für Claude Code belegte Änderungen an den Profilvorlagen zurück. Jede Einrichtung las die Sonderfälle mit und stellte in Phase 7 eine Frage, die immer mit Nein beantwortet wurde. Entschieden vom Nutzer am 2026-10-22 — zusammen mit dem Ziel, die Einrichtung für weniger versierte Kollegen kürzer zu machen.

**Was bleibt:** `AGENTS.md` als werkzeugneutrale Hauptdatei, `CLAUDE.md` importiert sie. Damit kann ein späteres Werkzeug ohne Umbau der Regeln dazukommen — OpenCode ebenso wie Codex (Punkt 44). Der alte Adapter liegt ungepflegt in `feedback/archiv/opencode/`, mit den Befunden aus `offene-punkte.md` (Punkte 1, 3, 9, 28, 33, 48).

**Revisionsbedingung:** Ein Projekt soll tatsächlich mit OpenCode arbeiten. Dann den Adapter aus dem Archiv gegen die aktuelle OpenCode-Doku neu prüfen, nicht wieder einsetzen wie er ist — er ist auf dem Stand 0.26.0 eingefroren, das Runbook nicht.

---

## `haengt-an:` — erklärte Abhängigkeit zwischen Dokumenten

Ein optionales Frontmatter-Feld mit den Pfaden, von denen ein Dokument abhängt, dazu eine Regel im Übersichtsgenerator und ein nicht blockierender `PostToolUse`-Hook, der nach einer Änderung an einer Grundlage die abhängigen Dokumente nennt. In einem Textprojekt belegt (Journal 2026-09-02): Die Prüfung schlug richtig an und der Hook nannte beide Arbeitsprodukte.

Abgelehnt wegen der Ebene, nicht wegen der Qualität. Das Template erzeugt weder ein Frontmatter-Schema noch einen Übersichtsgenerator. Ein vorgeschriebenes Feld, das die meisten Dokumente nicht tragen, erzeugt die Falschmeldungen, gegen die der Vorschlag selbst argumentiert. Übernommen ist die Verhaltensebene: die Nachzieh-Zeile im Textprofil, dazu die Trennlinie für Hooks im Adapter. Herleitung: `feedback/archiv/offene-punkte-geschlossen.md`, Punkt 32.

**Revisionsbedingung:** Ein zweites Projekt schreibt eine Abhängigkeit zwischen Dokumenten ausdrücklich auf, gleich in welcher Form. Dann prüfen, ob beide Fassungen eine gemeinsame Form haben, die sich als **Vorschlag** ins Textprofil aufnehmen ließe, nicht als Pflichtfeld.

---

## Entscheidungsgedächtnis (`docs/adr/`) in Zielprojekten

Das Template führt für sich selbst eine dauerhafte Entscheidungsablage: diese Datei, das Journal, die offenen Punkte. Den Projekten, die es einrichtet, legt es nichts Vergleichbares an. Bis 0.28.0 nannten es `docs/adr/` an mehreren Stellen als Ablageort, ohne dass eine Phase das Verzeichnis anlegte. Die Verweise sind mit 0.27.0 (Phase 7, Planungsvariante der `CLAUDE.md`) und 0.29.0 (`core/prinzip.md`) entfallen. Bleiben dürfen die Suche in Phase 0 und die Ausgabe von `grill-with-docs` im Codeprofil.

Nicht eingerichtet, weil nur ein Projekt eine solche Ablage aus eigenem Antrieb nachgerüstet hat (Textprojekt G, 2026-08-24). `uebergabe/` ist ein Arbeitsstand je Aufgabe, keine Entscheidungsablage. Was beim Abschließen einer Übergabe offen bleibt, geht seit 0.24.0 ins Projekt.

**Revisionsbedingung:** Ein zweites Projekt rüstet eine dauerhafte Entscheidungsablage nach. Kandidat ist die Vorhabensdatei aus Textprojekt I (Journal 2026-10-22, Vorschlag 2); ob sie Entscheidungen trägt oder nur Status, ist ungeprüft. Dann `docs/adr/` in einer Phase anlegen und im Profil sagen, was hineingehört. Herleitung: `feedback/archiv/offene-punkte-geschlossen.md`, Punkt 22.
