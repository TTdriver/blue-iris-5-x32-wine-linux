# Blue Iris on Linux with Wine

**New BI 6 result:** [BI 6.1.3.10 x64 now opens and records under Wine 10.0](docs/BI6-64BIT.md) using a native IPHLPAPI workaround. One camera is verified; the ten-camera test is pending. That page has separate human instructions and a copy-paste AI prompt.

A practical record of getting **Blue Iris 5.9.9.98, 32-bit**, running on **Zorin OS 18.1 with Wine 10.0**, inside a Proxmox VM.

Ten Reolink cameras produced local recordings using their low-resolution RTSP substreams. Recorded video was decoded for every camera, and automatic deletion of old clips was observed. The final configuration survived a short, roughly six-minute functional test. This is an experimental Wine setup, not proof of overnight reliability or full-resolution recording.

## Choose the section you need

| Section | Who it is for | What it does |
| --- | --- | --- |
| [Human setup guide](docs/HUMAN-GUIDE.md) | People doing the setup themselves | Explains the installation, camera migration, networking, memory fix, recording settings, and checks in order. |
| [Copy-paste AI prompt](docs/AI-PROMPT.md) | People using an AI assistant with computer or terminal access | Gives the assistant a complete task, constraints, and success criteria. Fill in your own environment details privately. |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | People who are stuck | Separates network failures, authentication failures, system RAM exhaustion, and Wine crashes. |
| [What actually happened](docs/TESTED-SETUP.md) | People evaluating the result or reproducing it | Records the working versions, installation history, failed attempts, exact dependency workaround, and what remains untested. |
| [Script reference](scripts/README.md) | People who want repeatable commands | Describes each utility, whether it changes anything, and how to use it safely. |
| [Reddit post draft](docs/REDDIT-POST.md) | The person sharing this project | Provides a short, accurate introduction you can edit before posting. |

## The fix that made ten cameras work

Changing the RTSP path to a substream was **not enough**. Seven imported cameras still had cached full-resolution dimensions, including 3840×2160. Starting all ten cameras pushed the 32-bit process close to 4 GB of virtual address space and it crashed with a Wine page fault.

We measured the actual substreams and updated these camera registry values before launching:

```text
xres / yres
fullxres / fullyres
zrect_right / zrect_bottom
zrect_left = 0
zrect_top = 0
```

The tested substreams were 640×360 or 640×480. With the cached dimensions corrected, all ten cameras recorded, and Blue Iris settled near 1 GB resident memory and 1.9 GB virtual memory during the observed test. This fixed the crash in this setup; it is not a guarantee for other camera models or software versions.

## What you need

- A Linux desktop that can run 32-bit Wine applications. The observed working system used Wine 10.0 from Zorin's packages.
- Legitimately obtained vendor packages for the legacy installation described in the guide, plus an appropriate Blue Iris license or evaluation.
- Camera access over TCP RTSP, working camera credentials, and the actual dimensions of the stream you choose.
- Enough guest RAM and disk space. The working VM had 8 GB RAM and a 64 GB disk. Increasing RAM does not remove the application's 32-bit address-space limit.

The repository contains our instructions and helper code. It does **not** contain Blue Iris binaries, Microsoft/vendor DLLs, license keys, camera registry exports, passwords, recordings, screenshots, or the original private network configuration.

## A useful first goal

Get **one** camera to display video, create a growing recording, and play back a completed clip. Then expand gradually. Keep the test on local disk until recording and deletion of older clips both work.

The final test used a 2 GiB configured total across New, Stored, Alerts, and Clipboard. The New folder temporarily exceeded its 256 MiB setting between cleanup cycles, then fell from 317 MiB to 247 MiB when old clips were deleted. These are managed retention settings, not a filesystem quota.

## Development checks

```bash
python3 -m unittest discover -s tests -v
bash -n scripts/launch-blue-iris.sh scripts/prepare-prefix.sh
```

The reusable scripts were extracted and generalized after the successful live session. Synthetic tests cover the registry transformations and filtering; a fresh installation using the whole repository has not yet been repeated from scratch.

## Help improve this

If you reproduce the setup, open an issue with your Linux/Wine/Blue Iris versions, camera model, measured stream dimensions, and a redacted description of the result. Useful next tests include overnight recording, restart behavior, a legitimate full-resolution setup, and newer Blue Iris versions. Keep camera exports, credentials, private footage, and detailed network configuration out of issues.

Independent community documentation; not affiliated with Blue Iris or Wine. The repository's original code and documentation use the [MIT license](LICENSE). Blue Iris and bundled third-party components retain their own licenses.
