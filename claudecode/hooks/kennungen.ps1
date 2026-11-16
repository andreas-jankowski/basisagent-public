#requires -Version 5.1
<#
    PostToolUse-Hook auf Write|Edit an .md-Dateien. Meldet nur, blockiert nie.

    Sucht die Kennungen aus dem neu geschriebenen Text im uebrigen Bestand und
    nennt, wo sie schon vorkommen. Gegenstueck zur Regel "Jede Kennung, die
    erst bei der Arbeit auftaucht, im Bestand suchen" in der Profilvorlage.

    Anlass (Journal 2026-11-02, Textprojekt I): Eine bei der Erhebung gefundene
    Adresse stand in der neuen Doku als "nicht erhoben", obwohl drei Dokumente
    den Host laengst kannten. Gesucht war nach dem Thema, nicht nach der
    Kennung, die erst unterwegs auftauchte.

    Was als Kennung gilt:
      - Begriffe in Backticks ohne Leerzeichen und ohne / oder \
      - seltene Woerter: ab vier Zeichen, im uebrigen Bestand in hoechstens
        $schwelleWort Dokumenten. Das faengt Eigen- und Produktnamen, die
        niemand formatiert. Haeufige Woerter fallen ohne Stoppliste heraus.
      - projektspezifische Muster aus $muster (unten anpassen)
    Muster und Backticks werden nur bis $schwelleSonst Dokumenten gemeldet:
    Was ueberall steht, ist bekannt. Hoechstens 12 Kennungen, je 3 Fundstellen.

    ANPASSEN bei der Einrichtung: nur der Block "Anpassen" unten.

    Testen nur als echter Unterprozess, mit denselben Schaltern wie in
    settings.json (sonst sieht ein stiller Abbruch aus wie "kein Treffer"):
        '{"tool_input":{"file_path":"<projekt>\\docs\\x.md","new_string":"<satz>"}}' |
            powershell -NoProfile -ExecutionPolicy Bypass -File .claude\hooks\kennungen.ps1
#>
$ErrorActionPreference = 'Stop'

# --- Anpassen ----------------------------------------------------------------
# Muster, die die Projektart kennt. Art ist frei, Ohne schliesst Treffer aus.
# Beispiele, je nach Projekt einkommentieren oder ersetzen. Die Datei bleibt
# reines ASCII (PowerShell 5.1 liest sie ohne BOM als ANSI), Sonderzeichen
# deshalb als \uXXXX in die Regex:
#   IT:        @{ Art = 'ip';   Regex = '(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?![\d])'; Ohne = '^(0\.|127\.|255\.)' }
#              @{ Art = 'host'; Regex = '(?i)\b(srv-[a-z0-9][a-z0-9-]*)'; Ohne = '' }
#   Gutachten: @{ Art = 'az';   Regex = '\b(\d{1,2} ?[A-Z][A-Za-z]{0,3} \d{1,5}/\d{2,4})\b'; Ohne = '' }
#              @{ Art = 'norm'; Regex = '((?:Art\.|\u00a7\u00a7?) ?\d+[a-z]?(?: (?:Abs\.|Absatz) ?\d+)?)'; Ohne = '' }
$muster = @(
)
# Ordnernamen, die in jeder Tiefe uebersprungen werden: maschinelle
# Massendaten, Abhaengigkeiten, Build-Ausgaben. Ordner mit Punkt am Anfang
# fallen immer heraus.
$ohneOrdner = @('node_modules', 'vendor', 'dist', 'target', 'rohdaten')
# Eigener Ordner: die ersten $eigenTiefe Pfadteile, wenn die Datei tiefer
# liegt (systeme/<name>/doku.md -> systeme/<name>/), sonst nur die Datei.
# Dass die Doku eines Gegenstands ihn selbst nennt, ist keine Nachricht.
$eigenTiefe = 2
# Sechs, nicht drei: Bei drei fiel im Anlassfall "loki" am selben Tag heraus,
# an dem es in die vierte und fuenfte Datei kam.
$schwelleWort = 6
$schwelleSonst = 10
# -----------------------------------------------------------------------------

