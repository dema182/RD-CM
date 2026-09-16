#!/usr/bin/env python3
from pathlib import Path
import struct
import zlib
import sys


def write_png(path: Path, size: int = 256) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            cx, cy = size / 2, size / 2
            dx, dy = (x - cx) / (size * 0.42), (y - cy) / (size * 0.36)
            inside = dx * dx + dy * dy <= 1
            bezel = dx * dx + dy * dy <= 1.18
            if bezel and not inside:
                raw += bytes([12, 13, 16, 255])
            elif inside:
                raw += bytes([21, 22, 28, 255] if 40 < y < size - 36 else [12, 13, 16, 255])
            else:
                raw += bytes([12, 13, 16, 0])
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


if __name__ == "__main__":
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else "packaging/rd-cm.png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    write_png(dest)
    print(dest)
