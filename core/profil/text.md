# Profil — Textprojekte

Ergänzt `core/runbook.md`. Gilt für Recherche, Gutachten, Bewertung, Security-Analyse — alles, wo das Ergebnis ein Dokument ist und kein lauffähiges Programm.

Wo das Runbook `→ Profil` schreibt, gilt der Inhalt von hier. Das Werkzeugverhalten steht weiter im Adapter; die beiden Achsen sind unabhängig.

**Die Ausprägung** — Recherche, Gutachten, Bewertung, Security — verändert **nur** den `Rahmen`-Block der Vorlage und einzelne Berechtigungen. Nicht den Ablauf. Wenn du versucht bist, für eine Ausprägung eine eigene Phase zu bauen, ist die Annahme falsch.

---

## Phase 0 — zusätzlich ermitteln

- **Welche Dokumente existieren**, in welchen Formaten. Liegen Entwurf und Endfassung nebeneinander? Dann klären: **welche gilt.**
- **Gibt es eine Quellenablage** — Belegsammlung, PDF-Ordner, Linkliste, `quellen.md`?
- **Ist eine Zitierweise erkennbar?** Fußnoten, Klammerzitate, reine Links? Uneinheitlich ist der Normalfall — dann ist das eine Entscheidung für Phase 2, keine Bestandsaufnahme.
- **Existiert ein Glossar** oder eine Begriffsliste?
- **Worauf bezieht sich das Material zeitlich?** Ein Datum im Dokument, ein Gesetzesstand, eine Rahmenwerk-Edition. Das wird das Feld `Sachstand zum`.
- **Liegen personenbezogene, mandats- oder systembezogene Daten im Verzeichnis?** Fallakten, Exporte, Scans, Netzpläne, Zugangsdaten. Das bestimmt Phase 1 und ist der wichtigste Befund dieser Phase.

**Ausprägung raten und mitfragen.** Anhaltspunkte:

| Befund | Ausprägung |
|---|---|
| Linksammlungen, Vergleichstabellen, offene Fragen | Recherche |
| Paragrafen, Aktenzeichen, Sachverhalt/Würdigung-Struktur | Gutachten |
| Kriterienliste, Punkte, Gewichtungen, Vergleichsobjekte | Bewertung |
| CVE, CVSS, Netzpläne, Rahmenwerk-Kürzel, Prüfumfang | Security |

Die Frage in Phase 0 nennt beides in einem Satz: *„Ich stufe das als bestehendes Textprojekt (Gutachten) ein. Stimmt das?"*

**Was du hier nicht suchst:** `package.json`, Testbefehle, Paketmanager. Wenn du in einem Gutachtenordner nach `Cargo.toml` greppst, hast du die Projektart falsch bestimmt.

---

## Phase 1 — Berechtigungen

**Die Gewichte sind umgekehrt.** Bei Codeprojekten ist das Freigeben von Test- und Lintbefehlen die Arbeit. Hier gibt es fast nichts freizugeben — dafür ist das **Sperren** die eigentliche Aufgabe, und es ist wichtiger als bei Code.

### Freigeben

Wenig. Falls das Projekt Konvertierung braucht — `pandoc`, ein PDF-Werkzeug — gib genau die Befehle frei, die tatsächlich auftauchten. Baue keine Vorratsliste.

### Sperren — hier liegt der Ertrag

**1. Ausgehendes fragt immer.** Web-Suche und Web-Abruf bleiben auf `ask`, auch wenn es nervt. Die allgemeine Vorlage gibt die Web-Suche frei (Nutzerentscheidung vom 2026-10-12) — hier verschiebst du sie zurück: Claude Code `WebSearch` von `allow` nach `ask`.

Begründung, die du dem Nutzer nennst: Bei Codeprojekten ist eine Websuche harmlos. Hier kann die Suchanfrage selbst der Schaden sein — ein Mandantenname, eine Systembezeichnung, ein Aktenzeichen im Klartext an einen fremden Dienst. Das ist nicht rückholbar und fällt niemandem auf.

**1b. Externen Quellbestand gegen Veränderung sperren.** Der häufigere Fall als der unter Punkt 2: Das Material darf **gelesen** werden, aber nie verändert. Punkt 2 behandelt nur, was gar nicht gelesen werden darf.

