# Part IV — First steps with prompts

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

You understand what models are, how they tick at a high level, and where they shine or stumble. This part is **hands-on**: how **chat interfaces** are structured, how to **write prompts** that get closer to what you want, how to **recover** when the model drifts, and—just as important—**when to stop** and use another tool or a human expert. Part V then widens the lens to privacy, misinformation, and daily norms; Volume II goes deeper on shipping real systems.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 13–16.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Chat interfaces and roles | System vs user, scope, and keeping a prompt library |
| **2** | Writing prompts that work | Goals, audience, format—and few-shot patterns |
| **3** | Common failure modes | Diagnosing vagueness, length, format slips, ignored rules |
| **4** | When not to use an LLM | High stakes, secrets, correctness guarantees—and better fits |

**Contents (plain list — same as table):**

1. Chat interfaces and roles — system vs user; prompt library.  
2. Writing prompts that work — goal, audience, format; few-shot.  
3. Common failure modes — vagueness, length, format, ignored rules.  
4. When not to use an LLM — stakes, privacy, proof.

---

## Chapter 1 — Chat interfaces and roles

Most people meet LLMs through a **chat** UI or an **API** that imitates one. A little structure—who speaks first, what the “system” is allowed to say—goes a long way toward **stable** behavior.

### System, user, and assistant turns

In many products, messages are labeled by **role**:

- **System** (or “developer” in some APIs): high-level rules—tone, safety boundaries, format expectations. Not every app shows this field to end users, but it is often there under the hood.  
- **User**: what *you* ask for this turn.  
- **Assistant**: what the model already said; the interface usually fills this in as the conversation grows.

When you **can** edit the system message, treat it as the **contract** for the whole thread: voice, taboo topics, output shape. When you cannot, you may approximate some of that by starting your first user message with “For this conversation, please …”—less reliable, but common.

### Staying in scope

Models **drift**: they pick up style from the last few turns, chase tangents, or “helpfully” answer a different question than you asked. **Narrow** the task in one place (system or first user message): audience, length, what *not* to do. If the thread has gone wrong, **open a new chat** rather than fighting ten rounds of repair—often cheaper in time and tokens.

### Saving and revisiting useful prompts

Good prompts are **assets**. Keep a **personal library**: a note file, a doc, or snippets in a password manager for non-secret templates. Label them by **intent** (“polite decline,” “summarize for executives,” “extract action items”). Revise when a provider **changes models**; behavior shifts with updates.

Version one line of **metadata**: which product, which model name, and the date—future you will thank present you.

> **In this chapter.** Roles structure behavior; system-level instructions matter when exposed; scope and fresh threads beat endless correction; save prompts like reusable tools.

---

## Chapter 2 — Writing prompts that work

A prompt is not magic wording—it is **specification**. You get better results when you make the **goal**, **audience**, **format**, and **constraints** explicit. You can also **show** the pattern you want instead of only describing it.

### Goal and audience first

Before stylistic flourishes, state **what success looks like**:

- *Goal:* “List three pros and two cons,” not “think about this topic.”  
- *Audience:* “For a reader who knows Python but not Rust,” not “make it clear.”

Ambiguous goals invite **plausible** but useless answers.

### Format and constraints

Ask for a **shape**: bullet list, numbered steps, a table (as text), JSON-like fields, maximum words per section. **Constraints** reduce rambling: “At most 200 words,” “No preamble—start with the answer,” “If you are unsure, say what is unknown.”

Constraints also **surface** when the model is guessing—if it cannot obey, you may be asking for something it cannot know.

### Few-shot: show the pattern

**Few-shot** prompting means including **short examples** of input → output you like. The model locks onto **form** quickly: “Questions should be answered like this example.” Two or three mini-examples often beat a long paragraph of verbal description—especially for classification, extraction, or rigid formats.

Keep examples **honest**: do not embed false facts as exemplars unless you are illustrating error handling.

### Iterate, do not litigate

