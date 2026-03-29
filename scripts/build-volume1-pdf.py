#!/usr/bin/env python3
"""Build a single PDF for Volume I.

Combines the hub file (intro only), all part files I–VI, and the Notes section,
then renders Markdown → HTML (pandoc) → PDF (Chrome headless).

Usage (from repo root):

  python3 scripts/build-volume1-pdf.py

Requires: **pandoc** and **Google Chrome** (see scripts/render_pdf.py). No Python PDF packages.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from render_pdf import render_markdown_to_pdf

PART_FILES = [
    "from-tokens-to-understanding-part-i-finding-your-bearings.md",
    "from-tokens-to-understanding-part-ii-how-it-works-without-equations.md",
    "from-tokens-to-understanding-part-iii-capabilities-and-limits.md",
    "from-tokens-to-understanding-part-iv-first-steps-with-prompts.md",
    "from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md",
    "from-tokens-to-understanding-part-vi-whats-next.md",
]


def combine_hub_and_parts(
    book_dir: Path,
    hub_filename: str,
    part_filenames: list[str],
    mid_heading: str,
) -> str:
    """Everything before ## Detailed outline + mid_heading + parts + ## Notes onward."""
    hub_path = book_dir / hub_filename
    text = hub_path.read_text(encoding="utf-8")
    if "## Detailed outline" not in text:
        raise ValueError(f"Could not find ## Detailed outline in {hub_path}")
    if "## Notes" not in text:
        raise ValueError(f"Could not find ## Notes in {hub_path}")
    pre, _, rest = text.partition("## Detailed outline")
    notes_idx = rest.find("## Notes")
    if notes_idx == -1:
        raise ValueError(f"Could not find ## Notes after outline in {hub_path}")
    notes = rest[notes_idx:]
    chunks = [pre, mid_heading]
    for name in part_filenames:
        p = book_dir / name
        if not p.is_file():
            raise FileNotFoundError(p)
        chunks.append(p.read_text(encoding="utf-8"))
        chunks.append("\n\n---\n\n")
    chunks.append(notes)
    return "".join(chunks)


def combine_volume1_markdown(root: Path) -> str:
    return combine_hub_and_parts(
        root / "from-tokens-to-understanding",
        "from-tokens-to-understanding.md",
        PART_FILES,
        "\n## Full text — Parts I through VI\n\n",
    )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        type=Path,
        default=root / "build" / "from-tokens-to-understanding-print.md",
        help="Combined Markdown (default: written when using --combine).",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=root / "build" / "from-tokens-to-understanding.pdf",
    )
    ap.add_argument(
        "--combine",
        action="store_true",
        default=True,
        help="Regenerate combined .md from hub + parts + Notes (default: on).",
    )
    ap.add_argument(
        "--no-combine",
        action="store_false",
        dest="combine",
        help="Use existing --input Markdown only.",
    )
    args = ap.parse_args()

    if args.combine:
        combined = combine_volume1_markdown(root)
        args.input.parent.mkdir(parents=True, exist_ok=True)
        args.input.write_text(combined, encoding="utf-8")
        print(f"Wrote {args.input}")

    if not args.input.is_file():
        print(f"Missing input: {args.input}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        render_markdown_to_pdf(
            md_path=args.input,
            pdf_path=args.output,
            title="From Tokens to Understanding — Volume I",
            repo_root=root,
        )
    except Exception as e:
        print(f"PDF render failed: {e}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
