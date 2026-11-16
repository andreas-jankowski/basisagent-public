#!/usr/bin/env python3
"""Kontextbericht — wertet die Sitzungsprotokolle von Claude Code aus.

Beantwortet ohne Modell und ohne Kontextkosten:
  1. Wohin geht der Verbrauch?          (Anfragen, Cache, Ausgabe)
  2. Welche Sitzungen sind entgleist?   (Kontext je Anfrage)
  3. Wer hat den Kontext gefuellt?      (je Werkzeug: Aufrufe UND Ausgaben)

Aufruf:
    python kontextbericht.py                        Bericht, alle Sitzungen
    python kontextbericht.py --tage 7               nur die letzten 7 Tage
    python kontextbericht.py --projekt Beispiel     nur passende Projekte
    python kontextbericht.py gegenprobe             die /status-Anzeige pruefen
    python kontextbericht.py gegenprobe --stunden 168
    python kontextbericht.py --tage 7 bilanz        was Schnitte sparen

DREI BETRIEBSARTEN, UND SIE FILTERN VERSCHIEDEN. Das ist kein Versehen:

  bericht      filtert ganze SITZUNGEN nach ihrem letzten Zeitstempel.
               Richtig fuer die Frage "wie lief die vergangene Woche".
  gegenprobe   filtert einzelne ANFRAGEN nach ihrem eigenen Zeitstempel.
               Richtig fuer den Vergleich mit dem /status-Bildschirm: eine
               Sitzung, die vor 30 Stunden begann und vor zwei endete,
               gehoert nicht als Ganzes in ein 24-Stunden-Fenster.
  bilanz       filtert PAARE aufeinanderfolgender Sitzungen eines Projekts.
               Ein Paar zaehlt, wenn BEIDE Sitzungen nach ihrem letzten
               Zeitstempel im Fenster liegen -- stundengenau, nicht nach
               Tagesdatum. Paare, deren zweite Sitzung vor dem Ende der
               ersten begann, werden verworfen. --tage gehoert VOR 'bilanz'.

Wer die Betriebsarten vertauscht, bekommt plausible und falsche Zahlen.

Grundlage ist ~/.claude/projects/<projekt>/<sitzung>.jsonl — ein Format, das
Anthropic nicht als Schnittstelle zusichert. Aendert es sich, bricht dieses
Skript mit einer Meldung ab, statt still eine falsche Zahl zu liefern.

Herkunft: entstanden in Werkzeugprojekt A, dort gemessen ueber 49
Sitzungen und 4.780 Anfragen. Siehe belege/kontext-messung.md.
"""
import argparse
import datetime as dt
import glob
import json
import os
import statistics
import sys

# Preisfaktoren, bezogen auf den Preis fuer frische Eingabe (= 1,0).
# Beleg: code.claude.com/docs -> prompt caching: "Cache reads cost ~0.1x base
# input price. Cache writes cost 1.25x for 5-minute TTL, 2x for 1-hour TTL."
# Ausgabe kostet in der ganzen aktuellen Familie das Fuenffache der Eingabe.
F_CACHE_READ = 0.1        # Voreinstellung; Abweichungen je Modell unten
F_CACHE_WRITE = 1.25      # 5-Minuten-Cache
F_CACHE_WRITE_1H = 2.0    # 1-Stunden-Cache
F_AUSGABE = 5.0

# Seit Opus 5.5 und Fable 5.1 haengt der Cache-Lesefaktor am Modell.
# Beleg: platform.claude.com -> Pricing, abgerufen 24.09.2026: "0.025x on
# Claude Fable 5.1 and Claude Mythos 5.1; 0.05x on Claude Opus 5.5".
# Zuordnung ueber den laengsten passenden Praefix -- 'claude-opus-5' darf
# 'claude-opus-5-5' nicht mitfangen. Bis 24.09.2026 galt 0,1x fuer alle; alle
# Messungen davor liegen auf Modellen mit 0,1x (offene-punkte.md, Punkt 42).
F_CACHE_READ_JE_MODELL = {
    'claude-fable-5-1': 0.025,
    'claude-mythos-5-1': 0.025,
    'claude-opus-5-5': 0.05,
    'claude-fable-5': 0.1,
    'claude-mythos-5': 0.1,
    'claude-opus-5': 0.1,
    'claude-opus-4': 0.1,
    'claude-sonnet-5': 0.1,
    'claude-sonnet-4': 0.1,
    'claude-haiku-4': 0.1,
}

ZEICHEN_JE_TOKEN = 4   # Naeherung, nur fuer die Herkunftsanalyse


# ---------------------------------------------------------------- gemeinsam

