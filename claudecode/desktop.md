# Ergänzung — Claude Desktop, Einsteigerpfad

Gilt **zusätzlich** zu `claudecode/adapter.md`, nicht statt seiner. Wo beide
dasselbe regeln, gilt diese Datei. Eingelesen nur über `start-desktop.md`.

**Für wen:** Nutzer, die im Code-Tab der Claude-Desktop-App arbeiten, kein
Terminal benutzen und VS Code zu kompliziert finden (Nutzerentscheidung vom
2026-10-07). Daraus folgt alles Weitere: keine Befehle zum Selbstausführen,
Klickwege statt Tastenkürzel aus dem Terminal, weniger Fragen, Fachbegriffe
in einem Halbsatz erklären oder weglassen.

---

## Was gleich bleibt

Der Code-Tab ist laut Hersteller dieselbe Claude-Code-Engine wie die CLI und
liest dieselben Dateien: `CLAUDE.md`, `.claude/settings.json` mit allen
Berechtigungsregeln, Skills, Hooks, `.mcp.json`. Wörtlich: *„Permission rules,
allowed tools, and other settings in `settings.json` apply to Desktop
sessions."* Quelle: `code.claude.com/docs/en/desktop`, „Coming from the CLI?",
abgerufen 07.10.2026.

Damit gelten das Runbook, die Verhaltensregeln und die Vorlage
`claudecode/settings.json.tpl` unverändert. Diese Datei ändert nur, **was
angeboten** und **wie es dem Nutzer gesagt** wird.

---

## Einsteigermodus — was entfällt

Entfällt heißt: nicht anbieten, nicht erklären. Fragt der Nutzer ausdrücklich
danach, läuft die Phase wie im Runbook.

| Phase | Im Einsteigerpfad |
|---|---|
| 0 | Wie im Runbook. Die Git-Frage einmal, neutral; weiß er es nicht, ohne Git |
| 1 | **Globale Datei nicht auswerten** — mit einer Ausnahme, siehe unten. Die Frage nach Hilfsagenten bleibt, in einfachen Worten: „Darf ich Arbeit an Hilfsagenten abgeben? Das dauert meist länger und kostet mehr. Vorgabe: nein." Nur bei Ja die Budgetfrage: „Wie lange und auf welchem Modell darf ein Hilfsagent für dich recherchieren?" |
| 3 | **Entfällt.** Ein Ablaufgerüst braucht npm im Terminal. Ablageort für Kategorie B erfragen, wie das Runbook es für „Nein" vorsieht |
| 5 | **Nur Schritt 0** (`uebergabe` kopieren — das machst du selbst, ohne Terminal). Schritte 1 bis 4 entfallen; ein Satz genügt: „Weitere Skills gibt es, wir können sie später dazunehmen." |
| 6 | Läuft, aber MCP anders — siehe unten |
| 7, 8 | **Entfallen.** Plan-Modus steckt in der Modusauswahl der App |
| 9 | Läuft vollständig, Schritt 5 mit den Abweichungen unten |

**Die Ausnahme in Phase 1:** Sieh in `~/.claude/settings.json` nur nach
Interpreter-Freigaben (`python -c`, `node -e`, `pwsh -Command` und Verwandte,
→ Adapter, Falle 7). Findest du keine, sag nichts. Findest du eine, melde sie
in zwei Sätzen — sie hebt jede Sperre auf, die du gleich schreibst. Die beiden
anderen Klassen (widersprechende Freigaben, tote Regeln) übergehst du.

---

## Löschen: Explorer statt Befehl

Verhaltensregel 8 bleibt: Nach Phase 1 löschst du nicht. Statt einen Befehl zu
nennen, beschreibst du den Klickweg:

> Bitte lösch `<Dateiname>` im Explorer: Ordner `<voller Pfad>` öffnen, Datei
> markieren, Entf.

Du darfst anbieten, den Ordner mit markierter Datei zu öffnen
(`explorer.exe /select,"<voller Pfad>"`) — das ist kein Löschen, und der
Nutzer bestätigt den Aufruf. Bei mehreren Dateien: eine Liste, ein Klickweg.

**Sag dazu, wenn das Projekt auf einem Netzlaufwerk liegt:** Dort landet eine
gelöschte Datei in der Windows-Voreinstellung nicht im Papierkorb, sie ist weg
(hier nicht gemessen). Auf einem lokalen Laufwerk
lässt sie sich aus dem Papierkorb zurückholen.

---

## MCP-Server und Konnektoren

