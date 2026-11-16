# Übergabe als Addon — in ein bestehendes Projekt

Dieser Ordner ist mitnehmbar. Er braucht den Basisagenten nicht: `SKILL.md`
ist die ganze Auslieferung, diese Datei nur die Anleitung dazu. Sie wird von
keinem Werkzeug gelesen und kostet nichts.

## Einbau — drei Minuten

1. Diesen Ordner nach `.claude/skills/uebergabe/` im Zielprojekt **kopieren**.
   Keine Verknüpfung: das Projekt soll laufen, wenn diese Quelle weg ist.
2. Neue Sitzung starten. Ohne Neustart kennt Claude Code den Skill nicht.
3. `/uebergabe einrichten` aufrufen. Legt `uebergabe/` mit `_vorlage.md` an
   und nennt die drei Zeilen für die Regeldatei.
4. Die drei Zeilen in `AGENTS.md` oder `CLAUDE.md` eintragen.

Schritt 4 ist **nicht optional**. Ohne ihn erfährt der Agent nie, dass es
`/uebergabe` gibt — der Skill trägt `disable-model-invocation: true` und liegt
deshalb mit keiner Zeile im Kontext, bis jemand ihn tippt.

## Was das kostet

Dauerhaft: die drei Zeilen Auslöser, rund 200 Zeichen je Zug. Sonst nichts —
weder Name noch Beschreibung des Skills stehen im Kontext, solange er nicht
aufgerufen wird. Beleg: code.claude.com/docs, „Extend Claude with skills",
Abschnitt *Control who invokes a skill*, Tabelle „When loaded into context"
(abgerufen 23.08.2026).

Beim Aufruf: der Rumpf von `SKILL.md`, rund 7.200 Zeichen (gemessen am
2026-09-08; die Angabe stand bis dahin bei 5.800 und war schon vor der
Erweiterung um Schritt 4 zu niedrig — gemessen waren es 6.454). Der bleibt dann bis
zum Sitzungsende im Verlauf — was hier fast nichts kostet, weil unmittelbar
danach `/clear` folgt.

Die Übergabedateien selbst kosten nur, wenn sie gelesen werden. Abgeschlossene
Aufgaben werden nicht mehr geöffnet; der Ordner darf also wachsen. Teuer ist
allein die laufende Datei, weil sie zu Sitzungsbeginn gelesen wird und ab
Zug 1 mitläuft — dafür die 8.000-Zeichen-Grenze in `SKILL.md`, Schritt 2.

## Was es nicht tut

Kein Hook, keine Automatik, kein Eingriff. Der Nutzer löst aus, der Agent
schlägt vor. Eine Übergabe zu schreiben heißt zu entscheiden, was wesentlich
war — das darf ein Werkzeug nicht allein tun, und ein Skript kann es nicht.

## Prüfen, ob es sitzt

Nach dem Neustart `/context` aufrufen: `uebergabe` darf dort **nicht** unter
den Skills auftauchen. Taucht er auf, fehlt `disable-model-invocation: true`
im Frontmatter, und du bezahlst die Beschreibung in jedem Zug.

Und im Zielprojekt: eine neue Aufgabe beginnen und schauen, ob der Agent von
sich aus auf `/uebergabe` hinweist. Tut er das nicht, fehlt Schritt 4.
