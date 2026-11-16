# Profil — Codeprojekte

Ergänzt `core/runbook.md`. Gilt für alles, wo das Ergebnis ein lauffähiges Programm ist.

Wo das Runbook `→ Profil` schreibt, gilt der Inhalt von hier. Das Werkzeugverhalten steht weiter im Adapter; die beiden Achsen sind unabhängig.

---

## Phase 0 — zusätzlich ermitteln

- Gibt es bereits Quellcode, oder ist es leer/neu?
- Sprache, Runtime, Paketmanager — aus `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj` o. ä.
- **Test-, Typecheck- und Lint-Befehle** aus den Skripten der Projektdatei. Der wichtigste Befund dieser Phase: Phase 1 gibt sie frei, `AGENTS.md` nennt sie.
- Gesetzte Abhängigkeiten, die nicht durch Alternativen ersetzt werden sollen — soweit ablesbar. Sonst in Phase 2 erfragen.

**Kennzahlenprobe — nur bei Infrastruktur- und Betriebsprojekten.** Frag: *Gibt es Kennzahlen, an denen du den Zustand des Systems abliest?* Gemeint sind zwei oder drei Abfragen, an denen man erkennt, ob etwas läuft oder hängt — Warteschlangenlänge, Indexgröße, Anzahl laufender Prozesse. Sie neu herzuleiten kostet jedes Mal mehr, als sie zu notieren. **Wohin, entscheidet die Menge, nicht die Wiederholung:** Eine Kennzahl über *ein* System nennt der `Rahmen` in einem Satz. Läuft sie über *viele* (Rechner, Arbeitsplätze, Mandanten), wird sie ein Skript, und der `Rahmen` nennt das Skript.

**Belegt an zwei Projekten.** Infrastrukturprojekt A: drei Zählabfragen auf drei benannte Dinge, gemeinsamer Kern vier Zeilen (Journal 2026-08-21, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). Infrastrukturprojekt B: achtzig Arbeitsplätze mal sechs Prüfungen, das wurde ein Skript (Journal 2026-08-26, in `feedback/archiv/journal-0.12.0-0.13.0.md`). Beide Male hat die Frage etwas hergegeben (Punkt 30 in `feedback/offene-punkte.md`). **Melde das Ergebnis weiter nach Phase 9 Schritt 3c**, auch wenn die Frage nichts hergab: Zwei Projekte tragen die Regel, nicht schon ihre Reichweite.

---

## Phase 1 — Berechtigungen

**Die in Phase 0 gefundenen Test-, Typecheck- und Lint-Befehle als erlaubt ergänzen.** Sie laufen häufig und sind harmlos. Ohne diesen Schritt nervt die Einrichtung im Alltag, und genervte Nutzer schalten Berechtigungen ganz ab.

Geheimnisse vom Lesen ausschließen: `.env`, `.env.*`, Schlüsseldateien, `secrets/`.

---

## Phase 2 — Vorlage

Vorlage: **`core/profil/code/AGENTS.md.tpl`**. Lies sie samt Kommentarblock am Ende; der Kommentar wird nicht in die erzeugte Datei übernommen.

Der `Rahmen` ist der Teil mit dem höchsten Ertrag: ohne ihn rät der Agent bei jeder Bibliotheksentscheidung neu.

---

## Phase 3 — Ablaufgerüst

Höchstens eines. **Zwei davon parallel ist der teuerste Fehler der Einrichtung** — doppelte Beschreibungen in jedem Zug und zwei konkurrierende Abläufe, zwischen denen der Agent schwankt.

| | Wofür | Auswahlkriterium |
|---|---|---|
| **OpenSpec** | Vorschlag → Spec-Deltas → Aufgaben, mit Archiv | Wenn Änderungen nachvollziehbar dokumentiert bleiben sollen |
| **`to-spec` + `to-tickets` + `implement`** | Spec → Tickets → Umsetzung | Wenn der Ablauf leichtgewichtiger sein soll und keine Spec-Historie gebraucht wird |
| **keines** | Direkt arbeiten, Berechtigungen als Kontrolle | Kleines Projekt, wenige Beteiligte, überschaubare Änderungen |

**Prüfe die Skill-Namen vor der Installationsanweisung.** Die Liste ändert sich; sieh nach, was tatsächlich angeboten wird.

### Bei OpenSpec

> Führe im Projektverzeichnis aus:
> ```
> npx -y @fission-ai/openspec@latest init .
> ```
> Achte bei den Rückfragen auf drei Dinge:
> - **Profil `core` behalten** (Standard). Erweiterte Workflows nicht freischalten — jedes zusätzliche Kommando kostet dauerhaft Kontext. `core` heißt nicht minimal: In 1.14.2 umfasst es propose, explore, apply, update, sync und archive.
> - **Als Werkzeug Claude Code wählen.** `--tools` nimmt `all`, `none` oder eine kommaseparierte Liste.
> - **Skill-Auslieferung bevorzugen.** Claude Code liest `.claude/skills/`; separate Command-Dateien wären Dubletten. Ab OpenSpec 1.9 steuert das die globale Einstellung `delivery`, ab Werk auf `both`. Prüfen mit `openspec config get delivery`, umstellen mit `openspec config set delivery skills`.
>
> Sag mir Bescheid, wenn es durchgelaufen ist.

**Neben `delivery` ist auch die Workflow-Liste global** (`--scope` kennt in 1.14.2 nur `global`). Sie steuert, was `openspec update` wieder anlegt. Einen OpenSpec-Skill nur zu löschen, ist deshalb nicht dauerhaft. Außerdem aktualisiert `openspec config profile` das Projekt gleich mit: Es erzeugt alle Skills neu und stellt gelöschte wieder her. Belegt durch Journal 2026-10-20, Codeprojekt E, Nr. 3; nicht in der Doku nachgeschlagen.

