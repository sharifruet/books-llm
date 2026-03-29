# LLM Books

**Author:** Sharif Uddin

This project is a **three-volume series** on **large language models (LLMs)**. Each volume has its **own folder** with a hub file, part files, and shared `scripts/` and `build/` at the repo root.

## The series

| Book | Working title | Hub (folder) |
|------|----------------|------|
| Volume I — Basic | **From Tokens to Understanding** — *An introduction to large language models* | [from-tokens-to-understanding/from-tokens-to-understanding.md](from-tokens-to-understanding/from-tokens-to-understanding.md) |
| Volume II — Intermediate | **From Prompts to Systems** — *Intermediate practice with large language models* | [from-prompts-to-systems/from-prompts-to-systems.md](from-prompts-to-systems/from-prompts-to-systems.md) |
| Volume III — Advanced | **From Models to Frontiers** — *Advanced topics in large language modeling* | [from-models-to-frontiers/from-models-to-frontiers.md](from-models-to-frontiers/from-models-to-frontiers.md) |

### Volume I — parts

Read in order, or open the [hub](from-tokens-to-understanding/from-tokens-to-understanding.md) for the introduction and links.

| Part | Title | File |
|------|--------|------|
| I | Finding your bearings | [from-tokens-to-understanding-part-i-finding-your-bearings.md](from-tokens-to-understanding/from-tokens-to-understanding-part-i-finding-your-bearings.md) |
| II | How it works (without equations) | [from-tokens-to-understanding-part-ii-how-it-works-without-equations.md](from-tokens-to-understanding/from-tokens-to-understanding-part-ii-how-it-works-without-equations.md) |
| III | Capabilities and limits | [from-tokens-to-understanding-part-iii-capabilities-and-limits.md](from-tokens-to-understanding/from-tokens-to-understanding-part-iii-capabilities-and-limits.md) |
| IV | First steps with prompts | [from-tokens-to-understanding-part-iv-first-steps-with-prompts.md](from-tokens-to-understanding/from-tokens-to-understanding-part-iv-first-steps-with-prompts.md) |
| V | Responsibility in everyday use | [from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md](from-tokens-to-understanding/from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md) |
| VI | What’s next | [from-tokens-to-understanding-part-vi-whats-next.md](from-tokens-to-understanding/from-tokens-to-understanding-part-vi-whats-next.md) |

**PDFs.** You need **pandoc** (`brew install pandoc` on macOS) and **Google Chrome** (or set `CHROME_PATH` to a Chromium/Chrome binary). The scripts use Pandoc → HTML → headless print-to-PDF—no Python packages for PDF output.

**PDF (Volume I).** From the repo root:

`python3 scripts/build-volume1-pdf.py`

That writes `build/from-tokens-to-understanding-print.md` (combined source) and `build/from-tokens-to-understanding.pdf`. Mermaid blocks in Notes appear as plain code in the PDF.

### Volume II — parts

Read in order, or open the [hub](from-prompts-to-systems/from-prompts-to-systems.md) for the introduction and links.

| Part | Title | File |
|------|--------|------|
| I | Mental models and the model lifecycle | [from-prompts-to-systems-part-i-mental-models-and-the-model-lifecycle.md](from-prompts-to-systems/from-prompts-to-systems-part-i-mental-models-and-the-model-lifecycle.md) |
| II | Prompting as engineering | [from-prompts-to-systems-part-ii-prompting-as-engineering.md](from-prompts-to-systems/from-prompts-to-systems-part-ii-prompting-as-engineering.md) |
| III | Data, retrieval, and adaptation | [from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md](from-prompts-to-systems/from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md) |
| IV | Evaluation, quality, and safety in practice | [from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md](from-prompts-to-systems/from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md) |
| V | Systems: APIs, deployment, and operations | [from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md](from-prompts-to-systems/from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md) |
| VI | Teams, ethics, and the path forward | [from-prompts-to-systems-part-vi-teams-ethics-and-the-path-forward.md](from-prompts-to-systems/from-prompts-to-systems-part-vi-teams-ethics-and-the-path-forward.md) |

**PDF (Volume II).** From the repo root:

`python3 scripts/build-volume2-pdf.py`

That writes `build/from-prompts-to-systems-print.md` and `build/from-prompts-to-systems.pdf`.

### Volume III — parts

Read in order, or open the [hub](from-models-to-frontiers/from-models-to-frontiers.md) for the introduction and links. (Volume III uses **five** parts covering seventeen chapters.)

| Part | Title | File |
|------|--------|------|
| I | Scale, data, and the pretraining stack | [from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md](from-models-to-frontiers/from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md) |
| II | Alignment, safety, and robustness | [from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md](from-models-to-frontiers/from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) |
| III | Efficiency: training, inference, and systems | [from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md](from-models-to-frontiers/from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md) |
| IV | Beyond text: multimodal models and agents | [from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md](from-models-to-frontiers/from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md) |
| V | Frontiers and open problems | [from-models-to-frontiers-part-v-frontiers-and-open-problems.md](from-models-to-frontiers/from-models-to-frontiers-part-v-frontiers-and-open-problems.md) |

**PDF (Volume III).** From the repo root:

`python3 scripts/build-volume3-pdf.py`

That writes `build/from-models-to-frontiers-print.md` and `build/from-models-to-frontiers.pdf`.

## How to use this repo

- Open the **folder** for the volume you are editing; the **hub** file links to all parts.
- Cross-volume links in the manuscripts use relative paths (e.g. `../from-prompts-to-systems/…`).
- PDF build scripts read from those folders and write combined sources under `build/`.

---

*Work in progress.*
