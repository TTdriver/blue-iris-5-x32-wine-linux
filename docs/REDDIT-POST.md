# Reddit post draft

**Use this section as a draft to edit and post yourself.** No Reddit post has been published by this project setup.

## Suggested title

Blue Iris 5 running on Zorin/Wine: ten Reolink substreams, recordings verified, and the memory fix that stopped the crash

## Suggested post

I got an experimental Blue Iris setup recording on Linux and wrote up the steps so others can reproduce or improve it:

https://github.com/TTdriver/blue-iris-wine-linux

The working combination was Zorin OS 18.1, Wine 10.0, a dedicated 32-bit prefix, and Blue Iris 5.9.9.98. The VM had 8 GB RAM and a 64 GB disk. Ten Reolink cameras recorded using 640×360/640×480 RTSP substreams. Recorded video decoded successfully for every camera, and automatic deletion of old clips was observed.

The surprising part: switching the stream paths to substreams did not stop a ten-camera startup crash. Imported cameras still had cached full-resolution dimensions, including 3840×2160. Correcting those dimensions before enabling the cameras brought the process back to about 1 GB RAM / 1.9 GB virtual memory during the short test.

The repo has separate sections for:

- A plain-English human guide.
- A prompt you can copy into your own AI assistant, with your own environment details.
- Reusable migration/configuration helpers with dry runs and backups.
- The exact legacy installation/dependency route and a record of failed attempts.
- Troubleshooting and what has not been tested.

This is a short functional test, not a claim of production readiness or full-resolution support. Current Blue Iris 6 did not launch successfully in the combinations tried here. Overnight recording, GPU acceleration, alerts/PTZ, and NVR storage are still separate tests.

No installers, DLLs, license keys, camera exports, credentials, or footage are included. You need legitimate vendor packages and your own license/evaluation.

If you try it, I would be interested in your versions, camera models, measured stream sizes, and whether it survives longer tests. Please redact credentials and private network details from logs or issues.
