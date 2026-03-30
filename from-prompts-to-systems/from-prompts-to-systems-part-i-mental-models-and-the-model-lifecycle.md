# Part I — Mental models and the model lifecycle

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Volume I explained **what** LLMs are and how they behave in the abstract. This part is about **shipping**: the difference between a **demo** and a **product**, how **training stages** show up in model cards, how to **choose** a model, and how **context, memory, and retrieval** fit together before you dive into prompts and RAG in later parts.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 1–4.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | From playground to product | Latency, cost, ownership, and the stack around the model |
| **2** | Training stages in one picture | Pretraining, instruction tuning, preferences—“smart” vs “aligned” |
| **3** | Choosing a model and reading model cards | Context, license, deployment; open vs closed weights |
| **4** | Context, memory, and state | Truncation, summarization, retrieval vs fine-tune (preview) |

**Contents (plain list — same as table):**

1. From playground to product — stack and product concerns.  
2. Training stages in one picture — base vs chat, axes of capability.  
3. Choosing a model and reading model cards — constraints and cards.  
4. Context, memory, and state — what fits, what to design for.

---

## Chapter 1 — From playground to product

**When did “it works on my laptop” last survive first contact with a customer?** A **playground** proves the model can do something cool once. A **product** does it **reliably**, under **load**, with **clear ownership** when things break.

### What changes at launch

**Latency** budgets appear: users tolerate seconds for some tasks, milliseconds for others. **Cost** becomes continuous—tokens, seats, or inference hours—not a one-off experiment. **Versioning** matters: which **model ID**, which **prompt template version**, which **retrieval index** went into this answer? **Ownership** means an on-call path: who rolls back a bad prompt change?

*Friction smart teams ignore until 2 a.m.:* the model’s **answer** can be perfect while the **system** is wrong—timeouts, missing logs, no idempotent retries on tool calls. Reliability is not a property of the neural net alone.

### The stack around the model

Think in layers: **client** (web, mobile, internal tool) → **application** (your business logic) → **orchestration** (prompt assembly, retrieval, tool routing) → **model provider** (API or self-hosted weights) → **data** (vector store, caches, feature flags). The LLM is one box; **reliability** is a system property.

*Takeaway:* shipping adds latency, cost, versioning, and ownership—map the stack before you optimize the model in isolation.

---

## Chapter 2 — Training stages in one picture

You do not need to train models to **read** how they were produced. Model cards and blog posts refer to **pretraining**, **instruction tuning**, **preference tuning**—different pressures on the same weights.

### Pretraining

The model learns broad **language and world patterns** from large text (and often code). That stage sets rough **knowledge cutoff**, fluency, and “raw” behavior—sometimes ill-suited to chat without later steps.

### Instruction and preference tuning

Later stages teach **dialogue format**, **refusal** boundaries, and **helpfulness** as judged by raters or automated preference models. **Capability** (reasoning, knowledge) and **alignment** (policy, tone) are related but **not identical**: a base model can be strong yet unsafe for direct users; a chat model can be polite yet shallow.

*Memorable mistake:* “We upgraded to the **smarter** model” when the change was mostly **style and policy**—then the team is surprised when **reasoning** did not jump the way marketing implied.

**Compact read:** “Smarter” and “more aligned” are different axes; cards that describe pipeline stages help you predict behavior changes.

---

## Chapter 3 — Choosing a model and reading model cards

**If you A/B test prompts before you read the card, you are optimizing noise.** **Model cards** (and API docs) are your **contract** for what to expect: **context length**, **modalities** (text-only vs vision), **languages**, **license** (can you fine-tune? deploy how?), and **known limitations**.

### Deployment constraints

Will you run **hosted APIs** only, or **on-prem** / **VPC** with certain certifications? Do you need **structured outputs** or **tool calling** as first-class features? Match **requirements** before you benchmark accuracy.

### Open vs closed weights

**Open-weight** models can be inspected, fine-tuned, and run locally—at the cost of **your** ops burden. **Closed APIs** shift **scaling and safety** to the vendor; you get less control over internals. Neither is universally “better”; fit to **risk**, **budget**, and **latency**.

*Direct address:* the “best” model on a leaderboard is not the best model for **your** compliance checklist.

**Summary line:** read the card for context, license, modalities, and limits before A/B testing clever prompts.

---

## Chapter 4 — Context, memory, and state

Everything the model “remembers” in-session is what you put in the **prompt** (plus optional **retrieved** chunks). There is no hidden long-term memory unless **you** build storage and re-injection.

### Truncation and summarization

Long chats and documents exceed **context**. Strategies: **truncate** old turns, **summarize** history, or **start fresh** threads. Each trades **fidelity** for **space**.

*Tiny vignette:* summarization is a **lossy compression** of the conversation—fine for vibes, catastrophic if the lost line was “allergic to penicillin.”

### Session state vs retrieval vs fine-tuning

- **Session state**: your database of user facts, re-injected when relevant.  
- **Retrieval**: fetch **documents** per query (Part III).  
- **Fine-tuning**: adjust weights with **curated** examples—use when behavior must be **consistent** and **prompting + RAG** are insufficient (details in Volume III).

**Closing thread:** context is designed, not magical; retrieval and adaptation are separate tools with separate costs.

---

## Try it

1. **Playground vs product.** List **five** concerns that appear when moving an internal chat demo to a customer-facing feature (e.g. latency, logging). Which are **not** about the raw model quality? If everything on your list sounds like “make the prompt longer,” go back one chapter.

2. **Model card.** Open a **model card** or API doc for a model you might use. Note: **context length**, **license**, **one** limitation, and **one** training stage mentioned. Bonus smugness if you find a limitation that would have embarrassed you in production.

---

*End of Part I. Previous: [From Tokens to Understanding — Volume I](../from-tokens-to-understanding/from-tokens-to-understanding.md) · Next: [Part II — Prompting as engineering](from-prompts-to-systems-part-ii-prompting-as-engineering.md) · Or [main volume](from-prompts-to-systems.md).*