def tokenzahl(inhalt):
    """Zeichen eines content-Feldes, egal ob Text oder Blockliste."""
    if isinstance(inhalt, str):
        return len(inhalt)
    if inhalt is None:
        return 0
    if isinstance(inhalt, list):
        summe = 0
        for block in inhalt:
            if not isinstance(block, dict):
                summe += len(str(block))
                continue
            for schluessel in ('text', 'thinking'):
                if isinstance(block.get(schluessel), str):
                    summe += len(block[schluessel])
            if block.get('type') == 'tool_result':
                summe += tokenzahl(block.get('content'))
            elif block.get('type') == 'tool_use':
                summe += len(json.dumps(block.get('input', {}), ensure_ascii=False))
        return summe
    return len(json.dumps(inhalt, ensure_ascii=False))


def zeilen(pfad):
    try:
        datei = open(pfad, encoding='utf-8', errors='replace')
    except OSError as fehler:
        print(f"  uebersprungen: {os.path.basename(pfad)} ({fehler})", file=sys.stderr)
        return
    with datei:
        for zeile in datei:
            try:
                yield json.loads(zeile)
            except ValueError:
                continue


def lesefaktor(modell):
    """Cache-Lesefaktor fuer ein Modell: (Faktor, bekannt?)."""
    name = str(modell or '')
    for praefix in sorted(F_CACHE_READ_JE_MODELL, key=len, reverse=True):
        if name.startswith(praefix):
            return F_CACHE_READ_JE_MODELL[praefix], True
    return F_CACHE_READ, False


def aufwand_einer_anfrage(verbrauch, modell=None):
    """(Kontextgroesse, Aufwand) aus einem usage-Feld.

    Cache-Schreiben kostet je nach Haltedauer 1,25x oder 2x. Die Aufteilung
    steht in usage.cache_creation; was dort fehlt, wird als 5-Minuten-Cache
    gezaehlt -- der guenstigere Fall, der Aufwand ist dann eher zu niedrig.
    Cache-Lesen wird mit dem Faktor des Modells gewichtet (lesefaktor).
    """
    frisch = verbrauch.get('input_tokens', 0) or 0
    schreiben = verbrauch.get('cache_creation_input_tokens', 0) or 0
    lesen = verbrauch.get('cache_read_input_tokens', 0) or 0
    ausgabe = verbrauch.get('output_tokens', 0) or 0

    aufteilung = verbrauch.get('cache_creation') or {}
    w1h = aufteilung.get('ephemeral_1h_input_tokens', 0) or 0
    w5m = max(schreiben - w1h, 0)

    kontext = frisch + schreiben + lesen
    aufwand = (frisch
               + w1h * F_CACHE_WRITE_1H
               + w5m * F_CACHE_WRITE
               + lesen * lesefaktor(modell)[0]
               + ausgabe * F_AUSGABE)
    return kontext, aufwand


def kurz(zahl):
    if abs(zahl) >= 1_000_000:
        return f"{zahl / 1_000_000:.1f}M"
    return f"{zahl / 1000:.0f}k"


def wurzel_finden():
    wurzel = os.path.join(os.path.expanduser('~'), '.claude', 'projects')
    if not os.path.isdir(wurzel):
        sys.exit(f"Abbruch: {wurzel} gibt es nicht. Liegen die Protokolle woanders?")
    return wurzel


# ------------------------------------------------------- Betriebsart Bericht

