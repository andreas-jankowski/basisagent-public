# Basisagent

Einrichtungs-Templates für **Claude Code** — im Terminal, in der IDE oder in der Desktop-App. Ein Template richtet ein Projekt so ein, dass der Agent vor Änderungen fragt, wenig Kontext dauerhaft verbraucht und in einem geordneten Ablauf arbeitet.

Funktioniert für neue *und* für bestehende Projekte, für **Code** *und* für **Textprojekte** — Recherche, Gutachten, Bewertung, Security-Analyse. Die Projektart bestimmt der Agent in Phase 0 und fragt sie ab; sie entscheidet über Vorlage, Berechtigungen und Skillkatalog, nicht über den Ablauf.

Aktuelle Version: siehe [VERSION](VERSION) · Lizenz: [MIT](LICENSE)

---

## Holen

Öffentliche Fassung: <https://github.com/andreas-jankowski/basisagent-public>. Klonen oder als ZIP laden, wohin du willst:

```
git clone https://github.com/andreas-jankowski/basisagent-public.git
```

Die Beispiele unten nennen `C:\dev\basisagent-public`. Setz den Pfad ein, unter dem das Template bei dir liegt.

---

## Anwenden

Im **Zielprojekt** eine Claude-Code-Sitzung öffnen und eingeben:

```
Arbeite C:\dev\basisagent-public\start-claudecode.md ab.
```

**Ohne Terminal, in der Claude-Desktop-App:** Code-Tab öffnen, **+ New session**, Umgebung **Local**, als Ordner das Zielprojekt, Modus **Manual**. Dann:

```
Arbeite C:\dev\basisagent-public\start-desktop.md ab.
```

Das ist der Einsteigerpfad: derselbe Ablauf, aber ohne Ablaufgerüst und ohne Skill-Installation per Terminal. Wo etwas zu löschen ist, sagt der Agent, was du im Explorer löschen sollst. Einzelheiten: [claudecode/desktop.md](claudecode/desktop.md).

Der Pfad ist der einzige Ort, an dem er vorkommt — die Dateien untereinander verweisen relativ. Wer das Template woanders hinlegt, ändert nur den Satz, den er eintippt.

**Zuerst fragt der Agent nach dem Modus** — in beiden Wegen, Terminal und Desktop:

- **Schnell** (empfohlen): Der Agent richtet mit Vorgaben ein, zeigt dir **einmal** einen Plan und fragt, ob er passt. Danach nur noch Neustart und Probe. Für alle, die nicht jede Einzelheit entscheiden wollen. Einzelheiten: [core/schnell.md](core/schnell.md).
- **Ausführlich:** neun Phasen mit Haltepunkten, jede Entscheidung einzeln — der Ablauf unten.

Wer im Schnellmodus doch einzeln entscheiden will, sagt beim Plan „ausführlich".

### Was dich erwartet — ausführlich

| Phase | Was passiert | Wer handelt |
|---|---|---|
| 0 | Projektart bestimmen, Bestandsaufnahme, nichts wird geändert | Agent, dann eine Frage |
| 1 | Berechtigungen — größter Effekt, wirkt aber erst nach einem Neustart | Agent, nach Freigabe |
| 2 | `AGENTS.md` und die Regeldatei des Werkzeugs. Bei bestehenden Projekten: Altdateien Block für Block | Agent, viele Rückfragen |
| 3 | Ablaufgerüst — optional, höchstens eines | **du** installierst |
| 4 | Projektkontext füllen, Altdateien aufräumen | Agent, Einzelentscheidungen |
| 5 | Skill-Auswahl aus dem Katalog der Projektart | Agent schlägt vor, **du** installierst |
| 6 | Skills und MCP-Server aufräumen | Agent, Einzelentscheidungen |
| 7 | entfällt seit 0.27.0 (war: Zweitwerkzeug anbinden) | — |
| 8 | Rollentrennung — optional | Agent |
| 9 | Prüfliste, Versionsstempel, **Neustart und Wirkungsprobe** | Agent, dann du |

**Nichts wird ohne deine Zustimmung geschrieben oder gelöscht.** An jedem `⏸ HALT` endet der Zug des Agenten und er wartet.

**Phase 9 endet mit einem Neustart.** Das ist kein Beiwerk: Werkzeuge lesen ihre Berechtigungen beim Sitzungsstart, also gilt alles aus Phase 1 erst danach. Bis zum Neustart bist du nicht geschützt — und die Wirkungsprobe direkt danach ist die einzige Stelle, an der sich das überhaupt prüfen lässt.

Dauer, ausführlich: leeres Projekt etwa zwanzig Minuten. Bestehendes Projekt mit Altdateien eher eine Stunde — Phase 2b geht deine vorhandenen Anweisungsdateien einzeln durch.

### Abbrechen und fortsetzen

Denselben Satz erneut eingeben. Das Runbook hat eine Wiederaufnahmetabelle: Der Agent erkennt an den vorhandenen Dateien, wo er wieder einsteigt, und sagt es dir.

### Berechtigungsabfragen beim Lesen

Der Agent liest aus einem Verzeichnis außerhalb deines Projekts. Claude Code fragt deshalb nach — einmal pro Datei, also etwa vier Mal. Wer das dauerhaft loswerden will, trägt in `.claude/settings.json` des **Zielprojekts** ein:

```json
"permissions": { "additionalDirectories": ["C:\\dev\\basisagent-public"] }
```

---

## Du kopierst nichts

Das ist die häufigste Verwirrung, deshalb deutlich: **Es gibt keine Dateien, die du von Hand in dein Projekt kopierst. Keine einzige.**

