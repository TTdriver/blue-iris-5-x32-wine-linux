# What was tested and how the working setup was reached

**BI 6 x64 update:** The [BI 6 experiment](BI6-64BIT.md) has its own human instructions, copy-paste AI prompt, native IPHLPAPI workaround, ten-camera recording results, and current UI stability caveat. The material below documents the earlier BI 5 32-bit setup.

**Use this section to assess the evidence and reproduce the installation history.** It is a lab record, not a claim that every attempted step was necessary.

## Observed working environment

| Component | Observed value |
| --- | --- |
| Guest OS | Zorin OS 18.1, Ubuntu Noble base |
| Wine | 10.0, Zorin package `10.0~repack-6ubuntu1+zorin5` |
| Prefix | `#arch=win32` |
| Blue Iris | 5.9.9.98, 32-bit evaluation |
| Source configuration | Windows Blue Iris 6.1.3.9; camera definitions selectively migrated |
| Hypervisor | Proxmox |
| Guest resources after expansion | About 8 GB RAM; 64 GB disk; root filesystem expanded to about 63 GB |
| Cameras | Ten Reolink cameras |
| Tested stream | H.264 RTSP substream, TCP port 554 |
| Recorded resolutions | 640×360 and 640×480 |
| Stable observation after final fix | Roughly six minutes; all ten cameras recorded multiple segments |
| Process memory during final observation | Settled near 1.0 GB resident and 1.9 GB virtual |

## The installation route actually used

The initial current-version Blue Iris installer created an installation but its application exited at startup. Wine 9, Wine 10, Windows compatibility changes, Visual C++ runtime experiments, and Wine Staging 11.19 were explored. They did not establish a working version-6 installation. These failed experiments are not dependencies of the successful legacy route.

The successful route used a new 32-bit prefix, a vendor version-4 installation, and the extracted vendor version-5 update. Four DLLs from `Program Files/Blue Iris 4` were copied into `Program Files/Blue Iris 5`:

```text
SeaMAX.dll
ftd2xx.dll
msvcr120.dll
msvcp120.dll
```

The update had been extracted with 7-Zip into the version-5 folder. Launching its executable through system Wine 10 produced the working 5.9.9.98 application. The prefix has no custom Wine DLL overrides in its final recorded user registry. The earlier `vcrun2019` experiment targeted a different unsuccessful prefix; it should not be presented as a proven prerequisite for the final one.

### Historical vendor files

These URLs were used in the original session. They are included for provenance; availability and the content behind a rolling URL can change. The vendor's [updates page](https://blueirissoftware.com/?page_id=344) exposes its legacy 32-bit update link. Its current full installer is a different software generation.

| File | Historical official URL | SHA-256 of the local file used |
| --- | --- | --- |
| Version 4.8.6.3 installer | `https://blueirissoftware.com/BlueIris_48603.exe` | `5dad7d0d9c2634f44ccc37004f6cd6009f085e73fd2324fedbb62089b763460a` |
| Legacy version-5 update | `https://blueirissoftware.com/50/update32.exe` | `70f1f8740421854906749b55bc890eca76411f9516e6475da13bc28bb4c7abc5` |

The hashes identify the files used; they are not a substitute for obtaining software from its legitimate vendor. No installer or DLL is redistributed by this repository. The whole installation recipe has not yet been rerun on a fresh VM using the generalized scripts.

## Networking and migration

The guest was given a reserved DHCP address. Initially it was absent from an existing firewall alias permitted to access the camera VLAN. The narrow addition of the recorder's reserved address restored RTSP reachability. This public guide deliberately omits real addresses, MACs, VLAN IDs, camera names, and credentials.

The source camera export was transferred privately and imported selectively. Camera definitions, Clips, Motion, Zones, Overlay, and VFilters were retained for testing. Notifications, events, PTZ, and output actions were excluded from the intended migration. A cross-version export is not automatically compatible in every section; a live recording test was the acceptance criterion.

The original definitions included a mix of separate paths and paths embedded in the IP field. The latter were normalized. Some cameras already had timeout failures on the source recorder, so the source was not assumed to be universally correct.

## Two different memory problems

1. **Guest memory pressure:** before resource expansion, the guest saw about 4 GB RAM. Launching Blue Iris alongside the desktop/AI software triggered a system OOM event. The kernel killed the AI application; the VM continued running.
2. **32-bit process startup pressure:** enabling ten imported cameras caused allocation problems and a Wine page fault. Substream paths alone did not prevent another crash because seven newly enabled cameras still had full-resolution cached dimensions. Virtual memory approached 4 GB.

After correcting every enabled camera's cached dimensions to the measured substream resolution, the ten-camera launch succeeded. This observation supports the cached-dimension fix for this configuration; it does not establish a universal cause for all Wine page faults.

## Recording and deletion evidence

- One-camera main-stream recording was first established at 2560×1920.
- A three-camera substream test produced decodable clips while using substantially less memory.
- The final ten-camera substream test produced fresh BVR files and additional segments for each camera.
- At least 100 changing video frames were decoded from a recording for every camera. Longer single-camera clips were also decoded.
- The configured managed folder total was 2048 MiB: New 256, Stored 1024, Alerts 512, Clipboard 256.
- Old test recordings were backed up before testing deletion.
- During recording, New rose to 317 MiB and then fell to 247 MiB during automatic cleanup. This is evidence of running retention, not just a saved setting.
- Recordings and the database remained on the guest's local disk. The NVR drive was not mounted.

## Not established by this test

Overnight/continuous long-duration stability, production-grade reliability, ten-camera main-stream recording, GPU acceleration, AI detection, notifications, PTZ, Windows-service-style startup, NVR mounting, and a working current version-6 Wine installation were not verified. Evaluation restrictions and the manual startup dialog remain relevant.