def auswerten(wurzel, seit, filter_projekt):
    sitzungen, brocken = [], []
    # Anfragen je (Modell, Stufe). Die Stufe steht seit den 5er-Modellen je
    # Anfrage im Protokoll (Feld 'effort' neben 'message'); fehlt sie, '-'.
    modell_stufe = {}
    herkunft = {'Werkzeug-Ausgaben': 0, 'Werkzeug-Aufrufe': 0, 'Claude-Text': 0,
                'Deine Eingaben': 0, 'Anhaenge/System': 0}
    # Je Werkzeug beide Seiten: 'ruf' sind die Groessen der einzelnen Aufrufe
    # (fuer Summe, Anzahl und Median), 'aus' die Summe der Ausgaben.
    werkzeuge = {}

    for projekt in sorted(os.listdir(wurzel)):
        ordner = os.path.join(wurzel, projekt)
        if not os.path.isdir(ordner):
            continue
        if filter_projekt and filter_projekt.lower() not in projekt.lower():
            continue
        for pfad in glob.glob(os.path.join(ordner, '*.jsonl')):
            anfragen, offen, art_je_anfrage = {}, {}, {}
            erste = letzte = None
            # Erst je Datei sammeln. Uebernommen wird nur, was den Zeitfilter
            # besteht -- sonst wuerde --tage die Sitzungsliste filtern und die
            # Herkunftsanalyse still nicht.
            h_datei = dict.fromkeys(herkunft, 0)
            b_datei, w_datei = [], {}
            for satz in zeilen(pfad):
                stempel = satz.get('timestamp')
                if stempel:
                    erste = stempel if erste is None or stempel < erste else erste
                    letzte = stempel if letzte is None or stempel > letzte else letzte
                art = satz.get('type')
                nachricht = satz.get('message') or {}

                if art == 'assistant':
                    verbrauch = nachricht.get('usage')
                    kennung = satz.get('requestId')
                    modell = nachricht.get('model')
                    if verbrauch and kennung and kennung not in anfragen:
                        anfragen[kennung] = (verbrauch, modell)
                        art_je_anfrage[kennung] = (str(modell), satz.get('effort') or '-')
                    for block in (nachricht.get('content') or []):
                        if not isinstance(block, dict):
                            continue
                        if block.get('type') == 'text':
                            h_datei['Claude-Text'] += len(block.get('text') or '')
                        elif block.get('type') == 'tool_use':
                            eingabe = block.get('input') or {}
                            groesse = len(json.dumps(eingabe, ensure_ascii=False))
                            h_datei['Werkzeug-Aufrufe'] += groesse
                            # Die Aufrufseite je Werkzeug. Ohne sie ordnet der
                            # Bericht rund 40 % des Werkzeugverkehrs keinem
                            # Werkzeug zu -- und `Write`/`Edit` verschwinden,
                            # obwohl sie zusammen so viel tragen wie `Read`.
                            w_datei.setdefault(
                                block.get('name'), {'ruf': [], 'aus': 0}
                            )['ruf'].append(groesse)
                            ziel = (eingabe.get('file_path') or eingabe.get('command')
                                    or eingabe.get('pattern') or eingabe.get('url') or '')
                            offen[block.get('id')] = (block.get('name'), str(ziel)[:70])

                elif art == 'user':
                    inhalt = nachricht.get('content')
                    ist_ergebnis = isinstance(inhalt, list) and any(
                        isinstance(b, dict) and b.get('type') == 'tool_result'
                        for b in inhalt)
                    if ist_ergebnis:
                        h_datei['Werkzeug-Ausgaben'] += tokenzahl(inhalt)
                        for block in inhalt:
                            if isinstance(block, dict) and block.get('type') == 'tool_result':
                                name, ziel = offen.pop(block.get('tool_use_id'), ('?', ''))
                                menge = tokenzahl(block.get('content'))
                                w_datei.setdefault(
                                    name, {'ruf': [], 'aus': 0})['aus'] += menge
                                b_datei.append((menge, name, ziel, projekt))
                    else:
                        h_datei['Deine Eingaben'] += tokenzahl(inhalt)

                elif art == 'attachment':
                    h_datei['Anhaenge/System'] += tokenzahl(satz.get('attachment'))

            if not anfragen:
                continue
            if seit and (letzte or '') < seit:
                continue
            for schluessel, wert in h_datei.items():
                herkunft[schluessel] += wert
            brocken.extend(b_datei)
            for name, wert in w_datei.items():
                eintrag = werkzeuge.setdefault(name, {'ruf': [], 'aus': 0})
                eintrag['ruf'].extend(wert['ruf'])
                eintrag['aus'] += wert['aus']
            for schluessel in art_je_anfrage.values():
                modell_stufe[schluessel] = modell_stufe.get(schluessel, 0) + 1

            summe = lambda feld: sum(v.get(feld, 0) or 0 for v, _ in anfragen.values())

            w1h = w5m = wrest = 0
            for v, _ in anfragen.values():
                aufteilung = v.get('cache_creation') or {}
                eine_stunde = aufteilung.get('ephemeral_1h_input_tokens', 0) or 0
                fuenf_min = aufteilung.get('ephemeral_5m_input_tokens', 0) or 0
                w1h += eine_stunde
                w5m += fuenf_min
                wrest += max((v.get('cache_creation_input_tokens', 0) or 0)
                             - eine_stunde - fuenf_min, 0)
            groessen = [aufwand_einer_anfrage(v, m)[0] for v, m in anfragen.values()]
            sitzungen.append({
                'projekt': projekt, 'n': len(anfragen),
                'frisch': summe('input_tokens'),
                'cache_w': summe('cache_creation_input_tokens'),
                'w1h': w1h, 'w5m': w5m, 'wrest': wrest,
                'cache_r': summe('cache_read_input_tokens'),
                'cache_r_aufwand': sum((v.get('cache_read_input_tokens', 0) or 0)
                                       * lesefaktor(m)[0]
                                       for v, m in anfragen.values()),
                'ausgabe': summe('output_tokens'),
                'max_kontext': max(groessen), 'schnitt': sum(groessen) // len(groessen),
                'hoch': sum(1 for g in groessen if g > 100_000),
                'beginn': (erste or '')[:10],
                'zuletzt': (letzte or '')[:10],
            })
    return sitzungen, brocken, herkunft, werkzeuge, modell_stufe


