# Part I — Mental models and the model lifecycle

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Volume I explained **what** LLMs are and how they behave in the abstract. This part is about **shipping**: the difference between a demo and a product, how training stages show up in behavior you observe in the wild, how to choose a model and read its documentation, and how context and memory actually work in a system you build — not just in a chat interface.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 1–4.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | From playground to product | Latency, cost, ownership, and the stack around the model |
| **2** | Training stages in one picture | Pretraining, instruction tuning, preferences — capability vs. alignment |
| **3** | Choosing a model and reading model cards | Context, license, deployment; open vs. closed weights |
| **4** | Context, memory, and state | Truncation, summarization, retrieval vs. fine-tuning (preview) |

**Contents (plain list — same as table):**

1. From playground to product — stack and product concerns.
2. Training stages in one picture — base vs. chat, axes of capability.
3. Choosing a model and reading model cards — constraints and cards.
4. Context, memory, and state — what fits, what to design for.

---

## Chapter 1 — From playground to product

**When did "it works on my laptop" last survive first contact with a customer?** A playground proves the model can do something impressive once, under ideal conditions, with you watching. A product does it reliably, under load, for users who have different inputs than you tested, with clear ownership when things break and a path to recovery when they do not.

The gap between those two things is where most LLM feature projects get into trouble. Not because the model fails — but because everything surrounding the model was never designed to be a product.

### What changes at launch

**Latency becomes a user experience problem.** Users who will wait 30 seconds for a thoughtful response in a demo will abandon a product feature after 3–5 seconds of a loading spinner. Latency budgets differ by feature type: a background summarization job can take minutes; an inline autocomplete cannot take more than a few hundred milliseconds. Knowing your latency budget before you pick a model saves you from discovering the mismatch after you have built the feature.

**Cost becomes continuous.** A demo costs roughly nothing — a few API calls while you are testing. A product costs per user, per session, per day, indefinitely. The billing is invisible at demo scale and suddenly very visible at any scale beyond that. Surprises happen when the cost model was not understood before launch: a long system prompt, a verbose retrieval step, and a generous max-output setting can multiply costs by 5–10x compared to a naive estimate.

**Versioning becomes necessary.** Which model version produced this output? Which prompt template was in use? Which retrieval index did this answer draw from? These questions are irrelevant in a playground. In a product, they are the first questions asked during any incident investigation. Without versioning, you cannot compare before and after a change. You cannot roll back. You cannot reproduce a problem or confirm you fixed it.

**Ownership has to be explicit.** In a demo, "the developer" handles everything. In a product, someone needs to be on-call when the model starts producing bad outputs at 2 a.m. on a Sunday. Someone needs to own prompt changes. Someone needs to know what to do when the provider has an outage. That someone needs to be identified before launch, not discovered during an incident.

*Friction:* The failure mode that kills LLM features is not usually the model. It is timeouts that are never retried, logs that do not exist, cost spikes that nobody is alerted to, and prompt changes deployed without any review. Those are engineering and process problems, not model problems — and they are invisible in a demo.

### The stack around the model

The model is one box in a larger system. When something goes wrong, you need to know which box failed.

A typical minimal stack looks like:

    Client (browser, mobile, internal tool)
        → Application layer (business logic, auth, routing)
            → Orchestration layer (prompt assembly, retrieval, tool routing)
                → Model provider (API or self-hosted inference)
                    ← Data layer (vector store, cache, document store, feature flags)

The LLM lives at one level of this stack. Reliability is a property of the whole system. A 99.9% reliable model in a system with 90% reliable retrieval and 95% reliable application logic produces a system that works roughly 85% of the time — which is not good enough for most user-facing products.

Designing this stack requires thinking about each layer independently:

- What is the fallback if the model API is unavailable?
- What is the fallback if retrieval returns nothing relevant?
- What does the user see when the orchestration layer times out?
- What is logged at each step to make postmortems possible?

*Direct address:* If you cannot answer those questions for your feature, you have a demo, not a product. The answers do not have to be perfect — but they have to exist.

### Before you call it a product: a checklist

- Latency SLO defined and measured in testing, not assumed
- Cost per request estimated and validated against realistic usage patterns
- Model version pinned in configuration, not hardcoded in scattered strings
- Prompt version tracked alongside model version (same commit, same deploy)
- Timeout and retry logic implemented for the model API call
- Graceful degradation defined: what happens when the model is unavailable?
- Logging in place: request ID, latency, token counts, model ID, errors
- On-call path defined: who gets paged, what runbook do they follow?