try {
    # Als Bytes lesen: PowerShell 5.1 dekodiert [Console]::In in der
    # OEM-Codepage, Umlaute im neuen Text kaemen zerlegt an. Ein BOM
    # (etwa aus einer Testpipe) bricht ConvertFrom-Json, deshalb weg damit.
    $ms = New-Object IO.MemoryStream
    [Console]::OpenStandardInput().CopyTo($ms)
    $roh = [Text.Encoding]::UTF8.GetString($ms.ToArray()).TrimStart([char]0xFEFF)
    if ([string]::IsNullOrWhiteSpace($roh)) { exit 0 }
    $ein = $roh | ConvertFrom-Json

    $pfad = $ein.tool_input.file_path
    if ([string]::IsNullOrWhiteSpace($pfad) -or $pfad -notmatch '\.md$') { exit 0 }
    $neu = $ein.tool_input.new_string
    if ([string]::IsNullOrWhiteSpace($neu)) { $neu = $ein.tool_input.content }
    if ([string]::IsNullOrWhiteSpace($neu)) { exit 0 }

    $wurzel = $env:CLAUDE_PROJECT_DIR
    if ([string]::IsNullOrWhiteSpace($wurzel)) { $wurzel = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent }
    $wurzel = [IO.Path]::GetFullPath($wurzel).TrimEnd('\', '/')
    $voll = [IO.Path]::GetFullPath($pfad)
    if (-not $voll.StartsWith($wurzel + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { exit 0 }
    $rel = ($voll.Substring($wurzel.Length).TrimStart('\', '/') -replace '\\', '/')

    $teile = $rel -split '/'
    $eigen = if ($teile.Count -gt $eigenTiefe) { ($teile[0..($eigenTiefe - 1)] -join '/') + '/' } else { $rel }

    # Frontmatter und Linkziele stoeren nur.
    $text = [regex]::Replace($neu, '(?s)\A---.*?\n---', '')
    $text = [regex]::Replace($text, '\]\([^)]*\)', ']')

    # --- Kennungen -----------------------------------------------------------
    $kand = [ordered]@{}   # kennung (klein) -> art
    function Add-Kand([string]$k, [string]$art) {
        $k = $k.Trim().TrimEnd('.', ',', ';', ':').ToLowerInvariant()
        if ($k.Length -lt 3 -or $kand.Contains($k)) { return }
        $kand[$k] = $art
    }
    foreach ($mu in $muster) {
        foreach ($m in [regex]::Matches($text, $mu.Regex)) {
            $v = $m.Groups[1].Value
            if ($mu.Ohne -and $v -match $mu.Ohne) { continue }
            Add-Kand $v $mu.Art
        }
    }
    foreach ($m in [regex]::Matches($text, '`([^`\s]{3,60})`')) {
        $b = $m.Groups[1].Value
        # Pfade, Optionen, Variablen und blanke Zahlen sind keine Kennung.
        if ($b -notmatch '[/\\]' -and $b -notmatch '^[.~$:-]' -and $b -notmatch '^\d+([.,]\d+)*$') { Add-Kand $b 'backtick' }
    }
    foreach ($m in [regex]::Matches($text, '(?<![\p{L}\p{N}_`-])(\p{L}[\p{L}\p{N}]{3,})(?![\p{L}\p{N}_`-])')) {
        Add-Kand $m.Groups[1].Value 'wort'
    }
    if ($kand.Count -eq 0) { exit 0 }

    # --- Bestand lesen -------------------------------------------------------
    $dateien = New-Object System.Collections.Generic.List[string]
    $stapel = New-Object System.Collections.Generic.Stack[string]
    $stapel.Push($wurzel)
    while ($stapel.Count -gt 0) {
        $d = $stapel.Pop()
        try {
            foreach ($u in [IO.Directory]::EnumerateDirectories($d)) {
                $n = [IO.Path]::GetFileName($u)
                if ($n.StartsWith('.') -or $n -in $ohneOrdner) { continue }
                $stapel.Push($u)
            }
            foreach ($f in [IO.Directory]::EnumerateFiles($d)) {
                if ($f -match '\.(md|txt)$') { $dateien.Add($f) }
            }
        } catch { continue }
    }

    $treffer = @{}
    foreach ($k in $kand.Keys) { $treffer[$k] = New-Object System.Collections.Generic.List[string] }
    foreach ($f in $dateien) {
        $r = ($f.Substring($wurzel.Length).TrimStart('\', '/') -replace '\\', '/')
        if ($r -eq $rel -or $r.StartsWith($eigen, [StringComparison]::OrdinalIgnoreCase)) { continue }
        if ((New-Object IO.FileInfo $f).Length -gt 3MB) { continue }
        # Lesen ueber .NET statt Get-Content: auf Netzfreigaben ein Vielfaches
        # schneller.
        $low = [IO.File]::ReadAllText($f).ToLowerInvariant()
        foreach ($k in $kand.Keys) {
            if ($low.IndexOf($k, [StringComparison]::Ordinal) -lt 0) { continue }
            if ([regex]::IsMatch($low, '(?<![\p{L}\p{N}_])' + [regex]::Escape($k) + '(?![\p{L}\p{N}_])')) { $treffer[$k].Add($r) }
        }
    }

    # --- Auswahl: Muster zuerst, dann Backticks, dann seltene Woerter --------
    $melden = foreach ($k in $kand.Keys) {
        $n = $treffer[$k].Count
        $art = $kand[$k]
        if ($n -eq 0) { continue }
        if ($art -eq 'wort' -and $n -gt $schwelleWort) { continue }
        if ($art -ne 'wort' -and $n -gt $schwelleSonst) { continue }
        $rang = switch ($art) { 'wort' { 2 } 'backtick' { 1 } default { 0 } }
        [pscustomobject]@{ Kennung = $k; Rang = $rang; Anzahl = $n; Orte = $treffer[$k] }
    }
    $melden = @($melden | Sort-Object Rang, Anzahl | Select-Object -First 12)
    if ($melden.Count -eq 0) { exit 0 }

    $zeilen = foreach ($x in $melden) {
        $orte = @($x.Orte | Select-Object -First 3) -join ', '
        if ($x.Anzahl -gt 3) { $orte += " (+$($x.Anzahl - 3))" }
        "$($x.Kennung) -> $orte"
    }
    $hinweis = "Kennungen aus der Aenderung an $rel, die ausserhalb von $eigen schon vorkommen: " +
        ($zeilen -join '; ') +
        ". Lies die Fundstellen, bevor du eine dieser Kennungen als unbekannt, neu oder nicht erhoben beschreibst. Was nicht zum Thema gehoert, uebergehen."

    # PowerShell 5.1 schreibt stdout in der ANSI-Codepage: Nicht-ASCII als
    # \uXXXX ausgeben, sonst kommen Umlaute in Pfaden und Woertern zerlegt an.
    $json = @{ hookSpecificOutput = @{ hookEventName = 'PostToolUse'; additionalContext = $hinweis } } |
        ConvertTo-Json -Depth 4 -Compress
    [regex]::Replace($json, '[^\x00-\x7F]', { param($c) '\u{0:x4}' -f [int][char]$c.Value })
    exit 0
}
catch {
    exit 0
}
