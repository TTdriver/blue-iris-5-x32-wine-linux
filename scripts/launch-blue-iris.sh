#!/usr/bin/env bash
set -euo pipefail
export WINEPREFIX="$(realpath -m -- "${1:-${HOME}/.local/share/blueiris-wine}")"
export WINEDEBUG=-all
APP_DIR="$WINEPREFIX/drive_c/Program Files/Blue Iris 5"
[[ -f "$APP_DIR/BlueIris.exe" ]] || { echo 'Blue Iris 5 was not found in the selected prefix.' >&2; exit 1; }
STATE_DIR="${XDG_STATE_HOME:-${HOME}/.local/state}/blueiris-wine"
mkdir -p -- "$STATE_DIR"
chmod 700 "$STATE_DIR"
LOG="$STATE_DIR/blueiris.log"
if [[ -f "$LOG" && $(stat -c %s -- "$LOG") -gt 5242880 ]]; then
    mv -- "$LOG" "$LOG.previous"
fi
umask 077
cd -- "$APP_DIR"
exec wine ./BlueIris.exe >> "$LOG" 2>&1
