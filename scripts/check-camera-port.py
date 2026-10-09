#!/usr/bin/env python3
"""Check named cameras' TCP RTSP port; this does not verify authentication."""
import argparse
import json
from pathlib import Path
import socket

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("streams", type=Path)
args = parser.parse_args()
for camera in json.loads(args.streams.read_text()):
    try:
        with socket.create_connection((camera["address"], 554), timeout=3):
            result = "reachable"
    except OSError:
        result = "unreachable"
    print(camera["camera"] + ": TCP 554 " + result)
