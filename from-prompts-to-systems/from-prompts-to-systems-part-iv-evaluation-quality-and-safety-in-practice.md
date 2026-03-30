# Part IV — Evaluation, quality, and safety in practice

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

**You ship what you measure.** This part covers **metrics**, **golden sets** and **regression** discipline, and **product safety** layers—so improvements do not become accidents at scale.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 13–15.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | What to measure | Task quality, latency, cost, human vs automatic judgment |
| **2** | Test sets, regression testing, and CI | Golden sets, model upgrades, breaking changes |
| **3** | Safety and abuse in product context | Policies, classifiers, PII, escalation |

**Contents (plain list — same as table):**

1. What to measure — metrics that match the job.  
2. Test sets and regression — golden sets, CI mindset.  
3. Safety and abuse — layers and data handling.

---

## Chapter 1 — What to measure

**Which number would you defend in a postmortem—the leaderboard score or the refund rate?** **Accuracy** on a task is not one number: **correctness** of facts, **helpfulness**, **format** adherence, **latency**, **cost per success**, and **harm** rate. Pick **few** primary metrics aligned with **user value**—not every leaderboard score.

### Human vs model-as-judge vs automation

**Human** labels are gold but expensive. **Model-as-judge** scales but inherits **biases**. **Automatic** checks (JSON valid, regex, unit tests on tool args) are **cheap**—combine layers.

*Friction:* the metric you **optimize** becomes the behavior you **get**—Goodhart visits LLM teams too.

**Takeaway:** define success in user terms; mix human spot checks with scalable signals.

---

## Chapter 2 — Test sets, regression testing, and CI for LLM features

A **golden set** is a **fixed** batch of inputs (and often expected properties) you run on **every** prompt or model change. **Snapshot** outputs or **scores**—watch for **drift** when providers **silent-upgrade** models.

### CI mindset

**Block releases** when golden metrics fall below threshold—same as unit tests. **Pin** model versions in config until you **re-validate**.

*Tiny vignette:* “nothing changed in our code” is compatible with “the provider swapped weights on Tuesday.” Pinning is not paranoia—it is **versioning**.

**Summary line:** treat prompt and model changes like code changes: test before merge.

---

## Chapter 3 — Safety and abuse in product context

**Policy layers** (blocklists, classifiers, moderation APIs) sit **beside** the model—not as a substitute for **good prompts**, but as **defense in depth**. **PII**: **minimize** what you log; **retention** policies are part of **security**.

### Escalation

Define **when** a human reviews **edge cases**—legal, self-harm, targeted harassment. **Automation** should not be the last word on every abuse report.

*Direct address:* if your moderation story is “we used the API flag,” you may have outsourced **judgment** without outsourcing **accountability**.

**Closing thread:** safety is product design: layers, logging discipline, and human escalation paths.

---

## Try it

1. **One metric.** Pick a feature you know. Name **one** measurable outcome (e.g. “% answers with valid JSON”) and **one** human-judged aspect. If they are the same metric dressed in two adjectives, split them until they are not.

2. **Golden test.** Write **three** input prompts you would put in a **regression** suite for that feature and **what** you would check automatically vs manually. Bonus: include **one** nasty edge case you are tempted to skip—that is usually the one that burns you.

---

*End of Part IV. Previous: [Part III — Data, retrieval, and adaptation](from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md) · Next: [Part V — Systems: APIs, deployment, and operations](from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md) · Or [main volume](from-prompts-to-systems.md).*
