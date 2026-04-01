# Part II — Prompting as engineering

*Sharif Uddin*

*[From Prompts to Systems](from-prompts-to-systems.md) · Volume II*

---

Prompts are not vibes — they are **interfaces**. An interface has a contract: inputs, expected outputs, edge cases, and a version. This part treats prompts as versioned artifacts that are designed, tested, debugged, and maintained — not just typed, hoped for, and forgotten.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 5–8.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Prompt structure and patterns | System / user / tools; few-shot and chain-of-thought trade-offs |
| **2** | Iteration and prompt libraries | Versioning, A/B testing, templates and guardrails |
| **3** | Failure modes and debugging | Hallucination, format drift, sycophancy — diagnose and constrain |
| **4** | Interaction and UX for LLM features | Streaming, undo, error states, team norms |

**Contents (plain list — same as table):**

1. Prompt structure and patterns — roles, patterns, CoT trade-offs.
2. Iteration and prompt libraries — version control for prompts.
3. Failure modes and debugging — diagnose, constrain, validate.
4. Interaction and UX — streaming, expectations, team norms.

---

## Chapter 1 — Prompt structure and patterns

**Who speaks first in your API — and does your application even know?** In a well-structured prompt, every message has a clear role and purpose. The structure is not just aesthetic — it affects how reliably the model follows instructions, how you debug failures, and how changes in one part of the prompt affect behavior in other parts.

### Roles in an API context

Most LLM APIs structure messages as an ordered list with assigned roles. The names vary slightly by provider, but the semantics are consistent:

**System**: Persistent instructions for the entire session. Persona, format rules, hard constraints, scope limitations. Evaluated at the start of every turn.

**User**: What the user said, or what your application presents as the user's input. Also used for injected context like retrieved documents, structured data, or tool outputs in some patterns.

**Assistant**: Prior model responses, included so the model can respond coherently to the conversation so far. You can also pre-fill assistant turns to steer format or continuation.

**Tool** (in some APIs): The output from a function call the model requested. Structured result data the model needs to incorporate into its response.

The structure of a typical RAG-enabled turn looks like:

    [system]
    You are a helpful assistant for Acme Corp's internal knowledge base.
    Answer questions using only the provided CONTEXT sections.
    If the context does not contain enough information, say so explicitly.
    Never cite sources not present in the CONTEXT.

    [user]
    CONTEXT:
    --- Document: Q3 Expense Policy (updated 2024-09-01) ---
    Meals are reimbursable up to $75 per person per day when traveling...

    QUESTION: What is the meal reimbursement limit for domestic travel?

    [assistant]
    According to the Q3 Expense Policy...

The separation of system instructions from injected context from the user's actual question is not just organization — it creates a clear trust hierarchy (system instructions take precedence over user input) and makes debugging easier when the model behaves unexpectedly.

### Few-shot: showing the pattern

Few-shot examples teach format more reliably than verbal description for structured tasks. Three to five examples of input → desired output — placed in the prompt before the actual input — allow the model to lock onto the pattern you want.

Few-shot is particularly effective for:
- Classification with a specific label set
- Extraction into a specific JSON schema
- Responses that need a specific tone or register
- Tasks where the format is hard to describe verbally but obvious from examples

Keep examples honest. Do not embed false information in examples — the model will treat them as demonstrations of correct behavior.

### Chain-of-thought: when and when not

**Chain-of-thought (CoT)** prompting — asking the model to "think step by step" or "show your reasoning before giving the final answer" — can meaningfully improve accuracy on reasoning-heavy tasks. The mechanism: making intermediate steps visible in the token stream provides something like working memory for the task, allowing the model to condition later steps on earlier ones.

**Use CoT when:**
- The task involves multi-step reasoning, comparison, or analysis
- Intermediate steps are meaningful to you (for debugging or showing work)
- Accuracy matters more than speed

**Avoid CoT when:**
- Latency is a constraint (CoT significantly increases output tokens)
- The reasoning is internal infrastructure you do not want users to see
- The task is simple enough that reasoning steps add noise without benefit
- You need the response to be brief and structured

*Friction:* CoT can look like "more intelligent" output because it produces longer, more elaborate responses. This confuses token count with quality. Measure actual task accuracy on your golden set — not response length or apparent thoughtfulness.

