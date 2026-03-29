# Part II — Alignment, safety, and robustness

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

**Alignment** is not a single slider. This part covers **goals and tensions**, **evaluation under attack**, **interpretability and monitoring**, and **governance**—at a level that connects **papers** to **deployment** without pretending the field is solved.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 5–8.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Alignment in practice: goals and tensions | Helpfulness vs honesty vs harmlessness; Goodhart |
| **2** | Red teaming, eval harnesses, adversarial robustness | Jailbreaks, shift, long-horizon use |
| **3** | Interpretability and monitoring | Representations vs behavior; drift and escalation |
| **4** | Governance, deployment, and dual-use | Release, capability evals, policy pointers |

**Contents (plain list — same as table):**

1. Alignment goals and tensions — tradeoffs and gaming.  
2. Red teaming and robustness — eval harnesses, adversaries.  
3. Interpretability and monitoring — what you can monitor in prod.  
4. Governance and dual-use — release and institutions.

---

## Chapter 1 — Alignment in practice: goals and tensions

Common shorthand—**helpful, honest, harmless**—masks **tensions**: **helpful** answers can be **harmful** if wrong; **refusal** can be **honest** but **unhelpful**. **Metrics** for each axis conflict under **optimization**—**Goodhart** effects when teams maximize one score.

### Specification gaming

Models (and **humans** in the loop) optimize **measurable** proxies. **Red-team** for **proxy failure**; **combine** behavioral tests with **judgment**.

> **In this chapter.** Alignment is multi-objective; watch for gaming the metric you publish internally.

---

## Chapter 2 — Red teaming, eval harnesses, and adversarial robustness

**Red teaming** means **structured** attempts to elicit **harm** or **policy violations**—by **humans** and **automation**. **Jailbreaks** evolve with **mitigations**; **static** test suites go stale.

### Distribution shift and long horizons

**Train** distributions rarely match **deployment**. **Long-horizon** tasks compound **small** errors. **Robustness** requires **stress tests**, not only average-case accuracy.

> **In this chapter.** Safety evals are **living** systems; adversaries do not stop at your last benchmark.

---

## Chapter 3 — Interpretability and monitoring

**Interpretability** spans **mechanistic** (circuits, features in weights) and **behavioral** (does it do what we want on tests?). For **operators**, **behavioral** monitoring plus **limited** mechanistic insight often beats **pretty** visualizations with no **action**.

### Monitoring deployed systems

Track **drift** in inputs and outputs, **misuse** patterns, and **escalation** paths to **human** review. **Interpretability** without **governance** does not **fix** incidents.

> **In this chapter.** Know what you can **measure** in production; invest in **alerts** and **playbooks**.

---

## Chapter 4 — Governance, deployment, and dual-use

**Release** strategies range from **full open** weights to **API-only** with **safety** filters. **Capability evaluations** attempt to **bound** risk before **wide** release—**imperfect** but better than **vibes**.

### Dual-use and policy

Powerful models enable **benefit** and **misuse**; **international** and **institutional** contexts differ. This book **points** to policy literatures rather than **prescribing** law.

> **In this chapter.** Governance is **choices** under uncertainty; pair technical evals with **stakeholder** process.

---

## Try it

1. **Tradeoff.** Name **two** alignment goals that can **conflict** on the same user query and how you might **disambiguate** in product policy.

2. **Red team.** Draft **one** adversarial user goal (non-harmful to describe) that tests **over-refusal** vs **under-safety**—what would you **measure**?

---

*End of Part II. Previous: [Part I — Scale, data, and the pretraining stack](from-models-to-frontiers-part-i-scale-data-and-the-pretraining-stack.md) · Next: [Part III — Efficiency: training, inference, and systems](from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md) · Or [main volume](from-models-to-frontiers.md).*