def modelle_ausgeben(modell_stufe):
    """Modelle und Stufen im Fenster -- ohne sie ist kein Vorher/Nachher lesbar."""
    print("\n== Modelle und Aufwandstufen (Anfragen) ==")
    for (modell, stufe), n in sorted(modell_stufe.items(), key=lambda x: -x[1]):
        faktor, bekannt = lesefaktor(modell)
        hinweis = '' if bekannt else '  <-- unbekannt, 0,1x angenommen'
        print(f"{modell[:28]:28}{stufe:>8}{n:>8}   Cache lesen {faktor:g}x{hinweis}")
    if len({m for m, _ in modell_stufe}) > 1 or len({s for _, s in modell_stufe}) > 1:
        print("Mehr als ein Modell oder eine Stufe im Fenster: Ein Vergleich zweier "
              "Zeitraeume misst dann auch diesen Wechsel.")


def bericht_ausgeben(argumente):
    wurzel = wurzel_finden()
    seit = None
    if argumente.tage:
        seit = (dt.datetime.now(dt.timezone.utc)
                - dt.timedelta(days=argumente.tage)).isoformat()[:10]

    sitzungen, brocken, herkunft, werkzeuge, modell_stufe = auswerten(
        wurzel, seit, argumente.projekt)

    if not sitzungen:
        sys.exit("Abbruch: keine Sitzung mit Verbrauchsdaten gefunden. Entweder passt "
                 "der Filter nicht, oder das Protokollformat hat sich geaendert "
                 "(erwartet wird 'message.usage' in Zeilen mit type=assistant).")

    g = lambda feld: sum(s[feld] for s in sitzungen)
    anfragen, hoch = g('n'), g('hoch')
    aufwand = {
        'frische Eingabe': g('frisch') * 1.0,
        'Cache geschrieben': (g('w1h') * F_CACHE_WRITE_1H
                              + (g('w5m') + g('wrest')) * F_CACHE_WRITE),
        'Cache gelesen': g('cache_r_aufwand'),
        'Ausgabe': g('ausgabe') * F_AUSGABE,
    }
    gesamt = sum(aufwand.values()) or 1

    zeitraum = f"letzte {argumente.tage} Tage" if argumente.tage else "alle Sitzungen"
    print(f"== Verbrauch ({zeitraum}, {len(sitzungen)} Sitzungen, {anfragen} Anfragen) ==")
    print(f"{'':22}{'Tokens':>10}{'Aufwand*':>12}{'Anteil':>9}")
    for name, wert in sorted(aufwand.items(), key=lambda x: -x[1]):
        roh = {'frische Eingabe': g('frisch'), 'Cache geschrieben': g('cache_w'),
               'Cache gelesen': g('cache_r'), 'Ausgabe': g('ausgabe')}[name]
        print(f"{name:22}{kurz(roh):>10}{kurz(wert):>12}{100 * wert / gesamt:>8.1f} %")
    print("* in Einheiten frischer Eingabe: Cache lesen je Modell (0,1x; Opus 5.5 0,05x; "
          "Fable 5.1 0,025x), Ausgabe 5x")
    print(f"  Cache-Schreiben aufgeteilt: {kurz(g('w1h'))} mit 1-Std-Haltedauer (2,0x), "
          f"{kurz(g('w5m'))} mit 5-Min (1,25x)"
          + (f", {kurz(g('wrest'))} ohne Angabe (als 1,25x gezaehlt)"
             if g('wrest') else ""))
    print(f"\nAnfragen ueber 100k Kontext: {hoch} von {anfragen} "
          f"({100 * hoch / max(anfragen, 1):.0f} %)")
    schnitt = sum(s['schnitt'] * s['n'] for s in sitzungen) // max(anfragen, 1)
    print(f"Mitgeschleppter Kontext je Anfrage im Schnitt: {kurz(schnitt)} Token")
    modelle_ausgeben(modell_stufe)

    print("\n== Sitzungen mit dem groessten Kontext ==")
    print(f"{'Projekt':30}{'Anf':>5}{'max':>8}{'Schnitt':>9}{'>100k':>7}  zuletzt")
    for s in sorted(sitzungen, key=lambda s: -s['max_kontext'])[:10]:
        print(f"{s['projekt'][:30]:30}{s['n']:>5}{kurz(s['max_kontext']):>8}"
              f"{kurz(s['schnitt']):>9}{s['hoch']:>7}  {s['zuletzt']}")

    print("\n== Woraus der Kontext besteht (geschaetzt: Zeichen/4) ==")
    summe_h = sum(herkunft.values()) or 1
    for name, wert in sorted(herkunft.items(), key=lambda x: -x[1]):
        print(f"{name:22}{kurz(wert // ZEICHEN_JE_TOKEN):>10}{100 * wert / summe_h:>8.1f} %")
    print("Hinweis: Claudes Denkschritte sind im Protokoll nicht im Klartext "
          "enthalten und fehlen daher hier.")

    if brocken:
        print(f"\n== Die {argumente.brocken} groessten einzelnen Werkzeugausgaben ==")
        for menge, name, ziel, projekt in sorted(brocken, reverse=True)[:argumente.brocken]:
            print(f"{kurz(menge // ZEICHEN_JE_TOKEN):>6} | {str(name)[:12]:12} | "
                  f"{projekt[:20]:20} | {ziel[:50]}")

    if werkzeuge:
        # Beide Seiten je Werkzeug. Nur die Ausgaben zu zaehlen -- so war es bis
        # 25.08.2026 -- verschiebt die Rangfolge: `Write` und `Edit` bringen ihren
        # Inhalt im AUFRUF mit und haben eine winzige Ausgabe ("File updated").
        zusammen = {n: sum(w['ruf']) + w['aus'] for n, w in werkzeuge.items()}
        gesamt_w = sum(zusammen.values()) or 1
        ruf_gesamt = sum(sum(w['ruf']) for w in werkzeuge.values())
        print("\n== Welches Werkzeug fuellt den Kontext am meisten ==")
        print(f"{'Werkzeug':18}{'n':>6}{'Aufrufe':>9}{'Median':>8}"
              f"{'Ausgaben':>10}{'zusammen':>10}{'Anteil':>8}")
        for name in sorted(zusammen, key=lambda n: -zusammen[n])[:8]:
            w = werkzeuge[name]
            median = statistics.median(w['ruf']) if w['ruf'] else 0
            print(f"{str(name)[:18]:18}{len(w['ruf']):>6}"
                  f"{kurz(sum(w['ruf']) // ZEICHEN_JE_TOKEN):>9}"
                  f"{int(median) // ZEICHEN_JE_TOKEN:>8}"
                  f"{kurz(w['aus'] // ZEICHEN_JE_TOKEN):>10}"
                  f"{kurz(zusammen[name] // ZEICHEN_JE_TOKEN):>10}"
                  f"{100 * zusammen[name] / gesamt_w:>7.1f} %")
        print(f"Aufrufseite: {kurz(ruf_gesamt // ZEICHEN_JE_TOKEN)} von "
              f"{kurz(gesamt_w // ZEICHEN_JE_TOKEN)} = "
              f"{100 * ruf_gesamt / gesamt_w:.0f} % des Werkzeugverkehrs. "
              "'n' und 'Median' beziehen sich auf die Aufrufe.")


