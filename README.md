# LLM Books

**Author:** Sharif Uddin

A **three-volume series** on large language models — from first concepts to the research frontier. Each volume stands on its own, but they are designed to be read in order: each one assumes the vocabulary and habits of the one before it.

---

## The series at a glance

| Volume | Level | Title | Who it is for |
|--------|-------|-------|---------------|
| **I** | Beginner | [From Tokens to Understanding](from-tokens-to-understanding/from-tokens-to-understanding.md) | Curious readers and professionals who want a plain-language picture of what LLMs are, how they behave, and how to use them without embarrassing yourself |
| **II** | Intermediate | [From Prompts to Systems](from-prompts-to-systems/from-prompts-to-systems.md) | Developers, product managers, and technical writers who are past the demo stage and want to ship real features with LLMs |
| **III** | Advanced | [From Models to Frontiers](from-models-to-frontiers/from-models-to-frontiers.md) | Researchers, senior engineers, and technical leads who need depth on scaling, alignment, efficiency, and the frontier |

---

## Volume I — From Tokens to Understanding

*An introduction to large language models*

No math, no code required. You leave with a stable mental model: what these systems actually are, what they reliably do and reliably don't do, and how to use them without mistaking fluent text for verified fact.

**Parts:**

| Part | Title | File |
|------|-------|------|
| I | Finding your bearings | [part-i](from-tokens-to-understanding/from-tokens-to-understanding-part-i-finding-your-bearings.md) |
| II | How it works (without equations) | [part-ii](from-tokens-to-understanding/from-tokens-to-understanding-part-ii-how-it-works-without-equations.md) |
| III | Capabilities and limits | [part-iii](from-tokens-to-understanding/from-tokens-to-understanding-part-iii-capabilities-and-limits.md) |
| IV | First steps with prompts | [part-iv](from-tokens-to-understanding/from-tokens-to-understanding-part-iv-first-steps-with-prompts.md) |
| V | Responsibility in everyday use | [part-v](from-tokens-to-understanding/from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md) |
| VI | What's next | [part-vi](from-tokens-to-understanding/from-tokens-to-understanding-part-vi-whats-next.md) |

**Build PDF (Volume I):** `python3 scripts/build-volume1-pdf.py`

---

## Volume II — From Prompts to Systems

*Intermediate practice with large language models*

The gap between "this demo is amazing" and "this feature works in production" is a graveyard of good ideas. Volume II is about closing that gap: choosing between prompt, retrieval, and fine-tuning; building evaluation pipelines; wiring models into real applications; and operating them reliably.

**Parts:**

| Part | Title | File |
|------|-------|------|
| I | Mental models and the model lifecycle | [part-i](from-prompts-to-systems/from-prompts-to-systems-part-i-mental-models-and-the-model-lifecycle.md) |
| II | Prompting as engineering | [part-ii](from-prompts-to-systems/from-prompts-to-systems-part-ii-prompting-as-engineering.md) |
| III | Data, retrieval, and adaptation | [part-iii](from-prompts-to-systems/from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md) |
| IV | Evaluation, quality, and safety in practice | [part-iv](from-prompts-to-systems/from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md) |
| V | Systems: APIs, deployment, and operations | [part-v](from-prompts-to-systems/from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md) |
| VI | Teams, ethics, and the path forward | [part-vi](from-prompts-to-systems/from-prompts-to-systems-part-vi-teams-ethics-and-the-path-forward.md) |

**Build PDF (Volume II):** `python3 scripts/build-volume2-pdf.py`

---

## Volume III — From Models to Frontiers

*Advanced topics in large language modeling*

For those who need to understand the science behind the product: scaling laws, data curation at web scale, alignment research, training and inference efficiency, multimodal architectures, agents, and the open problems that still lack satisfactory answers.

**Parts:**

| Part | Title | File |
|------|-------|------|
| I | Scale, data, and the pretraining stack | [part-i](from-models-to-frontiers/from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md) |
| II | Alignment, safety, and robustness | [part-ii](from-models-to-frontiers/from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) |
| III | Efficiency: training, inference, and systems | [part-iii](from-models-to-frontiers/from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md) |
| IV | Beyond text: multimodal models and agents | [part-iv](from-models-to-frontiers/from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md) |
| V | Frontiers and open problems | [part-v](from-models-to-frontiers/from-models-to-frontiers-part-v-frontiers-and-open-problems.md) |

**Build PDF (Volume III):** `python3 scripts/build-volume3-pdf.py`

---

## How to use this repo

- Each volume lives in its own folder; the **hub file** (`from-tokens-to-understanding.md`, etc.) is the entry point with introduction, audience notes, and links to all parts.
- Part files are the actual book content — read them in order or jump to a topic.
- Cross-volume links use relative paths (`../from-prompts-to-systems/…`).
- PDF build scripts read from the volume folders and write combined output under `build/`.
- `scripts/` contains the PDF build helpers; `build/` contains compiled output.

**Dependencies for PDF build:** `pandoc` (`brew install pandoc` on macOS) and Google Chrome or Chromium (for headless print-to-PDF). Set `CHROME_PATH` if Chrome is not in the default location.

---

