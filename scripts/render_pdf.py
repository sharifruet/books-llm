"""Render combined Markdown to PDF via Pandoc → HTML → Chromium print.

Produces better typography than HTML→PDF via xhtml2pdf. Requires:
  - pandoc (brew install pandoc)
  - Google Chrome or Chromium (for headless --print-to-pdf)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_chrome() -> str:
    if p := os.environ.get("CHROME_PATH"):
        if Path(p).is_file():
            return p
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for c in candidates:
        if Path(c).is_file():
            return c
    raise FileNotFoundError(
        "Could not find Google Chrome or Chromium. Set CHROME_PATH to the browser binary."
    )


def render_markdown_to_pdf(
    *,
    md_path: Path,
    pdf_path: Path,
    title: str,
    repo_root: Path,
) -> None:
    md_path = md_path.resolve()
    pdf_path = pdf_path.resolve()
    css_path = (repo_root / "scripts" / "book-print.css").resolve()
    if not css_path.is_file():
        raise FileNotFoundError(css_path)
    if not md_path.is_file():
        raise FileNotFoundError(md_path)

    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise FileNotFoundError("pandoc not found in PATH (install: brew install pandoc)")

    with tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, dir=pdf_path.parent
    ) as tmp:
        html_path = Path(tmp.name)

    try:
        subprocess.run(
            [
                pandoc,
                str(md_path),
                "-f",
                "markdown+pipe_tables+fenced_code_blocks+backtick_code_blocks",
                "-t",
                "html5",
                "-s",
                "--toc",
                "--toc-depth=3",
                f"--metadata=title:{title}",
                f"--css={css_path}",
                "-o",
                str(html_path),
            ],
            check=True,
            cwd=str(repo_root),
        )

        chrome = find_chrome()
        html_uri = html_path.as_uri()
        subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                html_uri,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    finally:
        html_path.unlink(missing_ok=True)


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(
            "Usage: render_pdf.py <repo_root> <input.md> <output.pdf> <document_title>",
            file=sys.stderr,
        )
        return 1
    root = Path(argv[1])
    render_markdown_to_pdf(
        md_path=Path(argv[2]),
        pdf_path=Path(argv[3]),
        title=argv[4],
        repo_root=root,
    )
    print(f"Wrote {argv[3]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
