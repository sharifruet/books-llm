# Part V — Systems: APIs, deployment, and operations

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Models live behind **APIs**. This part covers **wrappers**, **observability**, **cost and rate limits**, and **security** basics—so production incidents are **boring**, not mysterious.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 16–19.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | API design and abstraction layers | Retries, streaming, structured outputs |
| **2** | Observability and logging | Traces, redaction, dashboards |
| **3** | Cost, capacity, and rate limits | Tokens, caching, right-sizing |
| **4** | Security basics for LLM applications | Prompt injection, trust boundaries, sandboxing |

**Contents (plain list — same as table):**

1. API design — abstraction, timeouts, streaming.  
2. Observability — logs, traces, what not to log.  
3. Cost and capacity — tokens, caching, limits.  
4. Security — injection, tools, least privilege.

---

## Chapter 1 — API design and abstraction layers

**How many places in your codebase spell the model name in a string?** Wrap vendor APIs behind **your** interface: **model name**, **temperature**, **max tokens** as **config**, not scattered strings. **Timeouts** and **retries** with **idempotency** keys for **side-effecting** tool calls.

### Structured outputs

Parse **JSON** defensively—models **stray**. **Schema validation** before downstream use. **Streaming** partial tokens: buffer until **valid** chunk if needed.

*Memorable detail:* half-valid JSON during streaming is a **feature** for UX and a **bug** for parsers—design the boundary explicitly.

**Takeaway:** one abstraction layer makes swaps and tests easier; validate all structured output.

---

## Chapter 2 — Observability and logging

Log **request IDs**, **latency**, **token counts**, **model ID**, **error codes**—not **raw** user PII unless required. **Trace** multi-step flows (retrieve → generate → tool).

### Dashboards

Track **error rate**, **p95 latency**, **cost per request**, and **quality** proxies from **offline** evals. **Alert** on spikes—often the first sign of a **bad deploy** or **provider** issue.

*Friction:* logs that **cannot** be correlated across steps are **story fragments**, not observability.

**Summary line:** observability enables blameless postmortems; redact before you aggregate.

---

## Chapter 3 — Cost, capacity, and rate limits

**Token** accounting per **route** and **customer**. **Cache** repeated **context** where safe. **Batch** where latency allows. **Right-size** models: small model for **classification**, large for **generation**—if routing is worth the complexity.

*Direct address:* if you only look at **average** cost per request, tail latency and **retries** will hide in the average like quiet debt.

**Compact read:** cost is a feature; measure before you optimize the wrong layer.

---

## Chapter 4 — Security basics for LLM applications

**Prompt injection**: untrusted text **in** the prompt **directs** the model to ignore instructions or **exfiltrate** data. **Mitigations**: **separate** trusted vs untrusted blocks, **downgrade** privileges for tool calls, **human** approval for **irreversible** actions.

### Sandboxing

Run tools in **minimal** environments; **no** raw SQL from model output without **validation**. **Trust boundaries** mirror classic **web security**—with new angles.

*One-line analogy:* the model is a **clever user agent** that reads every email in the thread—design permissions accordingly.

**Closing thread:** treat the model as an untrusted client; tools are the real power.

---

## Try it

1. **Envelope.** Sketch a **pseudo-request** object your API would send upstream: fields for **model**, **messages**, **tools**, **timeout**. What is **one** field you would **not** expose to the browser? If you cannot think of one, imagine your worst competitor’s **JavaScript** calling your API.

2. **Log policy.** List **three** things worth logging for a single LLM request and **one** thing you would **strip** or **hash** by default. If “full prompt text” is on your log list, say why out loud to a security-minded friend.

---

*End of Part V. Previous: [Part IV — Evaluation, quality, and safety in practice](from-prompts-to-systems-part-iv-evaluation-quality-and-safety-in-practice.md) · Next: [Part VI — Teams, ethics, and the path forward](from-prompts-to-systems-part-vi-teams-ethics-and-the-path-forward.md) · Or [main volume](from-prompts-to-systems.md).*
