# Part VI — Teams, ethics, and the path forward

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Shipping LLM features is cross-functional. Models do not fail in isolation — they fail in front of users, within systems built by teams, under policies set by organizations operating in specific legal and ethical contexts. This part covers the human infrastructure around the model: roles, documentation, responsible deployment, and the bridge to Volume III for those who need research-level depth.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 20–22.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Working in cross-functional teams | Roles, ownership, documentation, incident playbooks |
| **2** | Responsible deployment (intermediate stance) | Transparency, user control, proportionality, escalation |
| **3** | Bridge to *From Models to Frontiers* | What Volume III adds; who should read it |

**Contents (plain list — same as table):**

1. Working in cross-functional teams — roles, ownership, runbooks.
2. Responsible deployment — transparency, controls, escalation.
3. Bridge to Volume III — frontier topics and reading path.

---

## Chapter 1 — Working in cross-functional teams

**When the model misbehaves at 3 p.m. on a Friday, whose Slack gets the @-mention?** If the answer is "everyone's" or "nobody's," you have a team structure problem. LLM features touch more functions than most software — model selection, prompt engineering, data handling, user experience, legal compliance, and security — and the gaps between those functions are where incidents happen.

### Who does what

There is no single right team structure for LLM features, but these responsibilities need to be owned somewhere:

**Product**: Defines success criteria. Decides which user problems are worth solving with an LLM. Owns the feature definition, the scope boundaries, and the decision about when a feature is good enough to ship.

**Design**: Defines how the feature is presented to users. Owns disclosure (how do users know AI is involved?), the interaction model (streaming, editing, cancellation), error state copy, and the UX of the fallback when the model fails.

**Engineering**: Implements the system. Owns the abstraction layer, observability, cost controls, safety layers, and the runbook for incidents. Maintains the model version pinning and the golden test set.

**ML / AI (if present)**: Owns model selection, evaluation methodology, fine-tuning decisions, and reading model cards critically. In teams without a dedicated ML function, engineering takes this responsibility.

**Legal and compliance**: Reviews the feature for regulatory risk (data handling, jurisdictional requirements, regulated domain advice). Should be in the loop before launch, not after a complaint.

**Security**: Reviews the trust model, the prompt injection surface, and tool permission design.

The critical insight: **no single role "owns" safety**. Safety is a cross-cutting concern that design, engineering, legal, and product all contribute to. When everyone owns safety, specific decisions can still fall through the cracks. Use review checkpoints — design review, security review, legal sign-off for high-risk domains — to make sure they do not.

### Documentation that survives a team change

The goal of documentation is that someone new to the team can understand what the feature does and how to operate it, without needing to decode tribal knowledge from the person who built it.

**Runbook (per feature):**
- What the feature does and who it serves
- Model version and prompt version currently in production
- How to roll back a prompt or model change
- What to check first when something goes wrong
- Links to dashboards and alert definitions
- On-call rotation and escalation path

**Incident playbook (for the product):**
- What to do if model quality degrades unexpectedly
- What to do if cost spikes
- What to do if the model provider has an outage
- What to communicate to users and when
- Who makes the decision to take a feature offline

Documentation does not need to be long. It needs to be accurate and up to date. A two-page runbook that reflects reality is worth more than a fifty-page document that describes how the feature was designed two versions ago.

*Friction:* "We will document it after launch" is how tribal knowledge becomes customer-facing risk. The time pressure that makes documentation feel optional before launch is exactly when it matters most — because the first incident usually arrives within days of launch.

### The handoff problem

Every time a team member leaves or an LLM feature is transferred to a different team, tribal knowledge evaporates. Decisions that seemed obvious to the person who made them become inexplicable to the person who inherits them.

Good documentation converts tribal knowledge into institutional knowledge. It answers not just "what does this do" but "why was it built this way" and "what did we try that did not work." The "why" prevents teams from re-discovering the same decisions the hard way.

### Takeaway

- All critical responsibilities need explicit owners: product, design, engineering, ML, legal, security.
- No single role owns safety — use review checkpoints to close the gaps.
- Runbooks and incident playbooks are not bureaucracy; they are the difference between a blameless postmortem and a chaotic one.
- Document "why" alongside "what" — it prevents the same decisions from being undone and rediscovered.

