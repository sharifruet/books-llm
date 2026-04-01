# Part VI — What's next

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

Volume I ends where serious **practice** begins to need tools and teams: APIs, retrieval, measurement, and shipping. This short part collects what you should carry in your head — **terms** and **habits** — and points clearly to **Volume II**, *From Prompts to Systems*, so you know what comes next if you want to build rather than only chat.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 20–21.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Glossary and habits | Core terms consolidated; repeatable behaviors |
| **2** | Bridge to *From Prompts to Systems* | What Volume II covers; how to prepare |

**Contents (plain list — same as table):**

1. Glossary and habits — core terms; repeatable behaviors.
2. Bridge to *From Prompts to Systems* — what Volume II adds; how to prepare.

---

## Chapter 1 — Glossary and habits

You do not need to memorize a dictionary. You need a **small, firm** set of meanings — enough to read documentation without re-learning from scratch — and **habits** that survive when models and products change. Terms are anchors; habits are what you actually do on a Tuesday.

### Core terms

These twelve terms appear constantly in documentation, announcements, and conversations about LLMs. The definitions here are working definitions — they give you enough to operate; the parts of Volume I where each was introduced give you the full context.

**Token** — The model's atomic unit of text: roughly a subword, word, or punctuation mark. Cost and context limits are counted in tokens. The mapping between words and tokens is not one-to-one; common text costs fewer tokens than rare text.

**Context window** — The maximum number of tokens the model can consider in a single request, including system prompt, conversation history, retrieved documents, and the user's message. Material outside the window is invisible to the model during that request.

**Prompt** — Everything you send as input for a turn: system instructions, examples, prior conversation the interface includes, retrieved text, and your current message.

**Hallucination** — A confident, specific, fluent output that is factually false or unsupported. A structural property of how these models work, not a rare bug. Hallucinations are especially common for specific numbers, citations, biographical details, and events near or after the training cutoff.

**Temperature** — A parameter controlling how randomly the model samples from its probability distribution at each step. Lower temperature = more predictable, more repetitive. Higher = more varied, more creative, more likely to wander.

**Pretraining** — The large-scale first training phase where a model learns from enormous text corpora to predict the next token. Defines the model's raw capability and knowledge cutoff.

**Instruction tuning (SFT)** — A later training phase that teaches the model to behave as an assistant: answer questions, follow instructions, stay on topic. Runs on a smaller, curated dataset of example interactions.

**Fine-tuning** — Further training on a specific, smaller dataset to steer the model's behavior toward a particular domain, style, or task. Distinct from prompting (no weights change in prompting) and from retrieval (no training involved in retrieval).

**RAG (Retrieval-Augmented Generation)** — A pattern where relevant documents are fetched and injected into the context before generation, so the model can ground its answers in supplied text rather than parametric memory alone. Volume II covers this in depth.

**System prompt** — The instructions placed before the conversation begins, usually by the product or developer, setting rules and context for the entire session.

**Alignment** — The ongoing effort to make model behavior match intended goals: helpful, honest, avoiding harm. Not guaranteed by scale alone; an active area of research and practice.

**Model card** — A document published alongside a model describing its intended use, training data, known limitations, and evaluation results. Your primary reference for any model you use in production.

### Habits that compound

These are not one-time actions. They are repeated behaviors that build over time into something valuable.

**Verify before you rely.** Any specific claim — a number, a citation, a name, a date — that would matter if wrong should be checked against a primary source before you use it. Make this automatic for anything you publish, file, present, or share.

**Iterate prompts with structure.** When output is wrong in a fixable way, add one thing: a constraint, an example, a narrowed scope, a format specification. One change at a time tells you what actually worked. Five simultaneous changes tell you nothing.

**Note what worked.** Keep a prompt library. Date your entries. Note which model and product version produced the result. Future you will not remember the magic wording, and you will want it again.

**Re-read terms when you change products or features.** Privacy policies and training use policies change. Each time you turn on a new feature or switch to a new tool, skim the current policy. What you remembered from six months ago may no longer be accurate.

**Say no when the task needs proof, privacy, or human accountability.** This is the hardest habit. It requires recognizing when a task genuinely does not fit the tool — and choosing a different one.

*Tiny vignette:* The practitioners who get the most out of these tools are reliably boring about it: they write down what worked, they re-check their prompts when behavior changes, and they say "I need to verify this" out loud before sharing a model output with anyone who matters. There is no glamour in it. It works.

### Signs you have internalized Volume I

You know the material is in use when:

- You naturally distinguish between "the model is confident" and "the model is correct" — and reach for a second source for things that matter.
- You can explain to a colleague why a long conversation might produce worse results than a fresh one.
- You describe model behavior in mechanistic terms rather than anthropomorphic ones ("it continued the pattern" rather than "it decided").
- You check whether your task needs proof or privacy before using an AI tool, not after.
- You have a prompt library. Even a small one.

### Quick takeaway

- Twelve terms to know: token, context window, prompt, hallucination, temperature, pretraining, instruction tuning, fine-tuning, RAG, system prompt, alignment, model card.
- Five habits that compound: verify, iterate with structure, note what worked, re-read policies on change, say no when the task requires it.
- Understanding is in the behavior, not the memorization.