Das Muster dafür — Leserecht auf den Pfad, `Edit`-Sperre darauf, **und** Sperren für `mv`, `cp` und ihre PowerShell-Gegenstücke — steht im Adapter unter „Externer Quellbestand". Ohne die Befehlssperren ist der Bestand gegen Ändern geschützt und gegen Verschieben offen, und in der Berechtigungsdatei sieht das nach vollständigem Schutz aus. Hol es dort, statt es hier nachzubauen.

**2. Sensible Verzeichnisse vom Lesen ausschließen.** Das Gegenstück zu `.env` bei Codeprojekten, aber breiter. Nimm die in Phase 0 gefundenen Orte, nicht eine geratene Liste. Typisch: Fallakten, Mandatsordner, Rohexporte, Scans, Netzpläne, Zugangsdaten.

Frag einzeln nach — manches davon *muss* der Agent lesen können, sonst kann er nicht arbeiten. Der Unterschied ist: lesen dürfen, aber nicht nach draußen geben. Punkt 1 trägt diese Trennung.

**3. Bei Ausprägung Security zusätzlich:** Gefundene Artefakte werden **nie ausgeführt**. Samples, Skripte, Binärdateien aus einem Analyse- oder Fundverzeichnis sind Untersuchungsgegenstand, nicht Werkzeug. Sperre die Ausführung aus diesen Pfaden hart — nicht `ask`, sondern `deny`. Eine Rückfrage, die man um 23 Uhr wegklickt, ist hier keine Schranke.

**Denk daran, was der Adapter über Sperren sagt.** Bei Claude Code gilt: erst `deny`, dann `ask`, dann `allow` — eine Sperre lässt sich später nicht durch eine enge Freigabe aufweichen. Formuliere sie entsprechend eng, sonst musst du sie wieder anfassen.

---

## Phase 2 — Vorlage

Vorlage: **`core/profil/text/AGENTS.md.tpl`**. Lies sie samt Kommentarblock am Ende; der Kommentar wird nicht in die erzeugte Datei übernommen.

Zwei Felder im `Rahmen` verdienen eine eigene Rückfrage, weil sie sich nicht ablesen lassen und geraten schädlich sind:

- **`Sachstand zum`** — ein absolutes Datum. Nie „aktuell", nie „heute". Eine Rechtslage und ein CVSS-Score altern; ein Testbefehl tut das nicht. Ohne dieses Feld weiß in vier Monaten niemand, ob eine Aussage im Dokument noch gilt.
- **`Adressat`** — verändert jeden Satz. Ohne ihn schreibt der Agent für einen gedachten Fachkollegen, also für niemanden.

Die Klassifikation aus Phase 2b gilt unverändert, nur die Beispiele verschieben sich: **A** ist die Zitierweise und der verbindliche Quellenstand, **B** ist alles Sachliche über den Gegenstand — Vorgeschichte, Beteiligte, Systemlandschaft.

---

## Phase 3 — Ablaufgerüst

**Voreinstellung für Textprojekte: keines.** Bei Code trägt ein Gerüst, weil eine Änderung Dateien über das ganze Repo verteilt berührt. Ein Dokument hat seine Gliederung in sich — das Gerüst dupliziert sie dann nur.

Trotzdem vorlegen, nicht vorentscheiden. Höchstens eines:

| | Wofür | Auswahlkriterium |
|---|---|---|
| **keines** | Gliederung steht im Dokument, Ablage regelt der `Rahmen` | Voreinstellung. Ein Dokument, überschaubarer Umfang |
| **`to-spec` + `to-tickets`** | Gliederung als Spec, Abschnitte als Arbeitspakete | Umfangreicher Bericht, über mehrere Sitzungen, mehrere Zulieferungen |
| **OpenSpec** | Vorschlag → Delta → Aufgaben, mit Archiv | Nur wenn Fassungen nachvollziehbar bleiben müssen — eine Bewertung, die später angegriffen werden kann |

**`implement` gehört nicht dazu.** Es setzt Tickets in Code um. Bei `to-spec` + `to-tickets` endet die Kette hier, und du sagst das dazu — sonst installiert der Nutzer das dritte mit.

**Prüfe die Skill-Namen vor der Installationsanweisung.** Die Liste ändert sich. Sieh nach, was tatsächlich angeboten wird, statt diesen Namen zu vertrauen — das ist dieselbe Regel wie bei OpenSpec und dem Ort des Projektkontexts.