---

## Chapter 2 — Responsible deployment (intermediate stance)

**"Move fast and break things" is a poor fit when the things are people's health records, employment decisions, or access to essential services.** Responsible deployment is not about moving slowly — it is about moving deliberately, with a clear understanding of what could go wrong and mechanisms to catch it.

### Transparency: what users deserve to know

Users have legitimate interests in knowing when they are interacting with AI, what the AI can and cannot do, and what happens to their data. Transparency is both an ethical obligation and a practical trust-building strategy — users who understand a system's limitations are less disappointed when it fails.

**Disclose AI involvement.** Many jurisdictions are developing or have enacted requirements around disclosure when AI is involved in interactions, recommendations, or decisions. Beyond legal requirements: users who do not know they are talking to an AI may have different expectations than those who do. Be explicit.

**Disclose scope and limitations.** What does the feature not do? What should users not rely on it for? A single clear sentence at the right moment ("This assistant cannot access your account details — for account questions, contact support") prevents far more frustration than a detailed FAQ buried in the help center.

**Disclose data handling.** In context, at the relevant moment: "This conversation may be reviewed to improve the product." Users should not have to read a 40-page privacy policy to understand what happens to what they type.

### User control

Users should have meaningful control over their interaction with AI features:

**Opt-out paths.** Can users decline to use the AI feature and still accomplish their goal? Not every feature can offer this, but where possible, the opt-out should be visible and not punitive.

**Data deletion.** Can users delete their conversation history? Can they opt out of training use? What is the retention period? These questions have answers in your data model — make them visible to users.

**Human escalation.** For consequential interactions — customer support decisions, medical information, financial guidance — there should be a clear path to a human who can review and override the AI's output. This should be accessible, not buried.

### Proportionality: right-sizing risk and capability

Not every use case requires the most powerful model. Not every use case warrants the same level of safety investment. Proportionality means matching the level of caution to the level of risk.

A feature that generates marketing headlines for internal review has a very different risk profile than a feature that advises users on medication interactions. The first probably does not need a safety classifier. The second probably needs domain expert review, extensive testing on adversarial inputs, strong grounding requirements, and a prominent disclaimer.

**Questions to calibrate risk level:**
- Who uses this feature, and are they in a vulnerable position?
- What is the worst realistic outcome if the feature produces a wrong or harmful output?
- How easy is it to verify or override the model's output?
- What happens at scale — if 1% of outputs are harmful, how many harmful outputs is that per day?

### When to escalate to safety specialists

Not all safety decisions can be made well by generalist product teams. Bring in safety specialists, ethicists, or external reviewers when:

- The feature will be used by vulnerable populations (minors, people in mental health crisis, users in high-stakes situations)
- The domain is highly regulated or legally sensitive (healthcare, legal, financial)
- The feature could be used adversarially at scale (content generation for social media, personalized persuasion)
- Public commitments about safety are being made

*Anchor:* Responsible deployment is not a single checkbox — it is a set of ongoing practices. Features launched responsibly can become irresponsible as usage grows, the user population changes, or the underlying model is updated. Build the feedback loops that surface these changes before users do.

### Takeaway

- Disclose AI involvement, scope, limitations, and data handling — clearly and in context.
- Provide meaningful user controls: opt-out, data deletion, human escalation where it matters.
- Match safety investment to risk level: proportionality prevents both under-protection and unnecessary friction.
- Know when the decision requires expertise beyond your team.

---

## Chapter 3 — Bridge to *From Models to Frontiers*

*From Models to Frontiers* (Volume III) is for people who need to understand the science behind the product: not just what models do but why they do it, what the research says about their limits, and what is genuinely unknown. Read it when you need to evaluate frontier claims critically, participate in technical decisions at depth, or understand the alignment and safety science that underlies responsible deployment practices.

### What Volume III adds

**Scaling laws and pretraining.** Why do bigger models trained on more data generally perform better? What are the limits of that relationship, and when does it break? How is training data curated at web scale, and what does contamination mean for benchmark interpretation? Volume III answers these questions with the depth needed to evaluate claims in papers and announcements rather than just accept them.

