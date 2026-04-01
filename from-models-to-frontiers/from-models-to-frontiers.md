# From Models to Frontiers

*Sharif Uddin*

*Volume III of the LLM trilogy · [Volume I](../from-tokens-to-understanding/from-tokens-to-understanding.md) · [Volume II](../from-prompts-to-systems/from-prompts-to-systems.md)*

---

Most people who build with language models never need to look inside. They pick an API, craft a system prompt, add a retrieval layer, and ship. Volume II covered exactly that ground — and it covers most of what most practitioners need.

This volume is for the readers who hit the wall. The ones who need to evaluate whether a published scaling result applies to their domain. Who want to argue about alignment tradeoffs rather than just implement a safety layer. Who need to understand why their inference costs scaled badly, or why their fine-tuned model broke in a specific way. Who read a paper abstract and want to know whether to trust the benchmark.

*From Models to Frontiers* steps behind the API surface and into the science and engineering of the models themselves — why they are built the way they are, what the research says about their limits, and what is genuinely unknown.

---

## Who this book is for

**You build or evaluate systems, and you need depth.** You can follow a discussion of fine-tuning, RLHF, and retrieval without needing every term re-explained. You have read model cards and benchmark reports and developed a healthy suspicion of both. You want to be the person in the room who can engage with the paper, not just nod at the headline.

**You work in AI safety, alignment, or policy.** You need the technical vocabulary to participate in technical debates — what alignment actually means in a training pipeline, what capability evaluations can and cannot tell you, where the science is genuinely uncertain versus where it is settled.

**You make infrastructure or research decisions.** You need to evaluate efficiency claims, understand the tradeoffs between training and inference strategies, and decide when vendor roadmaps matter to your situation and when they are irrelevant.

**You are a senior contributor who reads the field.** You want a structured map of the frontier — enough to follow primary sources with judgment, to recognize hype, to decide where your own learning should go next, and to bring research context into product and engineering conversations.

**You do not need this book if:**
- You are building LLM features with APIs and the Vol II coverage of prompting, RAG, evaluation, and deployment is sufficient for your work.
- You want a textbook treatment of neural networks from first principles. This book connects research to practice, not mathematics to code.
- You are comfortable with the research literature and just need a quick reference. Start with the part that covers your gap.

---

## What this book is for

The boundary between Volume II and Volume III is the boundary between *building with models* and *understanding or critically evaluating the models themselves*.

That boundary matters in specific ways:

**Evaluating claims.** When a new model is released with a 40% improvement on a reasoning benchmark, you want to know whether that benchmark is contaminated, whether the evaluation methodology favors their training distribution, and whether the improvement translates to your use case. That judgment requires understanding how models are trained, evaluated, and where benchmarks go wrong.

**Making architectural decisions.** When you need to choose between RAG and fine-tuning, or between serving a large model and distilling it into a smaller one, the decision depends on understanding what fine-tuning actually does to a model's knowledge and behavior — not just the API surface.

**Understanding failure modes.** Sycophancy, hallucination, prompt injection vulnerability, alignment failures under distribution shift — these are product problems, but they have technical roots. Understanding the roots lets you design mitigations rather than patches.

**Participating in research and governance.** If your work involves alignment decisions, capability evaluations, release policy, or safety specifications, you need the vocabulary that comes from the research side of these conversations.

---

## How this volume is organized

The five parts form a progression from *how models are built* to *what they are becoming* to *how to engage with the field*.

**Part I — Scale, data, and the pretraining stack:** Why do large models look the way they do? Scaling laws, training data at web scale, architecture families, and the post-training pipeline that transforms a base model into something deployable.

**Part II — Alignment, safety, and robustness:** What does it mean to align a model, and what can go wrong? Goals and tensions in alignment, adversarial evaluation, interpretability tools, and the governance landscape around model release and dual-use.

**Part III — Efficiency:** Training systems, inference optimization, and hardware context. What techniques make large models affordable to serve, when do they trade quality, and how do infrastructure decisions filter which methods are practical at your scale.

**Part IV — Beyond text:** Multimodal models, tool-augmented agents, and the research challenges they introduce. Vision-language architectures, grounding at research depth, and the failure modes of multi-step agent systems.

**Part V — Frontiers and open problems:** Where does the field not know the answers? Evaluation at the frontier, open research directions, and how to build a sustainable reading practice without drowning in preprints.

---

## Prerequisites

This volume assumes you are comfortable with:
- The vocabulary and practices in Volume II: prompting, RAG, fine-tuning decisions, evaluation, deployment
- High-level discussions of training: that models are pretrained on text, that instruction tuning and preference optimization exist, and that they have different effects
- Reading research abstracts critically: understanding what a benchmark evaluates, what "RLHF" means in a paper headline, what "we fine-tuned on X" implies