Das Basisagent-Verzeichnis wird nur *gelesen*. Der Agent schreibt die Dateien selbst — und er kann sie nicht kopieren, weil die Vorlagen Platzhalter enthalten (`<Projektname>`, `<TEST-BEFEHL>`, `<LINT-BEFEHL>`). Eine kopierte `settings.json.tpl` wäre in deinem Projekt wertlos. Sie muss mit deinen Befehlen gefüllt werden, und genau dafür stellt dir der Agent in Phase 0 und 1 seine Fragen.

### Konkretes Beispiel

Dein Projekt liegt in `d:\Projekte\MeinNeuesProjekt`.

1. Claude Code **in deinem Projekt** öffnen — nicht im Basisagent.
2. Diesen Satz eintippen:
   ```
   Arbeite C:\dev\basisagent-public\start-claudecode.md ab.
   ```
3. Fragen beantworten.

Das war der ganze Vorgang. Kein Kopieren, kein Skript, keine Installation.

### Was danach in deinem Projekt steht

| Datei | Entsteht in Phase | Wie |
|---|---|---|
| `.claude/settings.json` | 1 | vom Agenten geschrieben, mit deinen Befehlen |
| `.claude/agents/recherche.md`, `recherche-gross.md` | 1 | nach deiner Wahl des Recherchebudgets — oder keine, wenn du „unbegrenzt" wählst |
| `AGENTS.md` | 2 | vom Agenten geschrieben, mit deinem Rahmen |
| `CLAUDE.md` | 2 | vom Agenten geschrieben — bindet `AGENTS.md` per Import ein |
| `.agent-template-version` | 2 | vom Agenten geschrieben, in Phase 9 fortgeschrieben |
| Projektkontext (`projekt.md` o. ä.) | 4 | vom Agenten geschrieben, Ort wird erfragt |
| `quellen.md` — nur Textprojekte | 4 | vom Agenten angelegt, falls du willst |
| `.claude/skills/uebergabe/` | 5 | gesetzt — kostet nichts, bis du `/uebergabe` tippst |
| `uebergabe/` mit `_vorlage.md` | 5 | von `/uebergabe einrichten` angelegt |
| `.claude/skills/template-feedback/` | 9 | nur bei Einrichtung aus der Entwicklungskopie, wenn deren Journal nicht erreichbar ist. Verteilkopien haben keinen Rückkanal |
| Ablaufgerüst, weitere Skills | 3 und 5 | **du** installierst, der Agent gibt dir den Befehl |

Danach hat dein Projekt **keine Verbindung** zum Basisagent. Du kannst das Template verschieben, umbenennen oder löschen — dein eingerichtetes Projekt läuft weiter.

---

## Aufbau

```
start-claudecode.md        Einstieg Claude Code   ─┐
start-desktop.md           Einstieg Desktop-App   ─┴─ dünn, fragen den Modus, verweisen

core/                      werkzeug- und artneutral
  prinzip.md               Warum alles so ist, wie es ist
  runbook.md               Phasen 0–9, der eigentliche Ablauf
  schnell.md               Schnellmodus: Vorgaben statt Rückfragen, legt sich übers Runbook
  verworfen.md             Warum etwas nicht drin ist
  skills/
    template-feedback/     Skill: erfassen, bewerten, einsammeln
                           (nur Entwicklungskopie)
    uebergabe/             Skill: Aufgabenstand sichern, dann /clear
                           SKILL.md + ADDON.md (Weg ohne Basisagent)

  profil/                  Achse Projektart — in Phase 0 bestimmt
    code.md                Was für Codeprojekte gilt
    code/AGENTS.md.tpl
    text.md                Was für Textprojekte gilt
    text/AGENTS.md.tpl

claudecode/                Adapter Claude Code — Achse Werkzeug
  adapter.md               Was in welcher Phase Claude-Code-spezifisch gilt
  desktop.md               Ergänzung Desktop-App, Einsteigerpfad
  CLAUDE.md.tpl
  settings.json.tpl
  agents/                  Rechercheagenten, Budget erfragt in Phase 1
  hooks/kennungen.ps1      Hook: Kennungen im Bestand suchen, Muster in Phase 1
```

Verweise auf `feedback/…` und auf Journaleinträge in den Dateien zeigen in die Entwicklungskopie. Sie belegen, woher eine Regel kommt; für die Anwendung brauchst du sie nicht.

**Zwei Achsen, eine Regel.** Der Adapter sagt, *wie* ein Werkzeug etwas tut. Das Profil sagt, *was* für eine Projektart überhaupt zu tun ist. Beide enthalten nur, was ohne sie sinnlos wäre. Alles, was für alle gilt, steht genau einmal in `core/` — wenn ein Adapter oder ein Profil anfängt, allgemeine Regeln zu formulieren, gehören die ins Runbook.

Die Achsen sind unabhängig: Ein Textprojekt kombiniert `profil/text.md` mit `claudecode/adapter.md`, ohne dass eine der beiden Dateien von der anderen weiß. Ein weiteres Werkzeug bekäme einen eigenen Adapter; der OpenCode-Adapter ist seit 0.27.0 stillgelegt (`core/verworfen.md`).

---

## Warum etwas *nicht* drin ist

[core/verworfen.md](core/verworfen.md) hält die Negativentscheidungen fest — karpathy, ponytail, oh-my-openagent, GSD Core, edit-guard, LSP, OpenCode als Zweitwerkzeug. Jede mit Begründung und **Revisionsbedingung**: dem beobachtbaren Umstand, unter dem sie neu zu treffen wäre.

Die Datei wird nie geladen. Sie existiert, damit dieselbe Frage nicht in sechs Monaten erneut recherchiert wird.
