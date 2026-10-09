"""Small offline Wine registry helpers. Never print complete registry values."""
import os
from pathlib import Path
import re
import shutil
from datetime import datetime, timezone

CAMERA_ROOT = r"Software\Perspective Software\Blue Iris\Cameras"
FOLDER_ROOT = r"Software\Perspective Software\Blue Iris\clips\folders"


def sections(text):
    return re.split(r"(?m)(?=^\[)", text)


def section_key(block):
    first = block.splitlines()[0] if block.splitlines() else ""
    if not first.startswith("["):
        return ""
    return first[1:].split("]", 1)[0].replace("\\\\", "\\")


def camera_name(key):
    if key.startswith(CAMERA_ROOT + "\\"):
        name = key[len(CAMERA_ROOT) + 1:]
        if "\\" not in name:
            return name
    return None


def set_value(block, name, value):
    pattern = r'^"' + re.escape(name) + r'"=.*$'
    line = '"' + name + '"=' + value
    if re.search(pattern, block, re.M):
        return re.sub(pattern, lambda _: line, block, flags=re.M)
    return block.rstrip("\n") + "\n" + line + "\n\n"


def dword(value):
    return "dword:" + format(value, "08x")


def string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def ensure_stopped(prefix):
    """Refuse offline edits while Wine processes for this prefix are alive."""
    for entry in Path("/proc").glob("[0-9]*"):
        if int(entry.name) == os.getpid():
            continue
        try:
            name = (entry / "comm").read_text().strip().lower()
            if "wine" not in name and not name.endswith(".exe"):
                continue
            env = (entry / "environ").read_bytes().split(b"\0")
            for item in env:
                if item.startswith(b"WINEPREFIX="):
                    actual = Path(os.fsdecode(item.split(b"=", 1)[1])).resolve()
                    if actual == prefix.resolve():
                        raise RuntimeError("Wine is running for this prefix. Close Blue Iris, stop this prefix's wineserver, then retry.")
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError as exc:
            # /proc entries owned by other users cannot affect this user's prefix.
            try:
                if entry.stat().st_uid == os.getuid():
                    raise RuntimeError("Cannot inspect a same-user Wine process; cannot safely edit offline.") from exc
            except FileNotFoundError:
                pass


def backup_registry(prefix, parent):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    destination = parent / stamp
    destination.mkdir(parents=True, mode=0o700)
    os.chmod(destination, 0o700)
    for name in ("system.reg", "user.reg", "userdef.reg"):
        source = prefix / name
        if source.exists():
            shutil.copy2(source, destination / name)
            os.chmod(destination / name, 0o600)
    return destination


def atomic_write(path, text):
    temporary = path.with_name(path.name + ".blueiris-tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
