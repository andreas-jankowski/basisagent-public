# Adapter — Claude Code

Ergänzt `core/runbook.md`. Nur was ohne Claude Code sinnlos wäre.

---

## Phase 0 — zusätzlich prüfen

- Existiert `CLAUDE.md` im Projektwurzelverzeichnis? Existiert `CLAUDE.local.md`?
- Existiert `.claude/`? Was liegt darin — `settings.json`, `settings.local.json`, `skills/`, `agents/`, `commands/`, `hooks/`?
- Existiert `~/.claude/settings.json` und `~/.claude/CLAUDE.md`? Deren Werte gelten mit; projektlokale gehen vor. **Unter Windows löst du `~` über `USERPROFILE` auf, nicht über `HOME`:** Im Bash-Werkzeug kann `HOME` auf ein Netzlaufwerk zeigen, dann ist `~/.claude` dort leer, und die Prüfung meldet „nichts global" (Journal 2026-09-28, Codeprojekt C, Nr. 6, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`).
- Sind MCP-Server konfiguriert — `.mcp.json` im Projekt oder global? Jeder bringt seine Werkzeugschemata in jeden Zug.

---

## Phase 1 — Berechtigungen

Zieldatei: **`.claude/settings.json`**. Vorlage: `claudecode/settings.json.tpl`.

**Was du dem Nutzer sagst:** Claude Code fragt bei Dateiänderungen **bereits von sich aus**, solange `defaultMode` auf `"default"` steht. Es gibt kein `"edit": "ask"` zu setzen — es ist der Ausgangszustand. Auch Lesen und Suchen im Arbeitsverzeichnis fragt nie, und für eine eingebaute Menge lesender Bash-Befehle gilt dasselbe.

Daraus folgt: **Die Arbeit in dieser Phase ist klein.** Sie besteht aus dem Freigeben der projekteigenen Test-, Typecheck- und Lint-Befehle und dem harten Sperren von Destruktivem und Geheimnissen. Baue keine Regelwand, die nur wiederholt, was ohnehin gilt.

