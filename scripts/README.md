# Script reference

**Use this section to understand exactly what each utility does before running it.** These tools do not log in to a hypervisor/firewall, download Blue Iris, or automatically accept installer dialogs.

| Tool | Purpose | Changes made |
| --- | --- | --- |
| `prepare-prefix.sh` | Creates a dedicated win32 Wine prefix | Creates a new prefix; leaves an existing win32 prefix unchanged; refuses win64. |
| `launch-blue-iris.sh` | Starts the installed legacy version | Launches Wine and writes a private local log, rotated above 5 MiB. |
| `filter-camera-export.py` | Narrows a Windows export to the camera test sections | Writes a new private `.reg` file with cameras disabled. It preserves credentials. It does not import automatically. |
| `configure-test.py` | Sets measured stream paths/dimensions, selected cameras, and local test limits | Dry run by default. `--apply` creates a private registry backup and writes settings in a fully stopped win32 prefix. |
| `check-camera-port.py` | Tests TCP 554 using the local streams JSON | Read-only network probe. An open port is not an authentication/video check. |
| `verify-video.py` | Checks decoded frames in a local H.264/H.265 recording | Read-only. Optional PyAV dependency; best-effort with tested BVRs, not a complete BVR parser. |
| `wine_registry.py` | Shared offline registry helpers | Library used by `configure-test.py`; no standalone action. |

## Private stream settings

Copy `examples/streams.example.json` outside the repository. The example uses reserved documentation addresses; they are deliberately not real cameras. Use names that exactly match your imported registry camera names. The address contains only the host/IP; the path is separate. Enter measured width/height and set `enabled` to true only for the next test group.

The JSON contains no password fields; credentials stay in the local registry. It still reveals your camera names and network addresses, so keep it private. Unlisted camera definitions are disabled by `configure-test.py`. Listed camera definitions keep their credentials and device model while their test fields are updated.

## Examples

```bash
bash scripts/prepare-prefix.sh "$HOME/.local/share/blueiris-wine"
python3 scripts/filter-camera-export.py /private/export.reg /private/camera-only.reg
python3 scripts/check-camera-port.py /private/streams.local.json
python3 scripts/configure-test.py --prefix /private/wine-prefix --streams /private/streams.local.json
python3 scripts/configure-test.py --prefix /private/wine-prefix --streams /private/streams.local.json --apply
bash scripts/launch-blue-iris.sh /private/wine-prefix
.venv/bin/python scripts/verify-video.py /private/finished-clip.bvr
```

No command here should be run against an active production prefix. The configuration helper checks same-user Wine processes before editing, and fails if it cannot inspect them safely. It targets the legacy `system.reg` format and the four existing recording-folder entries; it does not pretend to support arbitrary versions/layouts.

Backups default to `~/.local/state/blueiris-wine/registry-backups`, or the corresponding `XDG_STATE_HOME` directory. They include credentials and are deliberately outside the checkout. Use `--backup-dir` to choose another private location. Keep recordings and backups under their own storage limits; Blue Iris retention does not manage these private backups.
