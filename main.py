#!/usr/bin/env python3
"""Write the rendered 25 November infographic to /output/entry.png.

No network. Copies the PNG the repository holds, then checks the copy:
same byte size as the source, a valid PNG signature, and 1024x1024 pixels.
"""
import hashlib
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "news.png"
TARGET = Path("/output/entry.png")
PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1 << 16)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def run():
    if not SOURCE.is_file():
        return fail(f"missing source image: {SOURCE}")
    if SOURCE.stat().st_size == 0:
        return fail(f"source image is empty: {SOURCE}")
    if SOURCE.stat().st_size > 1048576:
        return fail(f"source image over 1 MiB: {SOURCE.stat().st_size} bytes")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    if not TARGET.is_file() or TARGET.stat().st_size == 0:
        return fail(f"output not written: {TARGET}")
    if TARGET.stat().st_size != SOURCE.stat().st_size:
        return fail("output size differs from source")
    with TARGET.open("rb") as handle:
        header = handle.read(33)
    if header[:8] != PNG_MAGIC:
        return fail("output lacks a PNG signature")
    if header[12:16] != b"IHDR":
        return fail("output lacks a PNG IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (1024, 1024):
        return fail(f"unexpected dimensions: {width}x{height}")
    print(f"wrote {TARGET}: {TARGET.stat().st_size} bytes, sha256 {digest(TARGET)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
