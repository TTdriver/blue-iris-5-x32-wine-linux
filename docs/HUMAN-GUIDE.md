# Human setup guide

**BI 6 x64 update:** The [BI 6 experiment](BI6-64BIT.md) has its own human instructions, copy-paste AI prompt, native IPHLPAPI workaround, ten-camera recording results, and current UI stability caveat. The material below documents the earlier BI 5 32-bit setup.

**Use this section if you are doing the work yourself.** It explains the steps and why they matter. If you want an AI assistant to do the work, use [AI-PROMPT.md](AI-PROMPT.md) instead.

This guide reconstructs a working legacy setup. Installation was achieved through several experiments, so the exact route below has not yet been repeated as a clean-room installation. Read [TESTED-SETUP.md](TESTED-SETUP.md) before choosing this over a supported Windows installation.

## 1. Check the Linux guest, not just the hypervisor

Run inside the guest:

```bash
cat /etc/os-release
free -h
df -h /
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS
ip -4 address
wine --version
```

The successful test used approximately 8 GB RAM and a 64 GB virtual disk. Earlier, the guest actually saw about 4 GB RAM; adding Blue Iris alongside the desktop and AI application triggered an out-of-memory event that killed the AI application. The VM itself remained running.

If you increase a virtual disk, the partition and filesystem may also need expansion. Check the result with `lsblk` and `df`; do not apply a partition-growth command until you know the guest's disk layout. Recheck guest RAM after changing hypervisor settings or ballooning.

## 2. Install Wine with 32-bit support

On a suitable Ubuntu/Zorin system, inspect the available package versions, then install from your distribution's repositories:

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine wine64 wine32:i386 p7zip-full ripgrep python3
wine --version
```

The observed working version was `wine-10.0 (Ubuntu 10.0~repack-6ubuntu1+zorin5)`. Other distributions or Wine versions are separate tests, not established equivalents.

Create a dedicated prefix so experiments do not alter your other Wine applications:

```bash
export BI_PREFIX="$HOME/.local/share/blueiris-wine"
bash scripts/prepare-prefix.sh "$BI_PREFIX"
```

This prefix must be **win32**. An existing win64 prefix cannot be converted merely by setting `WINEARCH=win32`; use a separate directory.

## 3. Reconstruct the legacy installation

The working route used files obtained from the official vendor:

1. Run the Blue Iris **4.8.6.3** installer in the 32-bit prefix. Complete its interactive setup. Review any license agreement yourself.
2. Extract the vendor's **legacy version-5 32-bit update** into `C:\Program Files\Blue Iris 5` using 7-Zip.
3. Copy four dependencies from the vendor's installed version-4 application folder into the version-5 folder: `SeaMAX.dll`, `ftd2xx.dll`, `msvcr120.dll`, and `msvcp120.dll`.
4. Launch the extracted `BlueIris.exe`. The build that worked was **5.9.9.98**.

With those installer/update files already obtained legitimately, the commands are:

```bash
export WINEPREFIX="$BI_PREFIX"
wine "/path/to/BlueIris-4.8.6.3.exe"

BI_APP="$BI_PREFIX/drive_c/Program Files/Blue Iris 5"
mkdir -p "$BI_APP"
7z x -y "/path/to/legacy-version-5-update32.exe" "-o$BI_APP"
cp "$BI_PREFIX/drive_c/Program Files/Blue Iris 4/"{SeaMAX.dll,ftd2xx.dll,msvcr120.dll,msvcp120.dll} "$BI_APP/"

bash scripts/launch-blue-iris.sh "$BI_PREFIX"
```

Historical official URLs and file hashes are in [TESTED-SETUP.md](TESTED-SETUP.md). Obtain the correct packages from the vendor; the general download button currently points to a newer version. Do not substitute an unrelated DLL download or cracked package.

If the installation folder or a required dependency is missing, stop and inspect the installer result. Some experimental installer runs returned nonzero exit codes despite creating files; an exit code alone was not proof of a usable installation. Do not treat this route as the vendor's supported installation procedure.

The evaluation dialog requires a manual click on startup. This project does not bypass activation or evaluation limits.

## 4. Give the guest a stable address and test camera access

A DHCP reservation worked for this setup. Reserve the guest's actual NIC MAC address, renew the lease or restart the connection, and check the address inside the guest. Choose an unused address consistent with your own DHCP configuration.

If cameras are on another VLAN, the firewall must allow the recorder's **new reserved address** to reach the cameras on the required ports. In this test, the recorder had been missing from an existing camera-client alias. Adding only that address to the existing restricted rule restored camera access.

Test TCP port 554 from the Linux guest. Reachability is separate from camera authentication. An open port does not prove that the credentials or stream path work. HTTP/ONVIF discovery may fail when ports 80 or 8080 are blocked even while RTSP works; do not widen the firewall just to make discovery succeed.

## 5. Migrate camera definitions privately

On the source Windows machine, make a Blue Iris settings backup and retain a copy of the source installation. Export the camera registry branch. For example, in a Windows terminal:

```powershell
reg export "HKLM\Software\Perspective Software\Blue Iris\Cameras" "C:\private\blueiris-cameras.reg" /y
```

Some installations store it under `HKLM\Software\Wow6432Node\Perspective Software\Blue Iris\Cameras`; inspect the actual source before exporting. A newer source version may not be fully compatible with the older target.

Move the export to a **private directory outside your public Git checkout**. It contains camera credentials, even when a password looks encoded. Close Blue Iris and stop Wine for the chosen target prefix before making a backup or importing:

```bash
export WINEPREFIX="$BI_PREFIX"
# Close Blue Iris normally first. This affects only Wine processes in this prefix.
wineserver -k
wineserver -w