### Hiding chain-of-thought

When CoT is useful for internal reasoning but should not appear in the user-facing response, use a two-step approach: generate reasoning in a scratchpad, then generate a clean final answer. Some APIs support this natively; others require you to strip the reasoning in post-processing. Document which approach you are using and why — it is easy to accidentally expose internal reasoning to users if this is not explicit.

### Takeaway

- Use system messages for persistent rules; keep user messages clean; inject context explicitly.
- Few-shot examples teach format faster than verbal description for structured tasks.
- Chain-of-thought helps reasoning tasks; adds latency and tokens; hide it from users when needed.
- Structure prompts deliberately — it makes debugging faster and behavior more predictable.

---

## Chapter 2 — Iteration and prompt libraries

**A prompt that works today and is not saved is a prompt that will be re-invented from scratch in three months.** Treating prompts as ephemeral chat messages rather than versioned artifacts is one of the most common sources of operational pain in LLM-powered products.

### Version control for prompts

Prompts should be stored in version control — git or a dedicated CMS — alongside the code that uses them. Each prompt version should have:

- A **version identifier** (e.g., `v1.0`, `v1.1-holiday-tone`, `v2.0-structured-output`)
- The **model version it was tested on**
- The **date it was introduced**
- A **brief description** of what changed and why

A minimal prompt entry in a file might look like:

    # summarize-for-executive
    # version: 2.1
    # tested-on: gpt-4o-2024-08-06
    # date: 2024-11-15
    # change: Added explicit "no bullet sub-points" constraint after QA failure

    You are an expert at condensing complex documents for busy executives.
    Produce a summary with: one sentence of context, three bullet points of
    key findings, one recommended action. No sub-bullets. Maximum 120 words.

This takes five minutes to maintain and saves hours of debugging when the behavior changes and you cannot remember what the prompt looked like before.

### Before you change a prompt

Before changing a production prompt: run the proposed change against your golden set (Part IV). Do not rely on informal "it looks better now" evaluations. The cases you test manually are almost never the cases that fail in production.

*Memorable detail:* The prompt that wins in a five-person Slack poll is not the prompt that wins on 10,000 real queries. Selection bias in manual review is extremely common. The only reliable comparison is a structured eval.

### A/B testing prompts

For changes that may affect user-facing quality, run offline eval first and online A/B second:

**Offline eval:** Run both prompt versions on your golden set. Compare scores on your defined metrics. If the new prompt clearly wins, proceed. If the scores are close, look at which cases it wins and loses — understand the trade-off before deploying.

**Online A/B:** Send a fraction of real traffic to the new prompt version. Define what you are measuring (task completion rate, user rating, refusal rate) and how long you will run the experiment before deciding. Have a rollback path ready.

Never ship prompt changes without a rollback path. A prompt can behave perfectly in testing and catastrophically on real user inputs the test set did not cover.

### Templates and guardrails

**Templates** separate the constant parts of a prompt from the variable parts. Instead of constructing prompts through string concatenation scattered across your codebase:

    # in a prompt file
    You are a customer service agent for {company_name}.
    Always address customers by their first name ({customer_first_name}).
    Respond in {response_language}.

    Customer inquiry: {inquiry}

Variable injection from a template is testable, reviewable, and easy to audit for prompt injection vulnerabilities (untrusted values should be clearly identified as data, not instructions).

**Guardrails** belong in the system message or in post-processing, not in hope. If the model must never output raw account numbers, that constraint goes in the system message explicitly, and ideally you also validate the output in code before returning it to the user. "I told the model not to" is not a safety guarantee.

### Takeaway

- Store prompts in version control with model version and date metadata.
- Run golden-set evaluations before changing production prompts.
- A/B test changes that affect user-facing quality; always have a rollback path.
- Use templates for variable injection; put guardrails in system messages and output validation.

---

## Chapter 3 — Failure modes and debugging

**Hallucination and format errors are not rare bugs — they are baseline risks.** Every production LLM feature has a failure rate on these dimensions; the question is whether you have measured it, whether it is acceptable, and whether you have mitigations in place. Debugging effectively requires identifying which kind of failure you have before attempting to fix it.