---

## Phase 4 — Projektkontext und Quellenverzeichnis

Ohne Gerüst gibt es keinen vorgegebenen Ort für den Kontext. Frag nach — Vorschlag `projekt.md` neben den Dokumenten, nicht in einem Unterordner, den niemand aufmacht.

Dorthin gehört Kategorie B aus Phase 2b: Vorgeschichte, Beteiligte, Abgrenzung des Prüfumfangs, verworfene Fragestellungen. Alles, was man einmal wissen muss und nicht in jedem Zug.

Der Rest der Phase — Dopplungen prüfen, Altdateien einzeln durchgehen, Parkplatz auflösen — gilt unverändert.

### Zusätzlicher Schritt: `quellen.md` anbieten

**Dieser Schritt stand früher in Phase 3 und fiel dort durch.** Bei der Voreinstellung „kein Gerüst" liest man die Optionstabelle, entscheidet, und ist aus der Phase heraus — alles darunter wird nicht mehr gelesen. Hier steht er richtig, weil in dieser Phase ohnehin Dateien angelegt werden.

> Soll ich eine `quellen.md` anlegen? Eine Zeile pro Beleg — Kurzkennung, vollständige Angabe, Fassung, Abrufdatum, Ablageort. Der Text zitiert dann die Kurzkennung.
>
> Das kostet keinen Kontext, weil die Datei nur gelesen wird, wenn ein Beleg zu prüfen ist. Und es macht die Nachher-Prüfung aus `AGENTS.md` überhaupt erst durchführbar: Ohne festen Ort für die Belege kann der Agent sie nicht gegenprüfen.

Sie ist das Gegenstück zur Lockfile — die Stelle, an der steht, worauf sich das Ergebnis stützt.

#### Wenn der Bestand neu, fremd und ungesichtet ist

**Dann ist dieser Schritt nicht durchführbar, und das ist kein Mangel.** Die Belege liegen in fremden Dokumenten, die du nach Verhaltensregel 7 nicht öffnest. Du müsstest die Regel brechen, um den Schritt auszuführen.

Der Befund, aus dem dieser Schritt stammt, kam aus einem **bestehenden** Textprojekt: Dort waren die Belege in Gebrauch und ihre Fassungen aus vorhandener Arbeit ablesbar. Bei einem neuen Projekt mit Altbestand gilt stattdessen:

- **`quellen.md` als Struktur anlegen, nicht füllen.** Spaltenköpfe, ein Beispielsatz, sonst nichts.
- **Das Feld `Verbindliche Quellen` verweisend formulieren, nicht behauptend.** Es zeigt auf `quellen.md`, statt eine Fassung zu nennen. Gerade hier ist die Versuchung am größten, eine Fassung aus einem Ordnernamen zu erschließen — es gibt ja nichts anderes zu lesen. Genau das nicht tun.
- **Die Korrektur als ersten Punkt nach der Einrichtung vormerken**, mit Datum, in den offenen Punkten aus Phase 9.

Der Prüfpunkt in Phase 9 ist dafür gefasst: belegt **oder** ausdrücklich verweisend mit vorgemerkter Korrektur. Beides ist erfüllt, keines ist ein Mangel.

**Und sie korrigiert Phase 2.** Beim Füllen von `quellen.md` siehst du die Belege zum ersten Mal genau. Geh danach zurück auf das Feld **`Verbindliche Quellen`** in `AGENTS.md` und prüfe die Fassungsangabe: Was du in Phase 2 aus einem Ordnernamen erschlossen hast, steht oft anders in den Dateinamen. Eine falsche Fassung in einer Zeile, die in jedem Zug gilt, ist der teuerste Einzelfehler dieser Projektart — und sie fällt nie von selbst auf.

Zeig die Korrektur und lass sie bestätigen, auch wenn sie klein aussieht.

---

## Phase 5 — Skills

**Der Regelfall bei Textprojekten ist ein eigener Skill, nicht einer aus dem Katalog.** Das ist gemessen, nicht vermutet: In zwei Projekten lagen alle drei Katalogvorschläge schon vor — einmal global installiert, einmal projektlokal und unsichtbar — und der Katalog lieferte beide Male nichts. Getragen hat beide Male ein projekteigener Skill.

