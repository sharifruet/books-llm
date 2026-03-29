# Part I — Scale, data, and the pretraining stack

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

This part is about **why** large models look the way they do: **scaling trends**, **data** at web scale, **architecture** choices at survey depth, and **post-training** stages that turn a base model into something you can ship. It complements Volume II’s practice with **research- and systems-level** framing.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 1–4.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Scaling laws and predictable returns | Compute, data, size, loss—budgeting without mysticism |
| **2** | Data at scale: curation, contamination, documentation | Filtering, leakage, datasheets |
| **3** | Architecture variants and inductive biases | Transformers, MoE, long context—what scale vs prior explains |
| **4** | Post-training: beyond next-token prediction | SFT, preferences, multistage pipelines |

**Contents (plain list — same as table):**

1. Scaling laws — predictable returns and limits.  
2. Data at scale — curation, contamination, documentation.  
3. Architecture variants — survey-level; inductive biases.  
4. Post-training — instruction tuning and preference optimization.

---

## Chapter 1 — Scaling laws and predictable returns

**Scaling laws** summarize empirical relationships: for a family of models, **loss** (or downstream metrics) often improves predictably as you increase **compute**, **data**, or **parameters**—holding other factors roughly constant.

### Chinchilla-style tradeoffs

Rough guidance from the Chinchilla line of work: given a **fixed compute** budget, **undertraining** huge models on too little data is wasteful; **balance** model size and **tokens seen**. Exact numbers depend on **recipe** and **architecture**—treat laws as **planning tools**, not universal constants.

### Limits of the intuition

**Data quality** beats raw token count when domains shift. **Saturation** appears when benchmarks max out or **memorization** dominates. **Domain shift** breaks naive scaling plots. **Inference** and **alignment** costs may dominate **product** economics even when training scaled well.

> **In this chapter.** Scaling laws help budget experiments; they do not replace measurement on **your** task and distribution.

---

## Chapter 2 — Data at scale: curation, contamination, and documentation

**Web-scale** corpora need **filtering** (quality, toxicity, PII), **deduplication** (exact and fuzzy), and often **language** or **domain** balancing. Aggressive dedup can **remove** useful repetitions (e.g. boilerplate) or **skew** rare domains—**tradeoffs**, not free wins.

### Contamination and benchmarks

**Test-set leakage** inflates scores. **Documentation** of training cutoffs and **benchmark** construction matters for **honest** comparisons. Treat leaderboard numbers with **provenance**.

### Datasheets for datasets

**Datasheets** and **data statements** document **intent**, **provenance**, **limitations**, and **biases**—minimal professionalism for datasets that train **foundation** models.

> **In this chapter.** Data is the second half of scaling; curation and documentation are part of **science**, not housekeeping.

---

## Chapter 3 — Architecture variants and inductive biases

Transformers remain **dominant**, but variants matter: **long-context** methods (attention approximations, sliding windows), **mixture-of-experts** (sparse activation for scale), **state-space** and hybrid models in some niches. At **survey** level: know **what problem** each family addresses.

### Scale vs prior

Some behaviors **emerge** with scale; others are **built in** by **architecture** and **objective**. Separating the two requires **controlled** comparisons—not only headline parameters.

> **In this chapter.** Architecture is a lever; empirical validation on your workload beats brand names.

---

## Chapter 4 — Post-training: beyond next-token prediction

**Pretraining** optimizes **next-token** loss on broad text. **Instruction tuning** (supervised fine-tuning on demonstrations) teaches **task format** and **dialogue**. **Preference** optimization (**RLHF**, **DPO**, cousins) nudges outputs toward **human-rated** or **AI-rated** preferences.

### Multistage pipelines

Typical story: **pretrain** → **SFT** → **preference** training → optional **iterative** rounds with **evaluation** gates. Each stage can **shift** capabilities and **failure modes**—**not** interchangeable knobs.

> **In this chapter.** Post-training aligns **behavior** to deployment needs; it is not “one more epoch” of pretraining.

---

## Try it

1. **Scaling intuition.** In two sentences, explain why **doubling parameters** without more **data** may **not** follow the same loss curve as a balanced scaling policy.

2. **Leakage.** Name **one** way benchmark **contamination** can inflate scores and **one** mitigation researchers use.

---

*End of Part I. Previous: [From Prompts to Systems — Volume II](../from-prompts-to-systems/from-prompts-to-systems.md) · Next: [Part II — Alignment, safety, and robustness](from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) · Or [main volume](from-models-to-frontiers.md).*