If the first answer is wrong in a **fixable** way, edit the prompt: add one constraint, one example, or one negative (“Do not …”). If the task is inherently **open-ended**, expect to **refine** in a few steps—that is normal, not failure.

> **In this chapter.** Specify goal, audience, format, and limits; use short examples when shape matters; improve prompts iteratively like any spec.

---

## Chapter 3 — Common failure modes—and simple responses

Even clear prompts fail. Recognizing **patterns** of failure speeds recovery: you change the setup instead of arguing with the model in plain anger.

### Too vague

**Symptom:** generic platitudes, hedging everywhere, or answers that could apply to anything.  
**Response:** narrow the task, add a **concrete scenario**, request **structure**, or ask for **assumptions** explicitly listed so you can correct them.

### Too long

**Symptom:** walls of text, repeated points, buried answer.  
**Response:** cap length (“max 150 words”), ask for **answer first then detail**, or request an **outline** before a full draft.

### Wrong format

**Symptom:** prose when you wanted a list; markdown when you needed plain text for a pipeline.  
**Response:** repeat the format **in the example**; use clear delimiters (e.g. lines that say `BEGIN JSON` / `END JSON`, or fenced code blocks in your own workflow); split **format** instruction into its own short paragraph.

### Ignored instructions

**Symptom:** the model does the opposite of a clear rule, or “forgets” earlier in long threads.  
**Response:** move critical rules to **system** or the **start** of the user message; **shorten** context (new thread); **break** the task into steps (“Step 1: outline only. Wait for my OK.”).

### Breaking tasks into steps

For complex work, **sequencing** beats one giant prompt: summarize, then critique, then revise. Ask for an **outline** first when structure matters. *From Prompts to Systems* expands this into workflows and tooling; here, the habit is enough: **decompose**.

> **In this chapter.** Match the fix to the failure—vagueness, length, format, or context limits—and prefer structure and fresh threads over endless repair in one conversation.

---

## Chapter 4 — When not to use an LLM

Competence includes **restraint**. Some tasks are **wrong** for probabilistic text generators: not because the model is “bad,” but because the **error profile** or **privacy** or **accountability** requirements do not fit.

### High-stakes decisions without human review

**Medical, legal, financial, and safety-critical** choices need qualified people and authoritative sources. An LLM might **brainstorm** or **explain concepts**, but it should not be the **sole** basis for diagnosis, filing a lawsuit, or signing a contract. Use it to **prepare questions** for a professional, not to replace one.

### Private or regulated data you should not paste

If putting text into a chat would **violate policy**, **breach contract**, or **harm** someone if leaked—**do not paste it**. Assume cloud chats may be **logged** or used under terms you have not read. For secrets, use **approved** tools: offline models, enterprise contracts with clear data handling, or no AI at all.

### Tasks that need guaranteed correctness

**Formal verification**, **exact accounting** without independent checks, **cryptography**, or **safety-critical control code** need **deterministic** tools and review processes. LLMs **guess** from statistics; they do not **prove** theorems or **certify** systems.

### Matching the tool to the job

Sometimes search, spreadsheets, databases, calculators, or a colleague’s judgment are **strictly better**. The model is strong where **language and rough structure** help; it is weak where **truth, privacy, or proof** is non-negotiable.

> **In this chapter.** Saying no is part of skill: skip or constrain LLM use when stakes, secrecy, or correctness demand something other than fluent text.

---

## Try it

1. **Structured prompt.** Ask for the same small task twice: (A) a vague one-liner, (B) a prompt with **goal, audience, format, and a word limit**. Which output is easier to **use** as-is?

2. **One failure mode.** Deliberately use a vague prompt; when the answer is fluffy, **rewrite the prompt once** using one technique from Chapter 3 (narrow goal, outline first, or split steps). Compare.

---

*End of Part IV. Previous: [Part III — Capabilities and limits](from-tokens-to-understanding-part-iii-capabilities-and-limits.md) · Next: [Part V — Responsibility in everyday use](from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md) · Or [main volume](from-tokens-to-understanding.md).*
