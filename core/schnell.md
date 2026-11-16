# Schnellmodus

Gilt **zusätzlich** zu Runbook, Adapter, Profil und — im Desktop-Pfad —
`claudecode/desktop.md`. Wo diese Datei etwas regelt, geht sie allen vor,
außer bei den Punkten unter „Was nie entfällt". Eingelesen nur, wenn der
Nutzer in der Modusfrage der Startdatei „schnell" gewählt hat.

**Für wen:** Kollegen, die mit Einzelentscheidungen über Berechtigungen,
Skills und Gerüste nichts anfangen können und denen der ausführliche Ablauf
zu lange dauert (Nutzerentscheidung vom 2026-10-22).

**Grundsatz: Vorgabe statt Frage.** Wo das Runbook fragt, entscheidest du
mit der Vorgabe unten und nennst die Entscheidung im Plan. Der Nutzer
korrigiert, was ihm nicht passt. Er muss keine der Fragen kennen.

**Ungemessen:** ob das die Einrichtung tatsächlich verkürzt. Deshalb die
Zusatzangaben im Journaleintrag (Phase 9), siehe `feedback/offene-punkte.md`,
Punkt 50.

---

## Was nie entfällt

- **Phase 1 vollständig geschrieben**, mit den Sperren aus Vorlage und Profil.
- **Neustart und Wirkungsprobe** (Phase 9 Schritt 5) und die Zeile `phase9:`.
- **Verhaltensregeln 6, 7 und 8.** Nicht raten, nicht mitarbeiten, nach
  Phase 1 nicht löschen. Im Schnellmodus gibt es nichts zu löschen:
  Altdateien bleiben liegen.
- **Interpreter-Freigaben in `~/.claude/settings.json` melden**, wie in
  `claudecode/desktop.md`, „Die Ausnahme in Phase 1". Die übrigen Klassen der
  globalen Datei übergehst du.
- **Der Journaleintrag aus Phase 9 Schritt 3c** — außer in einer
  Verteilkopie ohne Rückkanal (Phase 9 Schritt 1).

---

## Haltepunkte

Die `⏸ HALT` im Runbook gelten nicht. Du hältst nur hier:

1. **Plan** — am Ende von Phase 0. Die einzige inhaltliche Frage.
2. **Neustart** — Phase 9 Schritt 5.
3. **Ergebnis der Wirkungsprobe** — danach ist Schluss.

Dazu nur, wenn der Fall eintritt: Projektart nicht bestimmbar (Runbook
Phase 0 Schritt 1), Arbeitsverzeichnis leer (nach dem Ort fragen, ebenda).

**Verhaltensregel 3 ersetzt der Plan.** Neue Dateien zeigst du nicht im
Gespräch — Claude Code zeigt jede Änderung im Bestätigungsdialog. Was eine
**bestehende** Datei verliert oder gewinnt, steht im Plan.

**Sprache:** kurze Sätze, keine Fachbegriffe, die der Nutzer nicht braucht.
Die Phasenmarke `[Phase n/9]` bleibt.

---

## Phase 0 — Bestandsaufnahme wie im Runbook, dann der Plan

| Runbook fragt | Im Schnellmodus |
|---|---|
| Projektart bestätigen, neu/bestehend | im Plan nennen |
| Text: Ausprägung | raten, im Plan nennen |
| Externer Bestand: bleibt draußen oder wandert ein? | **bleibt draußen** (Lesen ja, Ändern nie, → Adapter) — im Plan nennen |
| Kein Git-Repo: versionieren? | nicht fragen, ohne Git weiter |
| Arbeitsbaum unsauber | im Plan: „Bevor du Ja sagst, committe bitte den aktuellen Stand." |
| Code: Kennzahlenprobe | entfällt — im Journal „nicht gefragt (Schnellmodus)" |
| Sammlungsprojekt: wo startet die Sitzung? | Wurzelordner — im Plan nennen |

**Lücken.** Was du für Phase 1 und 2 brauchst und nicht ablesen kannst —
Testbefehl, beim Textprofil `Sachstand zum` und `Adressat`, bei Entwurf und
Endfassung nebeneinander die gültige — kommt als Lücke in den Plan, mit
Vorschlag wo möglich. **Höchstens drei.** Was darüber hinaus fehlt, lässt du
in `AGENTS.md` weg statt es zu raten, und nennst es am Ende als offenen
Punkt. Ein weggelassenes Feld ist ehrlich, ein geratenes wirkt in jedem Zug.

**Vorhandene Anweisungsdateien** (`CLAUDE.md`, `.cursorrules` …): Klassifiziere
wie in Phase 2b, Schritt 2, und zeig das Ergebnis als **eine** kurze Tabelle
im Plan — Datei, Inhalt in Stichworten, wohin. Dabei:

- **A** → `AGENTS.md`, **B** → Projektkontext.
- **C** (veraltet) wird nicht übernommen und nicht gelöscht — die Altdatei
  bleibt liegen.
- **D** (unklar) → Projektkontext unter „Ungeklärt aus `<Datei>`".

### Vorlage für den Plan