# ---------------------------------------------------- Betriebsart Gegenprobe

def anfragen_sammeln(wurzel, seit):
    """Je requestId einmal: (Kontextgroesse, Aufwand, Projekt, Modell, Stufe)."""
    gefunden = {}
    for pfad in glob.glob(os.path.join(wurzel, '*', '*.jsonl')):
        projekt = os.path.basename(os.path.dirname(pfad))
        for satz in zeilen(pfad):
            if satz.get('type') != 'assistant':
                continue
            if (satz.get('timestamp') or '') < seit:
                continue
            nachricht = satz.get('message') or {}
            verbrauch = nachricht.get('usage')
            kennung = satz.get('requestId')
            modell = nachricht.get('model')
            # <synthetic> sind lokal erzeugte Nachrichten, keine bezahlte
            # Anfrage. Sie tragen trotzdem ein usage-Feld.
            if not verbrauch or not kennung or modell == '<synthetic>':
                continue
            if kennung in gefunden:
                continue
            kontext, aufwand = aufwand_einer_anfrage(verbrauch, modell)
            gefunden[kennung] = (kontext, aufwand, projekt, modell,
                                 satz.get('effort') or '-')
    return list(gefunden.values())


def gegenprobe_ausgeben(argumente):
    """Prueft die Zeile "NN% of your usage was at >150k context" aus /status.

    Claude Code nennt dort als Quelle "local sessions on this machine" --
    dieselben Protokolle. Die Zahl wird in ZWEI Gewichtungen ausgegeben:
    nach Anzahl der Anfragen und nach Aufwand. Welche der Anzeige entspricht,
    ist der eigentliche Befund.
    """
    wurzel = wurzel_finden()
    seit = (dt.datetime.now(dt.timezone.utc)
            - dt.timedelta(hours=argumente.stunden)).isoformat()
    werte = anfragen_sammeln(wurzel, seit)

    if not werte:
        sys.exit(f"Abbruch: keine Anfrage in den letzten {argumente.stunden} "
                 "Stunden gefunden. Entweder war die Zeit ueber ruhig, oder das "
                 "Protokollformat hat sich geaendert (erwartet wird 'message.usage' "
                 "und 'requestId' in Zeilen mit type=assistant).")

    unbekannt = sorted({str(m) for _, _, _, m, _ in werte if not lesefaktor(m)[1]})
    if unbekannt:
        print(f"Achtung: Modelle ohne Eintrag in F_CACHE_READ_JE_MODELL "
              f"({', '.join(unbekannt)}). Fuer sie gilt 0,1x; die Aufwandsspalte "
              "ist dort geraten.\n", file=sys.stderr)

    anzahl = len(werte)
    aufwand_gesamt = sum(a for _, a, _, _, _ in werte)

    print(f"== Anteil hoher Kontexte (letzte {argumente.stunden} h, "
          f"{anzahl} Anfragen) ==")
    print(f"{'Schwelle':>10}{'der Anfragen':>16}{'des Aufwands':>16}")
    for k in sorted({100, argumente.schwelle, 200}):
        treffer = [(kon, auf) for kon, auf, _, _, _ in werte if kon > k * 1000]
        anteil_n = 100 * len(treffer) / anzahl
        anteil_a = 100 * sum(a for _, a in treffer) / max(aufwand_gesamt, 1)
        marke = ' <-- Anzeige' if k == argumente.schwelle else ''
        print(f"{'>' + str(k) + 'k':>10}{anteil_n:>14.1f} %{anteil_a:>14.1f} %{marke}")

    schnitt = sum(kon for kon, _, _, _, _ in werte) // anzahl
    print(f"\nKontext je Anfrage im Schnitt: {schnitt // 1000}k Token")
    print("Aufwand* = frische Eingabe 1,0x, Cache schreiben 1,25x/2,0x, "
          "Cache lesen je Modell (0,1x; Opus 5.5 0,05x; Fable 5.1 0,025x), Ausgabe 5,0x")

    modell_stufe = {}
    for _, _, _, modell, stufe in werte:
        schluessel = (str(modell), stufe)
        modell_stufe[schluessel] = modell_stufe.get(schluessel, 0) + 1
    modelle_ausgeben(modell_stufe)

    je_projekt = {}
    for _, auf, projekt, _, _ in werte:
        eintrag = je_projekt.setdefault(projekt, [0, 0.0])
        eintrag[0] += 1
        eintrag[1] += auf
    print("\n== Woher der Aufwand kam ==")
    for projekt, (n, auf) in sorted(je_projekt.items(), key=lambda x: -x[1][1]):
        print(f"{projekt[:40]:40}{n:>6} Anfragen"
              f"{100 * auf / max(aufwand_gesamt, 1):>8.1f} %")


