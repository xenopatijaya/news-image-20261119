#!/usr/bin/env python3
"""Entry for news-image-20261119: copy the front page to the output dir.

The image (entry.png, drawn in this session with PIL) sits next to
this file in the repository. This program only copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library
only; it never deletes or recreates the output directory.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # The grader owns the output directory: create it if missing,
    # but never remove or replace it.
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    # copyfile is a plain byte copy, so repeated runs are identical.
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
