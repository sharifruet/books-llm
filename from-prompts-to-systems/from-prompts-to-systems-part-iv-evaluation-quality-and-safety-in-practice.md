# Part IV — Evaluation, quality, and safety in practice

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

**You ship what you measure.** Every LLM feature has a quality distribution — a range of outputs across the inputs it will actually receive. Without measurement, you are guessing where that distribution sits. With measurement, you can move it deliberately, catch regressions before users do, and make defensible decisions about what is good enough to ship.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 13–15.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | What to measure | Task quality, latency, cost, human vs. automated judgment |
| **2** | Test sets, regression testing, and CI | Golden sets, model upgrades, breaking changes |
| **3** | Safety and abuse in product context | Policy layers, PII handling, escalation paths |

**Contents (plain list — same as table):**

1. What to measure — metrics that match the job.
2. Test sets and regression — golden sets, CI mindset.
3. Safety and abuse — layers, data handling, escalation.

---

## Chapter 1 — What to measure

**Which number would you defend in a postmortem — the leaderboard score or the user refund rate?** Leaderboard benchmarks measure what their authors decided to measure. Your product has its own definition of success, and that definition needs to be explicit before you launch, not reverse-engineered from customer complaints.

### The layers of LLM quality

Quality for an LLM feature is not a single number. It has multiple dimensions that can move independently:

**Task quality**: Does the response actually accomplish what the user needed? This is the most important dimension and the hardest to measure automatically. A response can be grammatically flawless, perfectly formatted, and completely unhelpful. Task quality typically requires human judgment or a carefully designed automated proxy.

**Factual accuracy**: For features involving specific claims, are those claims correct? This requires checking against a ground truth source — either human raters or a retrieval-verified reference.

**Format adherence**: Does the response follow the required format? Did it return valid JSON when asked? Did it stay within the word limit? Is it in the right language? These are automatable — write the check in code.

**Latency**: How long did the user wait? Measured as time-to-first-token (for streaming features) and time-to-completion. Track percentiles (p50, p95, p99), not just averages — tail latency is where user experience degrades.

**Cost per successful response**: Not just cost per request — cost per response that actually accomplished the task. A cheaper model with a 60% task success rate may cost more per successful response than an expensive model with a 95% success rate.

**Safety and harm rate**: What fraction of responses violated safety policies or caused potential harm? For consumer-facing features, this needs active measurement, not just passive observation.

### Human evaluation vs. automated metrics

**Human evaluation** is the gold standard for task quality. Raters assess whether the response actually helped with the task, using a rubric you define. It is expensive, slow, and difficult to scale — but it is the ground truth. Use it for calibration and for catching things automated metrics miss.

**Automated metrics** scale, are consistent, and can run on every response. Their weakness is that they measure proxies for quality, not quality itself. Common automated metrics:

- *Format validation*: Does the output match the required schema or format? (Automatable, reliable)
- *Factual consistency*: Does the response contradict the provided context? (Partially automatable with a reference-checking prompt)
- *Groundedness*: Are all specific claims supported by the retrieved context? (Automatable with a grounding-check prompt)
- *Semantic similarity*: How similar is the response to a reference answer? (Useful as one signal; can be gamed)

**Model-as-judge**: Using a second LLM to evaluate the output of the first. Scales well and can capture nuanced quality better than keyword metrics. Inherits the judge model's biases — a judge that prefers verbose responses will score verbose responses higher. Calibrate model-as-judge scores against human ratings before trusting them as the primary signal.

*Friction:* The metric you optimize becomes the behavior you get. Teams that optimize model-as-judge scores without calibration against human ratings end up with responses that look good to an LLM and feel hollow to a person. Goodhart's Law visits LLM evaluation too.

### Defining success for your feature

For each feature, answer these questions before building your eval:

1. What does a successful response look like in user terms? (Not "correct" — specifically, what does the user do with it?)
2. What does a failure look like? (Not "wrong" — specifically, how does a bad response harm the user or the business?)
3. What can be measured automatically? (Format, grounding, latency, cost)
4. What requires human judgment? (Task completion, helpfulness, tone)
5. What is your minimum acceptable threshold for each metric?

The answers to these questions are your eval spec. Write them down before you build your golden set.

### Takeaway

- Define success in user terms before you define metrics.
- Measure multiple dimensions: task quality, accuracy, format, latency, cost, safety.
- Human evaluation is the ground truth; automated metrics are scalable proxies.
- Calibrate model-as-judge against human ratings before using it as a primary signal.