Not every item needs to be production-grade before first launch. But every item should be *decided*, even if the decision is "we will accept this risk for now."

### Takeaway

- A demo proves concept. A product requires latency, cost, versioning, and ownership to all be designed, not assumed.
- The model is one component in a larger stack. Reliability is a system property.
- Define your fallbacks, logs, and on-call path before you launch, not after your first incident.

---

## Chapter 2 — Training stages in one picture

You do not need to train models to read how they were produced. Model cards, blog posts, and API documentation refer to pretraining, instruction tuning, and preference tuning — each a different kind of pressure on the same set of weights, producing different behavioral effects.

### Pretraining: building raw capability

**Pretraining** is the large-scale first phase: the model learns to predict the next token on a vast text corpus. From this pressure alone, it absorbs grammar, factual associations, code syntax, reasoning patterns in worked examples, and the stylistic conventions of dozens of genres and domains.

A model after pretraining has a rough **knowledge cutoff** (anything after the training snapshot is unknown), broad language capability, and behavior that is often awkward for direct use: given "What is the capital of France?" it might continue in the style of a geography textbook rather than simply answering.

Pretraining is where most of the model's **raw capability** lives. A weaker pretrained model cannot be compensated for by better instruction tuning. This is why "smarter" and "more aligned" are different claims — and why you should ask which one changed when a provider announces an improvement.

### Instruction tuning: learning to be an assistant

**Instruction tuning** (SFT — supervised fine-tuning) runs on a curated dataset of examples: here is a request, here is a good response. The model learns the format of being an assistant — answer directly, stay on topic, follow instructions like "be brief" or "use bullet points," respond to follow-up questions.

This stage is far cheaper than pretraining and primarily affects **format and behavior**, not raw capability. A model that was weak at reasoning before instruction tuning is still weak at reasoning after — it now just expresses that weakness more politely and in the right format.

**What can shift:** response style, default length, refusal patterns for clearly harmful requests, tone, and adherence to simple formatting instructions.

### Preference tuning: shaping quality and policy

**Preference tuning** (RLHF, DPO, and related methods) trains the model on human or AI judgments about which of two responses is better. The model learns to produce outputs that score higher on the preference model — which reflects the values of whoever did the rating and what they considered "better."

This is where the model's **personality** comes from: how much it hedges, what it refuses, how long its responses tend to be, how it handles uncertainty, whether it argues back or validates. These are not intrinsic properties of intelligence — they are downstream of the preference data.

**What can shift:** refusal rates on edge cases, level of confidence in stated claims, verbosity, balance between helpfulness and caution, sycophancy (tendency to agree with the user).

*Memorable detail:* Sycophancy is not a pretraining problem — it is a preference tuning problem. If human raters systematically preferred responses that agreed with their stated position, the model learned that agreeing is "better." This means sycophancy can be introduced by a preference tuning round and not be present in earlier versions of the same model.

### What "we updated the model" actually means

When a provider says they updated their model, behavior can change because any of these stages changed. "Smarter" might mean:

- Better reasoning → pretraining data quality or scale improved
- Follows instructions better → instruction tuning dataset improved
- Refuses fewer harmless things → preference tuning recalibrated
- Refuses more harmful things → preference tuning or post-hoc classifiers recalibrated
- Different response length defaults → instruction tuning changed

A model update that improves benchmark scores may make behavior worse for your specific use case if the preference tuning shifted in a direction that conflicts with what you need. This is why golden test sets (Part IV) matter — they let you detect behavioral changes before they affect users.

### Capability vs. alignment: different axes

A common mistake is treating "smarter" and "safer" as the same direction. They are different axes. A very capable base model may be unsafe for direct user interaction. A well-aligned chat model may be less capable on certain tasks than its base version. A model can be sycophantically helpful in ways that reduce honesty. These tensions are real and managed — not eliminated — by post-training.

*Tiny vignette:* A team upgraded to a "more helpful" model version and found it was more agreeable but less accurate. The preference tuning had been recalibrated toward user satisfaction scores, which went up when the model validated user inputs — whether or not those inputs were correct.

### Takeaway

- Pretraining builds raw capability and defines the knowledge cutoff.
- Instruction tuning shapes format and assistant behavior.
- Preference tuning shapes personality, refusals, and style.
- Model updates can change any stage. "Smarter" and "more aligned" are different claims.
- Golden test sets detect behavioral drift that capability benchmarks miss.

---

## Chapter 3 — Choosing a model and reading model cards

