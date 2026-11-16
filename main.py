"""ai-excited-01 entry: write the murmuration image to the output dir.

The image is a starling murmuration forming a giant curling wave in a
violet and orange dusk sky, with a tiny lone figure silhouetted on a
hilltop below. It is bundled next to this program as entry.png; the
program copies it byte-for-byte to MAKEFUN_OUTPUT_DIR/entry.png so the
judge sees exactly the intended image, deterministically, with no
network access and no image processing at runtime.
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, SOURCE_NAME)

    shutil.copyfile(source, dest)

    # Flush to disk, then verify the copy is byte-identical in size.
    # A truncated or partial write would silently change the judged
    # image, so the size check is load-bearing, not cosmetic.
    with open(dest, "rb+") as handle:
        handle.flush()
        os.fsync(handle.fileno())

    expected = os.path.getsize(source)
    actual = os.path.getsize(dest)
    if actual != expected:
        raise RuntimeError(
            f"output size mismatch: wrote {actual} bytes, expected {expected}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
