# Das Übergabeverfahren in ein anderes Projekt bringen

Das Verfahren besteht aus **zwei Teilen**, und beide werden gebraucht:

| Teil | Wo | Was er kostet |
|---|---|---|
| Der Skill `/uebergabe` | `.claude/skills/uebergabe/SKILL.md` | **nichts**, bis du ihn tippst |
| Drei Zeilen Auslöser | `AGENTS.md` oder `CLAUDE.md` | rund 200 Zeichen je Zug |

Der Skill trägt `disable-model-invocation: true` und liegt deshalb mit keiner
Zeile im Kontext, solange niemand ihn aufruft. Genau deshalb braucht es die
drei Zeilen: **ohne sie erfährt der Agent nie, dass es `/uebergabe` gibt.**
Wer nur den Ordner kopiert, hat ein Werkzeug installiert, das niemand
vorschlägt.

Beleg für die Kostenaussage: code.claude.com/docs, „Extend Claude with
skills", Abschnitt *Control who invokes a skill*, Tabelle „When loaded into
context" (abgerufen 23.08.2026).

---

## Der Weg — vier Schritte

### 1. Ordner kopieren

Quelle ist der Basisagent; die Kopie in diesem Projekt tut es genauso.

```powershell
$quelle = "C:\dev\basisagent-public\core\skills\uebergabe"
$ziel   = "<PFAD-ZUM-PROJEKT>\.claude\skills\uebergabe"

New-Item -ItemType Directory -Force -Path $ziel | Out-Null
Copy-Item "$quelle\*" $ziel -Force
```

**Kopieren, nicht verlinken.** Das Zielprojekt soll laufen, wenn der
Basisagent verschoben, umbenannt oder gelöscht wird.

### 2. Sitzung neu starten

Ohne Neustart kennt Claude Code den Skill nicht. Das ist keine Formalie —
Schritt 3 schlägt sonst fehl und sieht aus wie ein Fehler im Skill.

### 3. `/uebergabe einrichten` aufrufen

Legt `uebergabe/` mit `_vorlage.md` an und gibt die drei Zeilen für die
Regeldatei aus. Der Skill richtet sich selbst ein.

Prüfe dabei, dass `uebergabe/` **nicht** ignoriert wird — anders als ein
Wegwerfordner wie `.tmp/` gehört er in die Versionshistorie. Er ist der
einzige Teil des Projekts, der Entscheidungen und Begründungen festhält.

### 4. Die drei Zeilen eintragen

In `AGENTS.md` bzw. `CLAUDE.md`, wörtlich:

```markdown
## Übergabe
- Neue Aufgabe oder Pause über einer Stunde: `/uebergabe` vorschlagen,
  danach `/clear`. Nicht `/compact`. Ein Wechsel in ein anderes Projekt
  ist so eine Pause.
- Stand je Aufgabe: `uebergabe/<aufgabe>.md`.
```

Dieser Schritt ist **nicht optional**. Siehe oben.

---

## Prüfen, ob es sitzt

**Der Skill kostet nichts:** Nach dem Neustart `/context` aufrufen.
`uebergabe` darf dort **nicht** unter den Skills stehen. Steht er da, fehlt
`disable-model-invocation: true` im Frontmatter — dann bezahlst du die
Beschreibung in jedem Zug.

**Der Auslöser wirkt:** Eine neue Aufgabe beginnen und schauen, ob der Agent
von sich aus auf `/uebergabe` hinweist. Tut er das nicht, fehlt Schritt 4
oder die Zeilen sind umformuliert worden.

**Das Verfahren trägt:** `/uebergabe` tippen. Am Ende soll ein Dateipfad, ein
nächster Schritt und die Empfehlung `/clear` stehen.

---

## Bei einem neuen Projekt

Dann nichts von alledem von Hand: Der Basisagent installiert es in **Phase 5
Schritt 0** als gesetzten Bestandteil und schreibt die drei Zeilen in die
erzeugte Regeldatei. Diese Anleitung ist der Weg für Projekte, die schon
stehen.

---

## Müssen die Übergabedateien aufgeräumt werden?

Ja, aber anders als man erwartet — und viel seltener.

**Eine Übergabe kostet nur, wenn sie gelesen wird.** Eine abgeschlossene
Aufgabe wird nie wieder geöffnet und kostet damit **null**, egal wie dick
ihre Datei ist. Der Ordner darf also wachsen. Es ist ein Archiv, kein
Ballast.

Teuer ist allein die **laufende** Datei. Sie wird zu Sitzungsbeginn gelesen
und läuft damit ab Zug 1 mit — dem teuersten Platz, den es gibt. Gerechnet
an diesem Projekt:

| Datei | Zeichen | Token ca. | über 40 Züge |
|---|---|---|---|
| `statusline.md` | 18.863 | 5.389 | 216k Token-Züge |
| `uebergabe-verfahren.md` | 8.824 | 2.521 | 101k |
| `auswertung.md` | 6.063 | 1.732 | 69k |

Die erste Zeile wäre fast eine komplette Durchschnittsanfrage (252k) — nur
für das Wiederlesen einer einzigen Datei. Sie kostet aber nichts, weil die
Aufgabe erledigt ist und niemand sie mehr aufschlägt.

**Die Regel daraus:** Ab rund **8.000 Zeichen** wird geschnitten, nicht
gekürzt. Aufgabe für beendet erklären, Datei nach `uebergabe/erledigt/`
verschieben, neue Datei anlegen, die unter „Stand" auf die alte verweist.
Der Ordner `erledigt/` ist dabei nur ein Signal an den Menschen und an den
Agenten: *hier wird nicht mehr gelesen.*

**Was du nicht tust:** verdichten, zusammenfassen, löschen. Der Wert einer
alten Übergabe liegt in den verworfenen Wegen und ihren Gründen — genau dem,
was jede Zusammenfassung als Erstes streicht. Eine Entscheidung, die man
nicht mehr begründen kann, wird beim nächsten Mal noch einmal getroffen,
und zwar auf gut Glück.

Und: Ein Fortschreibungs-Abschnitt darf ruhig entstehen. Ein zweiter auch.
Beim dritten ist meist die Aufgabe eine andere geworden als die, die
oben im Ziel steht — das ist der eigentliche Anlass zu schneiden.

---

## Warum überhaupt

Kurz, damit die Installation nicht wie Bürokratie aussieht. Die lange
Fassung mit den Zahlen steht in `core/belege/kontext-messung.md`.

Kontext, der einmal geladen ist, wird bei **jeder** folgenden Anfrage erneut
gelesen und erneut bezahlt. Gemessen über 49 Sitzungen und 4.780 Anfragen
dieses Rechners: rund 60 % des Gesamtaufwands ist wiedergelesener Kontext.
Der Verbrauch wächst **quadratisch** mit der Sitzungslänge — dieselbe Arbeit
auf zwei Sitzungen geteilt kostet die Hälfte.

Beim Beenden verliert man zu drei Vierteln Maschinenverkehr, der noch auf
der Platte liegt und gezielt nachlesbar ist. Nicht wiederbeschaffbar sind
Entscheidungen, Begründungen und verworfene Wege. **Der Fehler ist nie
`/clear`, sondern `/clear` ohne Übergabe.**
