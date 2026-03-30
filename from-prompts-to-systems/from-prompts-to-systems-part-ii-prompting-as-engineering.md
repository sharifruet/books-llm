# Part II — Prompting as engineering

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Prompts are not vibes—they are **interfaces**. This part treats them like **versioned artifacts**: structure, iteration, debugging, and **UX** for features that stream, fail, and get reviewed by humans.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 5–8.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Prompt structure and patterns | System / user / tools; few-shot and chain-of-thought tradeoffs |
| **2** | Iteration and prompt libraries | Versioning, A/B, templates and guardrails |
| **3** | Failure modes and debugging | Hallucination, format drift, tool misuse—fixes |
| **4** | Interaction and UX for LLM features | Streaming, undo, expectations, team norms |

**Contents (plain list — same as table):**

1. Prompt structure and patterns — roles, patterns, CoT when to use.  
2. Iteration and prompt libraries — version control for prompts.  
3. Failure modes and debugging — diagnose and constrain.  
4. Interaction and UX — streaming, expectations, collaboration.

---

## Chapter 1 — Prompt structure and patterns

**Who speaks first in your API—and does your app even know?** **System** messages set global rules; **user** messages carry the task; **assistant** history is prior output; **tool** messages carry **results** from your code. APIs differ in naming—map them mentally to those roles.

### Few-shot and chain-of-thought

**Few-shot** examples teach **format** faster than prose. **Chain-of-thought** (“think step by step”) can improve **reasoning-heavy** tasks—and can **hurt** when you need **speed**, **brevity**, or when the model **leaks** reasoning you do not want users to see. **Hide** chain-of-thought in internal prompts when appropriate.

*Friction:* CoT can look like “more intelligent” output when it is really **more tokens**—measure latency and user trust, not vibes.

**Takeaway:** roles are contracts; few-shot locks format; CoT is a tool with tradeoffs, not a universal upgrade.

---

## Chapter 2 — Iteration and prompt libraries

Treat prompts like **code**: **branch**, **review**, and **tag** versions (e.g. `prompt-v1.3`, `holiday-tone`). Store them in **git** or a **CMS**—not only in a chat box.

### A/B and offline comparison

For changes that affect **metrics**, run **offline** evals on a **golden set** (Part IV) before live A/B. **Online** experiments need **traffic** and **guardrails**—do not ship prompt changes without a rollback path.

*Memorable detail:* the prompt that wins in a **five-person** Slack poll is not the same as the prompt that wins on **10k** real queries—selection bias wears a friendly face.

### Templates and guardrails

**Variables** (user name, locale) belong in templates, not copy-paste. **Guardrails** (“never output raw JSON to end users”) belong in **system** or **post-processing**, not hope.

**Summary:** version prompts, measure before wide rollout, separate data from policy.

---

## Chapter 3 — Failure modes and debugging

**Hallucination** and **format errors** are not rare bugs—they are **baseline risks**. **Sycophancy** (agreeing with the user) can break **safety** or **accuracy**.

### Techniques

**Decompose** tasks into steps; **self-check** (“list assumptions before answering”); **constrain** output (**JSON schema**, **regex** validation). For **tools**, validate arguments in **code** before execution.

*Direct address:* if your “fix” is always **more instructions in English**, you may be fighting **sampling and objectives**—sometimes structure beats eloquence.

**Compact read:** debug with structure: smaller steps, validation, and explicit uncertainty.

---

## Chapter 4 — Interaction and UX for LLM features

**Streaming** tokens improves perceived speed; pair with **cancel** and **retry**. **Undo** or **edit** last turn reduces frustration when the model drifts.

### Expectations

Tell users **what the feature does not do** (no legal advice, no real-time data unless wired). **Loading** and **error** states should be honest—masking failures erodes trust faster than a blunt error string.

### Team norms

Decide how **engineering** and **design** review **tone**, **disclosure** of AI, and **fallbacks** when the model is down. Document **prompts** and **model IDs** in **runbooks**.

*One-line analogy:* bad loading states are like a **spinning wheel** on a payment form—polite, expensive, and untrustworthy.

**Closing thread:** UX and ops are part of the feature—not polish after the fact.

---

## Try it

1. **Template.** Write a **system** prompt + one **user** template with `{variable}` slots for a task you care about. Version it (`v0.1`) in a file. If you cannot stand to name `v0.1`, you are exactly who this exercise is for.

2. **Debug.** Reproduce **one** failure (wrong format or hallucination). Change **only** the prompt: add a constraint or a single-shot example. Did behavior improve? If not, note whether the failure was **prompt-shaped** at all—or retrieval, tools, or model limits.

---

*End of Part II. Previous: [Part I — Mental models and the model lifecycle](from-prompts-to-systems-part-i-mental-models-and-the-model-lifecycle.md) · Next: [Part III — Data, retrieval, and adaptation](from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md) · Or [main volume](from-prompts-to-systems.md).*
