# Troubleshooting

**Use this section when a step fails.** Work on the failing layer before changing unrelated settings.

| Symptom | Check first | Next action |
| --- | --- | --- |
| No signal; TCP 554 times out | Guest IP, DHCP reservation, routing, firewall source alias, camera power | Restore the narrow intended RTSP access. Do not change credentials to fix a blocked port. |
| TCP 554 works but no video | Authentication, enabled RTSP service, stream path, codec | Test the exact stream in a local player. Keep credentials private. |
| Discovery fails but RTSP works | Discovery/HTTP/ONVIF ports may be blocked | Configure the stream directly if possible; expanding firewall access is a separate decision. |
| Blue Iris exits before its main window | Application version, prefix architecture, missing dependencies | Confirm the legacy route and four vendor DLLs. The current installer did not work in this lab. |
| Ten cameras crash despite substream paths | Cached dimensions on every newly enabled camera | Measure the actual stream and normalize all cached dimensions before enabling it. |
| Desktop or AI application disappears | Kernel OOM log and actual guest-visible RAM | Check resource allocation/ballooning and host pressure. This differs from a Wine-only crash. |
| Wine reports a page fault | Private application log, camera count, VSZ and cached resolution | Roll back to a stable group. Diagnose the specific change; a page fault alone does not prove system OOM. |
| Registry changes disappear | Blue Iris/wineserver still running while offline files were edited | Stop the selected prefix, verify exit, then back up and edit. Live Wine may overwrite offline changes. |
| Database files exist, but no clips | Signal, recording profile, recording enablement and destination | Prove file growth and completed-clip playback; a database is not a recording. |
| Folder exceeds its setting temporarily | Open recordings and maintenance timing | Observe a cleanup cycle. Compare actual file size before and after deletion. |
| Size keeps growing across cleanup cycles | Database accounting, protected clips, folder action/path | Review Storage status and private diagnostics. Do not claim retention is working from saved settings alone. |

## Useful local checks

```bash
free -h
df -h /
ps -C BlueIris.exe -o pid,rss,vsz,etime
journalctl -k -b --no-pager -g 'oom|Out of memory|Killed process|segfault'
```

These outputs can contain private details. Review/redact them before sharing. The launcher writes a local log under `$XDG_STATE_HOME/blueiris-wine`, or `~/.local/state/blueiris-wine` by default.

## Restore the registry backup

Close Blue Iris normally. Stop Wine for the **same prefix**, wait for exit, then copy the backup's `system.reg`, `user.reg`, and `userdef.reg` back into that prefix. Do not mix files from unrelated prefixes. Keep the current files as another private backup first if you may need them later.

`wineserver -k` ends Wine processes in the selected prefix; it can also terminate other applications you put in that prefix. That is why this guide uses a dedicated prefix and checks process exit before editing.

## When to stop the experiment

If the same configuration repeatedly crashes, return to the last group with verified recording. A working Windows installation remains a separate option. Newer Wine, a newer Blue Iris build, a larger camera count, or full-resolution recording each needs its own validation; changing all of them together makes the result harder to interpret.
