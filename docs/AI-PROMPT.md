# Copy-paste prompt for your AI assistant

Use this if you want an AI assistant to help install BI 5 on your machine. It is a task brief, not a command to paste into a terminal. Your assistant needs terminal access or must guide you through the steps. Fill in your own details privately.

```text
Help me get Blue Iris 5 running under Wine using this personal setup guide:
https://github.com/TTdriver/blue-iris-wine-linux
Read README.md, docs/HUMAN-GUIDE.md, docs/TESTED-SETUP.md and scripts/README.md.

My Linux version: [fill in]
My RAM and free disk space: [fill in]
My Wine version and existing prefixes: [fill in]
My legitimate BI installer/update files: [private local paths]
My camera model and chosen RTSP stream: [fill in privately]

The reference is Zorin OS 18.1, Wine 10.0 and BI 5.9.9.98 in a win32 prefix.
Use a separate prefix and preserve my existing setup. Follow the documented
legacy route: legitimate BI 4.8.6.3 installation, extracted BI 5 32-bit update,
and the four listed dependencies from the BI 4 folder. Do not substitute
random DLL downloads or bypass evaluation/licensing.

Get BI to open, then configure ONE camera using a measured low-resolution
stream. Confirm network access and authentication. Correct cached dimensions
xres/yres, fullxres/fullyres and zrect values to that stream's actual size;
changing the RTSP path alone may leave large startup allocations. Start with
hardware acceleration off. Extra RAM does not remove the 32-bit address limit.
Back up settings and stop the relevant prefix before offline registry edits.
Read optional helpers, use their dry runs and keep credentials/backups private.

Use local test storage. Verify live video, a growing clip, and playback or
successful decoding of a completed clip. Do not change my production recorder,
NAS, firewall or camera settings without instructions. Ask only for missing
information required to do this setup; do not ask me for project feedback.

Finish with the working launch command, private prefix/log locations and
basic verification result. Stop there. Further configuration and operation
are my responsibility. This project is used at my own risk and is not a
support or production-reliability guarantee.
```
