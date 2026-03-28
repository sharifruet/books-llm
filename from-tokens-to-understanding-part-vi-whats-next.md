# Part VI — What’s next

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

Volume I ends where serious **practice** begins to need **tools and teams**: APIs, retrieval, measurement, and shipping. This short part **collects** what you should carry in your head—**terms** and **habits**—and points to **Volume II**, *From Prompts to Systems*, so you know what comes next if you want to build rather than only chat.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 20–21.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Glossary path and habits | A checklist of ideas; repeatable behaviors |
| **2** | Bridge to *From Prompts to Systems* | What Volume II covers; how to prepare |

**Contents (plain list — same as table):**

1. Glossary path and habits — core terms; repeatable behaviors.  
2. Bridge to *From Prompts to Systems* — what Volume II adds; how to prepare.

---

## Chapter 1 — Glossary path and habits

You do not need to memorize a dictionary. You **do** need a **small, firm** set of meanings—enough to read documentation without relearning from scratch—and **habits** that survive when models and products change.

### Core terms (working definitions)

Use these as **anchors**; glossaries in products may word them differently.

- **Token** — The model’s atomic piece of text (often a subword). **Cost** and **context limits** are counted in tokens.  
- **Context (window)** — How much text the model can **consider** at once for a single request; older material may drop off in long chats.  
- **Prompt** — Everything you send as **input** for a turn: instructions, examples, and prior dialogue the system includes.  
- **Hallucination** — Confident **false** or **ungrounded** specific claims—not mere disagreement, but **presented-as-fact** errors.  
- **Fine-tuning** — **Further training** on a smaller, task-specific dataset to steer behavior; distinct from **prompting** alone and from **retrieval** (Volume II goes deeper).

If one term still feels fuzzy, **return** to the part of Volume I where it was motivated—definitions stick better with **story**.

### Habits that compound

- **Verify** claims that could hurt someone or spread if wrong: health, money, law, reputation, safety.  
- **Iterate** prompts when output is wrong in a **pattern**: add one constraint, one example, or split the task.  
- **Note** what worked: a line in a notebook, a dated snippet in a doc—**future you** will not remember the magic wording.  
- **Re-read** terms of service when you **change** products or turn on **new** features (training opt-in, retention).  
- **Say no** when the task needs **proof**, **secrecy**, or **human accountability** (Part IV, Chapter 4).

### Keeping the glossary alive

Language drifts: “**alignment**,” “**reasoning**,” “**agent**” mean different things in marketing than in research. When you see a bold claim, ask: **which system**, under **which test**, with **which** limits?

> **In this chapter.** Own a small vocabulary; rehearse habits—verify, iterate, document, re-check policies, refuse bad fits—not just clever prompts.

---

## Chapter 2 — Bridge to *From Prompts to Systems*

*From Prompts to Systems* (Volume II) is the **next book** in this trilogy. Where Volume I stays at the level of **concepts and first prompts**, Volume II is for **people who ship**: features, workflows, and **defensible** choices in the real world.

### What Volume II adds

Expect **deeper** treatment of topics Volume I only **named**:

- **Evaluation** — Metrics, human review, regression when models update, “good enough” for release.  
- **APIs and integration** — Structured outputs, retries, abstraction layers, swapping providers.  
- **Retrieval (RAG)** — When to fetch documents instead of stuffing everything into context; chunking and grounding at a practical level.  
- **Fine-tuning and adaptation** — When it beats prompting, what it costs, what can go wrong.  
- **Tools and orchestration** — Function calling, simple pipelines, **operational** concerns: cost, latency, observability.  
- **Teams and responsibility** — Norms Volume V began; Volume II connects them to **product** decisions.

You do **not** need Volume II to **use** chat responsibly—but you need it to **own** an LLM-backed feature with clarity.

### Skills that help (optional but useful)

- **Light scripting** — Enough Python or JavaScript to call an API and parse **JSON** responses.  
- **Reading JSON** — Objects, arrays, strings; most HTTP APIs speak it.  
- **Basic git** — So experiments with prompts and small apps stay **reproducible**.

None of this requires a computer science degree; it requires **deliberate** practice alongside the book.

### How the trilogy continues

- **Volume III**, *From Models to Frontiers*, steps back to **research and scale**: training stacks, alignment science, efficiency, multimodal and agentic systems—when you need **depth**, not only **shipping**.

### Closing Volume I

If you have worked through Parts I–VI, you have a **grounded** picture: what LLMs are, how they behave, how to **prompt** and **when to stop**, and how to **live** with these tools without surrendering **judgment**. That is enough to be a **thoughtful** user—and a **prepared** reader for everything that follows.

> **In this chapter.** Volume II is the bridge to building; optional skills are learnable; Volume III awaits when you need the frontier.

---

## Try it

1. **Glossary flashcards.** On paper or in a note file, write the five terms from Chapter 1 (**token**, **context**, **prompt**, **hallucination**, **fine-tuning**) **without** peeking—then open the chapter and fix any gaps.

2. **Volume II preview.** Skim the **introduction** of [From Prompts to Systems](from-prompts-to-systems.md). Write **one** topic from Volume II you want next (e.g. evaluation, APIs, RAG) and **one** skill you might practice (e.g. read a JSON example).

---

*End of Volume I — From Tokens to Understanding. Previous: [Part V — Responsibility in everyday use](from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md) · Next: [From Prompts to Systems](from-prompts-to-systems.md) (Volume II) · Or [main volume](from-tokens-to-understanding.md).*
