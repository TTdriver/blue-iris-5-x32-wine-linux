#!/usr/bin/env python3
"""Best-effort H.264/H.265 decode check for a LOCAL recording, including tested BVRs."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("clip", type=Path)
parser.add_argument("--codec", choices=("h264", "hevc"), default="h264")
parser.add_argument("--frames", type=int, default=100)
args = parser.parse_args()
if args.frames < 2:
    parser.error("Check at least two frames.")
try:
    import av
except ImportError:
    parser.error("Install optional requirements-video.txt in a virtual environment first.")
av.logging.set_level(av.logging.PANIC)
count = 0
hashes = set()
try:
    with av.open(str(args.clip), format=args.codec) as container:
        for frame in container.decode(video=0):
            count += 1
            if count % 10 == 0 or count <= 2:
                hashes.add(hashlib.sha256(bytes(frame.planes[0])).hexdigest())
            if count >= args.frames:
                break
except Exception:
    # Decoder messages can embed filenames or URLs; do not echo them.
    print("Unable to decode this recording with the selected raw codec.", file=sys.stderr)
    sys.exit(1)
if count < 2:
    print("Too few video frames decoded.", file=sys.stderr)
    sys.exit(1)
print(json.dumps({"decoded_frames": count, "width": frame.width, "height": frame.height,
                  "distinct_sampled_frames": len(hashes)}, indent=2))