**Nach der Meldung prüfe:**

- Existiert `openspec/`?
- **Wo erwartet diese Version den Projektkontext?** Ältere Fassungen legen `openspec/project.md` an; ab 1.9 steht er in `openspec/config.yaml` unter dem Schlüssel `context:`. Sieh nach, was tatsächlich da ist, statt einen Dateinamen vorauszusetzen — das ändert sich mit den Versionen.
- Steht in `AGENTS.md` ein verwalteter OpenSpec-Block? Ab 1.9 entfällt er; die Anweisungen kommen über `.claude/skills/openspec-*/`.

Falls ein verwalteter Block existiert: Er trägt Markierungen, damit `openspec update` ihn auffrischen kann. **Er bleibt unangetastet** und zählt nicht gegen das 100-Zeilen-Budget.

→ Adapter, Abschnitt „Phase 3" — dort steht, wo das jeweilige Werkzeug die Kommandos findet.

---

## Phase 4 — Projektkontext

Ort ist das, was Phase 3 ergeben hat: `openspec/project.md` oder der Schlüssel `context:` in `openspec/config.yaml`.

Ohne Gerüst: `docs/projekt.md`, nach Rückfrage.

Ordne den Inhalt sinnvoll — Konventionen, Standards, Architekturmuster. Ergänze, was das Gerüst an Struktur erwartet und noch fehlt.

---

## Phase 5 — Skillkatalog

### Gruppe B — einmalig beim Projektstart

| Skill | Erzeugt | Wann |
|---|---|---|
| **`grill-with-docs`** | `CONTEXT.md` (Glossar), `docs/adr/` | Fachliches Neuland, unklare Begriffe, schwer umkehrbare Entscheidungen stehen an |
| **`domain-modeling`** | Domänenmodell, Fachsprache | Wie oben, aber laufend statt einmalig |

Abgrenzung zum Ablaufgerüst, falls der Nutzer fragt:

| | grill-with-docs | OpenSpec |
|---|---|---|
| Frequenz | Selten | Pro Änderung |
| Erzeugt | Glossar, ADRs | Vorschlag, Specs, Aufgaben |
| Ebene | Fachsprache, schwer umkehrbare Entscheidungen | Anforderungen der konkreten Änderung |

**Nicht beides für dieselbe Aufgabe.** Das wären zwei Interviews hintereinander, und das zweite fördert wenig zutage.

**`grill-with-docs` ist ein Wrapper.** Sein Rumpf ruft `grilling` und `domain-modeling` auf; ohne beide läuft er nicht und zeigt auf Namen, die es nicht gibt. Sie gehören in dieselbe Installationsauswahl — siehe Runbook, Phase 5 Schritt 4. Beachte dabei: `domain-modeling` steht eine Zeile höher als eigener Vorschlag, ist hier aber **Abhängigkeit, nicht Alternative**. Die Tabelle liest sich sonst so, als hätte man die Wahl.

**Dasselbe Muster, schwächer, bei `tdd`:** Er ruft `codebase-design` über das Skill-Werkzeug auf (Journal 2026-10-10, Codeprojekt D, Nr. 7). Wer `tdd` wählt, bekommt die Frage nach `codebase-design` mit dazu. Prüf bei jedem Skill vor der Installationsauswahl, ob sein Rumpf andere Skills aufruft.

Diese Gruppe wird **einmal** gebraucht. Danach steht das Ergebnis in Dateien und der Skill kostet nur noch. Zwei Wege, und der zweite ist meist der bessere:

| Weg | Folge |
|---|---|
| Entfernen | Die erzeugten Dateien bleiben. Beim nächsten Bedarf neu installieren |
| So auszeichnen, dass er nur per `/name` läuft (→ Adapter, Phase 6) | Bleibt verfügbar und wird nicht mehr von selbst vorgeschlagen. Die Beschreibung fällt aus dem Kontext, er kostet nur noch seine Auslöserzeile in der Regeldatei |

### Gruppe C — bedarfsgetrieben

Schlage hieraus nur vor, was zu deinem Phase-0-Befund passt. Die Spalte nennt den Auslöser:

| Skill | Vorschlagen wenn |
|---|---|
| `tdd` | Testframework vorhanden und Tests werden tatsächlich gepflegt |
| `diagnosing-bugs` | Bestehendes Projekt mit Laufzeitverhalten, das man debuggen muss |
| `code-review` | Mehr als eine Person am Projekt, oder PR-Ablauf erkennbar |
| `resolving-merge-conflicts` | Git-Repo mit mehreren aktiven Branches |
| `research` | Projekt hängt an fremden APIs oder Spezifikationen |
| `codebase-design` | Größere bestehende Codebasis, Umbau steht an. Sein Entwurf in zwei Varianten delegiert an parallele Subagenten — bei gesperrten Hilfsagenten (Phase 1, Vorgabe) nur teilweise nutzbar |
| `prototype` | Frühe Phase, Entwurfsfragen offen |

**Kein Auslöser, kein Vorschlag.** „Könnte man mal brauchen" ist kein Auslöser.

---

## Phase 9 — zusätzliche Prüfpunkte

- [ ] Test-, Typecheck- und Lint-Befehle sind freigegeben
- [ ] Der `Rahmen` nennt sie ebenfalls, damit der Agent sie kennt
- [ ] Geheimnisse sind vom Lesen ausgeschlossen
