# From Prompts to Systems

*Intermediate practice with large language models — Volume II*

## Audience

**Developers, analysts, product managers, and technical writers** who already use LLMs in daily work and want **clearer mental models**, **repeatable workflows**, and **enough depth to ship** features—not just one-off prompts—without yet diving into research-scale training or frontier theory (that is Volume III). You should be comfortable with *From Tokens to Understanding* (Volume I) or equivalent: tokens, context windows, basic prompting, and honest limits of the technology.

---

## Introduction

### What this book is for

Volume I answers **what** language models are and **how to begin** using them responsibly. *From Prompts to Systems* answers **how to turn that familiarity into practice you can defend**: choosing approaches (prompt vs. retrieval vs. fine-tuning), **iterating with data**, **measuring quality**, **wiring models into software**, and **operating** them with costs, failures, and teams in mind.

The emphasis is **applied**: fewer proofs, more **decision patterns**—when a longer prompt beats a pipeline change, when evaluation should block a release, how to structure an API layer so you can swap models later. The goal is that after this volume you can own an LLM-powered feature from prototype to something your team can maintain—and know what Volume III will unpack if you need to go deeper on training, safety science, or scale.

### How this volume is organized

The outline groups material into **pillars** that mirror real projects: **understanding what you are shipping**, **designing prompts and interactions**, **adapting behavior** (data, retrieval, light fine-tuning), **evaluating and monitoring**, **building integrations**, and **shipping responsibly**. Themes like **evaluation** and **safety** appear in more than one part because they are both design-time and runtime concerns.

Chapters are written to support **hands-on progression**: you can draft exercises (small apps, eval sets, prompt libraries) per part even before the prose is final.

### Prerequisites and suggested use

You should be comfortable using at least one **chat or API** interface, reading **JSON**-shaped API responses, and thinking in terms of **inputs, outputs, and failure cases**. Light scripting (e.g. Python or JavaScript) will help for later chapters; where code is essential, the book can stay pseudocode-first.

Use the outline as a **manuscript contract**: merge or split chapters as your teaching style evolves. Keep implementation notes, vendor-specific quirks, and bibliography in **Notes** or sidecar files so the main text stays durable.

---

## Detailed outline

### Part I — Mental models and the model lifecycle

1. **From playground to product**  
   - What changes when a demo becomes a feature: latency, cost, versioning, ownership.  
   - The stack: model provider, orchestration, application UI, data stores.

2. **How training, instruction tuning, and “the base model” relate**  
   - Pretraining vs. instruction-tuning vs. preference tuning—intuition only, enough to read model cards.  
   - Why “smarter” and “more aligned” are different axes.

3. **Choosing a model and reading model cards**  
   - Context length, modalities, license, and deployment constraints.  
   - Open vs. closed weights; what you can and cannot assume.

4. **Context windows, memory, and state**  
   - What fits in context; summarization and truncation as design problems.  
   - Session state vs. retrieval vs. fine-tuning—preview of later parts.

### Part II — Prompting as engineering

5. **Prompt structure and patterns**  
   - System vs. user vs. tool messages; role and format conventions.  
   - Few-shot examples, chain-of-thought when to use it, and when it hurts.

6. **Iteration and prompt libraries**  
   - Versioning prompts like code; A/B and offline comparison.  
   - Templates, variables, and guardrails in prompt design.

7. **Failure modes and debugging**  
   - Hallucination, sycophancy, formatting errors, inconsistent tool use.  
   - Techniques: decomposition, self-check, constraining output shape (JSON, schemas).

8. **Interaction and UX for LLM features**  
   - Streaming, partial results, undo, and setting user expectations.  
   - Writing and technical communication with LLM assistance—team norms.

### Part III — Data, retrieval, and adaptation

9. **When to retrieve vs. prompt vs. fine-tune**  
   - Decision flow: freshness, privacy, cost, latency.  
   - High-level picture of supervised fine-tuning and preference tuning (details deferred to Volume III where needed).

10. **Retrieval-augmented generation (RAG)**  
    - Chunking, embeddings, vector stores—conceptual and practical.  
    - Grounding, citation, and handling “not in the corpus.”

11. **Curating and labeling data for adaptation**  
    - Example formats; quality over quantity; avoiding feedback loops.  
    - Synthetic data: benefits and risks.

12. **Tools and function calling**  
    - Designing safe, bounded tools; error handling and retries.  
    - Orchestration patterns (single model vs. router vs. small pipelines).

### Part IV — Evaluation, quality, and safety in practice

13. **What to measure**  
    - Task accuracy, helpfulness, latency, cost per successful outcome.  
    - Human eval vs. model-as-judge vs. automatic metrics—tradeoffs.

14. **Test sets, regression testing, and CI for LLM features**  
    - Golden sets; snapshotting behavior across model upgrades.  
    - Breaking changes when the provider updates a model.

15. **Safety and abuse in product context**  
    - Policy layers, blocklists, classifiers, and escalation.  
    - PII, confidentiality, and data retention choices.

### Part V — Systems: APIs, deployment, and operations

16. **API design and abstraction layers**  
    - Wrapping providers; timeouts, retries, idempotency, streaming.  
    - Structured outputs and parsing robustness.

17. **Observability and logging**  
    - What to log (and what not to); tracing multi-step flows.  
    - Dashboards for quality and cost.

18. **Cost, capacity, and rate limits**  
    - Token accounting; caching; batch vs. interactive.  
    - Right-sizing model choice for each subtask.

19. **Security basics for LLM applications**  
    - Prompt injection overview; trust boundaries for tools and retrieval.  
    - Sandboxing and least privilege for automated actions.

### Part VI — Teams, ethics, and the path forward

20. **Working in cross-functional teams**  
    - Roles: ML, backend, design, legal; review checkpoints.  
    - Documentation and handoff for LLM features.

21. **Responsible deployment (intermediate stance)**  
    - Transparency, user control, and proportionality—without duplicating Volume III’s depth.  
    - When to escalate to safety specialists or policy review.

22. **Bridge to *From Models to Frontiers***  
    - What Volume III adds: scaling, alignment science, efficiency, frontier research.  
    - Suggested reading order and skills to sharpen next.

---

## Notes

_Add chapter notes, exercises, vendor-specific appendices, and references here as the manuscript grows._
