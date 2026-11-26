#!/usr/bin/env python3
"""news-25-b46-numbers: THE WORLD IN NUMBERS -- Wednesday, 25 November 2026.

A numbers-led front page for the make.fun news-image bounty
(news-image-20261125): 50 stories across 10 regions, led by a hero
trio built on giant figures -- a 20% tariff on China and duties on
14 partners, a Kospi selloff of -6.16% to 4,697.51 (Samsung -9.87%,
SK Hynix -11.05%), and Shenzhou-24 carrying the first foreign
astronaut on Tiangong (Pakistan's Muhammad Zeeshan Ali) -- plus a
BY THE NUMBERS strip and 47 compact numbered cards, each tagged
C (core), R (regional) or CL (close-up), with a two-line DATE CHECK
in the footer. The artwork (entry.png, 1024x640) is rendered at
build time by gen.py with Pillow; this file is the only thing the
grader runs, so it is standard-library only on purpose: it copies
entry.png into MAKEFUN_OUTPUT_DIR and nothing else. No network,
no image decoding, no third-party imports -- just os, shutil, sys
and struct for a light PNG header check before the copy.
"""

import os
import shutil
import struct
import sys

# Name of the artwork shipped next to this file in the entry repo.
ENTRY_NAME = "entry.png"

# Expected artwork geometry, enforced before the copy so a broken
# build can never silently ship a wrong-sized image to the grader.
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 640

# The grader sets this; "out" keeps local runs working unchanged.
DEFAULT_OUTPUT_DIR = "out"

# First eight bytes of every PNG file, checked before the copy.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _output_dir():
    """Return the directory the grader wants the artwork written to."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)


def _source_path():
    """Return the absolute path of entry.png next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ENTRY_NAME)


def _read_png_size(path):
    """Read width/height from a PNG IHDR chunk using only struct."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def _check_entry(path):
    """Fail loudly unless entry.png exists and has the right size."""
    if not os.path.isfile(path):
        raise FileNotFoundError("missing entry artwork: %s" % path)
    width, height = _read_png_size(path)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            "entry.png is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    return os.path.getsize(path)


def _copy_entry(source, output_dir):
    """Copy entry.png into the output dir and confirm the bytes."""
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, ENTRY_NAME)
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        raise IOError("copy incomplete: %s" % target)
    with open(target, "rb") as handle:
        if handle.read(8) != PNG_SIGNATURE:
            raise IOError("copied file is not a PNG: %s" % target)
    return target


def main(argv=None):
    """Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png; exit 0 on ok."""
    try:
        source = _source_path()
        size = _check_entry(source)
        target = _copy_entry(source, _output_dir())
    except (OSError, ValueError, IOError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("copied %s (%d bytes) -> %s" % (ENTRY_NAME, size, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
