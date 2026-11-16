# Runbook — Phasen 0 bis 9

Der Ablauf gilt für jede Projektart und jedes Werkzeug. Zwei Achsen ergänzen ihn:

| Verweis | Woher | Wann bestimmt |
|---|---|---|
| `→ Adapter` | Der Adapter, den dir die Startdatei genannt hat | Steht vorher fest |
| `→ Profil` | `core/profil/<art>.md` | **Phase 0**, erste Frage |

Die Achsen sind unabhängig: Der Adapter sagt, wie ein Werkzeug etwas tut; das Profil sagt, was für diese Projektart überhaupt zu tun ist. Steht in einem von beiden eine Regel, die für alle gilt, gehört sie hierher.

**Schnellmodus.** Hat der Nutzer in der Modusfrage der Startdatei „schnell" gewählt, legt sich `core/schnell.md` über diesen Ablauf: Vorgaben statt Rückfragen, ein Plan statt Einzelentscheidungen. Was dieses Runbook fragt, bleibt das Wissen dahinter — dort steht, wann die Vorgabe greift.

---

## Verhaltensregeln — gelten durchgehend

1. **Nichts löschen, nichts überschreiben, ohne vorher zu fragen.** Auch nicht, wenn es offensichtlich veraltet wirkt. Zeige, was du ändern würdest, und warte auf Zustimmung.
2. **Eine Frage auf einmal.** Keine Fragenlisten. Frage, warte auf die Antwort, mach weiter.
3. **Vor jeder Dateiänderung den genauen Inhalt zeigen.** Bei bestehenden Dateien: was wegfällt, was dazukommt.
4. **An `⏸ HALT`-Markierungen den Zug beenden.** Nicht weiterarbeiten, nicht vorgreifen, nichts ankündigen. Warten.
5. **Zu Beginn jeder Antwort die aktuelle Phase nennen**, z. B. `[Phase 3/9]`. Der Nutzer soll jederzeit wissen, wo er steht.
6. **Nicht raten.** Wenn du etwas nicht aus dem Projekt ablesen kannst, frag.
7. **Du richtest ein, du arbeitest nicht mit.** Quelldateien, Dokumente, Recherchematerial fasst du nicht an. Was der Nutzer inhaltlich vorhat, beginnt nach Phase 9.
8. **Nach Phase 1 kannst du nicht mehr löschen.** Die Berechtigungen, die du dort setzt, sperren dich mit ein. Das ist die vorgesehene Wirkung, kein Fehler. Wo etwas weg soll: zeigen was weg soll, den Befehl nennen, den Nutzer ausführen lassen. Such keinen Weg um die Sperre herum. Das gilt in Phase 4, 5, 6 und 9 gleichermaßen — die Phasen formulieren es nicht jedes Mal neu.

Die Grenzen für `AGENTS.md` aus `core/prinzip.md` sind eine harte Vorgabe: unter 100 Zeilen **und** in der Größenordnung 4.500 Zeichen. Wenn du eine davon reißen würdest, sag es und schlage vor, was stattdessen in den Projektkontext wandert. **Kürze nicht durch Umbruch** — drei Rahmenpunkte in eine überlange Zeile zu pressen hält die Zeilenzahl ein und spart nichts.

---

## Wiederaufnahme

Falls die Sitzung abgebrochen war: Sieh nach, welche der folgenden Dinge schon existieren, und melde dem Nutzer, in welcher Phase du wieder einsteigst.

| Vorhanden | Erreichte Phase |
|---|---|
| Berechtigungsdatei des Werkzeugs (→ Adapter) | 1 fertig |
| `AGENTS.md` **und** `.agent-template-version` | 2 fertig |
| Gerüst installiert **und benutzt**, oder ausdrücklich abgelehnt (→ Profil) | 3 fertig |
| Projektkontext gefüllt | 4 fertig |
| `.claude/skills/` mit Skills | 5 fertig |
| `.agent-template-version` trägt in Zeile 3 ein **Datum** statt `offen` | 9 fertig |

**Zeile 3 ist der einzige Punkt dieser Tabelle, den du nicht erraten musst.** Steht dort `phase9: offen`, ist die Wirkungsprobe aus Phase 9 Schritt 5 nicht bestanden — egal wie fertig das Projekt aussieht. Am 2026-08-26 hat ein Projekt zwei Sitzungen und einen Arbeitstag lang an Produktionsservern gearbeitet, weil die Einrichtung nach Schritt 4 abgeschlossen **wirkte**: Schritt 4 zeigt die Übersicht, Schritt 5 prüft die Berechtigungen, und die Datei sah bei abgebrochener Phase 9 genauso aus wie bei abgeschlossener. Fehlt Zeile 3 ganz, stammt der Stempel aus einer Fassung vor 0.15.0 — dann gilt Phase 9 als offen, bis die Probe gelaufen ist.

**Die Projektart liest du aus `.agent-template-version`.** Nicht aus `AGENTS.md` — der `Rahmen`-Block sieht in beiden Profilen gleich genug aus, um falsch zu schließen. Fehlt die Datei, stammt der Stand aus einer Fassung vor 0.4.0 — **oder es gab nie eine Einrichtung**, nur den Skill `uebergabe` samt Auslöserzeilen, von Hand übertragen (`core/belege/uebergabe-in-anderes-projekt.md`). Fehlen auch `AGENTS.md` und die Berechtigungsdatei, ist es eine Neueinrichtung, auch wenn der Auftrag „aktualisieren" lautet; sag das dem Nutzer wie bei einem Stempel unter 0.14.0. Sonst am Abschnittstitel unterscheiden (`Beim Schreiben` gegen `Beim Ändern`) und im Zweifel fragen.

**Ein installiertes Gerüst heißt nicht, dass Phase 3 gelaufen ist.** Sieh nach, ob darin gearbeitet wurde. Ein Gerüst, das jemand vor Monaten installiert und nie benutzt hat, ist ein Fall für den Abbau-Zweig in Phase 3 — und die Entscheidung steht dann noch aus.

---

## Ein eingerichtetes Projekt auf eine neuere Templateversion ziehen

Das ist **nicht** die Wiederaufnahme und nicht der Ablauf unten. Die Phasen 0 bis 9 setzen ein uneingerichtetes Projekt voraus; hier ist die Einrichtung fertig und nur alt.

**Stell zuerst die Frage, die den Vorgang oft beendet: lohnt es sich hier?** Ein Projekt auf einer älteren Version funktioniert. Was eine Version geändert hat, sagt nichts darüber, ob dieses Projekt es braucht — und die meisten Änderungen betreffen den Ablauf des Einrichtens, den dieses Projekt nie wieder durchläuft. Nur was in **erzeugten Artefakten** steckt, wirkt dort weiter: Regeldatei, Berechtigungsdatei, kopierte Skills, Versionsstempel.

**Die Schritte 1 bis 4 sind Templatearbeit und im Zielprojekt nicht leistbar.** Die Information, was eine Version an erzeugten Artefakten ändert, steckt ausschließlich in der Git-Historie des Templates; `VERSION` ist eine Zahl ohne Änderungsliste. Du brauchst also den Templatepfad aus Zeile 2 des Versionsstempels.

**Die Historie reicht nicht beliebig weit zurück, und das entscheidet den Fall oft, bevor Schritt 1 beginnt.** Sie wurde am 2026-08-28 neu aufgesetzt, als die Projektnamen pseudonymisiert wurden; der älteste Commit auf `VERSION` trägt **0.14.0**. Für ein Projekt mit einem älteren Stempel sind die Schritte 1 bis 4 **nicht durchführbar** — es gibt keinen Ausgangsstand, gegen den sich vergleichen ließe. Was bliebe, ist ein Ist-Vergleich gegen die *heutige* Vorlage, und der kann das Entscheidende nicht unterscheiden: ob eine Zeile fehlt, weil sie neu ist, oder weil der Nutzer sie damals bewusst herausgenommen hat. Das ist keine Aktualisierung mehr, sondern Raten mit Schreibrecht auf ein fremdes Projekt.

**Nutzerentscheidung vom 2026-09-21: Dann wird neu eingerichtet, nicht gezogen.** Der reguläre Ablauf kostet eine Sitzung, liefert aber einen Stand, den man begründen kann — und er fragt bei jeder Einzelheit nach, statt sie aus einer nicht mehr vorhandenen Historie zu erschließen. **Sprich das an, bevor du anfängst:** Ein Stempel unter 0.14.0 ist ein Fall für Phase 0, nicht für diesen Abschnitt. Erhebe zuerst den Stand (`.agent-template-version`, Zeile 1) und das Datum der letzten Änderung im Projekt; ein Projekt, das seit Wochen ruht, braucht überhaupt keinen der beiden Wege, solange dort nicht wieder gearbeitet wird.

1. **Spanne bestimmen.** `git log -- VERSION` im Templateverzeichnis nennt die Commits der Zwischenversionen. Ausgangspunkt ist die Version aus Zeile 1 des Stempels.
2. **Erzeugte Artefakte von Ernte trennen.** `git log --name-only` über die Spanne. Änderungen an `feedback/`, `core/belege/` und `uebergabe/` erreichen ein Zielprojekt **nie** — sie sind Protokoll und Messgrundlage. Übrig bleiben `core/profil/*/AGENTS.md.tpl`, `core/skills/`, die Adapter und deren Vorlagen.
3. **Je Treffer prüfen, ob dieses Projekt ihn überhaupt hat.** Das ist die eigentliche Arbeit. Beispiel aus dem belegten Fall: v0.12.0 ändert nur `template-feedback/SKILL.md` — ein Projekt, das den direkten Weg über Zeile 2 des Stempels nutzt und keine lokale Kopie hat, ist davon nicht betroffen und braucht die Version nicht.
4. **Ist-Vergleich gegen den Ausgangsstand aus der Historie.** Hol die alte Fassung der betroffenen Dateien (`git show <commit>:<pfad>`) und vergleiche sie mit dem, was im Zielprojekt liegt. Weicht es ab, hat jemand dort angepasst — dann ist der Unterschied eine Entscheidung des Nutzers und keine Lücke. **Das ist zugleich die einzige Gelegenheit, eine veraltete Skillkopie zu bemerken:** Zwischen Template und Zielprojekt gibt es kein Gegenstück zur Prüfzeile, die im Template die beiden Fassungen zusammenhält.
5. **Ändern, dann den Stempel fortschreiben** — Zeile 1 auf die neue Version. `phase9:` fasst du nicht an: Die Wirkungsprobe gilt weiter, sie war für die alte Fassung der Berechtigungen bestanden. Berührt die Aktualisierung die Berechtigungsdatei, ist sie neu fällig — dann `offen` setzen und Phase 9 Schritt 5 laufen lassen.