**If you A/B test prompts before you read the model card, you are optimizing noise.** The model card — along with the provider's API documentation — is your contract for what to expect: context length, supported modalities, license terms, known limitations, and the training stages that shaped behavior. Read it before you build, not after you hit a surprise.

### What to look for in a model card

**Context length.** How many tokens can the model consider in a single request? This determines whether your use case is feasible without retrieval, what your maximum document length is, and whether multi-turn conversation history will fit without truncation. Context windows range from a few thousand to over a million tokens across current models.

**Modalities.** Text-only, or also images, audio, video? Does vision support understanding and generation, or only understanding? If your feature involves non-text inputs, check explicitly.

**Languages.** Which languages does the model perform well in? Many models are predominantly English-trained and perform significantly worse in other languages, especially low-resource ones. "Supports multilingual" does not mean "performs equally across all languages."

**License terms.** Can you use this model commercially? Are there restrictions on fine-tuning? Are there deployment restrictions (e.g., cannot use for certain applications or in certain regions)? Does the license allow you to share or publish outputs? These matter before you build, not after you launch.

**Known limitations.** What does the provider say the model does not do well? Where does it fail predictably? Are there domains or tasks where it underperforms? A model card that lists no limitations is not reassuring — it is a red flag.

**Training stages mentioned.** Does the card describe pretraining data, instruction tuning approach, and preference training methodology? This tells you how much you can trust capability claims and where behavioral idiosyncrasies might come from.

### Deployment constraints that shape model choice

Before comparing quality, resolve constraints:

**Latency requirements.** Smaller models are faster. If your feature requires sub-second first-token latency, a frontier model served through a standard API may not meet it. Benchmark latency with realistic prompts before committing.

**Privacy and data handling.** Will your data be used for training by the provider? Is the model available through a VPC deployment or on-premises option? For sensitive data, the hosting arrangement matters as much as the model quality.

**Compliance requirements.** Healthcare (HIPAA), financial services, government contracts, and other regulated industries may require specific data handling commitments, audit logs, or geographic data residency. Check these before you invest in a model that cannot meet them.

**Cost at scale.** The cheapest model per token may not be cheapest per successful task completion. A smaller model that needs more retries or produces more unusable outputs can cost more in total than a larger model that gets it right the first time.

### Open vs. closed weights

**Closed-weight models** (API-only access from providers) shift scaling, infrastructure, and safety work to the vendor. You get less control over internals — you cannot inspect weights, modify them, or run them on your own hardware without special arrangement. You pay for inference as a service.

**Open-weight models** (weights publicly released, often under specific licenses) can be downloaded, fine-tuned, and run wherever you have hardware. You gain control and privacy; you accept the operations burden — hosting, scaling, updates, monitoring, and safety filtering become your responsibility.

Neither is universally better. The decision turns on:

| Consideration | Favors closed | Favors open |
|--------------|--------------|-------------|
| Operations capacity | Low → closed | High → open |
| Privacy / data sensitivity | Check vendor terms | Run locally |
| Customization needs | Moderate → prompt | Deep → open |
| Compliance requirements | Check vendor | Fully controllable |
| Cost at large scale | Depends on volume | May be cheaper at scale |

*Direct address:* The model that tops the leaderboard is not necessarily the model that fits your compliance checklist, your latency budget, or your cost model. Start with constraints, not benchmarks.

### Takeaway

- Read the model card for context length, modalities, language coverage, license, and known limitations before choosing a model.
- Resolve deployment constraints (latency, privacy, compliance, cost) before comparing quality.
- Open vs. closed weights is a trade-off between control and operational burden — neither is universally right.

---

## Chapter 4 — Context, memory, and state

**Everything the model "remembers" during a reply is whatever you put in the prompt.** There is no hidden persistent memory maintaining continuity across sessions unless you build it. The model starts each request with a blank slate — shaped only by what is in the context window for that request — and ends it having generated a response. Nothing persists automatically.

This is worth stating plainly because chat interfaces create the illusion of ongoing memory. The model seems to remember what you said twenty turns ago. It does — because those turns are included in the context. When they are not, it does not.

### What fills the context window in a real system

In a chat interface, the context for each request typically includes:

- **System prompt**: your application's instructions, persona, and rules
- **Conversation history**: prior user turns and assistant turns, concatenated
- **Current user message**: what the user just said
- **Retrieved content** (if RAG is used): chunks of documents fetched for this query
- **Tool outputs** (if tools are used): results from function calls made earlier in this turn

