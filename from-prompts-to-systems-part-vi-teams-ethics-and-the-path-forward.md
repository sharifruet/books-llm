# Part VI — Teams, ethics, and the path forward

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Shipping LLM features is **cross-functional**. This part covers **roles**, **documentation**, **responsible deployment** at an intermediate level, and the **bridge to Volume III** when you need research depth.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 20–22.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Working in cross-functional teams | ML, backend, design, legal; handoffs |
| **2** | Responsible deployment (intermediate stance) | Transparency, escalation, proportionality |
| **3** | Bridge to *From Models to Frontiers* | What Volume III adds; skills to sharpen |

**Contents (plain list — same as table):**

1. Working in cross-functional teams — roles and checkpoints.  
2. Responsible deployment — transparency without Volume III depth.  
3. Bridge to Volume III — frontier topics and reading path.

---

## Chapter 1 — Working in cross-functional teams

**Product** defines success; **design** shapes trust and disclosure; **backend** owns latency and **API** contracts; **ML** (if present) owns **eval** and **model** choice; **legal** reviews **data** and **claims**. **No** single role “owns” safety—**checkpoints** (design review, legal sign-off for risky domains) prevent late surprises.

### Documentation

**Runbooks**: which **model**, which **prompt version**, how to **rollback**. **Playbooks** for **incidents** (spike in abuse, provider outage). Handoff should not depend on **one** engineer’s head.

> **In this chapter.** Clarity of ownership beats heroics; document what you ship.

---

## Chapter 2 — Responsible deployment (intermediate stance)

**Transparency**: users should know **when** AI is involved and **how to** escalate or opt out where feasible. **User control** over **data** and **settings** reduces harm and **trust** erosion. **Proportionality**: not every feature needs the **largest** model—**cost** and **risk** scale together.

### When to escalate

Bring **safety specialists** or **policy** for **high-stakes** domains, **jurisdictional** questions, or **public** commitments. Volume III goes deeper on **alignment science** and **governance**; here, know **when** to ask for help.

> **In this chapter.** Ship with clear disclosure, controls, and escalation paths—not only metrics.

---

## Chapter 3 — Bridge to *From Models to Frontiers*

Volume III, *From Models to Frontiers*, is for **depth**: **scaling laws**, **training** stacks, **alignment** research, **efficiency**, **multimodal** and **agentic** systems, and **open problems**. Read it when you **build** or **evaluate** at the frontier—not when you only **consume** APIs.

### Skills to sharpen

- **Reading papers** and **model cards** critically.  
- **Basic** distributed training / inference vocabulary (even if you do not train).  
- **Structured** thinking about **failure modes** and **societal** impact.

> **In this chapter.** Volume II gets you to **ship**; Volume III helps you **reason** about what is coming next.

---

## Try it

1. **RACI-style.** For one LLM feature, name **who** is accountable for: **model choice**, **prompt changes**, **customer comms** if something goes wrong.

2. **Volume III preview.** Open [From Models to Frontiers](from-models-to-frontiers.md); read the **introduction** outline. **One** topic you want to learn next—write it down.

---

*End of Part VI — Volume II. Previous: [Part V — Systems: APIs, deployment, and operations](from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md) · Next: [From Models to Frontiers — Volume III](from-models-to-frontiers.md) · Or [main volume](from-prompts-to-systems.md).*
