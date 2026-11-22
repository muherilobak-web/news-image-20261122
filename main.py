#!/usr/bin/env python3
"""news-image-20261122 entrypoint.

Copies the entry image (entry.png, drawn by draw.py) byte-for-byte into the
output directory named by MAKEFUN_OUTPUT_DIR (default /output).

Pure copy: standard library only, no network, no randomness, no timestamps,
no image processing. The output is byte-identical to the repo's entry.png.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png not found next to main.py\n")
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