# ------------------------------------------------------- Betriebsart Bilanz

BAENDER = ((0, 150_000, '0-150k'), (150_000, 275_000, '150-275k'),
           (275_000, float('inf'), '>275k'))
KOSTEN_ANFRAGEN = 12   # Median eines Uebergabe-Vorgangs, gemessen 2026-08-24


def ist_uebergabe_aufruf(satz):
    """Ein echter Aufruf von /uebergabe, keine Erwaehnung.

    Zwei Formen zaehlen: der Befehl des Nutzers (type=user, Klartext mit
    '<command-name>/uebergabe</command-name>') und der Skill-Aufruf des
    Modells (tool_use 'Skill' mit skill='uebergabe'). Nicht zaehlen
    Werkzeugausgaben, die den Text enthalten -- core/belege/README.md selbst
    tut das --, und die Zeilen type=api-request-blob, die den Befehl als
    Kopie tragen. Am 2026-09-01 hat eine Klartextsuche 7 von 18 Sitzungen
    falsch zugeordnet und das Ergebnis von 2,73x auf 3,79x verschoben: Im
    Basisagenten wird ueber den Skill geredet, ohne ihn aufzurufen.
    """
    nachricht = satz.get('message') or {}
    inhalt = nachricht.get('content')
    if satz.get('type') == 'user':
        return isinstance(inhalt, str) and '<command-name>/uebergabe</command-name>' in inhalt
    if satz.get('type') == 'assistant' and isinstance(inhalt, list):
        return any(isinstance(b, dict) and b.get('type') == 'tool_use'
                   and b.get('name') == 'Skill'
                   and str((b.get('input') or {}).get('skill', '')).split(':')[-1] == 'uebergabe'
                   for b in inhalt)
    return False


def ist_clear(satz):
    inhalt = (satz.get('message') or {}).get('content')
    return (satz.get('type') == 'user' and isinstance(inhalt, str)
            and '<command-name>/clear</command-name>' in inhalt)


