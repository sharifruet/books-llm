# Part III — Efficiency: training, inference, and systems

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

**Efficiency** decides what is **affordable** to train and **cheap** enough to serve. This part spans **training** systems, **inference** tricks, and **hardware** context at a **decision-maker** level—not a cluster manual.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 9–11.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Training efficiency | Precision, parallelism, checkpoints, curriculum |
| **2** | Inference efficiency | Quantization, distillation, KV cache, latency–quality–cost |
| **3** | Specialized hardware and software stacks | GPUs/TPUs, compilers, APIs vs custom silicon |

**Contents (plain list — same as table):**

1. Training efficiency — scale compute wisely.  
2. Inference efficiency — serve cheaply at quality.  
3. Hardware and stacks — constraints on design.

---

## Chapter 1 — Training efficiency

**Mixed precision** (e.g. bf16/fp16) cuts **memory** and increases **throughput** when numerically stable. **Parallelism** (data, tensor, pipeline, expert) trades **complexity** for **scale**. **Checkpointing** and **fault tolerance** matter when jobs run **days** and **fail**.

### Curriculum and data order

**Data ordering** and **curriculum** can affect **convergence** and **final** behavior—often underexplored vs raw **FLOPs**.

> **In this chapter.** Training efficiency is **systems + ML**; profile before **mythical** optimizations.

---

## Chapter 2 — Inference efficiency

**Quantization** reduces **weight** and **activation** precision for **smaller** footprints and **faster** matmuls—watch **accuracy** cliffs per task. **Distillation** transfers behavior from **teacher** to **student**. **Speculative decoding** uses **small** models to **draft** tokens for **large** models. **KV-cache** memory dominates **long** contexts at **serve** time.

### Latency, quality, cost

Product decisions live on a **Pareto** surface—**no** single “best” model. **Measure** **SLOs** and **$/query**.

> **In this chapter.** Inference economics often **dominate** training **amortized** over users—optimize the **right** stage.

---

## Chapter 3 — Specialized hardware and software stacks

**GPUs** and **TPUs** remain central; **compiler** stacks (kernel fusion, layout) change **real** throughput. **Hosted APIs** outsource **capacity planning**; **self-hosted** shifts **burden** to your **team**.

### Custom silicon

**ASICs** for inference/training **reshape** **$/token** when **volume** justifies **NRE**. **Decision** level: know **when** vendor **roadmaps** matter to **your** **scale**.

> **In this chapter.** Hardware is **not** neutral—it **filters** which **techniques** are practical at **your** size.

---

## Try it

1. **Inference tradeoff.** Pick **one** technique (quantization, speculative decoding, smaller model). Name **what** you gain and **what** you risk.

2. **Bottleneck.** For a **long-context** chat product, is **training** or **inference** more likely to dominate **marginal** cost at scale? One sentence **why**.

---

*End of Part III. Previous: [Part II — Alignment, safety, and robustness](from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) · Next: [Part IV — Beyond text: multimodal models and agents](from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md) · Or [main volume](from-models-to-frontiers.md).*