---

## Chapter 2 — Test sets, regression testing, and CI

**A feature that worked last week may not work this week.** Model providers update their models — sometimes with announcements, sometimes silently. Prompt changes that seemed trivial can have unexpected effects on edge cases. Retrieval index updates can change which content gets returned. Without a structured test process, you discover regressions from user complaints rather than from your own monitoring.

### Building a golden set

A **golden set** is a fixed collection of inputs — and expected output properties — that you run on every prompt or model change. It is the LLM equivalent of a unit test suite: small enough to run quickly, representative enough to catch real regressions.

**What belongs in a golden set:**

- **Representative inputs**: A sample of the real queries your system receives, covering the main use cases.
- **Edge cases**: Inputs that are unusual, ambiguous, or known to be difficult. These are the ones that break in unexpected ways.
- **Adversarial inputs**: Inputs designed to trigger failures — instructions to ignore the system prompt, requests at the boundary of what the feature should handle, inputs in unexpected languages or formats.
- **Regression cases**: Every bug you have fixed should have a test case. If it broke once, it will break again.

**What to check:**
- For each input, define what a passing response looks like in terms of **properties**, not exact strings. "Contains a valid JSON object with keys: status, message" is better than "equals exactly this string." Exact-string matching makes your test suite brittle to irrelevant variations.
- For factual accuracy, define the ground truth and check that the response agrees with it.
- For tone and task completion, you may need automated proxies (key phrase presence, format validity) plus periodic human spot-checks.

A golden set of 50–200 well-chosen cases covers most situations better than a set of 10,000 randomly collected examples. Quality over quantity.

### The silent upgrade problem

Many model providers update their deployed models without version-bumping the model identifier you are using. A model called `gpt-4o` today may have different weights than the same identifier had last month. Your prompts, which were tuned for the previous behavior, now run against a model that behaves slightly differently — and you have no idea until users start complaining.

**Solution:** Pin the exact model version in your configuration. Most providers support version-specific identifiers (e.g., `gpt-4o-2024-08-06`). Use these, not the floating alias. When you are ready to update to a new version, run your golden set against it before switching.

*Tiny vignette:* "Nothing changed in our code" is completely compatible with "the provider swapped weights on Tuesday." Pinning is not paranoia — it is versioning. The same instinct that makes you pin library versions in `requirements.txt` applies here.

### CI for LLM features

Treat prompt and model changes like code changes: test before merge.

A minimal CI process for an LLM feature:
1. When a prompt or model version change is proposed, run the golden set automatically.
2. Compare scores to the baseline (the current production version).
3. Block the change if scores fall below defined thresholds.
4. Flag for human review if scores are close to the threshold.
5. After merging, monitor production metrics for 24–48 hours for unexpected drift.

This is the same process as software CI, with LLM-specific considerations:
- Some regression is expected and acceptable when you are deliberately trading off one dimension for another (e.g., accepting slightly shorter responses to improve latency).
- The threshold for "acceptable" needs to be defined explicitly, not eyeballed.
- Production monitoring catches what the golden set misses.

### Regression detection in production

Golden sets catch known failure modes. Production monitoring catches unknown ones. Build dashboards and alerts for:

- **Response quality proxies**: format validity rate, grounding rate, refusal rate.
- **Latency**: p95 and p99 time-to-first-token and time-to-completion.
- **Error rates**: model API errors, timeout rates, retry rates.
- **Cost**: tokens per request, cost per request — alert on unexpected spikes.

Set alerts for significant deviations from baseline, not just hard failures. A 15% increase in response latency is a regression even if no requests are failing.

### Takeaway

- Golden sets: fixed, well-chosen inputs with property-based expected outputs. Run them on every change.
- Pin exact model versions in configuration. Update deliberately, not accidentally.
- Treat prompt changes like code changes: test before deploying, have a rollback path.
- Monitor production for regressions your golden set did not cover.

---

## Chapter 3 — Safety and abuse in product context

**Safety is product design, not an afterthought.** Every LLM feature makes implicit choices about what outputs are acceptable, what inputs it will process, and what happens when something goes wrong. Making those choices explicit — and building them into the product architecture — produces better outcomes than hoping the base model handles it.

### Defense in depth

Safety for an LLM product is best structured as overlapping layers, each catching different things:

