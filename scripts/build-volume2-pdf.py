#!/usr/bin/env python3
"""Build a single PDF for Volume II (*From Prompts to Systems*).

Usage (from repo root):

  python3 scripts/build-volume2-pdf.py

Requires: pip install markdown xhtml2pdf
Reuses combine/render helpers from scripts/build-volume1-pdf.py
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

PART_FILES = [
    "from-prompts-to-systems-part-i-mental-models-and-the-model-lifecycle.md",
    "from-prompts-to-systems-part-ii-prompting-as-engineering.md",
    "from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md",
    "from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md",
    "from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md",
    "from-prompts-to-systems-part-vi-teams-ethics-and-the-path-forward.md",
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
        default=root / "build" / "from-prompts-to-systems-print.md",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=root / "build" / "from-prompts-to-systems.pdf",
    )
    ap.add_argument("--combine", action="store_true", default=True)
    ap.add_argument("--no-combine", action="store_false", dest="combine")
    args = ap.parse_args()

    if args.combine:
        combined = v1.combine_hub_and_parts(
            root,
            "from-prompts-to-systems.md",
            PART_FILES,
            "\n## Full text — Parts I through VI\n\n",
        )
        args.input.parent.mkdir(parents=True, exist_ok=True)
        args.input.write_text(combined, encoding="utf-8")
        print(f"Wrote {args.input}")

    if not args.input.is_file():
        print(f"Missing input: {args.input}", file=sys.stderr)
        return 1

    md_text = args.input.read_text(encoding="utf-8")
    fragment = v1.md_to_html(md_text)
    html = v1.wrap_html(fragment, "From Prompts to Systems — Volume II")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    from xhtml2pdf import pisa

    with args.output.open("wb") as pdf_file:
        status = pisa.CreatePDF(html.encode("utf-8"), dest=pdf_file, encoding="utf-8")
    if status.err:
        print("xhtml2pdf reported errors.", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