### Hallucination: confident errors

The model states a specific false fact confidently. Common in: citations, specific numbers, names, dates, events near the training cutoff.

**Debugging approaches:**

1. *Is this prompt-shaped?* If you can provide the correct information in the context, do it — retrieval grounding is more reliable than asking the model to recall from training memory.
2. *Is this citation-specific?* Do not ask the model to generate citations. Have it identify what to look for; your system retrieves the actual reference.
3. *Can you add self-check instructions?* "Before giving the final answer, list any specific facts you are uncertain about." This sometimes catches hallucinations early, but does not reliably prevent them.
4. *Can you validate the output?* For structured outputs (JSON, specific formats), validate programmatically. For factual claims, build a retrieval step that verifies key claims against your source documents.

### Format errors: the model didn't follow instructions

The model was told to return JSON and returned JSON wrapped in a paragraph. It was told to use a specific schema and invented different fields. It was told to be brief and returned 800 words.

**Debugging approaches:**

1. Move format instructions to the beginning of the system message, not buried in the middle of the user turn.
2. Provide a concrete example of the desired output format in the prompt.
3. Use schema-constrained generation if the provider supports it (many do for JSON output).
4. Validate the output format in code before using it downstream — never trust the model to have followed format instructions.
5. If format consistently drifts in a specific way, the prompt is fighting the model's learned defaults. A different prompt structure or a few-shot example usually fixes this faster than more instructions.

### Sycophancy: the model agrees when it should not

The model validates incorrect user inputs, adjusts its stated position when the user pushes back without providing new evidence, or completes tasks it should refuse because the user expressed confidence.

This is a preference-training failure mode, not a prompting failure mode — but it can be partially mitigated:

1. Instruct the model explicitly: "If the user's premise appears to be incorrect, say so politely before answering."
2. For factual tasks, provide ground truth in context: "Use only the provided documents. If the user's claim contradicts the documents, say so."
3. Design your evaluation to catch sycophancy: include cases where the correct behavior is to disagree with the user, and check whether the model does.

### Tool misuse: wrong arguments, wrong tool

The model calls a tool with hallucinated arguments, calls the wrong tool for the task, or fails to call a tool when it should.

**Debugging approaches:**

1. Validate all tool arguments in code before execution. Never trust model-generated arguments without validation.
2. Use strict JSON schemas for tool definitions. Ambiguity in tool names or parameter descriptions is usually the root cause of wrong tool selection.
3. Add examples to tool definitions: "When to use this tool: [example]. When NOT to use this tool: [example]."
4. For irreversible actions, require human approval in the loop regardless of apparent model confidence.

### A debugging diagnostic

When behavior is wrong, ask in sequence:

1. **Is this prompt-shaped?** → Change the prompt (constraint, example, structure).
2. **Is this retrieval-shaped?** → Bad context in → bad answer out. Fix the retrieval first.
3. **Is this model-shaped?** → The model genuinely cannot do this reliably. Consider a different model, a different approach, or a different task decomposition.
4. **Is this validation-shaped?** → The model produced an acceptable output that your application mishandled. Fix the parsing/validation layer.

*Direct address:* If your fix is always "more instructions in English," you are fighting sampling and training objectives with prose. Sometimes the right fix is structure — schema validation, a different few-shot example, or task decomposition — not a longer system message.

### Takeaway

- Identify the failure type before attempting a fix: prompt-shaped, retrieval-shaped, model-shaped, or validation-shaped.
- Hallucination: ground in retrieved context; validate structured outputs programmatically.
- Format errors: move instructions to the start; provide examples; validate in code.
- Sycophancy: instruct the model to disagree when warranted; design eval to catch it.
- Tool misuse: validate all arguments in code; use strict schemas; gate irreversible actions.

---

## Chapter 4 — Interaction and UX for LLM features

**The experience of using an LLM feature is shaped as much by the interface as by the model.** Streaming, error states, cancellation, and the way you set user expectations all determine whether users trust the feature — often more than model quality does.

### Streaming: showing work in progress

Most modern LLM APIs support streaming — returning tokens as they are generated rather than waiting for the complete response. This dramatically improves perceived speed: a response that takes 8 seconds to complete feels much faster when the user sees text appearing after 300 milliseconds.

