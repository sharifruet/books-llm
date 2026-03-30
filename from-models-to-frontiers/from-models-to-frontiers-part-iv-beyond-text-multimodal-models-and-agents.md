# Part IV — Beyond text: multimodal models and agents

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

Language is not the only **interface** to the world. This part surveys **multimodal** fusion, **tool use and grounding** at research depth, and **agents**—**planning**, **memory**, and **reliability** over **many** steps.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 12–14.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Multimodal foundations | Vision–language, audio–language, unified vs modular |
| **2** | Tool use, retrieval, and grounding | RAG vs fine-tune vs context; freshness |
| **3** | Agents: planning, memory, multi-step reliability | Architectures, failures, open problems |

**Contents (plain list — same as table):**

1. Multimodal foundations — fusion patterns and eval.  
2. Tool use and grounding — when to retrieve vs memorize.  
3. Agents — planning, memory, evaluation over time.

---

## Chapter 1 — Multimodal foundations

**Vision–language** models map **images and text** into **shared** representational spaces—**contrastive** pretraining, **generative** objectives, or **encoder–decoder** stacks. **Audio–language** follows similar **patterns** with **different** **tokenization** (spectrograms, discrete speech units).

### Unified vs modular

**Unified** transformers over **flattened** multimodal token streams vs **modular** encoders feeding **fusion** layers—**tradeoffs** in **data**, **latency**, and **interpretability**. **Evaluation** is harder than text-only: **grounding**, **hallucinated** objects, **fairness** across **modalities**.

*Memorable failure:* the model **describes** confidently what is not in the pixels—text-only QA errors feel quaint by comparison.

**Takeaway:** multimodal is **not** text plus a side channel—it changes **errors** and **metrics**.

---

## Chapter 2 — Tool use, retrieval, and grounding

Volume II treated **RAG** as engineering. Here the question is when **retrieval** beats long context or fine-tuning for **freshness** and **provenance**, and when **parametric** memory suffices. Grounding in external knowledge needs clear **protocols**—models confabulate citations without tool **discipline**.

*Friction:* “we added tools” does not fix **trust** if the model can still **sound** grounded when the tool returned **nothing**.

**Summary line:** grounding is a **systems** property: **tools**, **retrieval**, and **prompts** together.

---

## Chapter 3 — Agents: planning, memory, and multi-step reliability

**Agents** loop: observe → plan → act (tools, APIs) → update state. **Failure modes** include drift, infinite loops, wrong tool arguments, and unsafe chains of actions.

### Open problems

Credit assignment over long horizons, safe interruptibility, evaluation of open-ended tasks, and alignment when reward is delayed—all **active research**.

*Direct address:* if your agent demo is **five** steps, production is **five hundred**—the debugging surface scales faster than the slide count.

**Closing thread:** agents multiply risk and debugging surface—invest in eval harnesses before hype.

---

## Try it

1. **Multimodal.** Name one evaluation risk specific to vision–language models that does not arise in text-only QA. “Hallucination” is too generic—name a **vision-shaped** failure.

2. **Agent.** Describe one failure mode for a tool-using agent and one mitigation (architecture or process). If your mitigation is “more prompting,” try again with **tool policy** or **human gate**.

---

*End of Part IV. Previous: [Part III — Efficiency: training, inference, and systems](from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md) · Next: [Part V — Frontiers and open problems](from-models-to-frontiers-part-v-frontiers-and-open-problems.md) · Or [main volume](from-models-to-frontiers.md).*
