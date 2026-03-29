# Part III — Data, retrieval, and adaptation

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Not every problem is a **prompt** problem. This part is about **when to fetch facts**, **how RAG fits together** at a practical level, **data for adaptation**, and **tools** that connect models to your systems **safely**.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 9–12.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | When to retrieve vs. prompt vs. fine-tune | Decision flow: freshness, privacy, cost |
| **2** | Retrieval-augmented generation (RAG) | Chunking, embeddings, grounding, citations |
| **3** | Curating and labeling data for adaptation | Quality, formats, synthetic data risks |
| **4** | Tools and function calling | Safe tools, retries, orchestration patterns |

**Contents (plain list — same as table):**

1. When to retrieve vs. prompt vs. fine-tune — decision flow.  
2. RAG — chunk, embed, retrieve, generate.  
3. Curating data — labels, quality, synthetic caveats.  
4. Tools and function calling — contracts and orchestration.

---

## Chapter 1 — When to retrieve vs. prompt vs. fine-tune

**Prompting** alone works when **knowledge** is in the model or **not critical**. **Retrieval** when facts are **fresh**, **private**, or **too large** to memorize in weights. **Fine-tuning** when you need **stable style or behavior** across many inputs and prompts are brittle—subject to data cost and Volume III depth.

### Decision flow (simplified)

- Need **latest** docs or **internal** wiki? → **RAG** (or live API tools).  
- Need **consistent brand voice** on millions of requests? → consider **fine-tuning** + eval.  
- One-off **format** or **tone**? → **prompt** + few-shot first.

> **In this chapter.** Match mechanism to constraint: freshness, privacy, cost, and behavior stability.

---

## Chapter 2 — Retrieval-augmented generation (RAG)

**RAG** = **retrieve** relevant chunks, **inject** into context, **generate**. Quality hinges on **chunking** (size, overlap), **embedding** model choice, and **index** freshness.

### Grounding and “not in corpus”

Instruct the model to **cite** or **quote** retrieved text; **refuse** when chunks do not support an answer. **Hallucination** on top of bad retrieval is **worse** than admitting ignorance—design **fallback** UX.

> **In this chapter.** RAG is a pipeline: bad chunks in → fluent garbage out; invest in retrieval quality.

---

## Chapter 3 — Curating and labeling data for adaptation

Whether you **fine-tune** or **build eval sets**, **data quality** beats raw size. **Duplicates** and **biased** raters distort behavior. **Synthetic** data can bootstrap—but may **amplify** model biases; **human** spot checks matter.

> **In this chapter.** Label carefully; watch for feedback loops; synthetic data is a lever, not a cure-all.

---

## Chapter 4 — Tools and function calling

**Tools** are **your** functions: query DB, create ticket, fetch URL—with **schemas** the model fills. **Never** give the model **open shell** or **arbitrary** network unless you **sandbox**.

### Orchestration

Patterns: **single** model with tools; **router** model picks a skill; **small pipeline** (classify → retrieve → answer). Pick **complexity** to match **failure modes** you can test.

> **In this chapter.** Tools need schemas, validation, retries, and least privilege—same as any integration.

---

## Try it

1. **Decision.** Pick one real task (e.g. “answer from our handbook”). Write **two sentences**: why **RAG** vs **prompt-only** for that task.

2. **Tool contract.** Sketch a **JSON schema** for one function (name + two parameters). What could go wrong if the model **hallucinates** an argument?

---

*End of Part III. Previous: [Part II — Prompting as engineering](from-prompts-to-systems-part-ii-prompting-as-engineering.md) · Next: [Part IV — Evaluation, quality, and safety in practice](from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md) · Or [main volume](from-prompts-to-systems.md).*