Deshalb steht der Abschnitt „Eigene Skills" hier **vor** dem Katalog. Der Katalog ist der Nachschlag, nicht der Einstieg.

### Eigene Skills — hier anfangen

**Den Auslöser leitest du aus vorhandener Arbeit ab, nicht aus einer Liste.** Such nach Wiederholung:

- Hast du in diesem Projekt dasselbe Verfahren schon zweimal von Hand nachgebaut?
- Gibt es eine Aufgabenliste mit vielen gleichartigen offenen Posten — fünfzehn Checklisten nach demselben Muster, zwanzig Fälle nach demselben Schema?
- Ist aus einer früheren Sitzung eine Nutzerpräferenz zum Vorgehen dokumentiert?

**Das ist oft schon in Phase 0 sichtbar.** Wenn du dort auf eine Liste gleichartiger offener Posten stößt, merk sie dir.

**Aber: Aus Dateinamen und Ordnerstrukturen lässt sich Wiederholung nicht belegen, nur vermuten.** Zehn Dateien nach gleichem Muster beweisen, dass jemand zehnmal etwas **abgelegt** hat — nicht, dass er zehnmal dasselbe Verfahren **durchlaufen** hat. Der Unterschied ist von außen unsichtbar: Ein Ordner mit gleichartigen Dateien sieht identisch aus, ob ein Verfahren dahintersteht oder ob jemand gesammelt hat.

Das ist gemessen: In einem Projekt wurden auf diesem Weg drei Kandidaten gefunden und alle drei mit einem Satz des Nutzers widerlegt — abgelegte Momentaufnahmen ohne Verfahren, deren Aktualität er selbst bezweifelte.

**Belegt ist Wiederholung erst**, wenn ein Verfahren erkennbar ist — eine Vorlage, eine Checkliste, eine zweimal gleich durchlaufene Reihenfolge — **oder wenn der Nutzer sie bestätigt.**

Praktisch: Kandidaten in Phase 0 notieren, vor Phase 5 **gegen den Nutzer** prüfen, nicht gegen die Dateiliste. Ein Skill aus einer falsch erschlossenen Wiederholung erzwingt ein Schema, das nie jemand benutzt hat.

Die Grenze ist dieselbe wie überall im Template:

| | Gehört wohin |
|---|---|
| Ein **wiederkehrendes Verfahren** — Quellenprüfung nach festem Schema, Bewertung entlang eines Kriterienkatalogs, Berichtsaufbau nach Vorgabe | Skill. Wird geladen, wenn er dran ist |
| Eine **Regel, die immer gilt** — Zitierweise, Tonfall, Belegpflicht | `AGENTS.md`. Als Skill kostet sie doppelt |

Ziel ist `.claude/skills/<name>/SKILL.md`, wie bei allen anderen.

### Der Katalog — als Nachschlag

**Sag dem Nutzer offen, dass er dünn ist.** Die verfügbaren Skill-Sammlungen sind für Codearbeit gebaut. Das ist keine Lücke, die du mit Ungefährem füllst — ein Skill ohne Auslöser kostet in jedem Zug und trägt nichts.

**Prüfe zuerst, ob er schon da ist.** Drei Fälle, in denen der Katalog nichts liefert, und alle drei sind vorgekommen: schon global installiert (dann ins Projekt kopieren, Runbook Phase 5 Schritt 1), kein Auslöser, oder — der tückischste — er liegt projektlokal und ist **unsichtbar**, weil die Verknüpfung nach `.claude/skills/` fehlt. Für den dritten Fall gilt die Sichtbarkeitsprüfung aus Phase 6; zieh sie hier schon vor, wenn du einen Skill im Verzeichnis siehst, aber nicht in deiner eigenen Skill-Liste.

#### Was tatsächlich passt

