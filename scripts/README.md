# Optional installation and launch helpers

Read each script before running it. Obtain and install your own legitimate BI packages and dependencies using [the human guide](../docs/HUMAN-GUIDE.md).

| Helper | Purpose |
| --- | --- |
| `prepare-prefix.sh [prefix]` | Create a separate `win32` prefix; leave an existing matching prefix unchanged and refuse the other architecture. |
| `launch-blue-iris.sh [prefix]` | Launch the installed BI 5 application, saving a private local log. |

The default prefix is `~/.local/share/blueiris-wine`. The application folder is `drive_c/Program Files/Blue Iris 5` under that prefix.

Use the version-5 application directory shown in the installation guide.

Logs go to `~/.local/state/blueiris-wine/blueiris.log`, or beneath `XDG_STATE_HOME` if set. The previous log is rotated above 5 MiB. Keep logs local.

These helpers use Bash, Wine, Wineboot, ripgrep and standard Linux utilities. Launch from your graphical session. They do not download vendor files or provide autostart or headless operation.
