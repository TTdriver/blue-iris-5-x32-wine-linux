#!/usr/bin/env python3
"""Prepare a stopped 32-bit Wine prefix for a small local recording test."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from wine_registry import (CAMERA_ROOT, FOLDER_ROOT, atomic_write, backup_registry,
                           camera_name, dword, ensure_stopped, section_key,
                           sections, set_value, string)

FOLDERS = {"0": ("New", 256, 7), "1": ("Stored", 1024, 14),
           "2": ("Alerts", 512, 7), "16": ("Clipboard", 256, 7)}


def load_streams(path):
    data = json.loads(path.read_text())
    if not isinstance(data, list) or not data:
        raise ValueError("Streams file must be a nonempty JSON list.")
    result = {}
    for item in data:
        name = item["camera"]
        if not isinstance(name, str) or not name or any(c in name for c in '\\"\r\n'):
            raise ValueError("Invalid camera name.")
        if name in result:
            raise ValueError("Duplicate camera name.")
        address = item["address"]
        if not isinstance(address, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]+", address):
            raise ValueError("Address must contain only a hostname/IP, without credentials or a stream path.")
        path_value = item["path"]
        if not isinstance(path_value, str) or not path_value.startswith("/") or any(c in path_value for c in '\r\n"\\'):
            raise ValueError("Invalid stream path.")
        for dimension in ("width", "height"):
            if type(item[dimension]) is not int or not 16 <= item[dimension] <= 4096:
                raise ValueError("Use measured integer stream dimensions between 16 and 4096.")
        if type(item.get("enabled", False)) is not bool:
            raise ValueError("enabled must be true or false.")
        result[name] = item
    return result


def transform(text, streams):
    if "#arch=win32" not in text.splitlines():
        raise ValueError("This tool targets the verified win32 prefix format only.")
    blocks = sections(text)
    found = set()
    folders_found = set()
    for i, block in enumerate(blocks):
        key = section_key(block)
        name = camera_name(key)
        if name is not None:
            # Every imported camera begins disabled unless explicitly selected.
            block = set_value(block, "enabled", dword(0))
            if name in streams:
                item = streams[name]
                values = {"ip": string(item["address"]), "ip_path": string(item["path"]),
                          "ip_subpath": string(""), "ip_port2": dword(554),
                          "enabled": dword(int(item.get("enabled", False))),
                          "ip_hwaccel": dword(0), "bvrhwva": dword(0),
                          "xres": dword(item["width"]), "fullxres": dword(item["width"]),
                          "yres": dword(item["height"]), "fullyres": dword(item["height"]),
                          "zrect_left": dword(0), "zrect_top": dword(0),
                          "zrect_right": dword(item["width"]), "zrect_bottom": dword(item["height"])}
                for value_name, value in values.items():
                    block = set_value(block, value_name, value)
                found.add(name)
        if key.startswith(CAMERA_ROOT + "\\") and re.search(r"\\Clips\\[1-7]$", key):
            for value_name, value in {"continuous": 1, "breaktime": 60, "groupgb": 1, "transcode": 0}.items():
                block = set_value(block, value_name, dword(value))
        if key.startswith(FOLDER_ROOT + "\\"):
            number = key[len(FOLDER_ROOT) + 1:]
            if number in FOLDERS:
                folder, limit, days = FOLDERS[number]
                for value_name, value in {"name": string(folder), "path": string("C:\\BlueIris\\" + folder),
                                          "root": string("C:\\"), "archmb": dword(limit),
                                          "archdays": dword(days), "limitage": dword(1), "action": dword(0)}.items():
                    block = set_value(block, value_name, value)
                folders_found.add(number)
        blocks[i] = block
    if set(streams) != found:
        raise ValueError("Streams JSON names do not exactly match existing camera definitions.")
    if folders_found != set(FOLDERS):
        raise ValueError("Create New, Stored, Alerts, and Clipboard folder settings in Blue Iris first.")
    return "".join(blocks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--streams", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Write changes; default only validates and previews.")
    parser.add_argument("--backup-dir", type=Path, default=Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local/state"))) / "blueiris-wine/registry-backups")
    args = parser.parse_args()
    prefix = args.prefix.expanduser().resolve()
    try:
        ensure_stopped(prefix)
        streams = load_streams(args.streams)
        path = prefix / "system.reg"
        result = transform(path.read_text(), streams)
        print("Validated", len(streams), "camera settings; selected", sum(v.get("enabled", False) for v in streams.values()))
        print("Configured cap: 2048 MiB total. Existing credentials are preserved, not printed.")
        if not args.apply:
            print("Dry run: no files changed. Add --apply after reviewing the local streams JSON.")
            return
        backup = backup_registry(prefix, args.backup_dir.expanduser())
        for folder in ("New", "Stored", "Alerts", "Clipboard", "db"):
            (prefix / "drive_c/BlueIris" / folder).mkdir(parents=True, exist_ok=True)
        atomic_write(path, result)
        print("Saved configuration. Private registry backup:", backup)
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print("Configuration failed:", str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
