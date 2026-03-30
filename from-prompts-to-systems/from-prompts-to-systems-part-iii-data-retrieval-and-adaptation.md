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

**If the answer lives in your wiki and changes every Monday, “try a longer prompt” is not a strategy—it is denial.**

**Prompting** alone works when **knowledge** is in the model or **not critical**. **Retrieval** when facts are **fresh**, **private**, or **too large** to memorize in weights. **Fine-tuning** when you need **stable style or behavior** across many inputs and prompts are brittle—subject to data cost and Volume III depth.

### Decision flow (simplified)

- Need **latest** docs or **internal** wiki? → **RAG** (or live API tools).  
- Need **consistent brand voice** on millions of requests? → consider **fine-tuning** + eval.  
- One-off **format** or **tone**? → **prompt** + few-shot first.

*Friction:* teams **fine-tune** because it feels serious when the real bug was **chunking** and **index freshness**. Mechanism should match constraint.

**Takeaway:** match mechanism to constraint—freshness, privacy, cost, and behavior stability.

---

## Chapter 2 — Retrieval-augmented generation (RAG)

**RAG** = **retrieve** relevant chunks, **inject** into context, **generate**. Quality hinges on **chunking** (size, overlap), **embedding** model choice, and **index** freshness.

### Grounding and “not in corpus”

Instruct the model to **cite** or **quote** retrieved text; **refuse** when chunks do not support an answer. **Hallucination** on top of bad retrieval is **worse** than admitting ignorance—design **fallback** UX.

*Anchor:* fluent garbage with **citations that point at the wrong paragraph** is a special kind of betrayal—users trust the *shape* of an answer.

**Summary line:** RAG is a pipeline: bad chunks in → fluent garbage out; invest in retrieval quality before you tune adjectives in the prompt.

---

## Chapter 3 — Curating and labeling data for adaptation

Whether you **fine-tune** or **build eval sets**, **data quality** beats raw size. **Duplicates** and **biased** raters distort behavior. **Synthetic** data can bootstrap—but may **amplify** model biases; **human** spot checks matter.

*Direct address:* if your labeling queue is mostly **whatever was cheapest to export**, your “ground truth” is a **historical accident**, not a north star.

**Compact read:** label carefully; watch for feedback loops; synthetic data is a lever, not a cure-all.

---

## Chapter 4 — Tools and function calling

**Tools** are **your** functions: query DB, create ticket, fetch URL—with **schemas** the model fills. **Never** give the model **open shell** or **arbitrary** network unless you **sandbox**.

### Orchestration

Patterns: **single** model with tools; **router** model picks a skill; **small pipeline** (classify → retrieve → answer). Pick **complexity** to match **failure modes** you can test.

*Memorable mistake:* the model “called” a function with a **plausible** `user_id` that belonged to someone else—**validation** is not optional.

**Closing thread:** tools need schemas, validation, retries, and least privilege—same as any integration.

---

## Try it

1. **Decision.** Pick one real task (e.g. “answer from our handbook”). Write **two sentences**: why **RAG** vs **prompt-only** for that task. If you wrote “because RAG is more advanced,” try again with **freshness** or **privacy** in the first sentence.

2. **Tool contract.** Sketch a **JSON schema** for one function (name + two parameters). What could go wrong if the model **hallucinates** an argument? If your answer is “nothing, we trust it,” Part V has questions for you.

---

*End of Part III. Previous: [Part II — Prompting as engineering](from-prompts-to-systems-part-ii-prompting-as-engineering.md) · Next: [Part IV — Evaluation, quality, and safety in practice](from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md) · Or [main volume](from-prompts-to-systems.md).*