**Eine Quelle mehr als in der CLI.** Der Code-Tab lädt zusätzlich die Server
aus `claude_desktop_config.json`, der Konfiguration des Chat-Tabs (Quelle wie
oben, „MCP servers from the Claude Desktop chat app"). Nimm die Datei in die
Bestandsaufnahme von Phase 0 auf. Ihren Ort nennt die Doku nicht; unter
Windows liegt sie üblicherweise in `%APPDATA%\Claude\` — **ungeprüft**, also
nachsehen statt behaupten.

**Konnektoren** (Google Calendar, Slack, GitHub …) verwaltet der Nutzer in der
App: Einstellungen → Connectors, oder im Eingabefeld **+** → Connectors →
Manage connectors. Das ist der Klickweg, den du in Phase 6 nennst.
`disableClaudeAiConnectors` wirkt hier nicht: Die App liefert die Konnektoren
selbst aus, *„no MCP setting or `managed-mcp.json` reaches them"*
(`code.claude.com/docs/en/mcp`, abgerufen 07.10.2026). Ob eine `deny`-Regel
auf `mcp__<server>__*` sie erfasst, ist **ungeprüft**.

**Server aus Dateien** (`.mcp.json`, `~/.claude.json`,
`claude_desktop_config.json`): `claude mcp remove` setzt ein Terminal voraus,
und ob der Befehl ohne CLI-Installation überhaupt auf dem Pfad liegt, ist
ungeprüft. Zeig stattdessen den Eintrag. Ändern darfst du die Datei nur nach
ausdrücklichem Ja und mit Sicherungskopie daneben; bei einer globalen Datei
sag dazu, dass die Änderung **alle** Projekte trifft.

---

## Modusauswahl überstimmt `defaultMode`

*„A mode you pick in the selector is remembered per folder and takes
precedence over `defaultMode` for that folder, except Plan, which applies to
the current session only."* (Quelle wie oben, „Choose a permission mode".)

Die Vorlage setzt `defaultMode: "default"`; in der App heißt dieser Modus
**Manual**. Hat der Nutzer im Ordner einmal etwas anderes gewählt, gilt das
weiter, egal was in der Datei steht. Sag ihm in Phase 1:

> Unten neben dem Senden-Knopf steht der Modus. Für die Einrichtung und danach
> sollte dort **Manual** stehen — dann fragt Claude vor jeder Änderung.

`dontAsk` gibt es in der App nicht. Befehle, die in der CLI ein Dialogfenster
öffnen (`/permissions`), antworten mit *„isn't available in this
environment"* — für die Einrichtung egal, sie schreibt die Datei direkt.

---

## Phase 9 — was anders läuft

**Neustart heißt neue Sitzung.** Sag dem Nutzer:

> Starte eine neue Sitzung: links **+ New session** (oder Strg+N), Umgebung
> **Local**, derselbe Projektordner, Modus **Manual**. Schreib dort „Weiter
> mit der Wirkungsprobe aus Phase 9".

Ob eine neue Sitzung die Berechtigungen frisch liest, sagt die Doku nicht
ausdrücklich — die Wirkungsprobe zeigt es. Fällt sie durch, ist das der erste
Verdacht, vor jedem anderen.

**Vor der Probe den Modus erfragen.** Steht dort nicht Manual, ist die Probe
wertlos: Im Auto-Modus genehmigt Claude Code ohnehin, und „schreibend läuft
durch" belegt nichts (Journal 2026-09-28, Codeprojekt C, Nr. 10, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). Erst
umstellen lassen, dann prüfen.

**Bash-Zeile der Probe.** Fehlt der Sitzung das Bash-Werkzeug — etwa weil kein
Git für Windows installiert ist —, entfällt die vierte Zeile. Melde das so,
nicht als bestanden.

**Kommt die Regeldatei an?** Der Adapter nennt `/context`. Ob der Befehl im
Code-Tab den Abschnitt *Memory files* zeigt, ist **ungeprüft**; die App hat
für den Kontext sonst nur den Nutzungsring neben der Modellauswahl, der keine
Dateien nennt. Bitte den Nutzer, `/context` zu tippen. Antwortet die App mit
„isn't available", zitiere eine unverwechselbare Zeile aus dem `Rahmen` von
`AGENTS.md` **ohne** die Datei zu lesen — der Nutzer sieht im Verlauf, dass
kein Lesevorgang lief. Das ist ein Ersatzweg, kein gleichwertiger Beleg; nenn
ihn so.

**Aufwandstufe:** In der App über das Effort-Menü, Strg+Umschalt+E unter
Windows (Doku: Cmd+Shift+E, „On Windows, use Ctrl in place of Cmd"). Sonst
gilt der Abschnitt im Adapter.

**Alltagsablauf, angepasst:**

- Plan-Modus: in der Modusauswahl **Plan** wählen (Strg+Umschalt+M). Shift+Tab
  aus dem Terminal gilt in der App nicht.
- `/uebergabe` tippt der Nutzer wie in der CLI ins Eingabefeld; Skills und
  Befehle erscheinen nach `/`.
- Danach `/clear` — oder eine neue Sitzung im selben Ordner. Beides beginnt
  mit leerem Kontext.
- Große Recherche: „nimm die große Recherche" schreiben. Ob die
  `@`-Auswahl der App auch Agenten anbietet, ist ungeprüft — die Doku nennt
  dort nur Dateien.

---

## Nicht für Cloud-Sitzungen

Die Einrichtung läuft nur in einer Sitzung mit Umgebung **Local**. Eine
Cloud-Sitzung läuft auf Rechnern des Herstellers, erreicht das
Templateverzeichnis auf der eigenen Platte also nicht, und lädt
`~/.claude/skills/` nicht (Quelle wie oben, „Use skills"). Steht die
Umgebung nicht auf Local, sag es, bevor du mit Phase 0 beginnst.
