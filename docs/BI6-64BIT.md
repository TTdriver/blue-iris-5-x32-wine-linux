# Blue Iris 6 x64: experimental Wine setup

## What this section is for

This is the newer 64-bit experiment. Use it if you want to reproduce BI 6 startup and recording under Wine. The main human guide records the earlier BI 5 32-bit setup and remains useful as a fallback. Neither experiment establishes overnight reliability.

## What worked

On October 9, 2026, Blue Iris **6.1.3.10 x64** opened on Zorin OS 18.1 with the host **Wine 10.0**. All ten cameras produced local BVR recordings. Completed clips from the current ten-camera launch each decoded to 100 H.264 frames at 640×360 or 640×480, with ten distinct sampled frames per camera. BI 6 used approximately 1 GB resident memory during this short test. The duplicate BI 5 recorder was then stopped, with its separate prefix and launcher preserved as a fallback.

The startup workaround was an app-local native Windows **iphlpapi.dll**, used alongside the complete native Microsoft **14.51.36247 x64 VC/MFC runtime**. Earlier camera-free Bottles/Soda/Caffe, Proton/UMU, and Lutris Wine-GE tests exited before opening the UI. We have not repeated those runner tests with this DLL workaround.

## For people doing the setup

1. Keep your existing working recorder and prefix as a fallback. Create a separate 64-bit prefix and install legitimately obtained BI 6 and Microsoft's x64 Visual C++ runtime. This experiment used a clone of a full BI installation in its own prefix; a fresh end-to-end installation has not yet been reproduced.
2. Confirm that the main executable and runtime are x64. Keep the complete matching VC/MFC runtime together; copying only one runtime DLL did not solve the earlier startup failures.
3. Obtain `iphlpapi.dll` from the **System32** directory of your own authorized 64-bit Windows installation. System32 contains the 64-bit DLL; SysWOW64 contains the 32-bit version. Place your private copy beside the BI executable. Do not download arbitrary DLLs or commit this file to GitHub. Its use remains subject to Microsoft's license terms.
4. Launch with the override shown below. Use your actual prefix and install path.
5. Dismiss the normal evaluation Demo dialog. Start with one camera and verify live video, a growing recording, and playback of a completed clip before enabling more cameras.
6. Use measured low-resolution streams initially. Correct all cached camera dimensions as described in the [main guide](HUMAN-GUIDE.md), disable hardware acceleration for the initial test, and keep recording on a small local storage budget. Do not import license keys or replace your production recorder's settings.

```bash
export WINEPREFIX="$HOME/.local/share/wineprefixes/blue-iris-6"
export WINEDEBUG=-all
export WINEDLLOVERRIDES='iphlpapi,mfc140,mfc140u,msvcp140,msvcp140_1,msvcp140_2,msvcp140_atomic_wait,msvcp140_codecvt_ids,vcruntime140,vcruntime140_1,vcruntime140_threads,concrt140,vcamp140,vcomp140,vccorlib140=n,b'
cd "$WINEPREFIX/drive_c/Program Files/Blue Iris"
wine ./BlueIris.exe
```

Use a launcher that survives closure of your terminal if you want recording to continue. Our live experiment uses a separate user-systemd service with a 2.5 GiB memory ceiling and a short stop deadline. A memory ceiling is a safeguard, not a sizing recommendation for full-resolution recording.

## For people using an AI assistant

Copy this prompt into your own assistant and provide environment details privately:

```text
Help reproduce the experimental Blue Iris 6 x64 Wine setup described in this
repository. First inspect my Linux/Wine version, RAM, disk and existing recorder.
Preserve my working recorder and create a separate win64 prefix. Use my own
legitimate BI installation and complete matching Microsoft x64 VC/MFC runtime.
If BI exits during startup, test the documented native IPHLPAPI workaround using
System32/iphlpapi.dll from my own authorized x64 Windows installation, placed
beside BlueIris.exe with the documented native overrides. Do not redistribute
vendor DLLs, patch BI, bypass its demo/licensing, or expose credentials.
Start camera-free, then test one measured low-resolution RTSP camera. Verify a
growing recording and decoded changing frames from a completed clip. Expand
cameras only after checking memory and recording. Keep a small local storage
budget and verify cleanup; do not mount my NAS or change production camera or
Windows-recorder settings without explicit instructions. Preserve a fallback
and report exact versions, observed results and anything still untested.
```

## Limits of the result

The workaround enabled startup and ten-camera recording; the exact failing IPHLPAPI export or behavior has not been identified. Thread-context and exception probes passed both native Windows and Wine, so the handled single-step exception alone did not explain the failure. No diagnostic shim is required by the working launch command.

The tested native IPHLPAPI file was AMD64, 220,528 bytes, SHA-256
`8521026d021cc5193a7cd7c0256bd14c7ab39738d22c019e6d544b37deee12c0`.
Other Windows DLL versions have not been tested. Full-resolution recording,
hardware acceleration, every BI feature, reboot recovery and overnight stability
remain unverified.
