#!/usr/bin/env python3
"""Build a single PDF for Volume III (*From Models to Frontiers*).

Usage (from repo root):

  python3 scripts/build-volume3-pdf.py

Requires: **pandoc** and **Google Chrome** (see scripts/render_pdf.py).
Reuses `combine_hub_and_parts` from scripts/build-volume1-pdf.py.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

PART_FILES = [
    "from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md",
    "from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md",
    "from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md",
    "from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md",
    "from-models-to-frontiers-part-v-frontiers-and-open-problems.md",
]


def _load_v1():
    here = Path(__file__).resolve().parent
    path = here / "build-volume1-pdf.py"
    spec = importlib.util.spec_from_file_location("build_volume1_pdf", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    v1 = _load_v1()
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        type=Path,
        default=root / "build" / "from-models-to-frontiers-print.md",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=root / "build" / "from-models-to-frontiers.pdf",
    )
    ap.add_argument("--combine", action="store_true", default=True)
    ap.add_argument("--no-combine", action="store_false", dest="combine")
    args = ap.parse_args()

    if args.combine:
        cover = v1.make_cover_html(
            title="From Models to Frontiers",
            subtitle="Advanced topics in large language modeling",
            volume="Volume III",
            level="Advanced",
        )
        combined = cover + v1.combine_hub_and_parts(
            root / "from-models-to-frontiers",
            "from-models-to-frontiers.md",
            PART_FILES,
            "\n## Full text — Parts I through V\n\n",
        )
        args.input.parent.mkdir(parents=True, exist_ok=True)
        args.input.write_text(combined, encoding="utf-8")
        print(f"Wrote {args.input}")

    if not args.input.is_file():
        print(f"Missing input: {args.input}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        v1.render_markdown_to_pdf(
            md_path=args.input,
            pdf_path=args.output,
            title="From Models to Frontiers — Volume III",
            repo_root=root,
        )
    except Exception as e:
        print(f"PDF render failed: {e}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