**Web-Suche ist frei, Web-Abruf fragt** (Nutzerentscheidung vom 2026-10-12). Ohne Regel fragt Claude Code bei beiden (`code.claude.com/docs/en/permissions`, Tabelle „Permission system", abgerufen 12.10.2026); die Vorlage gibt deshalb `WebSearch` in `allow` frei und hält `WebFetch` in `ask`, damit eine globale Freigabe es nicht still öffnet. **Textprofil:** `WebSearch` von `allow` nach `ask` verschieben (→ Profil, Sperre 1).

### Regelformat

`Werkzeug(Spezifikation)`. Für die Praxis reichen drei Bauformen:

```
"Bash(npm run test *)"    Präfix — alles, was mit `npm run test` beginnt
"Edit(src/**)"            Pfad, gitignore-Syntax, relativ zum Arbeitsverzeichnis
"Read(.env)"              blanker Dateiname — greift in jeder Tiefe
```

Acht Dinge, an denen man sich schneidet — die ersten sechs betreffen einzelne Regeln, die letzten zwei das ganze Regelwerk:

1. **Der Stern braucht ein Leerzeichen vor sich.** `Bash(ls *)` matcht `ls -la`, aber nicht `lsof`. `Bash(ls*)` ohne Leerzeichen matcht beides — fast nie gewollt. Die Kurzform `Bash(ls:*)` ist gleichbedeutend mit `Bash(ls *)`, aber nur am Ende eines Musters; mittendrin ist der Doppelpunkt ein normales Zeichen.
2. **`Bash(*)` ist dasselbe wie `Bash`** — als `deny` nimmt das dem Agenten das Werkzeug komplett aus dem Kontext. Nie als Auffangregel schreiben. Die Denkweise „`*` auf ask, dann Ausnahmen" funktioniert hier nicht.
3. **Reihenfolge ist egal, Strenge gewinnt:** erst `deny`, dann `ask`, dann `allow`, erster Treffer entscheidet. Ein breites `deny` lässt sich durch ein enges `allow` **nicht** aufweichen — `Bash(aws *)` in deny blockiert auch bei `Bash(aws s3 ls)` in allow. Ausnahmen von einer Sperre gibt es nicht; entsprechend eng formulieren.
4. **Pfadregeln greifen nur bei `Read` und `Edit`.** `Write(...)`, `Glob(...)`, `NotebookEdit(...)` mit Pfad werden angenommen, aber nie geprüft — mit Startwarnung. Schreib `Edit(docs/**)` statt `Write(docs/**)`.
   **Die schwerere Folge: Shell-Befehle unterliegen überhaupt keiner Pfadregel.** `Edit(//p/**)` in `deny` schützt einen Bestand gegen Editieren — `mv`, `cp`, `Move-Item` und `Copy-Item` laufen trotzdem durch, weil sie über Bash oder PowerShell gehen und dort nur der Befehlsname geprüft wird. Der Bestand ist dann gegen Verändern gesperrt und gegen Verschieben offen, und in der Berechtigungsdatei **sieht das wie vollständiger Schutz aus**, weil dort eine `deny`-Zeile mit dem richtigen Pfad steht. Wer einen Pfad wirklich schützen will, braucht beides: die Pfadregel *und* die Befehlssperren. Siehe „Externer Quellbestand".
   **Gegenbefund, zugunsten der Sicherheit:** `Test-Path .env` über das PowerShell-Werkzeug wurde **abgelehnt**, obwohl `Read(.env)` eine Pfadregel ist und PowerShell ein Shell-Werkzeug. Dateipfade in Shell-Argumenten werden also mitgeprüft, jedenfalls bei `Read`-gesperrten Dateien. **Verlass dich nicht darauf** — für `mv` und `cp` gilt der Absatz darüber unverändert, und das ist der wichtigere Fall. Die Aussage „keine Pfadregel" ist nur nicht ausnahmslos.
   **Die Fehlermeldung nennt dabei den falschen Grund**, und das ist die teurere Hälfte: Gemeldet wurde, der Zugriff sei blockiert, weil nur Dateien in den erlaubten Arbeitsverzeichnissen zugänglich seien — mitsamt Auflistung des Verzeichnisses, in dem die Datei liegt. Ursache war die `deny`-Regel. **Eine Ablehnung mit Verweis auf Arbeitsverzeichnisse kann eine `deny`-Regel sein.** Sieh in die Sperrliste, bevor du an `additionalDirectories` schraubst — sonst weichst du eine Regel auf, um ein Problem zu lösen, das keines ist, oder hältst die Datei für nicht vorhanden.
5. **Tiefe hängt vom Regeltyp ab.** `Edit(src/**)` als `allow` greift nur in `<cwd>/src`; dasselbe Muster als `deny` oder `ask` greift auf jedes `src` in jeder Tiefe. Für „überall" im allow: `Edit(**/src/**)`.
6. **Verkettung ist abgedeckt.** Claude Code kennt `&&`, `||`, `;`, `|`, `&` und Zeilenumbrüche; jeder Teilbefehl muss einzeln passen. `Bash(safe-cmd *)` erlaubt kein `safe-cmd && rm -rf`.
   **Andere Schreibweisen sind es nicht.** Die Regel matcht den Befehlstext, nicht das Programm: `git -C . push`, `git -c k=v push` und `git 'push'` kommen an `Bash(git push *)` vorbei. Die Doku nennt eine solche Regel ausdrücklich *„not a security boundary around the program"* (`code.claude.com/docs/en/permissions`, „What a Bash rule doesn't match", abgerufen 23.09.2026). `git -C` ist dabei keine Randform: Die Harness rät, Befehle nicht mit `cd` einzuleiten, also schreibt der Agent von sich aus `git -C <pfad>` (Journal 2026-09-22, Infrastrukturprojekt D, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`). Die Vorlage führt deshalb für ihre drei git-Sperren die `-C`-Form mit. Die übrigen Formen fängt keine Regel.
7. **Interpreter-Freigaben heben das Regelwerk auf.** `Bash(python -c *)`, `Bash(python -)`, `Bash(node -e *)`, `Bash(bash -c *)`, `PowerShell(pwsh -Command *)` — die Prüfung sieht die Kommandozeile, nicht das, was der Interpreter darin ausführt. Ein `fs.unlinkSync` im Skript kommt an `Bash(rm *)` vorbei, ein `fetch` an der Web-Sperre. **Das ist gravierender als die sechs Punkte darüber zusammen:** Die anderen weichen eine Regel auf, dieser hebt alle auf. Nimm solche Regeln nie in eine Vorlage, und melde sie, wenn du sie in einer bestehenden Datei findest — projektlokal wie global.
8. **Auf Windows läuft PowerShell, nicht Bash.** Claude Code stellt dort beide Werkzeuge bereit, aber die primäre Shell ist `PowerShell`. `Bash(dotnet test *)` greift nicht, wenn der Aufruf über das PowerShell-Werkzeug läuft — auf Windows der Normalfall. Führe jede Regel für beide Werkzeuge. Sonst sind nicht nur die Freigaben wirkungslos, sondern auch die Sperren, und das täuscht Sicherheit vor. Auf macOS und Linux können die `PowerShell(...)`-Zeilen entfallen.

### Geheimnisse: nicht der Agent liest sie, sondern das Programm

`Read(.env)` in `deny` ist richtig und wirkt (siehe Falle 4) — aber dann braucht der Agent einen Weg, ohne den Schlüssel zu arbeiten. Der tragfähige: Ein Prüf- oder Startskript liest die `.env` selbst — `dotenv` und Verwandte — und gibt sie nie aus; der Agent ruft das Skript auf und sieht nur dessen Ergebnis. Das tritt bei jedem Projekt mit API-Zugang auf, und es ist der Grund, die Sperre **nicht** aufzuweichen, wenn sie das erste Mal im Weg steht.

### defaultMode

| Wert | Bedeutung |
|---|---|
| `default` | Fragt beim ersten Gebrauch jedes Werkzeugs. **Voreinstellung dieses Templates.** |
| `plan` | Liest und erkundet, ändert keine Quelldateien |
| `acceptEdits` | Nimmt Dateiänderungen automatisch an |
| `auto` | Genehmigt automatisch mit Hintergrundprüfung |
| `dontAsk` | Verweigert alles, was nicht ausdrücklich erlaubt ist |
| `bypassPermissions` | Überspringt Abfragen. Nur in Containern oder VMs |

Setz `default`, außer der Nutzer verlangt ausdrücklich etwas anderes.

**Die Datei ist nicht der Modus der Sitzung.** In der CLI (Shift+Tab) und in der VS-Code-Erweiterung wählt der Nutzer einen Modus, der `defaultMode` für die laufende Sitzung überstimmt. Im Auto-Modus prüft ein Klassifikator statt des Nutzers (`code.claude.com/docs/en/permissions`, abgerufen 07.10.2026) — ein durchlaufender Befehl belegt dann keine `allow`-Regel, und die Probezeile „Nutzer lehnt nicht pauschal ab" sagt nichts. Die Sperren trennt die Probe trotzdem. Beobachtet am 2026-09-28: Auto-Modus in der Erweiterung gewählt, `defaultMode` stand auf `default` (Journal, Codeprojekt C, Nr. 10, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). **Vor der Wirkungsprobe in Phase 9 den Modus erfragen** und, falls nötig, auf den Standardmodus umstellen lassen. Desktop-App: → `desktop.md`, Phase 9.

**Was du anpasst:** Die in Phase 0 gefundenen Test-, Typecheck- und Lint-Befehle in `allow` ergänzen.

### Hook beim Sitzungsstart — gehört immer dazu

Die Vorlage bringt einen `SessionStart`-Hook mit (Matcher `startup|clear|resume`). Er nennt die offenen Übergaben, also `uebergabe/*.md` ohne `_vorlage.md` und ohne `erledigt/`; gibt es keine, gibt er nichts aus. **Nutzerentscheidung vom 2026-10-22:** bei jeder Einrichtung, nicht erst, wenn etwas liegen geblieben ist. Anlass war ein Vorhaben, das 47 Tage unberührt auf `wartet` stand (Journal 2026-10-22, Infrastrukturprojekt D).

Was ein `SessionStart`-Hook als einfache Ausgabe schreibt, kommt als Kontext beim Agenten an, nicht als Nachricht beim Nutzer (`code.claude.com/docs/en/hooks`, abgerufen 2026-10-22). Deshalb steht in der Profilvorlage im Abschnitt „Übergabe" die Zeile, dass die erste Antwort das Offene nennt. Hook und Zeile gehören zusammen — keins ohne das andere.

**Was du anpasst:**

- **macOS und Linux:** `command` und `args` ersetzen durch
  `"command": "sh", "args": ["-c", "cd \"$CLAUDE_PROJECT_DIR/uebergabe\" 2>/dev/null && f=$(ls *.md 2>/dev/null | grep -vx _vorlage.md | tr '\\n' ' ') && [ -n \"$f\" ] && echo \"Offene Uebergaben in uebergabe/: $f\"; exit 0"]`.
- **Führt das Projekt eine eigene Übersicht offener Arbeit** (erzeugte Statusdatei, Vorhabenliste), gehört sie mit in die Ausgabe. Dann wird aus dem Einzeiler ein Skript unter `.claude/hooks/`; die Fallen stehen unter „Hooks" unten. **Neu erzeugen oder nur lesen entscheidet eine Messung:** den Hook einmal als Unterprozess mit Zeitmessung laufen lassen. Unter 2 s darf er erst neu erzeugen, dann ausgeben, weil Fälligkeit vom Erzeugungstag abhängt. Darüber liest er nur, gibt den Erzeugungsstand der Übersicht und das heutige Datum mit in den Kontext, und ein `Stop`-Hook erzeugt sie nach einer Antwort neu, wenn im Bestand etwas jünger ist; Timeout dann 15 s. Belegt: unter 1 s auf lokalem Datenträger, 5,5 s auf einer NAS-Freigabe, 43 s auf einer Firmenfreigabe — derselbe Generator (Journal 2026-10-22, Textprojekt I). Die 2 s sind eine Nutzersetzung vom 2026-10-22, keine Messgrenze. **Ein Skript für diesen Fall bringt der Basisagent nicht mit;** es existiert nur als Projektkopie (Infrastrukturprojekt D, Textprojekt I).
- **Bestehende `hooks` in der Projektdatei:** den Eintrag unter `SessionStart` ergänzen, nichts ersetzen.

**Prüfen, bevor du weitergehst:** den Befehl einmal als Unterprozess laufen lassen, mit `CLAUDE_PROJECT_DIR` auf das Projekt gesetzt — Ausgabe die offenen Übergaben oder leer, Exit 0. In der Exec-Form (`command` + `args`) geht der Befehl ohne Shell-Zwischenschritt an PowerShell; deshalb enthält der Windows-Befehl nur einfache Anführungszeichen. **Ungeprüft:** ab welcher Claude-Code-Version die Exec-Form gilt, und wie Dateinamen mit Umlauten ankommen (PowerShell 5.1 schreibt im ANSI-Codepage, `feedback/powershell-fallen.md`).

### Hook für Kennungen — gehört immer dazu

Die Vorlage bringt einen zweiten Hook mit: `PostToolUse` auf `Write|Edit`, Skript `claudecode/hooks/kennungen.ps1`. Er greift nur an `.md`-Dateien. Aus dem neu geschriebenen Text zieht er Kennungen und meldet dem Agenten, in welchen anderen Dokumenten des Projekts sie schon stehen. Er meldet nur und blockiert nie. **Nutzerentscheidung vom 2026-11-02:** bei jeder Einrichtung, für jede Projektart. Anlass war eine Adresse, die ein Agent als „nicht erhoben" beschrieb, obwohl drei Dokumente den Host kannten. Gesucht hatte er nach dem Thema, nicht nach der Kennung, die erst unterwegs auftauchte (Journal 2026-11-02, Textprojekt I). Gegenstück in der Regeldatei ist die Kennungen-Zeile im ersten Block. Die Zeile gilt auch ohne den Hook, der Hook nicht ohne die Zeile.

Als Kennung gelten Begriffe in Backticks, **seltene Wörter** und projektspezifische Muster. Seltene Wörter sind solche ab vier Zeichen, die höchstens sechs andere Dokumente enthalten. Diese Schwelle trägt den Kern: Sie fängt Eigen- und Produktnamen, die niemand formatiert, und lässt häufige Wörter ohne Stoppliste fallen. Gemeldet werden höchstens zwölf Kennungen mit je drei Fundstellen. Muster und Backticks erscheinen nur, wenn sie in höchstens zehn Dokumenten stehen.

**Was du anpasst** — nur den Block „Anpassen" oben im Skript, und das Skript nach `.claude/hooks/kennungen.ps1` kopieren:

- **`$muster`**: die Kennungsformen der Projektart. Das Skript trägt Beispiele für IT (Adressen, Hostnamen nach dem Namensschema des Projekts) und Gutachten (Aktenzeichen, Normstellen). Frag nach dem Namensschema, wenn du es in Phase 0 nicht gesehen hast (Schnellmodus: nicht fragen, `core/schnell.md`). Ohne Muster arbeitet der Hook mit Backticks und seltenen Wörtern, das trägt schon. Die Datei bleibt reines ASCII: Sonderzeichen wie `§` als `§` in die Regex.
- **`$ohneOrdner`**: Ordner mit maschinellen Massendaten aus Phase 0. Ordner mit Punkt am Anfang fallen immer heraus.
- **`$eigenTiefe`**: Treffer im eigenen Ordner sind keine Nachricht. Bei `2` gilt `systeme/<name>/` als eigener Ordner für `systeme/<name>/doku.md`. Eine Datei direkt in einem Hauptordner zählt nur selbst. Projekte mit Frontmatter, das Dokumente einem Gegenstand zuordnet, können dessen Ordner zusätzlich ausnehmen; Textprojekt I tut das für Übergaben mit `system:`.
- **macOS und Linux:** `command` auf `pwsh` setzen. Ungeprüft. Ohne PowerShell entfällt der Hook, die Regelzeile bleibt.

**Was der Nutzer wissen muss:** Jeder Schreibvorgang an einer `.md`-Datei kostet einen Prozessstart und einen Lesedurchgang über den Bestand. Gemessen am 2026-11-02: lokal mit 57 Dateien 0,5 bis 1,1 s, auf einem Netzlaufwerk mit über 500 Dateien 2,3 bis 3,9 s, kalt 6,6 bis 7,5 s. Beim Schreiben ganzer Dokumente gibt es Beifang. Im Zielprojekt waren von zwölf Meldungen etwa vier einschlägig. In einem kleinen Bestand rutschen auch Allerweltswörter unter die Schwelle („from", „over"). Der Hinweistext sagt dem Agenten, Beifang zu übergehen.

**Prüfen, bevor du weitergehst:** einmal als Unterprozess, mit `CLAUDE_PROJECT_DIR` auf das Projekt und denselben Schaltern wie in `settings.json` (Aufruf im Kopf des Skripts). Als Text einen Satz mit einem Namen, der im Projekt schon vorkommt. Erwartet: JSON mit `additionalContext`, Exit 0. Ein stiller Abbruch sieht aus wie „kein Treffer". Das Skript fängt jeden Fehler ab, damit nie ein Schreibvorgang scheitert. Bleibt die Ausgabe leer, prüfst du deshalb mit einem Namen, der sicher vorkommt. Beim Testen per Pipe aus PowerShell kommt ein BOM mit; das Skript entfernt es. `${CLAUDE_PROJECT_DIR}` setzt Claude Code in der Exec-Form auch in `args` ein (`code.claude.com/docs/en/hooks`, abgerufen 2026-11-02).

### Externer Quellbestand — lesen ja, verändern nie

Der häufigste Fall bei Textprojekten: Das Material liegt außerhalb des Projekts, auf einer Freigabe, und gehört jemand anderem oder allen. Das Projekt gehört einem. Gebraucht wird Leserecht ohne jedes Schreibrecht.

**`additionalDirectories` ist dafür das falsche Werkzeug.** Es macht den Ordner zum Arbeitsbereich und gibt Schreibrecht mit — genau das, was hier nicht gewollt ist.

Richtig ist diese Kombination:

```json
"allow": [ "Read(//p/Projekte/Materialbestand/**)" ],
"deny":  [
  "Edit(//p/**)",
  "Bash(mv *)", "Bash(cp *)", "Bash(rsync *)",
  "PowerShell(Move-Item *)", "PowerShell(Copy-Item *)"
]
```

**Absolute Pfade schreibt man `//<laufwerksbuchstabe>/<pfad>`** — der doppelte Schrägstrich verankert am Dateisystemwurzelverzeichnis. Ohne ihn wäre der Pfad relativ zum Arbeitsverzeichnis und die Regel greift ins Leere.

**Die Befehlssperren sind kein Beiwerk.** Ohne sie schützt `Edit(//p/**)` gegen Editieren und nicht gegen Verschieben — siehe Falle 4. Für Textprojekte ist das der empfindlichste Fall überhaupt: Der Quellbestand ist das, was nicht verloren gehen darf, und ein verschobenes Dokument unter achtzig fällt später auf als eine geänderte Zeile.

**Sie stehen nicht in der Vorlage**, weil `mv` und `cp` in vielen Projekten legitim gebraucht werden. Sie kommen dazu, wenn ein Pfad wirklich zu schützen ist — dann aber vollständig. Wäge das mit dem Nutzer ab und sag ihm, was er im Gegenzug verliert.

**Zwei Dateien, ein Zweck:**

| Datei | Gehört ins Repo | Wofür |
|---|---|---|
| `.claude/settings.json` | ja | Regeln, die für alle im Projekt gelten |
| `.claude/settings.local.json` | nein, `.gitignore` | Persönliche Zusätze, Experimente |

Frag den Nutzer, ob das Projekt geteilt wird. Bei einem Einzelprojekt reicht `settings.json`. Bei einem Team: die harten Sperren nach `settings.json`, den persönlichen Komfort nach `settings.local.json`, und `.claude/settings.local.json` in die `.gitignore`.

**Ohne Git fällt diese Aufteilung weg.** Sie hängt vollständig an der `.gitignore` — ohne sie liegen beide Dateien gleichberechtigt im Verzeichnis und gelten für jeden, der von dort startet. Ist in Phase 0 kein Git gewählt worden: **eine Datei**, `settings.json`, und die Frage nach dem Teilen entfällt mit. Sie hätte keine Konsequenz mehr.

Dann auch **keine Git-Regeln aufnehmen** — die neun `Bash(git …)`- und `PowerShell(git …)`-Zeilen der Vorlage sind wirkungslos. Notier den Verzicht als offenen Punkt, damit sie bei einem späteren `git init` nicht fehlen.

**Wenn ihm die Sperren nicht hart genug sind:** Berechtigungsregeln greifen pro Werkzeugaufruf. Wer eine Bedingung braucht, die eine Regel nicht ausdrücken kann — etwa „niemals in Dateien schreiben, die seit dem letzten Lesen verändert wurden" —, braucht einen `PreToolUse`-Hook in `.claude/settings.json`. Das ist ein eigener Schritt und gehört nicht in diese Einrichtung. Erwähnen, nicht bauen — siehe den Abschnitt unten, bevor du zusagst.

### Sammlungsprojekte — wo die Sitzung startet

`.claude/settings.json` wird **nicht** von Elternordnern geerbt, anders als `CLAUDE.md` (`code.claude.com/docs/en/large-codebases`, „Choose where to start Claude", abgerufen 07.10.2026). Startet jemand in einem Unterordner, gelten die Regeln aus dieser Phase dort nicht — außer der Unterordner hat eine eigene, in sich vollständige `settings.json`.

Hat das Projekt Unterprojekte mit eigener `CLAUDE.md` oder eigenem Paketmanifest, frag:

> Startest du Claude Code immer im Wurzelordner, oder auch direkt in einzelnen Unterprojekten?

- **Immer im Wurzelordner:** eine Zeile „Sitzung startet im Wurzelordner" in `AGENTS.md`.
- **Auch in Unterprojekten:** Jedes braucht dann eine eigene vollständige `.claude/settings.json`. Leg das dem Nutzer vor, statt die Datei stillschweigend zu vervielfachen.

**Skills in Unterprojekten laden erst später.** Was unter `<unterordner>/.claude/skills/` liegt, erscheint nicht beim Start. Es lädt, sobald eine Datei in diesem Unterordner gelesen oder bearbeitet wird, und bleibt dann bis zum Sitzungsende (`code.claude.com/docs/en/skills`, abgerufen 22.10.2026). Die Beschreibungen kosten also erst ab dem ersten Zugriff, und die Suche in Phase 6 findet sie nur, wenn sie die Unterordner mit absucht.

Befehle für Unterprojekte aus dem Wurzelordner — etwa `npm --prefix <unterordner> test` statt `cd` — brauchen `allow`-Muster mit Stern in der Mitte. **Ob sie greifen, ist ungeprüft** (offener Punkt 46); die Wirkungsprobe zeigt es nur im Standardmodus, siehe `defaultMode`.

### Artefakte und Claude Docs — Vorgabe aus

**Nutzerentscheidung vom 2026-10-22:** Die Vorlage schaltet die Veröffentlichung auf claude.ai grundsätzlich ab — Artefakte, die Vorlagen Slides und Design, die darauf aufsetzen, und den Konnektor „Claude Docs". Sonst verlässt Projektinhalt das Projekt auf eine private, teilbare Seite, ohne dass jemand danach gefragt hat. Fünf Stellen in `settings.json.tpl`:

- **`"enableArtifact": false`** — der Projektschalter. Ein `true` in der Projekt- oder lokalen Datei schaltet ihn nicht zurück. Er braucht Claude Code ab v2.1.242 (`code.claude.com/docs/en/artifacts`, Abschnitt „Disable artifacts", abgerufen 22.10.2026).
- **`"Artifact"` in `deny`** — nennt dieselbe Doku als gleichwertigen Weg. Steht zusätzlich da, weil er nicht an die Version gebunden ist.
- **`"mcp__claude_ai_Claude_Docs__*"` in `deny`** — Dokumente laufen über den Konnektor, nicht über das Artefakt-Werkzeug; den Schalter erreichen sie nicht. Zum Weg siehe „Phase 6 — MCP-Server trennen". In der Desktop-App ungeprüft.
- **`skillOverrides`** für `artifact-design`, `artifact-diagramming`, `artifact-capabilities` und `anthropic-skills:docs` — ob die Skills mit dem Schalter von selbst aus der Liste verschwinden, ist ungeprüft. Codeprojekt C hat sie so abgeschaltet (Journal 2026-09-28, Nr. 8, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). Der Konnektor bleibt davon unberührt (Phase 6).

**Will der Nutzer Artefakte oder Docs,** streichst du die zugehörigen Zeilen — nicht nur eine, sonst bleibt der Weg halb offen. Frag nicht von dir aus danach. Prüf in Phase 9 Schritt 5, ob die Skills noch in der Liste stehen und ob `Artifact` noch unter den Werkzeugen erscheint.

### Hooks — was du dazu sagst, wenn der Nutzer danach fragt

**Erwähnen, nicht bauen bleibt** — außer bei den beiden Hooks, die die Vorlage mitbringt: Sitzungsstart und Kennungen (Phase 1, oben). Ein Hook entsteht aus beobachteter Wiederholung, nicht aus einer Vermutung bei der Einrichtung; alle drei belegten Fälle sind im Alltag entstanden, Wochen nach dem Aufsetzen. Was hier steht, ist für das Gespräch — damit du weder abwinkst noch etwas zusagst, das teurer wird als es aussieht.

**Warum die Frage überhaupt aufkommt.** Geladener Regeltext ist Kontext, keine Durchsetzung. Die Herstellerdoku sagt es selbst: *„Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."* (`code.claude.com/docs/en/memory`, abgerufen 2026-09-03). Zwei Projekte haben daraufhin unabhängig voneinander Hooks gebaut — belegt im Journal am 2026-09-02 und 2026-09-03.

**Die Trennlinie ist nicht „mechanisch prüfbar", sondern „mechanisch prüfbar ohne Fehlalarm".** Das ist der teuerste Satz dieses Abschnitts. Ein Glossar mit Verbotsliste sieht aus wie der ideale Hook-Kandidat; im belegten Fall blieben von der Liste **vier** Wörter übrig, weil Begriffe wie „Server" oder „Protokoll" dort als Typbezeichnung verboten, im Fließtext aber richtig sind. Ein Hook, der bei jedem Schreiben falsch anschlägt, wird überlesen — dann ist er schlechter als keiner.

Draußen bleiben deshalb alle Regeln, die ein **Urteil** verlangen: Belegpflicht, Kürze, Unsicherheit benennen, Widersprüche melden statt auflösen. Für sie ist der Kontextweg der einzige.

**Drei Fallen, jede einmal bezahlt:**

- **Ein blockierender Hook darf nicht nach einer Zeichenfolge suchen, sondern nach einem ausgeführten Befehl.** Im belegten Fall verweigerte er einen `git commit`, weil die Commit-Nachricht den gesperrten Befehl im Fließtext erwähnte — der zu prüfende Befehl umfasst das ganze Here-Dokument. Anführungszeichen und Here-Dokumente ausblenden, den Befehl nur am Zeilenanfang oder hinter `;`, `&&`, `|` suchen.
- **Positivtests sagen nichts über Fehlalarme.** Alle Prüfungen waren vor der Registrierung positiv getestet, und trotzdem gab es vier Fehlalarme in der ersten Stunde — ein Hook, der nach Zeichenfolgen sucht, findet zuerst seine eigene Dokumentation. Vor dem Scharfschalten einmal gegen den **eigenen Bestand** laufen lassen: Regeldateien, Vorlagen, die Hookdateien selbst.
- **Ein still versagender Hook sieht aus wie ein Hook, der nicht greift.** In beiden Projekten sah der erste Testlauf nach „Regel wirkt nicht" aus, obwohl das Skript korrekt war. Als **echten Unterprozess** testen, nicht im laufenden Shell-Prozess anpipen. Und mit denselben Schaltern, mit denen `settings.json` ihn aufruft. Ohne `-ExecutionPolicy Bypass` bricht PowerShell mit einer Fehlermeldung ab, und ein Test, der auf „Ausgabe nicht leer" prüft, meldet dann jeden Fall als gesperrt. **Prüf auf die Entscheidung, nicht auf Ausgabe.** Das ist die gefährlichere Richtung: Der Hook sieht aus, als greife er (Journal 2026-09-22, Infrastrukturprojekt D, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`). Die Einzelheiten für PowerShell stehen als Punkt in `feedback/offene-punkte.md`, nicht hier.

**Der dritte belegte Fall meldet, statt zu sperren: offene Arbeit beim Sitzungsstart.** Seit 0.30.0 Teil der Vorlage, siehe Phase 1. Für den Ausbau zu einem Skript: **Was der Hook liefert, sieht nur der Agent:** Der Kontext „doesn't appear as a chat message in the interface" (`code.claude.com/docs/en/hooks`, abgerufen 2026-10-22). Je Ausgabe gelten 10.000 Zeichen, darüber kommen nur Dateipfad und Vorschau an. Ob `systemMessage` beim Sitzungsstart angezeigt wird, ist ungeprüft.

**Die Kostenseite gehört ins Gespräch.** Jeder Hook ist ein Prozessstart je passendem Werkzeugaufruf. Drei `PostToolUse`-Hooks auf `Edit|Write` sind drei Prozessstarts je Schreibvorgang — auf einer Netzfreigabe ist das spürbar. Wer mehrere meldende Prüfungen will, legt sie in **eine** Datei und schiebt teure Vollscans in den `Stop`-Hook.

---

### Hilfsagenten überhaupt — die erste Frage, Vorgabe nein

**Subagenten und Workflows sind in der Vorlage gesperrt** (Nutzerentscheidung
vom 2026-10-12): Sie laufen lange und kosten ein Vielfaches. Gemessen war eine
Recherche über Subagenten rund doppelt so teuer wie in der Hauptsitzung
(`core/prinzip.md`, vierter Hebel), einzelne Läufe dauerten 22 bis über 40
Minuten. Frag, bevor du die Budgetfrage stellst:

> Darf ich Arbeit an Hilfsagenten abgeben? Sie arbeiten neben mir, brauchen
> aber meist deutlich länger und ein Vielfaches an Kontingent. **Vorgabe:
> nein** — dann erledige ich alles selbst in der Sitzung.

| Antwort | `settings.json` |
|---|---|
| nein, oder keine klare Antwort | `"Agent"` und `"Workflow"` in `deny` bleiben stehen. Keine Rechercheagenten, die Budgetfrage entfällt |
| ja | beide Zeilen streichen, dann weiter mit „Rechercheagenten" |

**Was die Sperre bewirkt, laut Doku:** Ein blanker Werkzeugname in `deny`
*„removes the tool from Claude's context entirely"*
(`code.claude.com/docs/en/permissions`), und für Subagenten nennt die Doku
genau diesen Weg: *„To prevent Claude from delegating to any subagent, deny
the `Agent` tool itself"* (`code.claude.com/docs/en/sub-agents`). Damit fallen
auch `Explore` und `Plan` weg; der Agent liest und sucht selbst. Für
`Workflow` folgt die Wirkung nur aus der allgemeinen Regel — die
Workflow-Seite nennt stattdessen `"disableWorkflows": true` und
`CLAUDE_CODE_DISABLE_WORKFLOWS=1` (`code.claude.com/docs/en/workflows`). Alle
drei abgerufen 12.10.2026; am Werkzeug ungeprüft.

**Sag dem Nutzer die Folgen:**

- `/deep-research` und `ultracode` laufen nicht — beides sind Workflows.
- Skills, die delegieren, laufen nur teilweise: `research` aus dem Katalog,
  `codebase-design` mit seinem Entwurf über parallele Subagenten (Journal
  2026-10-10, Codeprojekt D, Nr. 6). In Phase 5 nicht ohne diesen Hinweis
  vorschlagen. Ob Skills mit `context: fork` betroffen sind, ist ungeprüft.
- **Je Aufgabe einschalten geht nicht:** `deny` schlägt jede Freigabe. Wer
  Hilfsagenten will, sagt „erlaube Hilfsagenten" — der Agent streicht die
  beiden Zeilen und stellt die Budgetfrage; danach Neustart.

---

### Der `env`-Block — Subagenten begrenzen

Die Vorlage setzt zwei Umgebungsvariablen. Sie sind kein Sicherheits-, sondern
ein Kostenmittel, und sie stehen dort, weil die Voreinstellung großzügig ist.
**Sie bleiben auch bei gesperrten Hilfsagenten stehen** — wirkungslos, bis
jemand die Sperre aufhebt, und dann ist die Grenze schon da:

| Variable | Vorlage | Voreinstellung laut Doku |
|---|---|---|
| `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` | `1` | `3` Ebenen unter dem Hauptagenten |
| `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | `5` | `20` gleichzeitig |

`1` heißt: Subagenten dürfen keine eigenen Subagenten starten. Ein Subagent
kostet nicht nur seine eigene Sitzung — sein Ergebnis kommt in die Hauptsitzung
zurück und wird dort ab da in jedem Zug mitgelesen (`core/prinzip.md`,
Wiederholkosten). Bei zwanzig gleichzeitigen ist das kein Randposten.

**Sag dem Nutzer, was die Zeilen tun: begrenzen, nicht ausschließen.**
Ausschließen tut die Sperre aus dem Abschnitt davor; hat er Hilfsagenten
erlaubt, darf der Agent weiter Subagenten starten, nur keine verschachtelten
und höchstens fünf gleichzeitig. Ein Nutzer hat nach der Einrichtung einen
Ausschluss angenommen, wo nur begrenzt war (Journal 2026-09-23, Textprojekt J,
seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`).

**Der Anlass ist modellabhängig und belegt:** Claude Opus 5 delegiert
bereitwilliger an Subagenten als seine Vorgänger; die Herstellerdoku nennt
genau diese beiden Variablen als deterministische Bremse und empfiehlt sie
ausdrücklich für Opus-5-Läufe. Eine Anweisung im Systemprompt steuert nur,
die Variablen greifen.

**Ungeprüft, und das ist die Einschränkung:** Der Doku-Abschnitt, der beide
Variablen mit Voreinstellung nennt, steht im Kapitel des Agent-SDK und
beschreibt dort den Weg über dessen `env`-Option. Dass dieselben Variablen
auch die interaktive CLI binden, nennt der Prompting-Leitfaden — belegt ist
es damit für das Werkzeug, nicht durch eine Messung an diesem Aufbau. Nimm
sie heraus, wenn ein Projekt breit fächernde Recherche braucht; dann ist die
Grenze der falsche Sparzwang.

**Mindestversion:** Claude Code 2.1.219 (Agent-SDK-Doku; der Prompting-
Leitfaden nennt 2.1.217). Auf älteren Fassungen fehlen die Grenzen oder
wirken anders — dann sind die Zeilen wirkungslos, nicht schädlich.

Quellen: `code.claude.com/docs` → Agent SDK, „Cap subagent depth, concurrency,
and spend"; `platform.claude.com` → „Prompting Claude Opus 5". Abgerufen
21.09.2026.

---

### Rechercheagenten — das Budget fragst du ab

**Nur, wenn der Nutzer Hilfsagenten erlaubt hat.** Sonst entfällt dieser
Abschnitt samt Dateien.

Der `env`-Block begrenzt Tiefe und Anzahl, **nicht Länge und Modell**. Ein
einzelner Rechercheagent lief am 2026-10-07 im Basisagent 22 Minuten mit 49
Abrufen; der Nutzer berichtet Läufe über 40 Minuten. Die Bremse dafür sind
eigene Agentendefinitionen mit `maxTurns`, `model` und `effort` — ein Zeit-
oder Tokenlimit gibt es nicht (`code.claude.com/docs/en/sub-agents`,
abgerufen 07.10.2026).

**Was der Nutzer wählt, ist seine Sache** (Nutzerentscheidung vom
2026-10-07). Du fragst, empfiehlst keine Stufe und kein Modell, und legst die
Vorlagen danach an. Zwei Fragen, nacheinander:

> Wie viel darf eine Recherche kosten, die ich an einen Hilfsagenten abgebe?
>
> | Stufe | Modell | höchstens Schritte | Aufwand |
> |---|---|---|---|
> | schmal | haiku | 8 | low |
> | mittel | sonnet | 15 | medium |
> | breit | wie die Sitzung (`inherit`) | 30 | high |
> | unbegrenzt | — keine eigene Definition, der eingebaute Allzweck-Agent bleibt | | |

> Soll es zusätzlich eine große Stufe geben, die nur läuft, wenn du sie
> ausdrücklich verlangst? (Vorgabe: wie die Sitzung, 40 Schritte, high — Werte
> frei wählbar.)

Eigene Werte statt der Stufen sind jederzeit möglich. Ein Schritt ist eine
Runde des Agenten, nicht ein Abruf — mehrere parallele Abrufe zählen als einer.

**Danach:**

| Wahl | Datei |
|---|---|
| eine Stufe außer „unbegrenzt" | `.claude/agents/recherche.md` aus `claudecode/agents/recherche.md.tpl`, Platzhalter gefüllt |
| große Stufe gewünscht | zusätzlich `.claude/agents/recherche-gross.md` aus der zweiten Vorlage |
| eine Stufe außer „unbegrenzt" | `"Agent(general-purpose)"` in `deny` bleibt stehen — sonst ist die Grenze umgehbar, weil der Hauptagent einfach den Allzweck-Agenten nimmt |
| „unbegrenzt" | keine Datei, und die `deny`-Zeile aus der Vorlage streichen |

**Auch wenn `~/.claude/agents/recherche*.md` und die `deny`-Zeile global schon
bestehen:** Leg beides im Projekt an (Runbook Phase 5 Schritt 1 — was nur
global liegt, fehlt auf einem anderen Rechner). Die Projektdatei gewinnt bei
gleichem Namen ohnehin, siehe Abschnitt „Phase 5 und 6 — Gleicher Name".

Sag dem Nutzer, was die Sperre bedeutet: Jede Delegation braucht dann einen
benannten Typ; `Explore` und `Plan` bleiben. Ruft der Agent ohne Typ auf,
schlägt der Aufruf fehl (`subagent_type is required`, Quelle wie oben).

**Später ändern — das ist der Teil, den der Nutzer sich merken soll.** Nenn
ihn in Phase 9 Schritt 4:

- **Je Aufgabe mehr:** „nimm die große Recherche", oder `@` tippen und
  `recherche-gross (agent)` wählen. Weniger: im Auftrag ein Budget nennen
  („höchstens fünf Abrufe") — das ist eine Bitte, keine harte Grenze; hart
  ist nur `maxTurns`.
- **Dauerhaft:** „stell die Recherche auf breit" — der Agent ändert
  `.claude/agents/recherche*.md`. Laut Doku greift die Änderung ohne Neustart
  bei der nächsten Delegation. **Ausnahme:** Die erste Datei in einem
  `agents`-Ordner, der beim Sitzungsstart noch nicht existierte, braucht einen
  Neustart — bei der Einrichtung ist das der Fall, Phase 9 startet ohnehin neu.

**Ungeprüft** ist, ob `maxTurns` einen Hintergrundagenten zuverlässig anhält
und wie viel ein Schritt im Mittel kostet (`feedback/offene-punkte.md`,
Punkt 45).

---

## Phase 2 — Besonderheit

Claude Code liest `AGENTS.md` seit v2.1.277 auch selbst — aber nur, wenn im Startordner und darüber **keine** `CLAUDE.md`, `.claude/CLAUDE.md` oder `CLAUDE.local.md` liegt. Liegt eine dort, liest es nur die `CLAUDE.md`-Dateien. In manchen Sitzungen kann es `AGENTS.md` gar nicht lesen; dafür nennt der Hersteller den Import (`code.claude.com/docs/en/memory`, Abschnitt „AGENTS.md", abgerufen 07.10.2026).

**Verlass dich nicht auf das native Lesen.** Eine `CLAUDE.local.md`, die der Nutzer später für eigene Notizen anlegt, schaltet es still ab. In Sammlungsprojekten mit eigener `CLAUDE.md` im Unterordner ebenso, sobald jemand dort startet (Journal 2026-09-28, Codeprojekt C, Nr. 2, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). Der Import trägt in allen drei Fällen.

In Phase 2 schreibst du `AGENTS.md`: Sie ist die werkzeugneutrale Quelle. **Direkt danach, noch in Phase 2, legst du `CLAUDE.md` an**, die sie per `@AGENTS.md` importiert. Vorlage: `claudecode/CLAUDE.md.tpl`; meist bleibt nur die Importzeile übrig.

**Wenn der Nutzer sicher nie ein zweites Werkzeug einsetzt**, frag, ob er es einfacher will: dann direkt `CLAUDE.md` statt `AGENTS.md`, ohne Import. Eine Datei weniger. Er verliert die Werkzeugneutralität — sag ihm das, und leg die Entscheidung ihm vor. Voreinstellung bleibt `AGENTS.md` + Import, weil sie sich später kostenlos erweitern lässt.

**Prüfen, ob der Import ankommt — gehört nach Phase 9 Schritt 5, nicht hierher.** Der Weg ist `/context`, Abschnitt *Memory files*: Dort muss `AGENTS.md` selbst auftauchen, nicht nur `CLAUDE.md`. Die Anzeige listet nach Herstellerangabe auf, welche Instruktionsdateien geladen sind (`code.claude.com/docs/en/context-window`, abgerufen 2026-09-04). **Nur der Nutzer kann den Befehl ausführen** — bitte ihn darum und lass dir die Zeilen zeigen, statt es zu behaupten.

Der Befehl ist erst nach dem Neustart aussagekräftig. In der Einrichtungssitzung sagt er nichts über eine Datei, die es beim Sitzungsstart noch nicht gab — dieselbe Sitzungsgrenze wie bei den Berechtigungen in Phase 1.

**Kommentare in der Regeldatei kosten nichts — block-level.** Block-level HTML-Kommentare (`<!-- … -->` auf eigenen Zeilen) werden entfernt, bevor die Regeldatei in den Kontext geht, und zwar **auch aus der per `@` importierten `AGENTS.md`**. Ein Kommentar am Zeilenende bleibt vollständig drin. Gemessen am 2026-09-01 mit drei Fundstellen, Claude Code 2.1.247 auf Windows (Journal 2026-09-01, seit dem Schnitt vom 2026-09-21 in `feedback/archiv/journal-0.14.0-0.16.0.md`); Doku: `code.claude.com/docs/en/memory`, Abschnitt „How CLAUDE.md files load".

Nutzbar für Begründungen und Wartungsnotizen, die beim **Ändern** der Datei zur Hand sein sollen — `Read` zeigt sie weiterhin. **Nicht** für Regeln, die wirken sollen: was entfernt wird, befolgt niemand. Seit 0.27.0 erzeugen die Profilvorlagen nur noch für Claude Code. Der Einwand gegen einen übernommenen Kommentarblock in den Vorlagen — OpenCode ungeprüft — ist damit weggefallen; umgesetzt ist er nicht (offener Punkt 28).

---

## Phase 3 — Ablaufgerüst

Welches Gerüst zur Wahl steht, sagt das Profil. Für Claude Code gilt unabhängig davon: Skillbasierte Gerüste landen unter `.claude/skills/<name>/SKILL.md` — der native Ort.

**Falls OpenSpec gewählt wurde:** Seine Skills liegen unter `.claude/skills/openspec-*/SKILL.md`. Die Kommandos stehen danach als `/opsx:…` zur Verfügung.

Legt die installierte Version einen verwalteten Block in `AGENTS.md` an, sieht Claude Code ihn über den Import aus Phase 2. Ab OpenSpec 1.9 entsteht kein solcher Block mehr. Weicht der Befund davon ab, melde es — repariere es nicht eigenmächtig.

---

## Phase 6 — Neue Skills ohne Neustart

Claude Code beobachtet die Skill-Verzeichnisse. Kommt in `~/.claude/skills/` oder im projekteigenen `.claude/skills/` ein Skill hinzu oder ändert sich einer, erscheint das in der laufenden Sitzung, ohne Neustart. **Ausnahme:** Ein Verzeichnis, das es beim Sitzungsstart noch nicht gab, wird nicht beobachtet — dann braucht es `/reload-skills`, nach jeder weiteren Änderung dort erneut. Erfasst wird nur der Text der `SKILL.md` (`code.claude.com/docs/en/skills`, abgerufen 07.10.2026; beobachtet am 2026-09-28, Journal, Codeprojekt C, Nr. 3, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`).

