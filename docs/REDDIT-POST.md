# Reddit post draft

**Use this section as a draft to edit and post yourself.** No Reddit post has been published by this project setup.

## Suggested title

Blue Iris 6 x64 running on Linux/Wine: ten Reolink substreams and recordings verified

## Suggested post

I got an experimental Blue Iris setup recording on Linux and wrote up the steps so others can reproduce or improve it:

https://github.com/TTdriver/blue-iris-wine-linux

The newer working combination is Zorin OS 18.1, Wine 10.0, a dedicated 64-bit prefix, and Blue Iris 6.1.3.10. It needed the complete native Microsoft x64 VC/MFC runtime and a native Windows IPHLPAPI DLL from my own Windows installation. The repo explains the workaround but does not distribute DLLs. The VM had 8 GB RAM and a 64 GB disk. Ten Reolink cameras recorded using 640×360/640×480 RTSP substreams. Completed recordings decoded to 100 changing video frames for every camera. Automatic deletion was observed in the earlier BI 5 setup; BI 6 retention settings are configured, but its cleanup behavior is still unverified.

In the earlier BI 5 32-bit experiment, switching the stream paths to substreams did not stop a ten-camera startup crash. Imported cameras still had cached full-resolution dimensions, including 3840×2160. Correcting those dimensions before enabling the cameras brought the process back to about 1 GB RAM / 1.9 GB virtual memory during the short test.

The repo has separate sections for:

- Plain-English human guides for the BI 6 x64 experiment and the earlier BI 5 fallback.
- A prompt you can copy into your own AI assistant, with your own environment details.
- Reusable migration/configuration helpers with dry runs and backups.
- The exact legacy installation/dependency route and a record of failed attempts.
- Troubleshooting and what has not been tested.

This is a short functional test, not a claim of production readiness or full-resolution support. Earlier Bottles/Proton/Lutris attempts failed before the native IPHLPAPI workaround; the successful BI 6 run uses the host Wine 10.0. Overnight recording, GPU acceleration, alerts/PTZ, and NVR storage are still separate tests.

No installers, DLLs, license keys, camera exports, credentials, or footage are included. You need legitimate vendor packages and your own license/evaluation.

If you try it, I would be interested in your versions, camera models, measured stream sizes, and whether it survives longer tests. Please redact credentials and private network details from logs or issues.