**Alignment and safety science.** Volume II covers safety as product engineering. Volume III covers it as a research field: the alignment problem in technical detail, red-teaming methodologies, interpretability research, and the governance frameworks being developed around model deployment. If you need to argue about alignment tradeoffs rather than just implement safety layers, this is where the vocabulary comes from.

**Training and inference efficiency.** Quantization, distillation, speculative decoding, mixture of experts, KV-cache mechanics, and the hardware constraints that shape what techniques are practical. Volume III gives you the depth to evaluate efficiency claims and make informed decisions about inference infrastructure.

**Multimodal models and agents.** Vision-language architectures, audio-language models, the agent loop and its failure modes, memory architectures for multi-step tasks, and the evaluation challenges for open-ended agent behavior. Volume II treats agents as a deployment concern; Volume III treats them as a research and engineering challenge.

**Frontiers and open problems.** Where does the field genuinely not know the answers? Volume III names the open problems honestly — continual learning, reliable reasoning, world models, long-horizon planning — and gives you the framing to follow research on them without being misled by hype.

### Who should read Volume III

**Read Volume III if:**
- You evaluate or make decisions about which models to use, and you want to understand the claims rather than just the benchmarks
- You work in AI safety, alignment, or governance and need the technical vocabulary
- You build or evaluate training infrastructure or inference systems at scale
- You want to follow ML research papers and need the foundation to read them critically
- You are responsible for a team that makes technical decisions about AI systems

**You do not need Volume III if:**
- You are building LLM features with standard APIs and do not need to understand the training pipeline
- Your safety requirements are met by product-level layers (classifiers, human review, policy)
- Volume II covers your current scope of practice

The boundary between Volume II and Volume III is roughly the boundary between building with models and building (or critically evaluating) the models themselves.

### Closing Volume II

If you have worked through this volume, you have the tools to build LLM-powered features that are reliable, observable, cost-controlled, and responsibly deployed. You can choose between prompting, retrieval, and fine-tuning. You can define what success looks like and measure it. You can build abstraction layers that survive model updates. You can have a conversation with legal, security, and design counterparts without being the person who "handles the AI stuff."

That is not a small thing. Most of the value that LLMs generate in the world over the next decade will come from teams of people like the readers of this volume — building carefully, measuring honestly, and making defensible decisions.

*Direct address:* Volume II taught you to ship responsibly. Volume III helps you argue about what is coming next without mistaking marketing slides for physics. When you are ready for that depth, the bridge is open.

---

## Try it

### Exercise 1 — RACI for one feature

For one LLM feature you are building or have built: fill in ownership for each of these:
- Who owns the decision about which model to use?
- Who owns prompt changes?
- Who reviews customer communications if something goes wrong?
- Who owns the on-call rotation?

If any line reads "the team" or "everyone," that is not ownership — it is a gap. Identify the person or role who should own it.

### Exercise 2 — Write a minimal runbook

For the same feature: write a two-page runbook. Include: what the feature does, the current model and prompt version, how to roll back a change, what to check first when something goes wrong, and who to contact.

If you cannot write it in two pages, the feature is probably not well enough understood to be in production.

### Exercise 3 — Disclosure audit

For a feature you interact with as a user: how does it disclose AI involvement? Where does it explain what it cannot do? Where does it offer a path to a human?

Then for a feature you are building: apply the same audit. What would a user not know that they should?

### Exercise 4 — Volume III preview

Open [From Models to Frontiers](../from-models-to-frontiers/from-models-to-frontiers.md). Read the introduction. Pick one topic you want to understand at research depth — scaling laws, alignment, efficiency, agents, evaluation. Write two sentences: what question you want that topic to answer, and what you would be able to do differently once you understood it.

---

*End of Part VI — Volume II. Previous: [Part V — Systems: APIs, deployment, and operations](from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md) · Next: [From Models to Frontiers — Volume III](../from-models-to-frontiers/from-models-to-frontiers.md) · Or [main volume](from-prompts-to-systems.md).*
