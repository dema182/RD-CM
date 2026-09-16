#!/usr/bin/env python3
from __future__ import annotations

import io
import stat
import urllib.request
import zipfile
from pathlib import Path

URL = "https://github.com/LeXofLeviafan/RAHasher/releases/download/1.8.3/RAHasher-x64-Linux-1.8.3.zip"


def main() -> None:
    dest_dir = Path("vendor")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "RAHasher"
    print("Downloading RAHasher 1.8.3…")
    data = urllib.request.urlopen(URL, timeout=120).read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extract("RAHasher", dest_dir)
    dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(dest, dest.stat().st_size)


if __name__ == "__main__":
    main()