**Implementation considerations:**

- Buffer partial output before displaying if the beginning of the response needs post-processing (e.g., removing a thinking prefix).
- Provide a cancel/stop button. Users who see the model going in the wrong direction will want to stop it without waiting for completion.
- Handle streaming failures gracefully — the connection can drop mid-stream. Define what the user sees if a streaming response is cut off.
- For structured output (JSON), either wait for the complete response before parsing, or use incremental JSON parsing if you need to render as it arrives.

### Error states and fallbacks

An LLM feature that fails silently — returning an empty result, a spinning loader that never resolves, or a generic "something went wrong" — is more damaging to user trust than an honest error message. Users can tolerate failures; they cannot tolerate failures that look like normal behavior until too late.

Good error states:
- Tell the user that something went wrong
- Tell them what they can do (try again, rephrase, contact support)
- Do not expose internal system details, prompt content, or stack traces

A feature that is down due to provider outage should fail fast with a useful message, not hang waiting for a timeout. Set realistic timeouts and handle them explicitly.

### Setting expectations

Users do not know what an LLM can and cannot do. Your interface has to communicate it:

- If the feature does not access real-time information, say so: "Based on information through [date]."
- If the feature can make mistakes on factual claims, say so — a small disclaimer is better than eroding trust after the first wrong answer.
- If there are scope limits ("only answers questions about our products"), communicate them before the user runs into them with an off-topic question.
- If the feature is AI-generated, many contexts (professional, legal, regulated industries) require you to disclose it. Check your jurisdiction and industry norms.

### Team norms around prompts and models

Prompt changes affect user experience. They should follow the same process as code changes:

- **Review**: Who reviews prompt changes before they go to production? Is it the same person who wrote them?
- **Testing**: Is there an eval run before any prompt change ships?
- **Documentation**: Are prompt versions documented in the runbook, alongside the model version?
- **Ownership**: When the feature misbehaves at 11 p.m., who has the context to diagnose and fix it?

These questions have boring answers that differ by team size and structure. The important thing is that they are answered — not assumed to be obvious.

*One-line analogy:* Treating prompt changes as one-off chat edits is like deploying code by editing files directly on the production server. It works until it doesn't, and when it doesn't, you have no idea what changed.

### Takeaway

- Streaming improves perceived speed significantly; implement cancel, handle dropped connections gracefully.
- Honest, fast error states build more trust than silent failures.
- Set explicit expectations about data freshness, scope, accuracy, and AI disclosure.
- Prompt changes need review, testing, and documentation — the same as code changes.

---

## Try it

### Exercise 1 — Version a prompt

Take a prompt you currently use — even informally. Store it in a file with the metadata format from Chapter 2: version, model tested on, date, reason for version.

Now make one small change. Store the new version alongside the old one. How does it feel to have a record of what changed and why?

### Exercise 2 — Debug a real failure

Pick a recent instance where an LLM feature or prompt produced a wrong result. Use the diagnostic from Chapter 3:

- Is it prompt-shaped? Retrieval-shaped? Model-shaped? Validation-shaped?
- What is the minimal change that would address it?
- Is there a way to detect this failure automatically in the future?

### Exercise 3 — Build a few-shot template

For a structured extraction task (e.g., extracting action items from a meeting transcript, classifying support tickets, or summarizing product reviews), write a prompt template with: system instructions, two to three input-output examples, and a variable slot for the actual input.

Test it on five real inputs. What edge cases does it fail on? What would you add to the examples to handle them?

### Exercise 4 — Design an error state

For a feature you are building or have built: design the error state for the model API being unavailable. What does the user see? What do the logs capture? What is the fallback behavior?

If your current answer is "they see a spinner indefinitely," you have found something worth fixing.

---

*End of Part II. Previous: [Part I — Mental models and the model lifecycle](from-prompts-to-systems-part-i-mental-models-and-the-model-lifecycle.md) · Next: [Part III — Data, retrieval, and adaptation](from-prompts-to-systems-part-iii-data-retrieval-and-adaptation.md) · Or [main volume](from-prompts-to-systems.md).*
