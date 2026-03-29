#!/usr/bin/env python3
"""Build a single PDF for Volume I.

Combines the hub file (intro only), all part files I–VI, and the Notes section,
then renders Markdown → HTML → PDF via xhtml2pdf.

Usage (from repo root):

  python3 scripts/build-volume1-pdf.py

Requires: pip install markdown xhtml2pdf
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

PART_FILES = [
    "from-tokens-to-understanding-part-i-finding-your-bearings.md",
    "from-tokens-to-understanding-part-ii-how-it-works-without-equations.md",
    "from-tokens-to-understanding-part-iii-capabilities-and-limits.md",
    "from-tokens-to-understanding-part-iv-first-steps-with-prompts.md",
    "from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md",
    "from-tokens-to-understanding-part-vi-whats-next.md",
]


def combine_hub_and_parts(
    root: Path,
    hub_name: str,
    part_filenames: list[str],
    mid_heading: str,
) -> str:
    """Everything before ## Detailed outline + mid_heading + parts + ## Notes onward."""
    hub_path = root / hub_name
    text = hub_path.read_text(encoding="utf-8")
    if "## Detailed outline" not in text:
        raise ValueError(f"Could not find ## Detailed outline in {hub_name}")
    if "## Notes" not in text:
        raise ValueError(f"Could not find ## Notes in {hub_name}")
    pre, _, rest = text.partition("## Detailed outline")
    notes_idx = rest.find("## Notes")
    if notes_idx == -1:
        raise ValueError(f"Could not find ## Notes after outline in {hub_name}")
    notes = rest[notes_idx:]
    chunks = [pre, mid_heading]
    for name in part_filenames:
        p = root / name
        if not p.is_file():
            raise FileNotFoundError(p)
        chunks.append(p.read_text(encoding="utf-8"))
        chunks.append("\n\n---\n\n")
    chunks.append(notes)
    return "".join(chunks)


def combine_volume1_markdown(root: Path) -> str:
    return combine_hub_and_parts(
        root,
        "from-tokens-to-understanding.md",
        PART_FILES,
        "\n## Full text — Parts I through VI\n\n",
    )


def md_to_html(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "markdown.extensions.tables",
            "markdown.extensions.fenced_code",
            "markdown.extensions.nl2br",
        ],
    )


def wrap_html(fragment: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<style>
@page {{ size: a4; margin: 2cm; }}
body {{
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 11pt;
  line-height: 1.45;
  color: #111;
}}
h1 {{ font-size: 20pt; page-break-after: avoid; }}
h2 {{ font-size: 15pt; margin-top: 1.2em; page-break-after: avoid; }}
h3 {{ font-size: 12pt; margin-top: 1em; page-break-after: avoid; }}
h4 {{ font-size: 11pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 10pt; }}
th, td {{ border: 1px solid #444; padding: 4px 6px; text-align: left; vertical-align: top; }}
blockquote {{
  margin: 0.8em 0;
  padding-left: 0.8em;
  border-left: 3px solid #999;
  color: #333;
}}
code {{ font-family: ui-monospace, monospace; font-size: 9pt; }}
pre {{
  background: #f4f4f4;
  padding: 8px 10px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 9pt;
}}
hr {{ border: none; border-top: 1px solid #ccc; margin: 1.5em 0; }}
a {{ color: #222; text-decoration: none; }}
ul, ol {{ padding-left: 1.4em; }}
</style>
</head>
<body>
{fragment}
</body>
</html>"""


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

    md_text = args.input.read_text(encoding="utf-8")
    fragment = md_to_html(md_text)
    html = wrap_html(fragment, "From Tokens to Understanding — Volume I")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("wb") as pdf_file:
        status = pisa.CreatePDF(
            html.encode("utf-8"),
            dest=pdf_file,
            encoding="utf-8",
        )
    if status.err:
        print("xhtml2pdf reported errors.", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
