#!/usr/bin/env bash
set -euo pipefail
command -v wine >/dev/null || { echo 'Install Wine with 32-bit support first; see docs/HUMAN-GUIDE.md.' >&2; exit 1; }
export WINEPREFIX="$(realpath -m -- "${1:-${HOME}/.local/share/blueiris-wine}")"
if [[ -f "$WINEPREFIX/system.reg" ]]; then
    rg -q '^#arch=win32$' "$WINEPREFIX/system.reg" || { echo 'Existing prefix is not win32; choose a new directory.' >&2; exit 1; }
    echo 'Existing 32-bit prefix found; leaving it unchanged.'
    exit 0
fi
export WINEARCH=win32
export WINEDEBUG=-all
umask 077
wineboot -u
echo 'Created a 32-bit prefix. Install your legitimately obtained Blue Iris package next.'