| Skill | Vorschlagen wenn |
|---|---|
| `research` | Primärquellen sind in großer Menge zu beschaffen. **Mit Vorbehalt:** Die Belegpflicht, die sein Rumpf mitbringt, steht schon in der Textvorlage unter „Beim Schreiben". Neu dazu kommt nur die Delegation an einen Hintergrundagenten, und die war in der einzigen Messung teurer als die Arbeit in der Hauptsitzung (→ `core/prinzip.md`, vierter Hebel). Vorschlagen nur, wenn der Nutzer die Delegation ausdrücklich will und Hilfsagenten in Phase 1 erlaubt hat. Rumpf geprüft am 23.09.2026 (`mattpocock/skills`, `skills/engineering/research/SKILL.md`) |
| `grill-with-docs` | Fachliches Neuland, unklare Begriffe, oder eine schwer umkehrbare Festlegung steht an — Prüfumfang, Bewertungsmaßstab, Abgrenzung |
| `domain-modeling` | Fremdes Fachgebiet, und die Begriffe müssen laufend sauber bleiben |
| `to-questionnaire` | Beteiligte oder Fachleute sollen etwas **asynchron ausfüllen** — häufig bei Gremien-, Erhebungs- und Bewertungsprojekten |

**Geprüft, aber ohne Auslöser** — damit der nächste Agent sie nicht neu recherchieren muss: `teach` (Mehrsitzungs-Unterricht mit dem Projektverzeichnis als Arbeitsbereich), `handoff` (Gespräch in ein Übergabedokument), `triage` und `wayfinder` (beide an einen Issue-Tracker gebunden, also code-nah).

**Zum Umfang der Sammlung:** `mattpocock/skills` enthält rund 25 Skills, nicht die vier hier. Neun sind reine Code-Skills, vier Router- oder Meta-Skills, die das Runbook ausschließt. Der Rest ist geprüft und steht oben. **Sieh trotzdem selbst nach** — die Liste ändert sich, und diese Aufstellung ist von August 2026.

Bei `grill-with-docs` derselbe Hinweis wie im Codeprofil: **einmal gebraucht.** Danach stehen Glossar und Entscheidungsvermerke in Dateien, und der Skill kostet nur noch. Entweder er kann weg — die Dateien bleiben — oder er wird so ausgezeichnet, dass er nur noch per `/name` läuft (→ Adapter, Phase 6); dann bleibt er verfügbar, statt beim nächsten Bedarf neu installiert zu werden.

**Und er ist ein Wrapper.** Sein Rumpf ruft `grilling` und `domain-modeling` auf. Ohne beide läuft er nicht, und das fällt bei der Sichtbarkeitsprüfung **nicht** auf, weil der Wrapper selbst korrekt liegt und aufrufbar ist. `domain-modeling` steht in der Tabelle darüber als eigener Vorschlag — hier ist es Abhängigkeit, nicht Alternative. Beide gehören in dieselbe Installationsauswahl.

#### Was du nicht vorschlägst, und warum

`tdd`, `diagnosing-bugs`, `code-review`, `resolving-merge-conflicts`, `codebase-design`, `prototype`, `implement` — sie setzen eine Codebasis voraus. Wenn der Nutzer danach fragt, sag den Grund, nicht nur nein.

Dazu unverändert aus dem Runbook: keine Router- und Meta-Skills, keine Regelwerke, die immer gelten sollen, keine kompletten Sammlungen. Ein Plugin ist dabei nicht Alles-oder-nichts — → Adapter, Phase 6.

---

## Phase 9 — zusätzliche Prüfpunkte

Ergänzend zur Liste im Runbook:

- [ ] `Sachstand zum` ist ein absolutes Datum, kein „aktuell"
- [ ] `Verbindliche Quellen` nennen eine Fassung, **und die ist aus `quellen.md` belegt, nicht aus einem Ordnernamen erschlossen**
- [ ] `Adressat` ist ausgefüllt
- [ ] `Stil und Form` ist ausgefüllt oder bewusst weggelassen
- [ ] Web-Abruf und Web-Suche stehen auf `ask`, nicht auf `allow`
- [ ] Die in Phase 0 gefundenen sensiblen Orte sind gesperrt
- [ ] Bei Security: Ausführung aus Fund- und Analyseverzeichnissen ist `deny`, nicht `ask`
- [ ] `quellen.md` existiert oder wurde bewusst abgelehnt

**Beim Alltagsablauf in Phase 9** nenne den einen Satz, der diese Projektart trägt:

> Prüfe die Belege, bevor du das Dokument weitergibst. Der Agent hält sich an die Belegpflicht, aber eine Fundstelle, die er nicht öffnen konnte, ist als Lücke gekennzeichnet und keine Prüfung. Die Lückenliste am Dokumentende ist dafür da, gelesen zu werden.