def sitzung_lesen(pfad):
    """Anfragen in Dateireihenfolge und die Merkmale fuer die Bilanz."""
    anfragen, gesehen = [], set()
    erste = letzte = None
    uebergabe_zeilen, clear_zeile, zeilen_n = [], None, 0
    for nummer, satz in enumerate(zeilen(pfad), 1):
        zeilen_n = nummer
        stempel = satz.get('timestamp')
        if stempel:
            erste = stempel if erste is None or stempel < erste else erste
            letzte = stempel if letzte is None or stempel > letzte else letzte
        if ist_uebergabe_aufruf(satz):
            uebergabe_zeilen.append(nummer)
        # /clear eroeffnet die neue Datei (README, "Falle in der
        # Protokollstruktur"). Gezaehlt wird es vor der ersten Anfrage, nicht
        # bis Zeile 5: Seit Oktober 2026 stehen davor Kopfzeilen wie
        # type=mode und type=cost-state, und /clear rutscht bis Zeile 20.
        if clear_zeile is None and not anfragen and ist_clear(satz):
            clear_zeile = nummer
        if satz.get('type') != 'assistant':
            continue
        nachricht = satz.get('message') or {}
        verbrauch, kennung = nachricht.get('usage'), satz.get('requestId')
        modell = nachricht.get('model')
        if not verbrauch or not kennung or modell == '<synthetic>' or kennung in gesehen:
            continue
        gesehen.add(kennung)
        kontext, aufwand = aufwand_einer_anfrage(verbrauch, modell)
        anfragen.append((kontext, aufwand, lesefaktor(modell)[0]))
    return {'anfragen': anfragen, 'erste': erste, 'letzte': letzte,
            'uebergabe': [z / max(zeilen_n, 1) for z in uebergabe_zeilen],
            'clear': clear_zeile}


def schnitte_sammeln(wurzel, seit, filter_projekt):
    """Verkettete Paare (A, B) je Projekt, A endet vor dem Beginn von B."""
    schnitte, verworfen = [], 0
    for projekt in sorted(os.listdir(wurzel)):
        ordner = os.path.join(wurzel, projekt)
        if not os.path.isdir(ordner):
            continue
        if filter_projekt and filter_projekt.lower() not in projekt.lower():
            continue
        sitzungen = [s for s in (sitzung_lesen(p)
                                 for p in glob.glob(os.path.join(ordner, '*.jsonl')))
                     if s['anfragen'] and s['erste'] and s['letzte']]
        sitzungen.sort(key=lambda s: s['erste'])
        for a, b in zip(sitzungen, sitzungen[1:]):
            # Fenster: beide Sitzungen nach ihrem LETZTEN Zeitstempel, wie im
            # Bericht. Ein Paar, dessen A vor dem Fenster endet, fehlt also.
            if seit and (a['letzte'] < seit or b['letzte'] < seit):
                continue
            # Ueberlappung: B begann, bevor A endete -- zwei parallele
            # Sitzungen, kein Schnitt.
            if b['erste'] < a['letzte']:
                verworfen += 1
                continue
            ende_a = a['anfragen'][-1][0]
            # Je Anfrage von B: Was haette sie ohne Schnitt mehr mitgeschleppt?
            # Nur der Teil ueber ihrem eigenen Stand (max(0, ...)), und als
            # Cache-Lesung gewichtet -- roh gerechnet war die Zahl 2026-08-25
            # um Faktor 10 zu gut.
            gespart = sum(max(0, ende_a - kontext) * faktor
                          for kontext, _, faktor in b['anfragen'])
            kosten = sum(auf for _, auf, _ in a['anfragen'][-KOSTEN_ANFRAGEN:])
            schnitte.append({
                'projekt': projekt, 'ende_a': ende_a,
                'ende_b': b['anfragen'][-1][0],
                'gespart': gespart, 'kosten': kosten,
                'faktor': gespart / kosten if kosten else 0.0,
                # Nur ein Aufruf in der zweiten Haelfte von A zaehlt: Die
                # Uebergabe soll die Sitzung beenden, nicht in ihr laufen.
                'uebergabe': any(pos >= 0.5 for pos in a['uebergabe']),
                'clear_b': b['clear'] is not None,
            })
    return schnitte, verworfen