All of these share the same token budget. A system prompt of 1,000 tokens plus 10 turns of conversation history (roughly 3,000 tokens) plus a retrieved document (5,000 tokens) has already consumed ~9,000 tokens before the user's question.

### What to do when context fills up

**Truncation.** Drop the oldest turns from the conversation history when the total approaches the limit. Simple to implement, easy to reason about. The risk: important early context (stated preferences, established constraints, key facts) silently disappears. The model never signals that it lost something.

**Summarization.** When the conversation history grows long, ask the model to summarize the key decisions and facts from older turns, then replace the raw history with the summary. Lossy — but preserves load-bearing information better than truncation. Requires an extra model call.

**Session state.** Important user facts (preferences, constraints, profile information) that the product needs to persist should be stored explicitly in a database and re-injected selectively when relevant — not left to accumulate in conversation history and hope they survive truncation.

**Retrieval.** For large document collections, fetch only the relevant chunks for each query rather than loading everything into context at once. This is RAG, covered in depth in Part III.

*Tiny vignette:* Summarization is a lossy compression of your conversation. "Fine for vibes" is one way to put it. Another way: it is perfect for "remind me what we were discussing" and catastrophic for "the patient is allergic to penicillin."

### Session state vs. retrieval vs. fine-tuning

These three approaches solve different problems and are frequently confused with each other:

**Session state** is user-specific facts stored in your application database and re-injected into context when relevant. Use this for: user preferences, profile details, account information, prior decisions made in earlier sessions. This is standard application development with a model layer on top.

**Retrieval (RAG)** is fetching relevant chunks of a document collection at query time and injecting them into context. Use this for: large knowledge bases, frequently updated documents, proprietary information too large to fit in context at once. The model answers from the retrieved text rather than from its training memory.

**Fine-tuning** is adjusting model weights on task-specific training data. Use this for: stable behavior that needs to be consistent across millions of requests, domain-specific style that cannot be reliably achieved through prompting, or significant efficiency improvements on narrow tasks. Fine-tuning is expensive, requires ongoing maintenance as models update, and should be a last resort after prompting and retrieval have been proven insufficient.

*Friction:* Teams fine-tune because it feels more serious and technical than prompting. The right question is not "should we fine-tune?" but "have we exhausted prompting and retrieval, and do we have a clear behavioral gap that training data can fill?" Most of the time, the answer to the second question is no.

### Takeaway

- Everything the model sees must fit in the context window. Nothing persists automatically across sessions.
- Context fills up: system prompt, history, retrieved content, and tools all share the same budget.
- Strategies for managing context: truncation (simple, lossy), summarization (richer, requires extra call), session state (for user facts), retrieval (for large document collections).
- Session state, retrieval, and fine-tuning solve different problems. Choose based on the constraint, not the complexity.

---

## Try it

### Exercise 1 — Playground vs. product checklist

Think of an LLM demo or feature you have seen or built. Work through the checklist from Chapter 1:

- What was the latency SLO?
- What was the cost per request at realistic scale?
- Was the model version pinned?
- Was there logging?
- Was there a defined fallback?
- Was there an on-call path?

For each "no" or "not defined": what would have happened if the feature had launched to real users with that gap? This exercise is most useful if you are honest about a real demo, not a hypothetical.

### Exercise 2 — Read a model card

Open the documentation or model card for a model you are considering or currently using. Find and note:

- Exact context length
- License terms (commercial use? fine-tuning allowed?)
- One stated limitation
- Which training stages are mentioned

If you cannot find one of these, note that too. Gaps in documentation are information.

### Exercise 3 — Map your context budget

For a feature you are building or have built: sketch out what goes into the context window for a typical request. Estimate token counts for each component: system prompt, typical history length, any retrieved content, the user's message.

What fraction of the context budget is consumed before the user says anything? Is there room for the reply you expect the model to generate?

### Exercise 4 — Trace a behavioral change

Think of a time when a model or product you use changed behavior unexpectedly — it started refusing something it previously did, it changed its response style, it became more or less verbose. Based on Chapter 2: was this likely a pretraining change, instruction tuning change, or preference tuning change?

What evidence would you need to be confident? This exercise builds the habit of diagnosing behavior changes rather than just experiencing them.

---

*End of Part I. Previous: [From Tokens to Understanding — Volume I](../from-tokens-to-understanding/from-tokens-to-understanding.md) · Next: [Part II — Prompting as engineering](from-prompts-to-systems-part-ii-prompting-as-engineering.md) · Or [main volume](from-prompts-to-systems.md).*
