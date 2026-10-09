#!/usr/bin/env python3
"""Create a PRIVATE camera-only Windows .reg import, disabled by default."""
import argparse
import os
from pathlib import Path
import re

ROOT = r"HKEY_LOCAL_MACHINE\Software\Perspective Software\Blue Iris\Cameras"
ALLOWED = {"Clips", "Motion", "Zones", "Overlay", "VFilters"}


def filtered(text):
    output = ["Windows Registry Editor Version 5.00\n\n"]
    count = 0
    for block in re.split(r"(?m)(?=^\[)", text):
        lines = block.splitlines()
        if not lines or not lines[0].startswith("["):
            continue
        key = lines[0].strip()[1:-1].replace(r"\Wow6432Node", "")
        if key.startswith("-") or not (key == ROOT or key.startswith(ROOT + "\\")):
            continue
        tail = key[len(ROOT):].lstrip("\\").split("\\") if key != ROOT else []
        if len(tail) > 1 and tail[1] not in ALLOWED:
            continue
        block = "[" + key + "]\n" + "\n".join(lines[1:]) + "\n\n"
        if len(tail) == 1:
            for name in ("enabled", "ip_hwaccel", "bvrhwva"):
                pattern = r'^"' + name + r'"=.*$'
                replacement = '"' + name + '"=dword:00000000'
                if re.search(pattern, block, re.M):
                    block = re.sub(pattern, replacement, block, flags=re.M)
                else:
                    block = block.rstrip() + "\n" + replacement + "\n\n"
            count += 1
        output.append(block)
    if not count:
        raise ValueError("No compatible HKLM camera definitions found in the export.")
    return "".join(output), count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path, help="A new private .reg file; existing files are never overwritten.")
    args = parser.parse_args()
    raw = args.source.read_bytes()
    text = raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
    result, count = filtered(text)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(args.destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-16", newline="\r\n") as stream:
        stream.write(result)
    print("Prepared", count, "disabled cameras. This .reg file still contains credentials: keep it private.")


if __name__ == "__main__":
    main()
