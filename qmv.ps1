<#
.SYNOPSIS
    Bulk-rename files by editing their names in a text editor -- a qmv(1) equivalent
    for Windows, where GNU renameutils isn't available.

.DESCRIPTION
    Writes the filenames in a directory to a temp file, opens it in your editor and
    blocks until you save and close. Each line is renamed to whatever you changed it
    to. Line order is the mapping, so don't add, remove, or reorder lines.

    Renames happen in two phases via temp names, so swaps and cycles (a->b, b->a)
    work correctly instead of clobbering each other.

.PARAMETER Path
    Directory to rename in. Defaults to the current directory.

.PARAMETER Filter
    Wildcard filter, e.g. '*.png'. Defaults to everything.

.PARAMETER Directories
    Rename subdirectory names instead of files.

.PARAMETER Editor
    Editor command. Defaults to $env:EDITOR, else 'subl -w' if Sublime is on PATH,
    else notepad. Must block until the file is closed -- hence -w for Sublime.

.PARAMETER DryRun
    Print the renames without performing them.

.EXAMPLE
    .\qmv.ps1 -Path .\design\03_design\exports -Filter *.png

.EXAMPLE
    .\qmv.ps1 -Directories -DryRun
#>
[CmdletBinding()]
param(
    [string]$Path = '.',
    [string]$Filter = '*',
    [switch]$Directories,
    [string]$Editor,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Resolve-Editor {
    if ($Editor) { return $Editor }
    if ($env:EDITOR) { return $env:EDITOR }
    if (Get-Command subl -ErrorAction SilentlyContinue) { return 'subl -w' }
    return 'notepad'
}

# Split "subl -w" or '"C:\path with spaces\subl.exe" -w' into exe + args.
function Split-EditorCommand([string]$cmd) {
    if ($cmd.StartsWith('"')) {
        $end = $cmd.IndexOf('"', 1)
        $exe = $cmd.Substring(1, $end - 1)
        $rest = $cmd.Substring($end + 1).Trim()
    } else {
        $parts = $cmd -split '\s+', 2
        $exe = $parts[0]
        if ($parts.Count -gt 1) { $rest = $parts[1] } else { $rest = '' }
    }
    return @{ Exe = $exe; Args = $rest }
}

$dir = (Resolve-Path -LiteralPath $Path).ProviderPath

if ($Directories) {
    $items = Get-ChildItem -LiteralPath $dir -Filter $Filter -Directory | Sort-Object Name
} else {
    $items = Get-ChildItem -LiteralPath $dir -Filter $Filter -File | Sort-Object Name
}

if (-not $items) {
    Write-Host "Nothing to rename in $dir (filter '$Filter')." -ForegroundColor Yellow
    return
}

$original = @($items | ForEach-Object { $_.Name })

$tempFile = [System.IO.Path]::Combine(
    [System.IO.Path]::GetTempPath(),
    "qmv_$([guid]::NewGuid().ToString('N').Substring(0,8)).txt")

# UTF-8 without BOM -- editors and the read-back path both handle it cleanly.
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($tempFile, $original, $utf8)

$ed = Split-EditorCommand (Resolve-Editor)
Write-Host "Opening $($original.Count) name(s) in: $($ed.Exe) $($ed.Args)" -ForegroundColor Cyan
Write-Host "Save and close the file to apply." -ForegroundColor DarkGray

try {
    $argList = @()
    if ($ed.Args) { $argList += $ed.Args -split '\s+' }
    $argList += $tempFile
    Start-Process -FilePath $ed.Exe -ArgumentList $argList -Wait -NoNewWindow

    $edited = @([System.IO.File]::ReadAllLines($tempFile, $utf8))

    # Trailing blank line from an editor's final newline is expected; drop just that.
    while ($edited.Count -gt $original.Count -and $edited[-1] -eq '') {
        $edited = $edited[0..($edited.Count - 2)]
    }

    if ($edited.Count -ne $original.Count) {
        throw "Line count changed ($($original.Count) -> $($edited.Count)). Lines are the mapping -- don't add or remove any. Aborted, nothing renamed."
    }

    # ---- validate before touching the filesystem -------------------------------
    $pairs = @()
    for ($i = 0; $i -lt $original.Count; $i++) {
        $new = $edited[$i].Trim()
        if ($new -eq '') { throw "Line $($i + 1) is empty (was '$($original[$i])'). Aborted, nothing renamed." }
        if ($new -match '[\\/:*?"<>|]') { throw "Line $($i + 1) ('$new') contains characters not allowed in a filename. This renames only -- it can't move between folders. Aborted." }
        if ($new -ne $original[$i]) {
            $pairs += [pscustomobject]@{ Old = $original[$i]; New = $new }
        }
    }

    if (-not $pairs) {
        Write-Host "No changes." -ForegroundColor Yellow
        return
    }

    $dupes = $edited | Group-Object | Where-Object { $_.Count -gt 1 }
    if ($dupes) { throw "Duplicate target name(s): $(($dupes | ForEach-Object { $_.Name }) -join ', '). Aborted, nothing renamed." }

    # A target may collide with an existing file only if that file is itself moving.
    $moving = @($pairs | ForEach-Object { $_.Old })
    foreach ($p in $pairs) {
        $target = Join-Path $dir $p.New
        if ((Test-Path -LiteralPath $target) -and ($moving -notcontains $p.New)) {
            throw "'$($p.New)' already exists and isn't being renamed away. Aborted, nothing renamed."
        }
    }

    # ---- apply -----------------------------------------------------------------
    foreach ($p in $pairs) { Write-Host "  $($p.Old)  ->  $($p.New)" }

    if ($DryRun) {
        Write-Host "[dry-run] $($pairs.Count) rename(s) not applied." -ForegroundColor Yellow
        return
    }

    # Two phases so swaps and cycles don't clobber each other.
    $stamp = [guid]::NewGuid().ToString('N').Substring(0, 8)
    $staged = @()
    foreach ($p in $pairs) {
        $tmpName = "qmv_tmp_${stamp}_$($staged.Count)"
        Rename-Item -LiteralPath (Join-Path $dir $p.Old) -NewName $tmpName
        $staged += [pscustomobject]@{ Temp = $tmpName; New = $p.New }
    }
    foreach ($s in $staged) {
        Rename-Item -LiteralPath (Join-Path $dir $s.Temp) -NewName $s.New
    }

    Write-Host "Renamed $($pairs.Count) item(s)." -ForegroundColor Green
}
finally {
    Remove-Item -LiteralPath $tempFile -Force -ErrorAction SilentlyContinue
}