**Layer 1: System prompt and prompt design.** The most cost-effective layer. Explicit instructions about what the model should and should not do, framed for the model's behavioral tendencies. "Never provide specific medical dosages" in a system prompt catches most straightforward cases.

**Layer 2: Input classifiers.** A separate, fast classifier (often a smaller model or a rule-based system) that screens inputs before they reach the main model. Useful for: detecting clearly off-topic requests, screening for obvious policy violations, rate limiting by content type.

**Layer 3: Output classifiers.** A classifier that screens model outputs before they are shown to users. More expensive than input classifiers (you pay for the generation first), but catches model outputs that slipped past the prompt. Use for: PII in outputs, specific content policy violations, format validation.

**Layer 4: Logging and monitoring.** Not a preventive layer, but an essential detection layer. Log enough to identify patterns of abuse, catch problems the other layers miss, and enable incident investigation.

**Layer 5: Human review.** An escalation path for edge cases that automation cannot handle reliably. Required for high-stakes domains (medical, legal, financial advice), for patterns of unusual activity, and for user-reported issues.

*Anchor:* Defense in depth means that no single layer is trusted to handle everything. The system prompt does not catch everything. The classifier does not catch everything. Logging and escalation close the gap.

### PII and data minimization

Every LLM request that passes through your system is a potential PII exposure point. User inputs may contain names, addresses, account numbers, health information, or other sensitive data — sometimes deliberately, sometimes inadvertently.

Principles for minimizing risk:
- **Do not log PII by default.** Request IDs, latency, token counts, error codes, and model IDs are generally safe to log. Full prompt text and full response text are not, unless you have a clear need and appropriate access controls.
- **Hash or redact identifying fields before logging.** If you need to debug user-specific issues, use pseudonymous identifiers.
- **Define retention limits.** Logs that exist indefinitely are logs that can be breached indefinitely. Define how long logs are kept and automate deletion.
- **Classify your log data.** Treat LLM logs with the same classification and access controls as other sensitive system logs.

### Building escalation paths

Automation should not be the last word on every safety decision. Define explicitly when a human should review:

- Flagged content that was borderline (the classifier was uncertain)
- User reports of harmful outputs
- High-severity content categories (self-harm, targeted harassment, illegal activity)
- Repeated unusual patterns from a specific user or prompt

An escalation path without a person at the end is not an escalation path — it is a log file. Ensure that escalated items reach a human who can act on them, within a time window appropriate for the severity.

*Direct address:* "We use the provider's moderation API" is a policy layer, not a complete safety program. It outsources the moderation decision without outsourcing the accountability. You remain responsible for what your product does, regardless of which classifier made the call.

### Takeaway

- Safety is layered: prompt design, input classifiers, output classifiers, logging, human review.
- Do not log full prompt and response text by default. Minimize, hash, and set retention limits.
- Define escalation paths that end with a person, not just a queue.
- You remain accountable for what your product does, regardless of which layer produced the behavior.

---

## Try it

### Exercise 1 — Define metrics for a feature

Pick a real LLM feature — something you are building or have built, or a feature from a product you use.

Write:
- One metric that can be measured automatically (format, latency, cost)
- One metric that requires human judgment
- Your minimum acceptable threshold for each

If you cannot write the threshold, you do not yet have a metric — you have an intention.

### Exercise 2 — Build a minimal golden set

For the same feature: write five test cases. For each, include the input and the expected properties of a passing response. Include at least one edge case and one adversarial case.

Run them against the current system. How many pass? For the ones that fail, is the failure prompt-shaped, retrieval-shaped, or model-shaped?

### Exercise 3 — Find your silent upgrade risk

Look up the model identifier used in a production feature you have access to. Is it a floating alias (like `gpt-4o`) or a pinned version (like `gpt-4o-2024-08-06`)?

If it is a floating alias: what would have happened if the model behavior changed silently last week? Is there a golden set that would have caught it?

### Exercise 4 — Map your safety layers

For a feature you are building: sketch the layers present. System prompt? Input classifier? Output classifier? Logging? Human review path?

For each missing layer: is it genuinely not needed for this feature, or is it a gap you have been meaning to add? Be honest about which is which.

---

*End of Part IV. Previous: [Part III — Data, retrieval, and adaptation](from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md) · Next: [Part V — Systems: APIs, deployment, and operations](from-prompts-to-systems-part-v-systems-apis-deployment-and-operations.md) · Or [main volume](from-prompts-to-systems.md).*