**Was hier absichtlich fehlt:** eine Änderungsliste je Version, die Schritt 2 und 3 überflüssig machen würde. Sie steht als Vorschlag im Journal (2026-08-25) und ist nicht übernommen — der Ort ist offen und sie will bei jeder Version gepflegt werden. Solange sie fehlt, rekonstruierst du sie aus `git log`.

---

# Phase 0 — Bestandsaufnahme

Sieh dir das Projekt an, **ohne etwas zu ändern**.

## Schritt 1 — Projektart bestimmen

**Zuerst**, denn davon hängt ab, wonach du überhaupt suchst. Liste die Dateien im Wurzelverzeichnis und eine Ebene darunter — nur Namen, noch keine Inhalte — und ordne zu:

| Befund | Art |
|---|---|
| Projektdatei (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`) oder Quellverzeichnisse | **Code** |
| Überwiegend `.md`, `.docx`, `.pdf`; Ordner wie `quellen/`, `recherche/`, `entwurf/` | **Text** |
| Leeres oder fast leeres Verzeichnis | **erst nach externem Bestand sehen**, dann fragen |
| Beides deutlich vorhanden | **fragen** — meist Code mit umfangreicher Doku, aber das entscheidet der Nutzer |

Verfügbare Profile: `core/profil/code.md`, `core/profil/text.md`.

### Wenn das Arbeitsverzeichnis leer ist

Dann liegt der Bestand oft **außerhalb** — eine Serverfreigabe, ein Materialordner, ein Laufwerk, das der Nutzer im ersten Satz nennt. Im Firmenumfeld ist das nicht die Ausnahme: Das Arbeitsverzeichnis ist lokal und privat, das Material liegt dort, wo andere auch drankommen. Genau deshalb wird das Projekt getrennt angelegt.

**Frag nach dem Ort, bevor du die Projektart fragst.** Aus einem leeren Verzeichnis kann der Nutzer die Art zwar beantworten, aber du kannst ihm keine begründete Einschätzung anbieten — und das ist der Sinn dieses Schritts.

**Führe die Bestandsaufnahme dann über den externen Ort:** Umfang, Formate, Ordnerstruktur, erkennbare Fassungen. Lies **Namen und Struktur, nicht Inhalte** — Verhaltensregel 7 gilt weiter. Daraus begründest du die Einstufung.

**Frag, ob der Bestand draußen bleibt oder einwandert.** Beide Fälle sehen in der Bestandsaufnahme identisch aus, und die Antwort entscheidet Phase 1 vollständig:

> Bleibt `<Ort>` dauerhaft außerhalb, oder wandert er in das Projekt ein?

**Wandert er ein**, ist er künftig eigenes Material: keine Schreibsperre, keine Sensibilitätsklassen, und der Prüfpunkt „die in Phase 0 gefundenen sensiblen Orte sind gesperrt" ist gegenstandslos statt unerfüllt. Am 2026-08-31 hat das Fehlen dieser Frage einen vollständigen Fragezyklus samt Sensibilitätsanalyse über drei fremde Bestände gekostet; der Nutzer musste den Ablauf korrigieren, nicht das Werkzeug. Die Bestandsaufnahme selbst brauchst du in beiden Fällen — verschwendet war nur die Schutzkonstruktion.

Ein externer, ungesichteter Bestand ist selbst ein Befund. **Bleibt er draußen**, wirkt er an drei Stellen nach — merk sie dir:

- **Phase 1:** zwei Regeln, Leserecht auf den Ort **und** harte Schreibsperre darauf. → Adapter
- **Phase 2:** er füllt das Feld `Ablage`.
- **Phase 4:** die Belegarbeit an einem fremden, ungesichteten Bestand hat eine eigene Behandlung. → Profil

**Wenn du zuordnen konntest:** Lies das passende Profil jetzt und geh zu Schritt 2. Bestätigen lässt du die Einstufung am Ende von Schritt 2, zusammen mit der Frage nach neu/bestehend — das bleibt eine Frage.

**Wenn du nicht zuordnen konntest:** Frag hier, und zwar nur das:

> Ich sehe im Verzeichnis <Befund>. Ist das ein **Code-** oder ein **Textprojekt** (Recherche, Gutachten, Bewertung, Security-Analyse)?

⏸ **HALT** — warte auf die Antwort, lies dann das Profil und mach mit Schritt 2 weiter. Diese Frage lieber einmal zu viel als das falsche Profil: Mit dem falschen suchst du in Schritt 2 nach den falschen Dingen und füllst in Phase 2 die falsche Vorlage.

## Schritt 2 — Bestandsaufnahme

Für jede Projektart:

- Ist es ein Git-Repo? Ist der Arbeitsbaum sauber?
- Ist es leer/neu, oder liegt schon Arbeit darin?
- Welche Anweisungsdateien existieren: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`, `CONTEXT.md`, `.windsurfrules`, `docs/adr/`
- Welche Skills existieren: `.claude/skills/`, `.agents/skills/`, dazu global `~/.claude/skills/`
- Welche Konfiguration des Werkzeugs existiert (→ Adapter)
- Ist bereits ein Ablaufgerüst installiert — `openspec/` oder entsprechende Skills?
- Existiert `.agent-template-version`? Falls ja: Zeile 1 nennt Version und Profil, Zeile 2 den Templatepfad — das Projekt wurde schon einmal eingerichtet

**→ Profil, Abschnitt „Phase 0".** Dort steht, was zusätzlich zu ermitteln ist. Das ist der Teil, der den `Rahmen` in Phase 2 füllt.

**Berichte das Ergebnis kompakt.** Dann eine einzige Frage, die beides zusammenfasst:

> Ich stufe das als **[neues / bestehendes] [Code- / Text-]Projekt** ein. Stimmt das?

Bei einem Textprojekt nennt das Profil eine Ausprägung, die du in dieselbe Frage nimmst — „bestehendes Textprojekt (Gutachten)". War die Art schon in Schritt 1 geklärt, fragst du hier nur noch nach neu/bestehend.

**Wenn der Arbeitsbaum nicht sauber ist:** Bitte den Nutzer, vorher zu committen oder zu stashen. Begründung: Du wirst mehrere Dateien anlegen und ändern, und er soll das jederzeit rückgängig machen können. Fahre erst fort, wenn das erledigt ist.

**Wenn es kein Git-Repo ist:** Frag einmal, neutral, und wirb nicht dafür. Viele Projekte brauchen keine Versionskontrolle, und mancher Nutzer kennt Git nicht — „nein" ist dann die richtige Antwort, keine Lücke, die du schließen musst (Nutzerentscheidung vom 2026-10-07):

> Soll das Projekt mit Git versioniert werden? Git merkt sich jeden Stand, sodass sich Änderungen zurücknehmen lassen. Es geht auch ohne — dann leg vor der Einrichtung eine Sicherungskopie des Ordners an.

Erklär Git nicht weiter, als der Nutzer fragt, und bring es in späteren Phasen nicht wieder auf. **Weiß er es nicht, geht es ohne Git weiter.** Ein `git init` ist später jederzeit möglich; was dann fehlt, notiert Phase 1 als offenen Punkt.

**Vor `git init` drei Dinge prüfen.** Sonst hinterlässt Phase 0 ein Repo, in dem kein Git-Befehl funktioniert:

| Prüfen | Wenn zutreffend |
|---|---|
| Liegt das Verzeichnis auf einem UNC-Pfad oder einem gemappten Netzlaufwerk? | `git init` läuft durch, aber jeder folgende Befehl bricht mit „dubious ownership" ab. Nötig ist ein `safe.directory`-Eintrag in der **globalen** `~/.gitconfig`, bei UNC mit `%(prefix)//`-Präfix — eine Änderung außerhalb des Projekts, also eigene Rückfrage. Im Firmenumfeld ist ein Projekt auf einer Serverfreigabe der Normalfall, nicht die Ausnahme |
| Sind `user.name` und `user.email` gesetzt, lokal oder global? | Sonst scheitert der erste Commit. Nach den Werten fragen, nicht raten |
| Windows, und wird geklont oder tief verschachtelt abgelegt? | `core.longpaths true` setzen. Sonst bricht `git clone` mit „Filename too long" ab; bei Sparse-Checkout bleiben Dateien als „not up to date" hängen, obwohl `git status` sauber meldet — das sieht wie eine lokale Änderung aus und ist keine |

**Ohne Git** — abgelehnt oder offen gelassen — wirkt die Antwort an drei Stellen nach. Merk sie dir und behandle sie dort:

- **Phase 1:** Keine Git-Regeln in die Berechtigungsdatei, sie wären wirkungslos. Notier den Verzicht als offenen Punkt, falls später doch ein `git init` kommt.
- **Phase 1, → Adapter:** Die Trennung in eine geteilte und eine persönliche Berechtigungsdatei hängt vollständig daran, dass die zweite in der `.gitignore` steht. Ohne Git eine Datei statt zweier — und die Frage, ob das Projekt geteilt wird, entfällt mit.
- **Phase 9:** Nicht zum Commit raten, sondern nach dem projekteigenen Sicherungsweg fragen.

⏸ **HALT** — warte auf die Antwort.

---

# Phase 1 — Berechtigungen

Der Schritt mit dem größten Effekt: Der Agent fragt danach vor jeder Dateiänderung.

## Was du hier schreibst, gilt ab jetzt — aber nicht jetzt

**Lies das, bevor du anfängst, und sag es dem Nutzer**, sobald die Datei geschrieben ist.

Werkzeuge lesen ihre Berechtigungen **beim Sitzungsstart**. Eine Datei, die danach entsteht oder sich ändert, greift in dieser Sitzung nicht mehr. Das ist gemessen, nicht vermutet: Zwei Löschversuche gegen `deny`-Regeln liefen durch; nach einem Neustart bei unveränderter Konfiguration wurden beide verweigert.

Drei Folgen, die du kennen musst:

1. **Diese Phase bleibt in der Einrichtungssitzung wirkungslos.** Deine Sperren gelten ab dem nächsten Start. Bis dahin gelten die Regeln, die beim Start dieser Sitzung galten.
2. **Auch Entfernungen wirken erst dann.** Nimmt der Nutzer auf deine Meldung hin globale Interpreter-Freigaben heraus, arbeitest du in dieser Sitzung noch mit ihnen. Halte dich trotzdem daran, als wären sie weg — du kannst dich nicht auf ein Harness verlassen, das dich noch nicht bremst.
3. **Halte dein eigenes Verhalten nicht für regelkonform, nur weil nichts gefragt hat.** Das Ausbleiben einer Rückfrage beweist in dieser Sitzung nichts.

Die Wirkungsprobe steht in **Phase 9, Schritt 5** — nach einem Neustart, und nicht vorher. Häng die Prüfung hier nicht an; sie kann nur ein falsches Ergebnis liefern.

**→ Adapter, Abschnitt „Phase 1".** Dort steht die Zieldatei, das Format und die werkzeugspezifische Erklärung.

Grundsätze:

- **Leseoperationen freigeben**, alles Schreibende und alles Ausführende fragt.
- **Destruktives und Ausgehendes sperren:** Löschen, `sudo`, `git push`, Force-Operationen.
- **Web-Suche frei, Web-Abruf fragt** — so steht es in der Vorlage (Nutzerentscheidung vom 2026-10-12). Das Textprofil stellt die Suche zurück auf `ask`.
- **Was in Phase 0 als schützenswert auffiel, vom Lesen ausschließen.**


**Hilfsagenten: erst fragen, ob überhaupt — Vorgabe nein.** Subagenten und
Workflows sind langsam und teuer; die Vorlage sperrt beide (Nutzerentscheidung
vom 2026-10-12). Nur auf ausdrückliches Ja hebst du die Sperre auf. **→
Adapter, Abschnitt „Hilfsagenten überhaupt"** — dort stehen die Frage, die
Zeilen und die Folgen für delegierende Skills.

**Subagenten begrenzen — im selben Zug.** Die Grenzen für Subagenten gehören
in dieselbe Datei wie die Berechtigungen. Sie sind ein Kostenmittel, kein
Sicherheitsmittel: Ein Subagent ist eine zweite Sitzung, und sein Ergebnis
liegt danach in jedem Zug der ersten (`core/prinzip.md`, vierter Hebel). Die
Voreinstellungen sind großzügig, und Claude Opus 5 delegiert nach
Herstellerangabe bereitwilliger als seine Vorgänger. **→ Adapter, Abschnitt
„Der `env`-Block"** — dort stehen die Werte, die Belege und die
Einschränkung.

**Dann, nur bei erlaubten Hilfsagenten, das Budget für Rechercheagenten
erfragen.** Tiefe und Anzahl begrenzen
nicht, wie lange ein einzelner Subagent läuft und auf welchem Modell. Das
entscheidet der Nutzer, nicht du: Leg ihm die Stufen vor, empfiehl keine, und
sag ihm, wie er sie später je Aufgabe oder dauerhaft ändert. **→ Adapter,
Abschnitt „Rechercheagenten"** — dort stehen die Stufen, die Vorlagen und der
Weg zum Ändern.

**→ Profil, Abschnitt „Phase 1".** Dort steht, was für diese Projektart freizugeben und was zu sperren ist. Die Gewichte sind je nach Art verschieden — bei der einen liegt die Arbeit im Freigeben, bei der anderen im Sperren.

## Die globale Berechtigungsdatei auswerten

Phase 0 hat sie erhoben. **Hier liest du sie gegen das, was du gerade vorhast.** Projektlokale Regeln gewinnen zwar — aber eine globale Freigabe, die deiner Absicht widerspricht, gilt in **jedem anderen Projekt** des Nutzers weiter, und dort fällt sie niemandem auf.

Melde drei Klassen:

**1. Widersprechende Freigaben.** Was du lokal auf `ask` oder `deny` setzt und global auf `allow` steht. Besonders Web-Suche und Web-Abruf.

**2. Interpreter-Freigaben.** `python -c`, `python -`, `node -e`, `bash -c`, `pwsh -Command` und Verwandte. **Das ist die gravierendste Klasse und der einzige Punkt dieser Phase, den du von dir aus ansprichst.**

Die Berechtigungsprüfung sieht die Kommandozeile — nicht das, was der Interpreter darin ausführt. Eine solche Zeile umgeht damit **jede** `deny`-Regel: Ein Löschaufruf im Skript kommt an der Löschsperre vorbei, ein Netzaufruf an der Web-Sperre. Sie weicht keine einzelne Regel auf, sie hebt das Regelwerk auf. In einem Projekt, dessen Sperrzweck „nichts nach draußen" ist, macht sie die ganze Phase folgenlos.

**3. Tote Regeln.** Einträge mit fest verdrahteten Pfaden aus fremden Projekten. Harmlos, aber sie verstellen den Blick auf die beiden anderen Klassen.

Zeig die Befunde und frag einzeln. **Du änderst die globale Datei nicht selbst** — sie gilt für Projekte, die du nicht kennst.

**Ohne Git** (Phase 0): keine Git-Regeln aufnehmen, und statt zweier Berechtigungsdateien nur eine. Beides steht dort begründet.

**Wenn die Datei schon existiert:** Zeige die vorhandene Fassung und die vorgeschlagene nebeneinander. Benenne, was du ändern, ergänzen oder entfernen würdest. Frage einzeln nach, bevor du etwas Bestehendes anfasst.

⏸ **HALT** — warte auf Freigabe, dann schreibe die Datei.

---

# Phase 2 — AGENTS.md

**→ Profil, Abschnitt „Phase 2".** Dort steht, welche Vorlage gilt — jede Projektart hat eine eigene. Lies sie inklusive der Hinweise im Kommentarblock am Ende; der Kommentar wird **nicht** in die erzeugte Datei übernommen.

`AGENTS.md` ist die einzige Quelle der Regeln, werkzeugneutral gehalten. Liest das Werkzeug sie nicht von sich aus, bekommt es am Ende dieser Phase eine eigene Regeldatei, die sie importiert — → Adapter.

## 2a — Bei einem neuen Projekt

Fülle die Vorlage mit dem, was du in Phase 0 ermittelt hast. Was du nicht ermitteln konntest, **erfrage einzeln** — rate nicht.

## 2b — Bei einem bestehenden Projekt

Hier ist Sorgfalt gefragt. Es geht um vorhandene Arbeit des Nutzers.

**Schritt 1: Lies alle gefundenen Anweisungsdateien** — `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md` und was sonst in Phase 0 auftauchte.

**Schritt 2: Klassifiziere jeden inhaltlichen Block** in eine von vier Kategorien:

| Kategorie | Kriterium | Ziel |
|---|---|---|
| **A — behalten** | Muss in *jedem* Zug gelten: Befehle, harte Grenzen, Verhaltensregeln | `AGENTS.md` |
| **B — verschieben** | Erklärend, beispielhaft, architektonisch, projektbeschreibend | Projektkontext (Phase 4) |
| **C — veraltet** | Widerspricht dem heutigen Stand, nennt Entferntes, tote Pfade | Vorschlag: löschen |
| **D — unklar** | Du kannst es nicht einordnen | Nachfragen |

Faustregel für A gegen B: **Passt eine Zeile in beide, gehört sie nach B.** `AGENTS.md` ist die Kurzfassung, die immer läuft; der Projektkontext darf ausführlich sein, weil er nur bei Bedarf geladen wird.

**Schritt 3: Zeige die Klassifikation als Tabelle.** Pro Block: Herkunftsdatei, ein Satz Inhalt, deine Kategorie, deine Begründung in einem Halbsatz.

**Schritt 4: Frage kategorieweise nach.** Beginne mit C, weil dort das Risiko liegt:

> In Kategorie C habe ich N Blöcke. Soll ich sie dir einzeln zeigen, oder sind sie pauschal freigegeben?

Bei Einzelbesprechung: einen Block zeigen, entscheiden lassen, nächster Block.

**Schritt 5: Schreibe die neue `AGENTS.md`.** Kategorie A plus die drei Verhaltensabschnitte aus der Vorlage. Kategorie B **parkst du zwischenzeitlich** — der Projektkontext existiert noch nicht.

Lege dafür `.setup-parkplatz.md` an und weise darauf hin, dass die Datei in Phase 4 aufgelöst wird.

**Nenne darin kein Ziel.** Wohin der Inhalt wandert, steht erst in Phase 3 oder 4 fest — schreibst du jetzt einen Ort hinein, kann er bis dahin verschwunden sein, und ein wiederaufnehmender Agent schreibt ins Leere. Dieselbe Lehre wie überall in diesem Runbook: keinen Ort festschreiben, bevor er ermittelt ist.

**Schritt 6: Die Originaldateien noch nicht anfassen.** Aufgeräumt wird in Phase 4, wenn der Inhalt sicher angekommen ist.

## Für beide Fälle

Zähle am Ende die Zeilen und nenne die Zahl. Über 100: sag es und schlage vor, was nach B wandert.

**→ Adapter, Abschnitt „Phase 2".** Manche Werkzeuge lesen `AGENTS.md` nicht von sich aus und brauchen eine eigene Regeldatei, die sie importiert. Ist das der Fall, wird sie **hier** angelegt, nicht später. Ohne sie bleibt alles wirkungslos, was du gerade geschrieben hast.

**Schreibe zuletzt `.agent-template-version`** — zwei Zeilen. Phase 9 schreibt sie nur noch fort.

```
<Version aus VERSION> text
C:\dev\basisagent-public
phase9: offen
```

Zeile 1: Version und Profil, durch ein Leerzeichen getrennt. **Die Version liest du aus `VERSION` im Templateverzeichnis** — dieses Beispiel nennt sie absichtlich nicht. Hier stand bis zum 2026-09-01 eine feste Zahl, und die war neun Nebenversionen alt; ein Agent, der sie für die Vorgabe hielt, hätte einen falschen Stempel geschrieben, den die Wiederaufnahmetabelle dann ausliest. Zeile 2: **der Pfad zum Templateverzeichnis**, aus dem du gestartet bist — `<TEMPLATE>`.

Zeile 3 schreibst du wörtlich `phase9: offen`. Sie wird in Phase 9 Schritt 5 auf das Datum der bestandenen Wirkungsprobe gesetzt und ist bis dahin das einzige Merkmal, an dem eine späte Sitzung eine **unvollständige** Einrichtung erkennt — die Wiederaufnahmetabelle liest genau diese Zeile.

Die zweite Zeile ist der Grund, warum später überhaupt Feedback entstehen kann. Der Feedback-Skill läuft Wochen danach in einer eigenen Sitzung und kennt diesen Pfad aus nichts anderem. Fehlt die Zeile, fällt er auf den umständlicheren Weg zurück (→ Phase 9, Schritt 1).

Die Datei entsteht hier und nicht erst am Ende, weil ein Abbruch danach sonst nicht mehr erkennen lässt, welches Profil gilt: Die Wiederaufnahmetabelle kann eine mit der Code-Vorlage gefüllte `AGENTS.md` nicht von einer Text-Vorlage unterscheiden — beide haben einen `Rahmen` und beide liegen unter 100 Zeilen. Ohne diese Datei schließt sie falsch.

⏸ **HALT** — warte auf Freigabe, dann schreibe.

---

# Phase 3 — Ablaufgerüst

Ein Ablaufgerüst führt eine nennenswerte Änderung durch feste Stationen — aus einer Idee wird eine Festlegung, daraus Arbeitspakete, daraus das Ergebnis.

**Höchstens eines.** Zwei parallel ist der teuerste Fehler dieser Einrichtung: doppelte Beschreibungen in jedem Zug und zwei konkurrierende Abläufe, zwischen denen der Agent schwankt. Deshalb fällt die Entscheidung hier, vollständig — in Phase 5 kommt sie nicht wieder auf.

**Du installierst nicht.** Der Nutzer macht das selbst, weil die Optionen von Projekt zu Projekt abweichen.

**→ Profil, Abschnitt „Phase 3".** Dort steht die Optionstabelle für diese Projektart, die Voreinstellung und die Installationsanweisung.

Leg die Optionen vor und frag:

> Willst du eines davon einsetzen? Für ein Projekt, in dem nur Kleinigkeiten anfallen, lohnt sich keines — dann sind die Berechtigungen die Kontrolle.

**Bei Nein:** Phase 4 läuft trotzdem. Nur der Ablageort für Kategorie B aus Phase 2b ist dann keiner, den ein Gerüst vorgibt — frag danach.

**Bei Ja:** Gib die Installationsanweisung aus dem Profil weiter.

## Wenn schon ein Gerüst installiert ist

Dieser Fall ist der häufigere bei bestehenden Projekten, und die Phase war ursprünglich nicht dafür geschrieben. **Frag zuerst, ob es bleiben soll** — und sieh vorher nach, ob darin überhaupt gearbeitet wurde. „Installiert" und „in Benutzung" sind zwei verschiedene Befunde, und nur der zweite ist ein Argument fürs Behalten.

**Bei Behalten:** weiter unten bei „Nach der Meldung".

**Bei Abbau vier Schritte, in dieser Reihenfolge:**

1. **Jede Datei im Gerüstverzeichnis lesen — auch die, deren Namen du nicht kennst.** Nicht nur die offensichtlichen. Genau in den unscheinbaren stecken Festlegungen, die sonst nirgends im Projekt stehen: ein Abschlusskriterium, eine Abgrenzung, ein Maßstab. Was du hier übergehst, ist danach weg.
2. **Inhalt in Phase 4 in den Projektkontext übertragen.** Auch den Bearbeitungsstand, falls einer geführt wurde — aber dann nur an *einer* Stelle, sonst führen hinterher zwei Dateien denselben Stand.
3. **Erst danach entfernen** — und lieber verschieben als löschen. Ein Archivordner kostet nichts, ein verlorener Maßstab kostet die Nacharbeit. Das Entfernen selbst gibst du dem Nutzer (Verhaltensregel 8).
4. **Skills und Kommandos des Gerüsts in Phase 6 mit abarbeiten**, nicht hier. Dort steht auch, warum Löschen allein wirkungslos sein kann.

⏸ **HALT** — beende hier deinen Zug. Warte, bis der Nutzer die Installation oder den Abbau gemeldet hat.

**Nach der Meldung:** Prüfe, was tatsächlich entstanden ist — insbesondere, **wo diese Version den Projektkontext erwartet**. Setz keinen Dateinamen voraus; das ändert sich mit den Versionen. Die Prüfpunkte je Gerüst stehen im Profil.

Berichte, was du vorgefunden hast. Fehlt etwas, frag nach — repariere es nicht eigenmächtig.

---

# Phase 4 — Projektkontext füllen und aufräumen

Jetzt existiert das Ziel für Kategorie B.

**→ Profil, Abschnitt „Phase 4".** Dort steht der Ort und was inhaltlich hineingehört.

**Schritt 1:** Übertrage den Inhalt aus `.setup-parkplatz.md` an diesen Ort. Ordne ihn dabei sinnvoll. Zeige das Ergebnis vor dem Schreiben.

**Schritt 2:** Ergänze, was noch fehlt. Frag bei allem nach, was du nicht aus dem Projekt ablesen kannst.

**Schritt 3:** Prüfe auf Dopplungen zwischen `AGENTS.md` und dem Projektkontext. Jede Doppelung ist ein Fehler — der Inhalt gehört an genau eine Stelle. Zeige gefundene Dopplungen und frage, welche Fassung bleibt.

**Schritt 4 — Aufräumen der Altdateien.** Erst jetzt. Gehe die in Phase 0 gefundenen Anweisungsdateien einzeln durch:

> `.cursorrules` enthält N Zeilen. Davon sind M inhaltlich jetzt in `AGENTS.md` oder im Projektkontext abgedeckt, K sind spezifisch für Cursor.
> Optionen: unverändert lassen / auf den Cursor-spezifischen Teil kürzen / löschen.
> Was möchtest du?

**Nichts entfernen ohne ausdrückliches Ja.** Bei Zweifel: liegen lassen und weitermachen. Und nach Verhaltensregel 8 entfernst du ohnehin nicht selbst — du zeigst, was weg soll, nennst den Befehl und lässt den Nutzer ausführen.

**Schritt 5:** `.setup-parkplatz.md` ist aufgelöst und kann weg — nach Rückfrage, auf demselben Weg.

⏸ **HALT** nach jeder Einzelentscheidung.

---

# Phase 5 — Skills auswählen

**Hier schlägst du vor.** Der Nutzer soll nicht raten müssen, was es gibt — aber du installierst nichts eigenmächtig und nichts pauschal.

Der Pfad ist immer **`.claude/skills/<name>/SKILL.md`** — der native Ort für Claude Code.

**Der Preis, den du jedes Mal nennst:** Jeder Skill kostet Name und Beschreibung in **jedem Zug**. Nicht beim Aufruf, sondern immer. Deshalb wird hier ausgewählt und nicht gesammelt.

**Eine Einschränkung dazu, damit der Satz nicht zu viel behauptet:** Ein Skill mit `disable-model-invocation: true` im Frontmatter kann nur per `/name` aufgerufen werden — und kostet dann **gar nichts**, bis das geschieht. Die Doku sagt es in einer Tabelle: Standardfall „Description always in context, full skill loads when invoked", mit dem Feld „Description **not** in context, full skill loads when you invoke" (code.claude.com/docs, „Extend Claude with skills", Abschnitt *Control who invokes a skill*, abgerufen 23.08.2026).

Das ist die richtige Form für alles, was nur auf Zuruf gilt: Verfahren, Abläufe mit Nebenwirkung, Dinge beim Projektstart. Der Preis dafür ist, dass **das Modell den Skill nicht selbst starten kann** — es kann ihn nur vorschlagen, und auch das nur, wenn der Name irgendwo dauerhaft steht. Wer diese Form wählt, braucht also drei Zeilen Auslöser in `AGENTS.md`; das ist der ganze verbleibende Dauerpreis.

**Für einen Skill, der dem Modell zur Verfügung stehen soll, gilt der Satz oben unverändert:** Beschreibung in jedem Zug, ohne Ausnahme.

---

## Schritt 0 — Gesetzt: `uebergabe`

Dieser eine wird nicht vorgeschlagen, sondern gehört zur Einrichtung — er ist die Umsetzung von Regel 4 aus `prinzip.md`, und er ist der Grund, warum die Regeldatei den Abschnitt „Übergabe" trägt.

Kopiere `<TEMPLATE>/core/skills/uebergabe/` nach `.claude/skills/uebergabe/` **und leg `.claude/skills/` vorher an**: Phase 1 schreibt nur `settings.json`, bei einem neuen Projekt fehlt das Verzeichnis, und der Kopierbefehl scheitert. (**Kopieren**, nicht verlinken — das Zielprojekt soll ohne das Template laufen, siehe README). Danach richtet er sich selbst ein: `/uebergabe einrichten` legt `uebergabe/` samt Vorlage an.

**Ist Kopieren gesperrt**, weil das Muster „Externer Quellbestand" `cp` und `Copy-Item` unabhängig vom Pfad sperrt, leg die Dateien mit dem Schreibwerkzeug inhaltsgleich an. Prüf danach mit `diff -r <TEMPLATE>/core/skills/uebergabe .claude/skills/uebergabe`, dass die Ausgabe leer ist (Journal 2026-10-20, Codeprojekt E, Nr. 5). Dieselbe Kollision steht für die Wirkungsprobe in Phase 9.

**Er zählt nicht gegen die vier Vorschläge aus Schritt 2** und braucht keinen Auslöser aus Phase 0, weil er nichts kostet: `disable-model-invocation: true`. Nenne dem Nutzer beides — den Nutzen und den Nullpreis —, sonst liest es sich wie eine Ausnahme von der Regel, die du gerade erklärt hast.

---

## Schritt 1 — Was schon da ist

Prüfe zuerst, was der Nutzer bereits hat, bevor du irgendetwas vorschlägst:

- Projektlokal: `.claude/skills/`, `.agents/skills/`
- Global: `~/.claude/skills/`
- **Plugins in `~/.claude/settings.json`** unter `enabledPlugins` — ein aktives Plugin bringt seine Skills mit, ohne dass ein Verzeichnis existiert. Das wird leicht übersehen und ist die häufigste Quelle unbemerkter Dauerkosten.

Was schon im Projekt liegt, schlägst du nicht noch einmal vor. **Was nur global liegt, ersetzt die Projektkopie nicht** (Nutzerentscheidung vom 2026-10-07): Auf einem anderen Rechner oder bei Fernzugriff auf das Projekt fehlt es. Frag, ob es ins Projekt soll — als Kopie, nicht als Verknüpfung auf den globalen Ort. Ein globales Plugin bringt seine Skills nicht ins Projekt; dort hilft nur, die benötigten Skills einzeln zu kopieren. Was bei gleichem Namen auf diesem Rechner gilt, nennt der Adapter.

---

## Schritt 2 — Den Katalog vorlegen

Nicht die ganze Liste. **Höchstens vier Vorschläge**, ausgewählt anhand dessen, was du in Phase 0 gefunden hast.

**Das Ablaufgerüst ist in Phase 3 entschieden.** Bring es hier nicht wieder auf — auch nicht die Alternativen, die dort nicht gewählt wurden. Wenn der Nutzer danach fragt, verweise auf die Entscheidung und nenne den Grund, der damals galt.

**→ Profil, Abschnitt „Phase 5".** Dort steht der Katalog für diese Projektart, gegliedert in einmalig gebrauchte und bedarfsgetriebene Skills, jeweils mit Auslöser.

**Kein Auslöser, kein Vorschlag.** „Könnte man mal brauchen" ist kein Auslöser.

### Was du nicht vorschlägst

- **Router- und Meta-Skills** (`ask-matt`, `wizard`, `setup-*`): Sie kosten eine Beschreibung, um auf andere Skills zu verweisen, die ihre Beschreibung ebenfalls kosten.
- **Regelwerke, die immer gelten sollen** (karpathy, ponytail und Verwandte): Ihr Inhalt gehört nach `AGENTS.md`, wo er einmal steht statt doppelt zu kosten. Die Vorlage deckt den Kern bereits ab. Herleitung: `feedback/offene-punkte.md`, Punkt 8.
- **Skills unklarer Herkunft.** Neben den Kontextkosten steht ein zweites Kriterium, und bei vertraulichem Material ist es das schwerere: **Ein Skill ist Text, der zu deinen Anweisungen wird.** Eine `ask`-Regel auf Web-Abruf fängt nur, was sie als Web-Abruf erkennt. Bei einem Projekt mit vertraulichem Bestand ist unklare Herkunft ein **Ausschlussgrund**, nicht bloß ein Preis. Sag dem Nutzer den Grund — ein Skill wird Teil deiner Anweisungen —, sonst liest es sich wie Vorsicht ohne Grund. Nenn keine Statistik zur Verbreitung unsicherer Skills: Die hier früher zitierte Zahl war nie gegen ihre Quelle geprüft und ist am 2026-10-22 gestrichen (`feedback/offene-punkte.md`, Punkt 17).
- **Komplette Skill-Sammlungen oder -Plugins.** Ein Plugin bringt seinen ganzen Satz mit. Das heißt aber **nicht**, dass es nur ganz oder gar nicht geht: Manche Werkzeuge können einzelne Skills eines Plugins abschalten oder auf den Namen reduzieren — → Adapter, Phase 6. Sag dem Nutzer nie, einzelne Skills ließen sich nicht herausnehmen, ohne im Adapter nachgesehen zu haben.

---

## Schritt 3 — Einzeln fragen

Pro vorgeschlagenem Skill:

> `<name>` — <was er tut, ein Satz>.
> Ich schlage ihn vor, weil <konkreter Befund aus Phase 0>.
> Installieren?

⏸ Warte auf die Antwort. Eine Frage auf einmal.

---

## Schritt 4 — Installationsanweisung geben

**Vorher: den Rumpf jedes freigegebenen Skills lesen.** Ruft er weitere Skills auf, gehören sie in dieselbe Auswahl — das „nichts sonst" unten meint den Satz **einschließlich seiner Abhängigkeiten**. Ohne diesen Blick ist ein Wrapper nicht von einem Router-Skill zu unterscheiden, den Schritt 2 ausschließt.

**Wie du an den Rumpf kommst.** Bei Sammlungen liegen die Skills meist unter `skills/<kategorie>/<name>/SKILL.md`, und die Kategorieebene ist von außen nicht zu erraten — ein Abruf ohne sie läuft auf 404. Nach zwei Fehlschlägen hol das Verzeichnis über die Tree-API des Anbieters, statt weiter zu raten (beobachtet am 2026-08-31, zwei verlorene Abrufe).

Gemessen: `grill-with-docs` besteht aus einem Satz, der `grilling` und `domain-modeling` aufruft. Installiert wurde nur der Wrapper; der einzige selbst gewählte Skill des Projekts war damit funktionslos und zeigte auf zwei Namen, die es nicht gab. Aufgefallen ist es Tage später und **nicht** durch die Sichtbarkeitsprüfung in Phase 6 — der Wrapper lag korrekt und war aufrufbar. Er war sichtbar und leer.

**Du installierst nicht.** Gib dem Nutzer für die freigegebenen Skills:

> ```
> npx skills@latest add mattpocock/skills --skill <name1> <name2> --agent claude-code --copy
> ```
> Das legt genau diese Skills unter `.claude/skills/` an, ohne Auswahlmenü. Dazu entsteht `skills-lock.json` im Projekt; die gehört dem Installer.
>
> Die Dateien landen editierbar in deinem Repo — du kannst sie anpassen, verlierst dann aber Aktualisierungen.
>
> Sag mir Bescheid, wenn du fertig bist.

**Warum `--agent claude-code --copy`:** Ohne `--agent` schreibt der Installer für jedes erkannte Werkzeug. Ohne `--copy` legt er Symlinks aus `.agents/skills/` an; unter Windows ohne Entwicklermodus scheitern sie, dann entstehen zwei echte Kopien, auf einer Netzfreigabe brach ein Lauf mit `EPERM` ab (Journal 2026-09-28, Codeprojekt C, Nr. 5, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`; und 2026-10-20, Codeprojekt E, Nr. 2; Optionen laut `vercel-labs/skills`, `docs/commands.md`, abgerufen 22.10.2026).

Falls die Skills nicht aus diesem Repo stammen: Ziel ist `.claude/skills/<name>/SKILL.md`, der Weg dorthin ist dem Nutzer überlassen.

⏸ **HALT** — beende hier deinen Zug.

---

# Phase 6 — Skills aufräumen

**Schritt 1:** Liste alle gefundenen Skills mit Pfad, Name und Beschreibung. Suche in: `.claude/skills/`, `.agents/skills/`, `~/.claude/skills/`. In Sammelprojekten auch `*/.claude/skills/` der Unterprojekte.

**Prüfe zu jedem Skill die Sichtbarkeit.** Sie misst tatsächliches Verhalten statt einer Annahme darüber — aber nur unter einer Bedingung, und sie beweist weniger, als sie zu beweisen scheint.

> Erscheint der Skill in der Skill-Liste deiner laufenden Sitzung?

**Bedingung: Die Sitzung muss nach der Installation gestartet sein.** Hast du in Phase 5 derselben Sitzung installiert, stammt deine Liste von vorher — ein völlig normaler Skill fehlt darin ebenfalls. Dann gehört die Prüfung an den Neustart in Phase 9 Schritt 5, wo ohnehin neu gestartet wird; sie kostet dort keinen zusätzlichen Zug. In Phase 6 bleibt die strukturelle Kontrolle: Verknüpfung und `SKILL.md` vorhanden.

**→ Adapter, Abschnitt „Phase 6 — Neue Skills ohne Neustart".** Manche Werkzeuge laden neue Skills in der laufenden Sitzung nach; dort gilt die Bedingung nur eingeschränkt.

**Vor dem Urteil „tot" zwei Gegenfragen:**

| Frage | Wenn ja |
|---|---|
| Läuft der Skill absichtlich nur per `/name`? (→ Adapter, Phase 6) | Nicht tot, sondern nur nicht vorgeschlagen. Nichts empfehlen |
| Wurde in dieser Sitzung installiert? | Kein Urteil möglich → Phase 9 Schritt 5 |

Erst wenn beide nein sind, ist er **tot**: Er belegt Platz, aber kein Werkzeug lädt ihn. Der häufigste Grund ist ein Installer, der nach `.agents/skills/` geschrieben und die Verknüpfung nach `.claude/skills/` nicht angelegt hat. Ein Verzeichnis voller Beschreibungen, die niemand liest, sieht bei einer Pfadprüfung korrekt aus — und ohne Gegenstück gibt es auch keine Dublette, die auffiele.

**Beide Fehlurteile gehen in dieselbe Richtung**, und das ist der Grund für diesen Umbau: Sie empfehlen, etwas Funktionierendes zu entfernen. Die Prüfung soll vor falschem Behalten schützen — sie rät hier zum falschen Wegwerfen, und der Nutzer merkt es erst, wenn er den Skill wieder braucht.

**Umgekehrt beweist „erscheint in der Liste" nur, dass der Skill geladen wird — nicht, dass er funktioniert.** Ruft sein Rumpf andere Skills auf, prüfe, ob die da sind. Ein Wrapper auf zwei fehlende Skills ist sichtbar und leer. Siehe Phase 5, Schritt 4.

**Ein fehlender Pfad in einem Globmuster-Listing belegt keine fehlende Verknüpfung.** Junctions und Symlinks werden dabei nicht durchlaufen; der Verknüpfungstyp braucht einen eigenen Aufruf (`Get-ChildItem -Force` zeigt `LinkType` und `Target`). Ohne diesen Zwischenschritt schlägst du eine Reparatur an einer intakten Verknüpfung vor.

Melde tote Skills getrennt von den Auffälligkeiten unten. Sie kosten nichts, aber sie leisten auch nichts, und der Nutzer hält sie vermutlich für aktiv.

**Schritt 2:** Markiere Auffälligkeiten:

- **Dubletten** — derselbe Skill an mehreren Orten. **Global *und* projektlokal ist keine Dublette zum Aufräumen:** Nur die Projektkopie reist mit auf andere Rechner (Phase 5, Schritt 1). Auffällig ist nur, wenn beide sich inhaltlich unterscheiden — welche auf diesem Rechner gewinnt, nennt der Adapter. Entfernen kommt höchstens für die globale in Frage, und nur, wenn kein anderes Projekt sie braucht. **Prüfe zuerst den Verknüpfungstyp:** Manche Installer legen die Dateien unter `.agents/skills/` ab und verlinken sie per Symlink oder Junction nach `.claude/skills/`. Das sieht wie eine Dublette aus, ist aber genau das gewollte werkzeugneutrale Muster und kostet nur einmal.
- **Funktionale Überschneidung** — mehrere Skills mit ähnlichem Zweck, besonders bei allem, was klärt oder plant. Zwei Klärungswerkzeuge hintereinander bringen wenig.
- **Falscher Ort** — projektlokale Skills unter einem Verzeichnis, das Claude Code nicht liest (etwa `.opencode/skills/` aus früheren Einrichtungen). Werden sie gebraucht: nach `.claude/skills/` verschieben.
- **Regeln statt Skill** — ein Skill, dessen Inhalt eigentlich immer gelten soll, gehört inhaltlich nach `AGENTS.md`. Er kostet sonst doppelt: Beschreibung in jedem Zug plus Rumpf beim Laden.

**Bevor du erzeugte Dateien löschst:** Prüfe, ob das erzeugende Werkzeug sie wieder anlegt. Bei OpenSpec entscheiden die globalen Einstellungen `delivery` und die Workflow-Liste darüber (Codeprofil, „Bei OpenSpec") — steht `delivery` auf `both` oder der Skill noch in der Liste, bringt das nächste `openspec update` das Gelöschte zurück. Erst `openspec config set delivery skills` und die Liste anpassen, dann löschen.

**Schritt 3:** Zeige die Liste mit deinen Anmerkungen und frage **pro Skill einzeln**:

> `<name>` — <Beschreibung>. <Deine Anmerkung.>
> Behalten, verschieben oder entfernen?

**Nichts eigenmächtig entfernen.** Auch offensichtliche Dubletten nicht.

**Schritt 3b — MCP-Server.** Dieselbe Rechnung wie bei Skills: Jeder verbundene Server bringt seine Werkzeugschemata in jeden Zug, benutzt oder nicht. Nimm die in Phase 0 gefundenen Server und frage pro Server einzeln:

> `<name>` — <was er tut>. Für dieses Projekt <mit / ohne Auslöser>.
> Verbunden lassen oder trennen?

Global verbundene Server gelten für **alle** Projekte — sag das dazu, bevor der Nutzer entscheidet. Den werkzeugspezifischen Trennbefehl nennt der Adapter.

**Schritt 4:** Falls `CONTEXT.md` existiert **und Inhalt hat**, schlage diese zwei Zeilen für `AGENTS.md` vor:

```markdown
## Fachsprache
Verbindliches Glossar: `CONTEXT.md`. Verwende diese Begriffe für Bezeichner.
```

Danach die Zeilenzahl neu prüfen und nennen.

⏸ **HALT** nach jeder Einzelentscheidung.

---

# Phase 7 — entfällt

Bis 0.26.0 stand hier das Anbinden eines Zweitwerkzeugs (OpenCode). Es wurde nie eingesetzt und ist seit 0.27.0 aus der Einrichtung genommen (`core/verworfen.md`, „OpenCode als Zweitwerkzeug"). Die Nummer bleibt frei, damit Verweise auf Phase 8 und 9 stimmen.

**Nicht danach fragen.** Bringt der Nutzer selbst ein zweites Werkzeug zur Sprache: `AGENTS.md` ist werkzeugneutral, viele Werkzeuge lesen sie nativ. Sag ihm, dass die Anbindung nicht Teil dieser Einrichtung ist, und schreib einen Journaleintrag — er ist die Revisionsbedingung.

---

# Phase 8 — Rollentrennung (optional)

Frage:

> Möchtest du eine Rolle, die nicht schreiben darf? Nützlich, wenn du mitten in der Ausführung kurz nachdenken willst, ohne das Werkzeug zu wechseln.

**→ Adapter, Abschnitt „Phase 8".** Claude Code bringt es schon mit.

Grundsatz: Eine solche Rolle ist eine **Berechtigungsgrenze, kein Anweisungssatz.** Alles, was mit Anweisungen zu erreichen ist — Fragen stellen, Mehrdeutigkeiten benennen, Vorgehen vorschlagen — kommt aus `AGENTS.md` und den Skills. Schreib es nicht in die Rollendefinition.

Was sie leistet und ein Skill nicht: ein **Schreibverbot, das vom Harness erzwungen wird.** Eine Anweisung in einer Skill-Datei ist Kontext und kann überschrieben werden.

**Kein Modell festlegen.** Weder in der Rollendefinition noch als Empfehlung. Die Modellwahl trifft der Nutzer selbst und situativ — sie gehört nicht in diese Einrichtung. Wenn eine Vorlage ein `model:`-Feld hat, lass es weg; die Rolle erbt dann das Modell der Sitzung.

⏸ **HALT**

---

# Phase 9 — Abschluss

`<TEMPLATE>` steht unten für das Verzeichnis, aus dem du gestartet bist — dort, wo die Startdatei liegt.

**Schritt 1 — Feedback-Weg klären.** Zwei Wege, und du prüfst zuerst, welcher hier möglich ist.

**Prüfe: Existiert `<TEMPLATE>/feedback/journal.md` und lässt sich lesen?**

Das genügt. **Mach keinen Schreibtest.** Eine Testdatei landet im Templateverzeichnis, in das nichts gehört — und nach Verhaltensregel 8 kannst du sie nicht mehr entfernen, sodass Phase 9 mit einer Aufräumbitte an den Nutzer beginnt. Die Schreibbarkeit zeigt sich beim ersten echten Eintrag von selbst: Ein fehlgeschlagener Schreibvorgang scheitert sichtbar und hinterlässt nichts.

**Ein fehlender `additionalDirectories`-Eintrag ist kein Hindernis.** Das Schreiben ins Journal funktioniert auch ohne ihn — es kostet nur eine Rückfrage je Vorgang. Der Eintrag ist Komfort, keine Voraussetzung. Verwechsle das nicht, sonst installierst du den Skill als Rückfallebene, obwohl das Template erreichbar ist, und das Projekt zahlt seine Beschreibung in jedem Zug.

**Wenn ja — der Regelfall.** Dann ist **kein Skill zu installieren.** Sag dem Nutzer:

> Wenn dir im Alltag auffällt, dass diese Einrichtung etwas nicht abdeckt oder im Weg steht, sag es einfach in der Sitzung, in der es passiert. Der Agent schreibt den Befund direkt ins Journal des Templates — mit dem Kontext, den er gerade hat.
>
> Das kostet dich einen Satz und dieses Projekt keinen Kontext: Es wird kein Skill installiert, also auch keine Beschreibung in jedem Zug bezahlt.

Der Pfad dafür steht in Zeile 2 von `.agent-template-version`, die du in Phase 2 geschrieben hast. **Prüf, dass sie stimmt** — daran hängt der ganze Weg.

**Wenn nein, aber `<TEMPLATE>/core/skills/template-feedback/` existiert** — anderer Rechner, Freigabe ohne Schreibrecht, Template nicht erreichbar: Dann den Skill installieren, `<TEMPLATE>/core/skills/template-feedback/` nach `.claude/skills/template-feedback/` **kopieren**, nicht verlinken. Er schreibt dann nach `.template-feedback.md` im Projekt, und der Nutzer erntet später von Hand ein.

Sag ihm dabei den Preis: Der Skill kostet seine Beschreibung in jedem Zug dieses Projekts. Er ist die Rückfallebene, nicht die bessere Lösung.

**Wenn beides fehlt — eine Verteilkopie** (öffentliche Fassung, Lesekopie auf einer Freigabe): Dann gibt es **keinen Rückkanal**, und das ist gewollt (Nutzerentscheidung vom 2026-11-16). Installier nichts, leg keine `.template-feedback.md` an, und Schritt 3c entfällt. **Sag dem Nutzer nichts dazu** — er kennt den Rückkanal nicht, und ein Hinweis auf etwas, das fehlt, wirft nur Fragen auf.

**Schritt 2 — Versionsstempel fortschreiben.** Die Datei `.agent-template-version` entstand am Ende von Phase 2. Prüfe alle drei Zeilen — Version und Profil, den Templatepfad, dazu `phase9:` — und schreib sie fort, falls sich unterwegs etwas geändert hat. Fehlt sie oder fehlt ihr eine Zeile, leg sie jetzt vollständig an.

**`phase9:` bleibt hier auf `offen`.** Es wird erst in Schritt 5 auf das Datum gesetzt, und zwar erst nach bestandener Probe. Wer es hier schon setzt, nimmt der Zeile ihren ganzen Zweck: Sie soll gerade den Fall kennzeichnen, dass die Einrichtung nach Schritt 4 endet.

**Schritt 3 — Prüfen und melden:**

- [ ] `AGENTS.md` unter 100 Zeilen (verwaltete Fremdblöcke nicht mitgezählt) — Ist-Zahl nennen
- [ ] Der Block „Rahmen" ist konkret ausgefüllt, keine Platzhalter übrig
- [ ] Keine Dopplung zwischen `AGENTS.md` und dem Projektkontext
- [ ] Die Regeldatei des Werkzeugs existiert und bindet `AGENTS.md` ein (→ Adapter)
- [ ] Berechtigungsdatei ist geschrieben und syntaktisch plausibel — **ob sie greift, prüft Schritt 5, nicht dieser Punkt**
- [ ] Kein Skill installiert, der nicht gebraucht wird
- [ ] `.setup-parkplatz.md` ist weg
- [ ] Keine MCP-Server verbunden, die nicht gebraucht werden
- [ ] Hilfsagenten nach der Wahl des Nutzers: gesperrt (Vorgabe) — oder erlaubt und Rechercheagenten nach seiner Stufe angelegt, bei „unbegrenzt" keine Datei (→ Adapter)
- [ ] `.agent-template-version` geschrieben — Version, Profil, Templatepfad **und** `phase9: offen`
- [ ] Der Feedback-Weg ist geklärt: direkt ins Journal oder Skill installiert. In einer Verteilkopie lässt du den Punkt in der Meldung weg
- [ ] Der Übergabe-Auslöser steht in der Regeldatei **und** der Skill liegt im Projekt (→ Phase 2 für die Zeilen, Phase 5 Schritt 0 für den Skill)

**→ Profil, Abschnitt „Phase 9".** Die zusätzlichen Prüfpunkte dieser Projektart kommen hinzu — arbeite sie mit ab.

**Schritt 3b — Dauerkosten beziffern.**

Zeilen zählen genügt nicht. Dieselbe `AGENTS.md` hat 39 Zeilen oder 55, je nachdem wie umgebrochen wird, bei praktisch gleichem Verbrauch — die Zeilengrenze lässt sich durch Umbruchverhalten unterlaufen, ohne dass jemand etwas falsch macht. Nenne deshalb Zahlen, die die Größe messen, aus der `core/prinzip.md` die Regel herleitet:

| Zahl | Wie |
|---|---|
| Zeichen der Regeldatei, importierte Dateien mitgezählt | `wc -c`, bzw. `(Get-Content -Raw).Length` |
| Zeichen aller Skill-Beschreibungen zusammen, **globale mitgezählt** | `name:` und `description:` je `SKILL.md` |
| Anzahl der Skills mit Beschreibung | zählen |

Bei deutschem Text sind rund drei Zeichen ein Token. Das reicht für die Größenordnung; genauer musst du nicht werden.

**Die Zahl allein sagt nichts.** Die Prüffrage lautet nicht „ist es wenig", sondern **„wofür wird bezahlt, und wirkt es":**

- Für **jede** Skill-Beschreibung muss der Auslöser nennbar sein. Kannst du ihn nicht nennen, gehört der Skill in Phase 6 zurück auf den Tisch.
- Für die Regeldatei muss belegt sein, dass das Werkzeug sie **überhaupt liest**. Eine `AGENTS.md` ohne die Regeldatei, die sie einbindet, kostet null und wirkt null. Eine Einrichtung, die sie zum ersten Mal wirksam macht, **erhöht** die Dauerkosten und ist trotzdem richtig — sag das dazu, sonst liest der Nutzer die Zahl als Verschlechterung.
- **Stell beide Posten nebeneinander.** Übersteigen die Skill-Beschreibungen die Regeldatei, ist Phase 6 der größere Hebel als jede Kürzung an `AGENTS.md`. Gemessen: 5.215 gegen 3.276 Zeichen (Journal 2026-09-22, Textprojekt J, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`), vorher schon 1.186 gegen null (`feedback/offene-punkte.md`, Punkt 7).

**MCP-Werkzeugschemata sind lokal nicht messbar.** Kennzeichne sie ausdrücklich als nicht erfasst, statt den Eindruck von Vollständigkeit zu erzeugen. Bei mehreren verbundenen Servern sind sie oft der größte Posten.

**Schritt 3c — Zurückmelden, was nur diese Einrichtung wissen kann.**

Schritt 1 hat den Weg für **künftige** Befunde eingerichtet. Dieser Schritt ist etwas anderes: eine Meldung **jetzt**, mit Angaben, die nach dieser Sitzung niemand mehr erheben kann. Die Regeldatei wächst weiter, der erste Eindruck des Nutzers verblasst, und ob der Platz eng war, weiß nur, wer sie gerade gefüllt hat.

Schreib einen Journaleintrag über den Weg aus Schritt 1 — direkt nach `<TEMPLATE>/feedback/journal.md`, oder in die Rückfalldatei, falls das Template nicht erreichbar war. **Verteilkopie ohne Rückkanal:** Dieser Schritt entfällt.

**Vorher:** Schreib das Projekt als `<Art>projekt ?`, nie mit Namen. Das Pseudonym vergibt die Bewertung im Template. Schließ den Eintrag mit `**Urteil:** offen` und trag ihn mit einer Zeile in `## Unbewertet` ein. Ohne diese drei Angaben findet die Bewertung den Eintrag nicht, und der Klarname wandert mit dem Journal weiter (Codeprojekt F, 2026-10-22: alle drei fehlten).

Vier Angaben, je ein bis zwei Sätze:

| Angabe | Warum sie gebraucht wird |
|---|---|
| Ist-Zeichen und Ist-Zeilen der Regeldatei aus Schritt 3b, dazu die Einschätzung: war der Platz gebraucht, oder kam die Grenze nie in Sicht? | Die Grenze 100 Zeilen / 4.500 Zeichen stammt aus einer Herstellerempfehlung, nicht aus einer Messung an gefüllten Dateien |
| Ob die Übergabe-Zeilen in der erzeugten Regeldatei stehen, und was der Nutzer dazu gesagt hat | Ob der Auslöser überhaupt ankommt, ist bisher unbelegt |
| Bei einem Codeprojekt: was die Kennzahlenprobe aus Phase 0 hergab — **auch wenn sie nichts hergab** | Ein negatives Ergebnis schließt die Frage genauso wie ein positives; offen bleibt sie nur ohne Antwort |
| Was nicht funktioniert hat wie beschrieben, auch Kleinigkeiten | Der Rest dieser Phase erzeugt beim Nutzer den Eindruck, alles sei glatt gegangen |

**Fass im Templateverzeichnis nur das Journal an.** Nicht `feedback/offene-punkte.md`, nicht `core/`. Die Punkte dort werden im Template beim Bewerten nachgezogen, nicht von hier aus — sonst führen zwei Stellen dieselbe Buchhaltung und keine davon vollständig.

**Ein „nichts aufgefallen" ist auch eine Meldung** und gehört hin. Eine Einrichtung, die glatt lief, ist der einzige Beleg dafür, dass eine Änderung trägt; ohne sie steht im Journal nur, was schiefgegangen ist, und das Template lernt einseitig.

**Warum dieser Schritt hier steht und nicht am Ende.** Ein Prüfschritt hinter dem Abschlussschritt wird übersprungen — belegt am Übergabeverfahren, wo „Größe prüfen" hinter „Ergebnis nennen" stand und in drei von vier Fällen nicht ausgeführt wurde. Schritt 4 zeigt die Übersicht und beendet den Vorgang für den Nutzer. Was danach kommt, ist eine Bitte; was davor steht, ist Teil der Arbeit.

**Schritt 4 — Übersicht zeigen:**

| Datei | Status |
|---|---|
| Berechtigungsdatei (→ Adapter) | neu / geändert / unverändert |
| `AGENTS.md` | ... |
| Projektkontext (Ort → Phase 3/4 ermittelt) | ... |
| Altdateien | was blieb, was ging |


**Nenne die Aufwandstufe.** Sie ist der Regler, den der Nutzer täglich
benutzt, ohne ihn zu kennen. Sag ihm: dass es sie gibt, wie die Voreinstellung
lautet, welche Stufe du für die Arbeit dieses Projekts vorschlägst — mit
Begründung in einem Halbsatz — und ob ein Wechsel mitten in der Sitzung den
Zwischenspeicher kostet. Das hängt vom Modell ab; wo er kostet, gehört er an
den Sitzungsanfang. Die Wahl
trifft er, nicht du; das Template setzt keine Stufe. **→ Adapter, Abschnitt
„Aufwandstufe".** Kennt das Werkzeug keine Stufe, übergeh den Punkt, statt
etwas zu behaupten.

**Nenne die Wahl zu Hilfsagenten aus Phase 1.** Gesperrt: sag, dass sie aus
sind und wie er sie einschaltet. Erlaubt: die gewählte Stufe und die beiden
Wege, sie zu ändern — je Aufgabe und dauerhaft. **→ Adapter, Abschnitte
„Hilfsagenten überhaupt" und „Rechercheagenten".** Wer nur die Grenze kennt und nicht den Weg darüber
hinaus, umgeht sie irgendwann, statt sie anzupassen.

**Nenne offene Punkte:** alles, was der Nutzer vertagt hat, und alles, was du nicht eindeutig klären konntest.

---

## Schritt 5 — Neustart und Wirkungsprobe

**Der wichtigste Schritt dieser Phase.** Bis hierher ist die Einrichtung geschrieben, aber die Berechtigungen greifen noch nicht — siehe Phase 1. Ohne diesen Schritt verlässt der Nutzer die Einrichtung mit dem Eindruck, geschützt zu sein, und ist es nicht.

Sag ihm:

> Starte das Werkzeug jetzt neu, bevor du inhaltlich weiterarbeitest. Berechtigungen werden beim Sitzungsstart gelesen — alles, was wir in Phase 1 geschrieben haben, gilt erst danach. In dieser Sitzung galten noch deine alten Regeln.
>
> Danach machen wir eine kurze Probe, ob die Sperren tatsächlich greifen.

⏸ **HALT** — beende hier deinen Zug.

### Nach dem Neustart: zuerst die Skill-Liste

**Hierher gehört die Sichtbarkeitsprüfung aus Phase 6**, falls dort in derselben Sitzung installiert wurde. Erst jetzt ist die Liste aktuell. Sieh nach, ob die in Phase 5 installierten Skills erscheinen, und wende die beiden Gegenfragen aus Phase 6 an, bevor du einen für tot erklärst. Ein Skill, der auch jetzt fehlt, ist ein Befund — vorher war er keiner.

### Dann: kommt die Regeldatei überhaupt an?

Schritt 3b verlangt den Beleg, dass das Werkzeug die Regeldatei **überhaupt liest**. Dort war er nicht zu führen: Ob ein Import ankommt, zeigt sich erst zu Beginn einer Sitzung, die ihn geladen hat. Hier ist er zu führen — **→ Adapter, Abschnitt „Phase 2 — Besonderheit"** nennt den Weg für das jeweilige Werkzeug.

**Existiert ist nicht wirksam.** Der Prüfpunkt in Schritt 3 sagt „die Regeldatei existiert und bindet `AGENTS.md` ein". Beides kann stimmen, während der *Inhalt* der importierten Datei zu Sitzungsbeginn nicht im Kontext liegt — dann steht die Regel korrekt gebaut auf der Platte und erreicht den Agenten nie. Belegt am 2026-09-03 (Journal, Infrastrukturprojekt C): Der Agent legte Skripte am falschen Ort ab, obwohl `AGENTS.md` den richtigen vorschreibt, und kannte die Regel erst, als er die Datei aus anderem Anlass selbst las.

Steht der Inhalt nicht im Kontext, ist das ein Befund wie ein fehlender Skill — melden, nicht wegerklären. Er ist auch nicht durch Nachlesen zu heilen: Dass der Agent die Datei später einmal liest, macht die Regel nicht dauerhaft wirksam.

### Dann vier Aufrufe, nicht einer

**Vorher den Modus der Sitzung erfragen.** Genehmigt das Werkzeug in einem automatischen Modus ohne Rückfrage, belegt ein durchlaufender Aufruf keine Freigabe — die erste Zeile der Tabelle sagt dann nichts. **→ Adapter, Abschnitt zum Modus**, sofern das Werkzeug einen hat.

**Ein einzelner Löschversuch beweist nichts.** „Abgelehnt" unterscheidet nicht zwischen einer `deny`-Regel und einer Ablehnung des Nutzers im Dialog. Erst das selektive Muster trennt beides:

| Aufruf | Muss | Zeigt |
|---|---|---|
| **schreibend, nicht gesperrt** — Testdatei anlegen, außerhalb des Repos | durchlaufen | Der Nutzer lehnt nicht pauschal ab |
| **lesend** — Verzeichnis auflisten | durchlaufen | Es ist nicht alles blockiert |
| **gesperrt über PowerShell** — dieselbe Datei mit `Remove-Item` löschen | scheitern | Die Sperre greift |
| **gesperrt über Bash** — dasselbe mit `rm` | scheitern | Sie greift auf **beiden** Wegen |

Erst wenn alle vier so ausgehen, ist belegt, dass die Regel gewirkt hat. Auf macOS und Linux entfällt die vierte Zeile mit den PowerShell-Regeln.

**Liegt der scharfe Schutz nicht in `deny`, sondern in einem Hook,** gilt dasselbe Muster mit den Befehlen, die dort tatsächlich gesperrt sind: Einer schreibt, einer liest, ein gesperrter scheitert über jede Shell. Die Befehle der Tabelle setzen die Vorlage voraus, das Muster nicht (Journal 2026-09-22, Infrastrukturprojekt D, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`).

**Schreib den gesperrten Aufruf zusätzlich so, wie du ihn ohne Probe geschrieben hättest.** Eine Sperre matcht die Schreibweise, nicht das Programm: `git -C <pfad> clean` kommt an `git clean *` vorbei (→ Adapter, Falle 6). Die Standardform bestätigt nur die Regel. Ob sie dich im Alltag aufhält, zeigt erst die eigene Schreibweise.

**Danach, und nur danach: `phase9:` auf das Datum setzen.** Zeile 3 von `.agent-template-version` trägt bis hierher `offen`; jetzt kommt das heutige Datum hinein. Das ist der Abschluss der Einrichtung — nicht Schritt 4, der nur die Übersicht zeigt. Gehen die vier Aufrufe **nicht** wie erwartet aus, bleibt `offen` stehen und du meldest, was fehlt: Eine unvollständige Einrichtung, die als vollständig markiert ist, ist schlechter als eine, die sich als unvollständig zu erkennen gibt.

**Warum Anlegen und nicht Verschieben.** Verschieben ist gesperrt, sobald ein Pfad nach dem Adapter-Muster „Externer Quellbestand" geschützt wird — und das empfiehlt dieses Runbook selbst. Das frühere Beispiel war damit ausgerechnet dort unbrauchbar, wo die Einrichtung am gründlichsten war.

**Wohin die Testdatei gehört: außerhalb des Repos**, ins Temp- oder Scratchpad-Verzeichnis der Sitzung. Die Sperren sind Befehlssperren und pfadunabhängig, das Ergebnis ist also genauso aussagekräftig. Im Projekt darf sie nicht liegen: Löschen ist ja gerade das, was gesperrt ist, nach Verhaltensregel 8 entfernst du ohnehin nichts selbst — und der nächste Rat lautet „committe den Stand jetzt". Eine Datei, die die Probe selbst erzeugt hat, läge dann im Commit.

**Warum vier und nicht drei.** Nach Falle 8 des Adapters muss jede Regel für beide Shells geführt werden. Ist nur eine der beiden Hälften wirksam, sieht die Berechtigungsdatei nach vollständigem Schutz aus, und drei Aufrufe hätten das bestätigt. Genau dieser Fall hat die Vorlage schon einmal vollständig wirkungslos gemacht.

Melde das Ergebnis, und **hak den Prüfpunkt aus Schritt 3 erst jetzt ab.**

### Wenn ein Ergebnis einem früheren widerspricht

**Frag nach einem Neustart, bevor du einen bestehenden Befund widerrufst.** Du kannst nicht wissen, ob zwischenzeitlich neu gestartet wurde — dein eigener Sitzungszustand ist dir nicht vollständig zugänglich. Die naheliegende Ersatzerklärung „die Regeln greifen wohl verzögert" verwandelt einen belastbaren Befund in einen unbrauchbaren.

---

**Schlage als letztes zwei Dinge vor. Erstens sichern:**

> Committe den Stand jetzt, bevor du weiterarbeitest.

**Ohne Git** (Phase 0) rate nicht zum Commit — frag stattdessen, wie er diesen Stand sichert: Kopie, Freigabe, Sicherungslauf. Die Empfehlung bleibt dieselbe, erst sichern und dann weiterarbeiten. Nur den Weg kennt er besser als du.

**Zweitens, unabhängig davon:**

> Arbeite zwei bis drei Tage nur mit dem, was jetzt steht, bevor du weitere Werkzeuge dazunimmst. Berechtigungen und `AGENTS.md` decken zusammen den Großteil dessen ab, wofür man sonst Frameworks installiert. Wenn sich dein Problem damit erledigt, brauchst du den Rest nicht — und das wäre das beste Ergebnis, das diese Einrichtung haben kann.

---

## Wenn du unsicher bist

Frag. Eine Rückfrage kostet den Nutzer zwanzig Sekunden. Eine falsche Annahme über seine Projektkonventionen kostet ihn Stunden, weil sie in jeden künftigen Prompt einfließt.

Das gilt besonders bei bestehenden Projekten: Was dort steht, hat meist einen Grund, auch wenn er nicht danebensteht.