Für die Bedingung in Runbook Phase 6 heißt das:

| `.claude/skills/` beim Sitzungsstart | Sichtbarkeitsprüfung |
|---|---|
| vorhanden | gilt schon in Phase 6 |
| erst in dieser Sitzung entstanden — im neuen Projekt meist durch `uebergabe` in Phase 5 Schritt 0 | Nutzer um `/reload-skills` bitten, danach prüfen |
| unbekannt, oder der Skill fehlt auch danach | Prüfung nach Phase 9 Schritt 5, wie im Runbook |

Wegen `disable-model-invocation` fehlt ein Skill trotzdem — siehe den Abschnitt darunter.

---

## Phase 5 und 6 — Gleicher Name global und im Projekt

Das Runbook verlangt die Projektkopie, auch wenn global schon eine liegt. Welche
auf **diesem** Rechner gilt, ist bei Skills und Agenten entgegengesetzt
(`code.claude.com/docs/en/skills` und `…/sub-agents`, abgerufen 07.10.2026):

| Art | gewinnt | Folge |
|---|---|---|
| Skill | die **globale** (`~/.claude/skills/` vor `.claude/skills/`) | Die Projektkopie ist hier verdeckt und wird nicht geladen. Auf einem Rechner ohne globale Kopie trägt sie |
| Agent | die **projektlokale** (`.claude/agents/` vor `~/.claude/agents/`) | Die Projektkopie gilt überall |

