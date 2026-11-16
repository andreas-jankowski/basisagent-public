@AGENTS.md

<!--
Hier steht nur, was ausschließlich Claude Code betrifft — oft ist das
nichts, und die Datei bleibt bei der Importzeile allein. Dann diesen
Kommentar entfernen. Sonst darunter:

## Nur für Claude Code
<...>


HINWEISE FÜR DEN EINRICHTENDEN AGENTEN — nicht übernehmen.

1. `@AGENTS.md` wird beim Start expandiert, als stünde der Inhalt inline.
   `AGENTS.md` bleibt damit die einzige Quelle der Regeln und
   werkzeugneutral: Ein späteres zweites Werkzeug liest sie ohne Umbau.

2. Nichts hier hineinschreiben, was auch ohne Claude Code gelten würde.
   Das gehört nach `AGENTS.md`. Doppelte Pflege ist der häufigste Fehler
   in dieser Konstruktion.

3. Wenn kein Inhalt übrig bleibt, ist eine Datei mit nur `@AGENTS.md` das
   richtige Ergebnis. Nichts dazuerfinden.

4. Schreibsperren gehören nicht hierher. Anweisungsdateien sind Kontext,
   keine erzwungene Konfiguration. Wer harte Sperren will, braucht
   `deny`-Regeln in `.claude/settings.json` — dem Nutzer sagen, nicht
   ungefragt setzen.
-->
