# Blue Iris 5 on Linux with Wine

This is how I got **Blue Iris 5.9.9.98, 32-bit**, running on **Zorin OS 18.1 with Wine 10.0**. I am sharing the steps and helper scripts so other people have a starting point.

**Try this at your own risk.** This is a personal project that worked in my setup, with no support or reliability guarantee. The guide ends after installation and a basic recording check; further configuration and ongoing operation are your responsibility.

## Pick your starting point

| Section | What it is for |
| --- | --- |
| [Human setup guide](docs/HUMAN-GUIDE.md) | Install BI 5 and get your first camera recording. |
| [Copy-paste AI prompt](docs/AI-PROMPT.md) | Give your own AI assistant a generic setup task. |
| [Scripts](scripts/README.md) | Understand the optional helpers before using them. |
| [Tested setup](docs/TESTED-SETUP.md) | Check the versions, dependencies and limits behind this guide. |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Resolve common installation, network and memory problems. |

## What worked here

The test used an 8 GB RAM / 64 GB disk VM and ten cameras recording 640×360 or 640×480 RTSP substreams. Recorded video decoded for every camera, and automatic deletion of old clips was observed. This does not establish full-resolution or overnight reliability.

The working legacy installation route used a legitimate BI 4 installer, the vendor's BI 5 32-bit update, and four DLLs from the BI 4 installation: `SeaMAX.dll`, `ftd2xx.dll`, `msvcr120.dll`, and `msvcp120.dll`.

Imported cameras can retain full-resolution cached dimensions even after their stream path is changed. Correcting those dimensions to the measured substream size fixed the ten-camera startup crash in this setup. More VM RAM does not remove the 32-bit application's address-space limit.

## Before you start

Use a Linux desktop with 32-bit Wine support, your own legitimate vendor packages and license/evaluation, camera credentials, and sufficient local disk space. Start with a separate prefix and one camera. Confirm a growing recording and playback before making the setup larger.

No installers, DLLs, license keys, camera exports, credentials or footage are included. Keep your own settings private. The helper scripts are optional and should be read before use.

For BI 6 x64, use the separate [Blue Iris 6 repository](https://github.com/TTdriver/blue-iris-6-wine-linux). This repository covers BI 5 only.

Independent community documentation, not affiliated with Blue Iris or Wine. Original code and documentation use the [MIT license](LICENSE); vendor software retains its own terms.
