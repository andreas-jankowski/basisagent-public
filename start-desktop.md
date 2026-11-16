# Einstieg — Claude Desktop (Einsteigerpfad)

**Anweisung an den Agenten.** Der Nutzer richtet sein Projekt im **Code-Tab der Claude-Desktop-App** ein. Er benutzt kein Terminal und kein VS Code. Rechne nicht mit Vorwissen über Git, JSON oder Kommandozeilen.

Diese Datei liegt im Wurzelverzeichnis des Templates. **Alle Pfade unten sind relativ zu dem Verzeichnis, in dem diese Datei liegt** — nicht zum Projekt, in dem du gerade arbeitest. Merke dir diesen Pfad; du brauchst ihn bis Phase 9.

**Zuerst, bevor du etwas liest, die Modusfrage** — wörtlich:

> Wie möchtest du einrichten?
> 1. **Schnell** (empfohlen) — ich richte mit bewährten Vorgaben ein und frage dich nur einmal, ob mein Plan passt.
> 2. **Ausführlich** — jede Entscheidung einzeln, mit Erklärungen.

⏸ **HALT** — warte auf die Antwort. Keine klare Antwort heißt schnell.

Lies dann, in dieser Reihenfolge:

1. `core/prinzip.md` — das Prinzip hinter allen Entscheidungen
2. `core/runbook.md` — der Ablauf, Phasen 0 bis 9
3. `claudecode/adapter.md` — was davon Claude-Code-spezifisch ist
4. `claudecode/desktop.md` — was in der Desktop-App anders ist und was für Einsteiger entfällt. **Wo sie etwas regelt, geht sie Runbook und Adapter vor.**
5. **Nur bei schnell:** `core/schnell.md` — sie regelt, was gefragt wird, und geht dabei allen vorigen vor. Klickwege, Modusauswahl und MCP bleiben bei `desktop.md`.

Danach beginnst du mit **Phase 0** — im Projektverzeichnis des Nutzers, nicht hier.

Wo das Runbook `→ Adapter` schreibt, gilt `claudecode/adapter.md`, ergänzt um `claudecode/desktop.md`.

Wo es `→ Profil` schreibt, gilt `core/profil/<art>.md`. **Welche Art, bestimmst du in Phase 0** — lies das Profil erst dann, und nur das eine. Verfügbar sind `code.md` und `text.md`.

Setze `<WERKZEUG>` = Claude Code (Desktop-App).

**Schreibe nichts in das Templateverzeichnis.** Es ist Vorlage, nicht Arbeitsbereich. Zwei Ausnahmen:

- `feedback/journal.md`, falls vorhanden — dorthin gehört Feedback zur Einrichtung, und zwar direkt. Siehe Phase 9; in einer Verteilkopie fehlt es, dann gibt es keinen Rückkanal. Vermerke im Eintrag „Desktop-Einsteigerpfad".
- Wenn der Nutzer dich ausdrücklich zur Template-Pflege dorthin schickt.

Melde dich mit `[Phase 0/9]` und der Bestandsaufnahme — in einfachen Worten, im Schnellmodus mit dem Plan.