```
[Phase 0/9] So würde ich dein Projekt einrichten:

Projekt:   <bestehendes Codeprojekt, Node/npm | neues Textprojekt (Gutachten) …>
Schutz:    Claude fragt vor jeder Änderung. Gesperrt: Löschen, <…>.
           Ohne Rückfrage erlaubt: <Testbefehl …>
Regeln:    AGENTS.md, eingebunden über CLAUDE.md
Projektbeschreibung: <Ort aus dem Profil>
Dazu:      /uebergabe — sichert deinen Arbeitsstand, kostet nichts,
           bis du es tippst
Später möglich: weitere Skills, Ablaufgerüst, Hilfsagenten

<nur wenn vorhanden: Tabelle Altdateien>
<nur wenn vorhanden: Lücken, je eine Zeile mit Vorschlag>

Passt das? Ein „ja" genügt, Änderungen sag einfach dazu.
Danach klickst du ein paar Mal „Erlauben" — Claude lässt dich jede neue
Datei bestätigen.
```

Im Desktop-Pfad kommt eine Zeile dazu: „Unten neben dem Senden-Knopf sollte
**Manual** stehen."

⏸ **HALT** — warte auf die Antwort.

**Bei „ja" oder kleinen Änderungen:** einarbeiten und ohne weiteren Halt bis
Phase 9 Schritt 5 durchlaufen. **Bei „ausführlich"** oder wenn der Nutzer
einzeln entscheiden will: ab hier das Runbook ohne diese Datei — die
Bestandsaufnahme ist ja gemacht.

---

## Phase 1 bis 8 — Vorgaben

**Phase 1:**
- Vorlage und Profil wie beschrieben. Eine Datei `settings.json`, keine
  Aufteilung in eine persönliche Datei.
- **Hilfsagenten gesperrt** (Vorgabe der Vorlage), keine Frage, keine
  Budgetfrage.
- Textprofil, sensible Orte: Zugangsdaten und Schlüssel vom Lesen
  ausschließen; Fallakten und Ähnliches bleiben lesbar — sie sind
  Arbeitsmaterial, und die Web-Suche fragt (Profil, Sperre 1). Im Plan nennen.
- Hook für Kennungen: `$muster` nur mit Formen, die du in Phase 0 im Bestand
  gesehen hast, sonst leer lassen; keine Frage nach dem Namensschema.
- Bestehende `settings.json`: ergänzen, nichts entfernen.

**Phase 2:**
- `AGENTS.md` plus `CLAUDE.md` mit Import. Die Frage „nur `CLAUDE.md`?" aus
  dem Adapter entfällt.
- Kategorie B schreibst du direkt an den Ort des Projektkontexts — **kein
  `.setup-parkplatz.md`**, der Ort steht durch die Vorgabe zu Phase 4 schon
  fest.
- **Ohne Git** sicherst du eine bestehende `CLAUDE.md` oder `AGENTS.md`
  vor dem Ersetzen unverändert als `CLAUDE.vor-einrichtung.md` bzw.
  `AGENTS.vor-einrichtung.md` daneben. Klassifikation C geht sonst
  unwiederbringlich verloren. Mit Git trägt der Commit vor dem Ja.

**Phase 3 entfällt.** Ein schon installiertes Gerüst bleibt, wie es ist; den
Projektkontext legst du dann dort ab, wo das Profil es für dieses Gerüst
nennt.

**Phase 4:** Ort ohne Rückfrage nach Profilvorgabe — Code `docs/projekt.md`,
Text `projekt.md` neben den Dokumenten. Dopplungen löst du nach der
Klassifikation auf, ohne zu fragen. Altdateien bleiben. Textprofil:
`quellen.md` als Struktur anlegen, nicht füllen; `Verbindliche Quellen`
verweist darauf (Profil, „Wenn der Bestand neu, fremd und ungesichtet ist").

**Phase 5:** nur Schritt 0, `uebergabe`.

**Phase 6:** kein Gespräch. Die Zahlen für Phase 9 Schritt 3b erhebst du
trotzdem. Auffälligkeiten — tote Skills, teure Plugins, MCP-Server ohne
Auslöser — nennst du am Ende als offene Punkte, höchstens drei, je ein Satz.

**Phase 8 entfällt.** Der Plan-Modus kommt am Ende in einem Satz vor.

---

## Phase 9

- **Schritt 1 bis 3:** wie im Runbook, aber still. Melde nur, was **nicht**
  erfüllt ist.
- **Schritt 3b:** eine Zeile — Zeichen der Regeldatei, Zeichen der
  Skill-Beschreibungen.
- **Schritt 3c:** der Eintrag wie im Runbook, dazu zwei Angaben:
  **Modus: schnell** und die **Zahl der Nutzerantworten** bis hierher — mit
  dem, was er am Plan geändert hat. Die Dauer liest das Template später aus
  dem Sitzungsprotokoll; frag nicht danach und miss sie nicht per Befehl,
  jeder Befehl vor dem Neustart kann eine Berechtigungsabfrage auslösen.
- **Schritt 4**, kurz statt Tabelle:

  ```
  Fertig eingerichtet: <drei bis fünf Zeilen, was jetzt gilt>

  Gut zu wissen:
  - Erst planen lassen: <Shift+Tab | Modusauswahl „Plan">
  - Arbeitsstand sichern: /uebergabe, danach /clear
  - Denktiefe: <Aufwandstufe, ein Satz mit Vorschlag>

  Offen: <Lücken, Auffälligkeiten aus Phase 6 — oder „nichts">
  ```

  Hilfsagenten, Skills und Gerüst nennst du nicht noch einmal — sie stehen im
  Plan unter „Später möglich".

- **Schritt 5** unverändert, in einfachen Worten. Die vier Aufrufe sind
  Pflicht; erklären musst du sie nicht, nur das Ergebnis.

---

## Wiederaufnahme

Die Tabelle im Runbook gilt. Ist aus dem Verlauf nicht erkennbar, welcher
Modus lief, frag einmal. Existiert `AGENTS.md`, war der Plan bestätigt.