mkdir -p "$HOME/.local/state/blueiris-wine/manual-backup"
chmod 700 "$HOME/.local/state/blueiris-wine/manual-backup"
cp "$BI_PREFIX/"{system.reg,user.reg,userdef.reg} "$HOME/.local/state/blueiris-wine/manual-backup/"
chmod 600 "$HOME/.local/state/blueiris-wine/manual-backup/"*.reg

python3 scripts/filter-camera-export.py "/private/source.reg" "/private/camera-only.reg"
wine reg import "$(winepath -w /private/camera-only.reg)"
# Replace /private/camera-only.reg with the actual private output file.
wineserver -k
wineserver -w
```

The filter retains camera definitions plus Clips, Motion, Zones, Overlay, and VFilters. It excludes notification/event/PTZ/output subtrees and disables imported cameras initially. It does not remove credentials: its output must stay private. Review the result locally, especially when migrating from version 6 to version 5. The script is a narrow helper for this export structure, not a complete cross-version migration engine.

## 6. Measure a substream, then fix the cached dimensions

For the tested Reolink cameras, `/h264Preview_01_sub` gave H.264 at 640×360 or 640×480 over RTSP port 554. Verify your own model's path, credentials, and dimensions in a trusted local player such as VLC. Enter credentials locally; do not paste them into public issues or a shareable AI transcript.

Keep the IP/hostname in the address field and the stream path in the path field. Some exported definitions had a path embedded in the IP field; those were separated. Disable hardware acceleration for the first test.

Copy the example JSON to a private location, replacing names and addresses and entering the **measured** dimensions. Select only one camera initially:

```bash
cp examples/streams.example.json /private/streams.local.json
# Edit /private/streams.local.json locally.

python3 scripts/configure-test.py --prefix "$BI_PREFIX" --streams /private/streams.local.json
python3 scripts/configure-test.py --prefix "$BI_PREFIX" --streams /private/streams.local.json --apply
bash scripts/launch-blue-iris.sh "$BI_PREFIX"
```

The first command is a dry run. `--apply` backs up the registry before writing. Wine must be fully stopped before either command. All other imported cameras are disabled unless selected in the JSON. The configuration helper corrects the cached dimensions as well as the stream paths.

## 7. Record locally and verify playback

In Blue Iris, check the recording profile and folder settings. The helper configures continuous recording in the existing seven profile entries, 60-second segments, hardware acceleration off, and transcoding off. These settings are internal legacy registry values; inspect them in the application rather than assuming every build behaves identically. Evaluation restrictions can affect recording behavior.

Use `C:\BlueIris\New`, `Stored`, `Alerts`, `Clipboard`, and `db` for the local test. In the application, verify the database path is `C:\BlueIris\db`; the helper creates this directory but does not rewrite an unknown database-path setting.

Configured caps: New 256 MiB, Stored 1024 MiB, Alerts 512 MiB, Clipboard 256 MiB, totaling 2048 MiB. The helper selects deletion rather than movement for the four managed folders. Retention can remove old files: back up any clips you want to keep before using this test configuration.

Success means all of these happen:

1. The camera displays a live image.
2. A recording file grows.
3. A completed segment plays back with actual video.
4. A later segment is created.
5. Older recordings are deleted when retention runs.

Optional decoder check:

```bash
sudo apt-get install python3-venv
python3 -m venv .venv
.venv/bin/pip install -r requirements-video.txt
.venv/bin/python scripts/verify-video.py "/private/finished-clip.bvr"
```

This is a best-effort raw H.264/H.265 decode check that worked with the tested BVR files, not a general BVR parser. If it fails, use Blue Iris playback or its normal export feature before concluding the recording is corrupt.

## 8. Expand gradually and observe resource use

After one camera passes, test small groups—such as three, six, then ten. Before enabling any camera, save its measured dimensions, even if it was previously disabled. Close the application and verify that Wine has stopped before editing its registry offline.

```bash
ps -C BlueIris.exe -o pid,rss,vsz,etime
free -h
df -h /
```

`rss` and `vsz` are reported in KiB here. Available system RAM and a 32-bit process's virtual address space are different limits. Watch both. Stop adding cameras if either is becoming tight.

Allow at least one cleanup cycle before judging a retention cap: Blue Iris documents database maintenance on a five-minute cycle in its [official manual](https://blueirissoftware.com/BlueIris.PDF). In this test New reached 317 MiB and then fell to 247 MiB. Private backups outside the managed recording folders are not covered by the configured caps.

Leave the NVR/NAS unmounted during this first test. Storage mounting, permissions, startup ordering, and longer-term recording are a separate next phase after the local setup passes.