You do not need to derive backpropagation or read CUDA kernels. Where topics depend on linear algebra, distributed systems, or statistics at depth, the text signals it and points to standard references rather than rederiving everything from scratch.

---

## Detailed outline

→ See parts below.

---

## Parts and chapters

| | Part | Chapters | Core question |
|---|------|----------|---------------|
| **I** | [Scale, data, and the pretraining stack](from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md) | Scaling laws · Data at scale · Architecture variants · Post-training | Why do models look the way they do? |
| **II** | [Alignment, safety, and robustness](from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) | Alignment goals · Red teaming · Interpretability · Governance | How do we steer model behavior — and where does that fail? |
| **III** | [Efficiency: training, inference, and systems](from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md) | Training efficiency · Inference optimization · Hardware and stacks | What makes large models affordable to build and serve? |
| **IV** | [Beyond text: multimodal models and agents](from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md) | Multimodal foundations · Tool use and grounding · Agents | What happens when language is not the only modality? |
| **V** | [Frontiers and open problems](from-models-to-frontiers-part-v-frontiers-and-open-problems.md) | Evaluation at frontier · Open research · Reading the field | What do we not know, and how do we follow the field honestly? |

**Parts (plain list):**

1. Part I — Scale, data, pretraining stack
2. Part II — Alignment, safety, robustness
3. Part III — Efficiency, training, inference, hardware
4. Part IV — Multimodal models and agents
5. Part V — Frontiers and open problems

---

## Notes

### Key terms used throughout this volume

**Scaling law** — An empirical relationship linking compute, data volume, model size, and loss. Useful for budgeting training experiments and reasoning about tradeoffs. Not a promise about any specific downstream task or domain.

**Chinchilla-optimal** — A training allocation that roughly balances model parameters and training tokens for a given compute budget. Derived from research showing that many earlier large models were trained on too little data relative to their size.

**Pretraining** — Training a model on massive amounts of text with a next-token prediction (or similar) objective. Produces a base model that encodes broad statistical patterns from language; not directly deployable without post-training.

**Instruction tuning (SFT)** — Supervised fine-tuning on demonstrations of desired behavior. Teaches the model what task format looks like, how to respond to instructions, and basic dialogue conventions.

**RLHF / DPO** — Preference-based post-training methods. RLHF (reinforcement learning from human feedback) trains a reward model on human comparisons then uses it to update the policy. DPO (direct preference optimization) achieves a similar goal without a separate reward model. Both aim to steer outputs toward human-preferred behavior.

**Alignment** — The broad project of making models behave in accordance with intended goals — helpful, honest, harmless in common shorthand. Not guaranteed by scale; requires deliberate design and ongoing evaluation.

**Emergence** — Capabilities that appear at scale without being explicitly trained for, as measured by a discontinuity on some benchmark. The definition and mechanism are actively debated.

**Hallucination** — Model outputs that are confidently stated and factually wrong. A symptom of the model generating plausible-sounding text without a ground-truth check, not a bug that will be fully "fixed."

**KV cache** — The key-value pairs from the attention mechanism stored in memory during inference, so the model does not re-compute previous context on each new token. A major component of inference memory cost.

**Quantization** — Reducing the numerical precision of model weights (e.g., from 32-bit floats to 8-bit integers) to reduce memory and speed up computation. Involves a quality tradeoff that varies by task and precision level.

**Red teaming** — Structured attempts to elicit harmful, policy-violating, or otherwise undesired behavior from a model. Both a safety practice and an ongoing research methodology.

**Model card** — A document accompanying a model release that describes its intended use, training data, evaluation methodology, limitations, and known risks. A minimum standard of transparency for foundation model releases.

---

### How to use this volume

**Read it as a map, not a textbook.** Each chapter explains a landscape — what the key techniques are, what they trade off, what the open questions are — not how to implement every detail. Primary sources (papers, model cards, documentation) remain the authoritative reference.

**Read primary sources alongside it.** When a chapter references Chinchilla scaling results or a specific alignment technique, that is a pointer to read the original work. The chapter gives you framing; the paper gives you detail.

**Return to Volumes I and II.** Frontier topics connect back to shipping constraints regularly. When a Part III efficiency technique connects back to a Vol II deployment decision, that is the connection the book is trying to build.

**Track the field selectively.** Part V covers reading strategy in detail. The short version: one trusted aggregator, one conference track relevant to your work, one open-model release line you follow. Depth beats breadth.

---

*Start with [Part I — Scale, data, and the pretraining stack](from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md). Or start with the part that covers your gap. Previous volume: [From Prompts to Systems — Volume II](../from-prompts-to-systems/from-prompts-to-systems.md).*