def bilanz_ausgeben(argumente):
    """Was ein Schnitt spart, getrennt nach Schnitten mit und ohne Uebergabe."""
    wurzel = wurzel_finden()
    seit = None
    if argumente.tage:
        seit = (dt.datetime.now(dt.timezone.utc)
                - dt.timedelta(days=argumente.tage)).isoformat()
    schnitte, verworfen = schnitte_sammeln(wurzel, seit, argumente.projekt)
    if not schnitte:
        sys.exit("Abbruch: kein verkettetes Sitzungspaar gefunden. Entweder passt "
                 "der Filter nicht, oder das Protokollformat hat sich geaendert.")

    gruppen = {'mit Uebergabe': [s for s in schnitte if s['uebergabe']],
               'ohne': [s for s in schnitte if not s['uebergabe']]}
    zeitraum = f"letzte {argumente.tage} Tage" if argumente.tage else "alle Sitzungen"
    print(f"== Schnittbilanz ({zeitraum}, {len(schnitte)} Schnitte in "
          f"{len({s['projekt'] for s in schnitte})} Projekten, "
          f"{verworfen} ueberlappende Paare verworfen) ==")

    def zeile(titel, werte):
        print(f"{titel:30}" + ''.join(f"{w:>16}" for w in werte))

    def median(liste):
        return statistics.median(liste) if liste else None

    zeile('', gruppen.keys())
    g = gruppen.values()
    zeile('Schnitte', [len(x) for x in g])
    zeile('Faktor gesamt', [f"{sum(s['gespart'] for s in x) / max(sum(s['kosten'] for s in x), 1):.2f}x"
                            for x in g])
    zeile('Median je Schnitt', [f"{median([s['faktor'] for s in x]):.2f}x" if x else '-'
                                for x in g])
    zeile('Fehlschlaege (unter 1,0x)', [f"{sum(s['faktor'] < 1 for s in x)} von {len(x)}"
                                        for x in g])
    zeile('netto (Aufwandseinheiten)', [kurz(sum(s['gespart'] - s['kosten'] for s in x))
                                        for x in g])
    zeile('Kontext bei Schnitt, Median', [kurz(median([s['ende_a'] for s in x])) if x else '-'
                                          for x in g])
    zeile('Ende B hoeher als Ende A', [f"{sum(s['ende_b'] > s['ende_a'] for s in x)} von {len(x)}"
                                       for x in g])
    zeile('B beginnt mit /clear', [f"{sum(s['clear_b'] for s in x)} von {len(x)}"
                                            for x in g])

    print("\n== Auf den Kontextstand kontrolliert ==")
    print(f"{'Kontext bei Schnitt':20}{'n mit':>7}{'Median mit':>12}{'n ohne':>8}"
          f"{'Median ohne':>13}{'Kosten mit':>12}{'Kosten ohne':>13}")
    for unten, oben, name in BAENDER:
        teil = {k: [s for s in v if unten <= s['ende_a'] < oben] for k, v in gruppen.items()}
        mit, ohne = teil['mit Uebergabe'], teil['ohne']
        f = lambda x, feld, fmt: fmt(median([s[feld] for s in x])) if x else '-'
        print(f"{name:20}{len(mit):>7}{f(mit, 'faktor', lambda m: f'{m:.2f}x'):>12}"
              f"{len(ohne):>8}{f(ohne, 'faktor', lambda m: f'{m:.2f}x'):>13}"
              f"{f(mit, 'kosten', kurz):>12}{f(ohne, 'kosten', kurz):>13}")

    anteil = 100 * len(gruppen['mit Uebergabe']) / len(schnitte)
    print(f"\nNutzungsrate: {anteil:.0f} % der Schnitte tragen eine Uebergabe.")
    print("Annahme, nicht belegt: B ist dieselbe Arbeit, die ohne Schnitt in A "
          "weitergelaufen waere. Kosten = Aufwand der letzten "
          f"{KOSTEN_ANFRAGEN} Anfragen von A.")


# ------------------------------------------------------------------- Einstieg

def hauptteil():
    zerleger = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    zerleger.add_argument('--tage', type=int, help='nur Sitzungen der letzten N Tage')
    zerleger.add_argument('--projekt', help='nur Projekte, deren Name das enthaelt')
    zerleger.add_argument('--brocken', type=int, default=12,
                          help='wie viele Einzelausgaben auflisten (Standard 12)')

    unter = zerleger.add_subparsers(dest='betriebsart')
    gegen = unter.add_parser('gegenprobe',
                             help='die /status-Anzeige gegen die Protokolle pruefen')
    gegen.add_argument('--stunden', type=int, default=24,
                       help='Fenster in Stunden (Standard 24, wie die Anzeige)')
    gegen.add_argument('--schwelle', type=int, default=150,
                       help='Kontextschwelle in Tausend Token (Standard 150)')

    unter.add_parser('bilanz',
                     help='was ein Schnitt spart, mit und ohne Uebergabe')

    argumente = zerleger.parse_args()
    if argumente.betriebsart == 'gegenprobe':
        gegenprobe_ausgeben(argumente)
    elif argumente.betriebsart == 'bilanz':
        bilanz_ausgeben(argumente)
    else:
        bericht_ausgeben(argumente)


if __name__ == '__main__':
    hauptteil()