---

## Chapter 2 — Bridge to *From Prompts to Systems*

*From Prompts to Systems* (Volume II) is for people who are past the demo stage and want to build. Where Volume I stays at the level of **concepts and first prompts**, Volume II is about **defensible practice**: choosing approaches, measuring quality, wiring models into software, and operating them with costs, failures, and teams in mind.

### What Volume II adds

**Evaluation.** Volume I tells you hallucination is a structural risk. Volume II teaches you how to measure it: building golden test sets, running regression checks when models update, distinguishing human evaluation from automated metrics, and defining "good enough for release."

**APIs and integration.** Moving from a chat interface to an API call is not a large technical step — but it opens the door to everything else. Volume II covers prompt versioning, structured outputs, retries, abstraction layers that let you swap models without rewriting your application, and the operational questions that follow: latency, cost accounting per route, and what to log.

**Retrieval-Augmented Generation (RAG).** The practical pattern for giving models access to your own documents, databases, or up-to-date information without fine-tuning. Chunking strategies, embedding models, vector stores, retrieval quality, and the failure modes that matter when bad retrieval produces fluent garbage.

**Fine-tuning and adaptation.** When prompting and RAG are not enough, and when fine-tuning the model's weights is actually worth the cost and complexity. Volume II covers the decision, the data requirements, and the risks.

**Tools and orchestration.** Function calling, structured tool use, simple pipelines (classify → retrieve → answer), and the security and validation requirements that come with giving a model the ability to take actions.

**Teams and responsibility.** The norms Volume V began — Volume II connects them to product decisions: who owns what, what to document, how to handle incidents, and what responsible deployment looks like in practice rather than in principle.

### Who should read Volume II

Volume II is worth reading if you are:

- A **developer** building any feature that calls an LLM API, even occasionally.
- A **product manager** who needs to make decisions about which approach to use, what to measure, and how to scope LLM features.
- A **technical writer or analyst** who creates or evaluates AI-assisted content workflows.
- Anyone who needs to **defend a choice** about LLM use to a team, a client, or a stakeholder.

You do not need Volume II to use chat tools responsibly — Volume I is enough for that. You need it to **own a feature** with clarity.

### Skills that will help

These are not prerequisites — they are things that make Volume II richer:

- **Light scripting** — enough Python or JavaScript to call an HTTP endpoint and parse a JSON response. One evening with a tutorial is sufficient.
- **Reading JSON** — objects, arrays, strings, numbers. Most model APIs speak JSON; most structured outputs are JSON.
- **Basic git** — so you can version control prompts as you do code, and so experiments stay reproducible.

None of this requires formal training. It requires deliberate practice alongside the reading.

### How the trilogy continues

**Volume III**, *From Models to Frontiers*, is for those who need research depth: scaling laws, training stacks, alignment science, efficiency at the hardware level, multimodal architectures, agentic systems, and the open problems that define the field's current limits. It is worth reading when you need to **evaluate frontier claims critically**, **contribute to technical decisions**, or **understand the science behind the product** rather than just the product.

### Closing Volume I

If you have worked through Parts I–VI, you have a grounded picture: what these systems are, how they behave, how to prompt thoughtfully, when to stop, and how to live with these tools without surrendering judgment. That is enough to be a thoughtful user — and a prepared reader for everything that follows.

The tools will change. The mechanisms described in this book will be implemented in new ways and with new capabilities. But the fundamental structure — statistical pattern-completion, no internal truth-checking, finite context, outputs that can sound certain while being wrong — is durable. What you have learned here ages better than any specific product feature.

*Direct address:* If you only skimmed this volume, the glossary and habits in Chapter 1 still help. But the habits work best when *Try it* was not only read. Go back and do one exercise you skipped. The friction is the point.

---

## Try it

### Exercise 1 — Glossary recall

Without peeking, write a one-sentence definition of each of the twelve terms from Chapter 1. Then check against the chapter.

For any you got wrong or could not remember: return to the part of Volume I where that term was motivated. Definitions stick better after the story behind them.

### Exercise 2 — Habits audit

Look at the five habits from Chapter 1. For each one, write honestly: do you do this consistently, sometimes, or never? For the "never" ones, pick one and decide on a specific trigger — "when I am about to share a model output with someone else, I will..." — that would turn it into a behavior.

### Exercise 3 — Volume II preview

Open [From Prompts to Systems](../from-prompts-to-systems/from-prompts-to-systems.md). Read the introduction section. Pick one topic from Volume II that you most want to learn next — evaluation, RAG, APIs, fine-tuning, teams — and write two sentences: what you want to understand about it, and what problem you are hoping it solves for you.

No wrong answers. Only unfollowed curiosity.

### Exercise 4 — Teach it back

Find someone who has not read this book — a colleague, a friend, a family member who has asked about AI. Explain one idea from Volume I in under two minutes, without notes.

What you can explain to someone else, you understand. What comes out mangled is what you should re-read.

---

*End of Volume I — From Tokens to Understanding. Previous: [Part V — Responsibility in everyday use](from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md) · Next: [From Prompts to Systems](../from-prompts-to-systems/from-prompts-to-systems.md) (Volume II) · Or [main volume](from-tokens-to-understanding.md).*