Unterscheiden sich globale und Projektkopie eines Skills, arbeitet der Nutzer
je nach Rechner mit einem anderen Skill und merkt es nicht. Melde das in
Phase 6 und frag, welche Fassung gilt; angeglichen wird die andere.

---

## Phase 6 — Einzelne Skills eines Plugins abschalten

**Ein Plugin ist nicht Alles-oder-nichts.** In `settings.json` schaltet `skillOverrides` je Skill:

```json
"skillOverrides": {
  "mattpocock-skills:tdd": "off",
  "mattpocock-skills:code-review": "name-only",
  "mattpocock-skills:research": "user-invocable-only"
}
```

| Wert | Wirkung |
|---|---|
| `off` | Skill verschwindet vollständig, kostet nichts mehr |
| `name-only` | Nur der Name bleibt im Kontext, die Beschreibung fällt weg |
| `user-invocable-only` | Bleibt per `/name` aufrufbar, wird aber nicht mehr von selbst vorgeschlagen |

**Nutze qualifizierte Namen** (`plugin:skill`), sonst kollidiert der Eintrag mit einem gleichnamigen Bordskill.

Das gilt auch für das kontoseitig synchronisierte Anthropic-Set: `"anthropic-skills:pptx": "off"` wirkt. Über einen Neustart gemessen: fünf abgeschaltete verschwanden, drei nicht abgeschaltete blieben (Journal 2026-09-22, Textprojekt J, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`).

**Auch die mit Claude Code gebündelten Skills** schaltet `skillOverrides` einzeln ab: `"<name>": "off"`. Alle zusammen nimmt `disableBundledSkills: true` heraus (`code.claude.com/docs/en/skills`, „Remove a skill", abgerufen 22.10.2026).

Das ist der Hebel für den häufigsten Fall in dieser Phase: Ein Plugin bringt neun Skills, sechs davon setzen eine Codebasis voraus, und das Projekt ist ein Textprojekt. Ohne `skillOverrides` bliebe nur „ganz weg oder ganz da" — mit ihm ist es eine Einzelentscheidung wie bei allen anderen Skills.

Frag also **pro Skill**, nicht pro Plugin. Und sag nicht, einzelne Skills ließen sich nicht herausnehmen — das ist falsch.

**Dasselbe gibt es von der Skill-Seite:** `disable-model-invocation: true` im Frontmatter einer `SKILL.md` nimmt den Skill aus dem, was dem Modell von selbst angeboten wird; per `/name` bleibt er voll aufrufbar. Beobachtet: Er **verschwindet dabei aus der Skill-Liste der Sitzung** — die Sichtbarkeitsprüfung in Phase 6 urteilt bei ihm „tot", obwohl er läuft. Prüf deshalb das Frontmatter, bevor du einen fehlenden Skill für tot erklärst.

**Die Beschreibung fällt dabei aus dem Kontext**, der Rumpf lädt erst beim Aufruf (`code.claude.com/docs/en/skills`, „Control who invokes a skill", abgerufen 22.10.2026; Punkt 18). Dauerkosten null. Der Preis: Das Modell startet ihn nicht selbst, er braucht einen Auslöser in der Regeldatei. Für einen projekteigenen Skill ist das Feld deshalb der bessere Schalter als `name-only`, weil es beim Skill steht.

---

## Phase 6 — MCP-Server trennen

Auflisten mit `claude mcp list`, trennen mit `claude mcp remove <name>`. Global verbundene Server stehen in `~/.claude.json` unter `mcpServers`; der Befehl meldet, welche Datei er geändert hat. Die Werkzeuge verschwinden erst mit dem nächsten Sitzungsstart aus dem Kontext.

**Ein dritter Fall: Konnektoren aus claude.ai.** `claude mcp get <name>` meldet sie mit `Scope: claude.ai config`, in `~/.claude.json` stehen sie nicht (Journal 2026-09-22, Textprojekt J, seit 2026-10-07 in `feedback/archiv/journal-0.18.0.md`). Verwaltet werden sie auf claude.ai (`claude.ai/customize/connectors`); dort getrennt, fehlt einer in **allen** Projekten. In Claude Code gibt es zwei Wege:

- **Je Server, je Projekt:** `"mcp__claude_ai_<Server>__*"` in `deny`, etwa `"mcp__claude_ai_Claude_Docs__*"`. Konnektorwerkzeuge heißen `mcp__claude_ai_<server>__<tool>`, und ein Glob-Deny auf den Werkzeugnamen nimmt sie aus dem Kontext (`code.claude.com/docs/en/permissions`, abgerufen 07.10.2026). Beobachtet sofort, ohne Neustart (Journal 2026-09-28, Codeprojekt C, Nr. 11, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). Den Servernamen liest du an den Werkzeugnamen der Sitzung ab. In der Desktop-App ungeprüft.
- **Alle auf einmal:** `"disableClaudeAiConnectors": true` in einem beliebigen Settings-Bereich, also auch projektlokal, oder `ENABLE_CLAUDEAI_MCP_SERVERS=false` für eine Shell. Beides wirkt im Terminal und in der IDE, nicht in der Desktop-App.

**`skillOverrides` erfasst Konnektoren nicht.** `"anthropic-skills:docs": "off"` ließ den Konnektor „Claude Docs" verbunden (ebenda, Nr. 11). Wer einen Skill abschaltet, prüft den gleichnamigen Konnektor gesondert. Ob `claude mcp remove` bei ihnen etwas tut, sagt die Doku nicht. Nenn den Befehl dafür nicht. Quelle: `code.claude.com/docs/en/mcp`, „Use MCP servers from claude.ai" und „Disable claude.ai connectors", abgerufen 23.09.2026.

---

## Phase 7 — entfällt

Seit 0.27.0 nicht Teil der Einrichtung (→ Runbook, Phase 7). Der frühere OpenCode-Adapter liegt ungepflegt in der Entwicklungskopie unter `feedback/archiv/opencode/`.

---

## Phase 8 — Rollentrennung

**Claude Code bringt den Plan-Modus mit.** Er ist genau das, was Phase 8 beschreibt: eine erzwungene Grenze, hinter der nicht geschrieben wird. Ein eigener Agent dafür ist überflüssig.

Sag dem Nutzer:

> Plan-Modus schaltest du mit Shift+Tab durch. Wenn du dauerhaft dort starten willst, setze in `.claude/settings.json`:
> ```json
> "permissions": { "defaultMode": "plan" }
> ```

**Wann ein eigener Subagent trotzdem sinnvoll ist:** wenn eine Rolle mit einem eingeschränkten Werkzeugsatz laufen soll, etwa für Recherche in einem eigenen Kontextfenster. Dann `.claude/agents/<name>.md`:

```markdown
---
name: think
description: Analysiert ohne zu schreiben. Für Architekturfragen und Fehlersuche im Konzept.
tools: Read, Grep, Glob, WebFetch
---

Analysieren und erklären. Keine Dateiänderungen.
```

**Kein `model:`-Feld.** Der Subagent erbt dann das Modell der Sitzung. Die Modellwahl trifft der Nutzer selbst — nicht vorschlagen, nicht danach fragen. Ausnahme sind die Rechercheagenten aus Phase 1: Dort ist das Modell Teil der Budgetfrage und wird gefragt, aber nicht empfohlen.

**Achtung, Dauerkosten:** Ein Subagent kostet seine Beschreibung in jedem Zug, weil der Hauptagent wissen muss, dass es ihn gibt. Nur anlegen, wenn er benutzt wird. Der Plan-Modus kostet nichts.

---

## Aufwandstufe — nenne sie in Phase 9

Claude Code kennt fünf Stufen (`low`, `medium`, `high`, `xhigh`, `max`). Die
Voreinstellung ist `high`, auf Opus 5.5 `medium`. Die Regeldatei trägt dazu drei Zeilen im Abschnitt
„Antwort und Aufwand"; hier steht, was der Agent dem Nutzer dazu sagt.

**Wo sie sich setzen lässt:**

| Weg | Reichweite |
|---|---|
| `/effort` in der Sitzung | Slider; Enter speichert als Vorgabe, sonst nur diese Sitzung |
| `--effort <stufe>` beim Start | diese Sitzung |
| `"effortLevel"` in `settings.json` | Vorgabe für Modelle ohne eigene Stufe (`max` wird hier nicht angenommen) — **gilt nicht für Opus 5.5 und neuere Modelle**, die auf ihrer eigenen Voreinstellung starten, bis `/effort` oder `/model` eine Stufe setzt |
| `"modelSettings"` in `settings.json` | je Modell |
| `CLAUDE_CODE_EFFORT_LEVEL` | überschreibt `--effort` und `/effort` |
| `effort:` im Frontmatter eines Skills oder Subagenten | solange er läuft; schlägt die Sitzungsstufe, nicht die Umgebungsvariable |

**Wo sie sich ablesen lässt**, denn danach fragt der Nutzer zuerst:

- **Terminal:** im Sitzungskopf neben dem Modell („with low effort") und kurz
  in der Fußzeile, beim Start und bei jedem Wechsel. `/effort` ohne Argument
  öffnet dort den Schieberegler.
- **VS-Code-Erweiterung:** auf dem Knopf mit dem Modellnamen und in der Zeile
  „Effort" des Modellwählers (ab v2.1.257). Jede dort gewählte Stufe außer
  `max` wird als Vorgabe für das Modell gespeichert. `/effort` ohne Argument
  zeigt in der Erweiterung nur die Befehlsübersicht (beobachtet 2026-09-24).
- **Statuszeile:** das Feld `effort.level`, auch nach einem Wechsel mitten in
  der Sitzung. Ob die Erweiterung eine eigene Statuszeile anzeigt, ist
  ungeprüft.
- **Im Nachhinein:** Das Sitzungsprotokoll trägt die Stufe je Anfrage
  (`effort`, `perTurnEffort`; beobachtet, keine zugesicherte Schnittstelle).
  `core/belege/kontextbericht.py` weist sie seit 2026-09-24 aus.

Die Rangfolge beim Start: ausdrückliche Wahl (Umgebungsvariable, `--effort`,
`/effort`), dann die je Modell gespeicherte Stufe, dann die Voreinstellung
des Modells.

**Das Template setzt keine Stufe.** Das ist dieselbe Entscheidung wie beim
Modell (`core/verworfen.md`, „Modellempfehlungen"): eine Nutzerentscheidung,
situativ, nicht Sache einer Einrichtung, die einmal läuft. Der Agent schlägt
vor und begründet, der Nutzer wählt.

**Ein Wechsel kostet, und deshalb steht er in der Regeldatei.** Die
Herstellerdoku sagt für die Schnittstelle: Ein geänderter Wert auf oberster
Ebene erhält den Zwischenspeicher **nicht** — „pick an effort level at the
start and keep it constant", wenn eine lange Sitzung auf Cache-Treffer setzt.
Claude Code zeigt beim Wechseln mitten in der Arbeit dazu eine Cache-Warnung,
die zu bestätigen ist. Was ein Cache-Verlust kostet, steht in
`core/belege/README.md`: gemessen das 6,5-Fache einer Anfrage mit warmem
Cache. **Der richtige Zeitpunkt ist deshalb der Sitzungsanfang** — also genau
nach einem `/clear`, und damit an derselben Stelle, an der das
Übergabeverfahren ohnehin schneidet.

**Ausnahme Opus 5.5 und Fable 5.1.** Über Abo oder API-Schlüssel erhält Claude
Code auf diesen beiden Modellen den Zwischenspeicher beim Wechsel und fragt
nicht nach — auf Fable 5.1 erst ab v2.1.260. Das gilt nicht über Bedrock,
Google Cloud, das Claude-Apps-Gateway, mit
`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` oder bei HIPAA-Konfiguration. Dort
ist die Stufe ein Regler je Aufgabe, nicht je Sitzung: Schlag sie beim
Aufgabenwechsel vor, nicht nur nach `/clear`. Die Regeldatei trägt diese
Ausnahme seit 0.19.0 im letzten Satz der Aufwandzeile.

**Was du in Phase 9 sagst**, als Anhaltspunkt und nicht als Vorschrift:

- Mehrdateiige Änderungen, Refactoring, lange Recherche mit Belegketten → `xhigh`
- Der Normalfall → `high`, die Voreinstellung
- Einzeledit, Formatierung, Nachschlagen, kurze Frage → `medium` oder `low`
- Die Herstellerempfehlung für Opus 5 lautet ausdrücklich, `low` und `medium`
  großzügig zu verwenden, wo die Qualität hält, und auf `xhigh` zu gehen, wo
  es anspruchsvoll wird.
- **Auf Opus 5.5 eine Stufe tiefer ansetzen.** `medium` erreicht dort laut
  Hersteller Opus 5 auf `high`; `xhigh` und `max` nur, wo ein
  Qualitätsgewinn gemessen ist. Stufen nicht vom alten Modell übernehmen —
  und den Nutzer darauf hinweisen, dass sein bisheriges `effortLevel` für
  Opus 5.5 nicht greift.

**Was die Stufe nicht tut:** Sie kürzt die Antwort nicht. Sie steuert die
Denkmenge; die sichtbare Antwortlänge ändert sie auf Opus 5 nicht verlässlich.
Dafür ist die Kürze-Zeile in der Regeldatei da, nicht die Stufe.

**Ein Skill mit eigener Stufe ist immer ein Wechsel mitten in der Sitzung.**
Das ist der Grund, warum die mitgelieferten Skills **kein** `effort:` tragen,
und er gilt unabhängig davon, wie teuer der Wechsel ausfällt: Ein Skill läuft
dann, wenn er aufgerufen wird, nie am Sitzungsanfang. Wer ihm eine Stufe gibt,
hebelt genau die Empfehlung aus, die zwei Absätze weiter oben steht.

Beim `uebergabe`-Skill wäre der Schaden am größten, und das Naheliegende ist
dort zweimal falsch. Er läuft **vor** dem `/clear`, also am Ende der alten
Sitzung bei vollem Kontext — ein Cache-Bruch träfe die teuerste Anfrage
überhaupt. Und sein Inhalt ist der eine Text, bei dem Kürzen etwas kostet:
Was die Übergabe festhält, sind Entscheidungen, Begründungen und verworfene
Wege (`core/prinzip.md`, Regel 4). Eine sparsamere Übergabe ist eine
schlechtere — hier gibt es eine Gegenrechnung, anders als bei der Antwortlänge.

**Offen bleibt die technische Frage** — ob das Aktivieren eines Skills mit
eigener Stufe denselben Cache-Bruch auslöst wie ein Wechsel von Hand. Sie
entscheidet nichts über `uebergabe`, wohl aber über Skills und Subagenten,
die eine **höhere** Stufe brauchen könnten (`feedback/offene-punkte.md`,
Punkt 38). Auf Opus 5.5 und Fable 5.1 spricht die Herstellerangabe dafür, dass
auch dieser Wechsel den Zwischenspeicher erhält; den Frontmatter-Fall nennt
sie aber nicht ausdrücklich.

Quellen: `code.claude.com/docs` → „Model configuration", „Settings reference";
`platform.claude.com` → „Effort". Abgerufen 21.09.2026. Opus 5.5 und Fable
5.1: `code.claude.com/docs` → „Model configuration", „How Claude Code uses
prompt caching"; `platform.claude.com` → „Effort". Abgerufen 24.09.2026.

---

## Alltagsablauf — nenne ihn in Phase 9

Der Teil, der immer gilt:

**Kleine, klar umrissene Änderung:** Direkt fragen. Kein Plan-Modus, kein Gerüst. Die Berechtigungsabfrage ist die Kontrolle.

**Nennenswerte Änderung:** Plan-Modus (Shift+Tab), klären, Vorgehen bestätigen lassen. Erst danach ausführen lassen.

**Fachliches Neuland:** Vorher einmal `grill-with-docs`, falls installiert.

**Falls OpenSpec läuft**, schiebt sich das dazwischen:

1. Plan-Modus, klären
2. `/opsx:propose <name>` — Vorschlag, Specs, Aufgaben entstehen
3. **Den Vorschlag selbst lesen.** Das ist das eigentliche Kontrolltor — eine Markdown-Spec liest sich leichter als ein großer Diff
4. `/opsx:apply`
5. Ergebnis prüfen, `/opsx:archive`

Ein anderes Gerüst hat eigene Kommandos — dann nenne die. Das Profil sagt, welches gewählt wurde, und ergänzt für die Projektart einen Satz zur Nachkontrolle.

**Aufgabe fertig, oder Pause über einer Stunde — ein Wechsel in ein anderes Projekt zählt als Pause:** `/uebergabe`, dann `/clear`. Nicht `/compact`. Der Stand kommt nach `uebergabe/<aufgabe>.md`, damit die Sitzung enden kann, ohne dass Entscheidungen und Begründungen verlorengehen — Werkzeugausgaben gehen dabei absichtlich verloren, die liegen noch auf der Platte.

Das ist keine Sparsamkeitsgeste, sondern der Hebel gegen Wiederholkosten (→ `prinzip.md`): Der Verbrauch wächst quadratisch mit der Sitzungslänge, dieselbe Arbeit auf zwei Sitzungen geteilt kostet die Hälfte. **Nenne in Phase 9, dass `/uebergabe` nur der Nutzer auslösen kann** — der Skill trägt `disable-model-invocation: true`, der Agent kann ihn also vorschlagen, aber nicht selbst starten. Das ist Absicht: was wesentlich war, entscheidet nicht das Werkzeug.

**Auf Langläufer wartest du nicht in der Sitzung.** Build, Crawl, Migration, Reindex: nicht mit `sleep` pollen und wieder nachsehen. Jeder Blick ist eine volle Anfrage mit dem ganzen bisherigen Kontext. In Infrastrukturprojekt A enthielten 12 von 20 Fortschrittsbeobachtungen ein solches Messfenster (Journal 2026-08-21, seit 2026-10-22 in `feedback/archiv/journal-0.19.0-0.23.0.md`). Claude Code bringt zwei Wege mit (`code.claude.com/docs/en/tools-reference`, abgerufen 22.10.2026):

- `run_in_background: true` am Bash-Werkzeug startet den Befehl als Hintergrundaufgabe, und die Sitzung arbeitet weiter. Mit `/tasks` siehst du die Aufgaben und hältst sie an.
- Das Werkzeug `Monitor` meldet jede Ausgabezeile eines Hintergrundbefehls, sobald sie kommt. Seine Frist ist 5 Minuten, höchstens 30.

Läuft der Prozess länger als eine Sitzung, startest du ihn abgesetzt und lässt ihn in eine Datei protokollieren. Das Fertigkriterium kommt in die Übergabe, ausgewertet wird später genau einmal.

**Der Scratchpad ist kein Ablageort.** Claude Code gibt jeder Sitzung einen eigenen Arbeitsordner (Systemprompt: „session-specific"). `/uebergabe` räumt ihn in Schritt 4 mit ab: Was Wert hat, kommt ins Projekt, den Rest bekommt der Nutzer als löschbar genannt. Anlass: Die einzige Kopie einer Rechtesicherung lag zwei Tage nur dort (Journal 2026-10-22, Textprojekt I).
