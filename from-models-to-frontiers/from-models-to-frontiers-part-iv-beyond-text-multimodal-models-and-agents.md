# Part IV — Beyond text: multimodal models and agents

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

Language is one modality among many. The world produces images, audio, video, structured data, sensor readings, and code — and increasingly, capable AI systems need to work across these modalities together, not in isolation. This part covers multimodal models, the research foundations of tool use and grounding, and the architecture and failure modes of agents that operate over multiple steps in the world. Each of these is an active research area; this part gives you the depth to read it critically.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 12–14.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Multimodal foundations | Vision-language architectures, audio-language, unified vs. modular, evaluation challenges |
| **2** | Tool use, retrieval, and grounding at research depth | When to retrieve vs. use long context vs. parametric memory; grounding protocols |
| **3** | Agents: planning, memory, and multi-step reliability | Architectures, failure modes, evaluation over time, open problems |

**Contents (plain list — same as table):**

1. Multimodal foundations — fusion, architectures, evaluation.
2. Tool use and grounding — retrieval vs. context vs. memory.
3. Agents — planning, memory, evaluation, failure modes.

---

## Chapter 1 — Multimodal foundations

**When the model describes what is not in the image as confidently as what is, you have a new category of failure that text-only evaluation never surfaced.**

Language models learn statistical patterns over tokens. Images produce a very different kind of statistical pattern — pixel values, spatial relationships, edges, objects, scenes — and the challenge of multimodal modeling is building a system that can reason about both kinds of information jointly, not just process them separately.

### The basic architecture question: unified vs. modular

There are two broad approaches to building a model that handles both text and images (or other modalities).

**Modular approach**: A separate visual encoder (often a vision transformer pretrained on image classification or contrastive image-text pairs) processes images into a representation, which is then projected into the language model's token embedding space. The language model sees the image as a sequence of "visual tokens" alongside the text tokens. Common examples: early LLaVA-style models, many production VLMs (vision-language models).

**Unified approach**: A single model is trained from the start on both text and images, with image patches tokenized directly and interleaved with text tokens. No separate encoder — just one model that processes multiple modalities with the same architecture.

The modular approach is more practical for combining existing strong visual encoders with existing strong language models. The unified approach potentially allows tighter integration between modalities but requires much more training data and compute to match strong specialized encoders.

### Vision-language pretraining

**Contrastive pretraining** (the approach behind CLIP) trains an image encoder and text encoder jointly so that matching image-text pairs are represented close together in embedding space. This produces strong visual representations that can identify objects, scenes, and concepts without requiring labeled classification data.

**Generative objectives** train the model to generate text descriptions from images, or to generate images from text descriptions. These objectives require the model to represent detailed visual content, not just coarse category labels.

Modern vision-language models typically combine both: contrastive pretraining for the visual encoder, followed by supervised fine-tuning on image-text pairs for the specific task format (captioning, visual question answering, document understanding).

### Audio-language models

Audio introduces different challenges than images:
- Audio is inherently temporal — meaning depends on sequence and duration, not spatial layout.
- The same acoustic signal can correspond to different meanings depending on prosody, accent, and context.
- Speech recognition (converting audio to text) is not the same as audio understanding (understanding tone, emotion, background sounds, music).

**Speech tokens** are typically produced by a discrete audio encoder — a model that converts audio into a sequence of discrete codes, analogous to how images are converted to visual tokens. These can then be processed by a language model alongside text tokens.

**Whisper-style** models trained on large amounts of speech-text pairs achieve strong transcription performance. Audio language models that extend beyond transcription to understanding non-linguistic audio content are less mature.

### Evaluation challenges specific to multimodal models

Text-only evaluation is difficult enough — multimodal evaluation introduces additional failure modes:

**Hallucinated objects.** The model describes objects, text, or details that are not present in the image. This is qualitatively different from text hallucination: the model is not confabulating about facts from training data, but about the specific visual content it was given. A user who trusts a VLM's description of an image may be misled about what is actually there.

**Spatial relationship errors.** Models often fail on questions about relative positions: "Is the cup to the left or right of the plate?" requires precise spatial reasoning that models frequently get wrong despite being able to describe both objects individually.

**Text in images (OCR).** Reading and understanding text that appears in images (signs, documents, screenshots) is a separate capability from visual reasoning. Models vary dramatically in OCR quality; this is often a surprising failure for users who expect a VLM to handle documents.

**Modality anchoring.** When text and image information conflict, models often anchor on the modality that dominates their training data — typically text. A model shown an image of a red car with the caption "blue car" may answer questions based on the caption rather than the image.

**Fairness and representation.** Multimodal models inherit biases from both their text training data and their visual training data. Visual biases — what kind of faces appear when a model generates "a doctor" or "a criminal" — are distinct from text biases and require separate evaluation.

*Memorable failure:* the model describes a picture confidently and incorrectly. The user assumes they can trust it. Text-only QA errors feel quaint by comparison because at least with text-only hallucination, the model's training data had the content. With visual hallucination, the evidence was right there in the input and the model invented something else.

### Takeaway

- Multimodal models combine visual and text understanding through modular (separate encoder) or unified (single model) architectures.
- Vision-language pretraining uses contrastive and generative objectives to build strong visual representations.
- Audio-language models extend the same principles to speech and audio content.
- Evaluation challenges specific to multimodal: hallucinated objects, spatial errors, OCR quality, modality anchoring, and visual representation bias.
- Multimodal errors are qualitatively different from text-only errors — they require multimodal evaluation, not text evaluation applied to captions.

---

## Chapter 2 — Tool use, retrieval, and grounding at research depth

**Volume II covered RAG as an engineering practice. This chapter asks the harder question: when is retrieval the right architecture at all, and what makes grounding reliable?**

The basic problem: language models have parametric knowledge (learned during pretraining, frozen into weights) and context knowledge (what is present in the current input). Neither alone is sufficient for many production tasks. The interesting research question is how to combine them well — and how to tell when the model is actually using retrieved content versus generating from parametric memory despite being told to retrieve.

### Parametric vs. non-parametric memory

**Parametric memory** (knowledge in weights) is:
- Fast to access — no external retrieval step.
- Potentially stale — knowledge is frozen at training time.
- Hard to audit — you cannot check which training examples the model is drawing on.
- Hard to correct — changing specific facts requires retraining or fine-tuning.
- Subject to hallucination — the model can be confident about things it does not actually know.

**Non-parametric memory** (retrieved from an external store) is:
- As fresh as the store — can be updated without retraining.
- Auditable — you can inspect what was retrieved and trace the model's answer.
- Bounded — the model can only answer based on what was retrieved.
- More expensive — requires a retrieval step, a vector store, chunked documents, and embedding infrastructure.

The decision between retrieval and long context is a variant of this question: when does it make sense to retrieve a subset of relevant content versus including all potentially relevant content in the context window?

### Long context vs. retrieval

As context windows have grown to 128k, 1M, and beyond, the question has emerged: do we still need retrieval, or can we just include everything in context?

The tradeoffs are real:

**In favor of long context over retrieval:**
- No retrieval infrastructure to build and maintain.
- No chunking decisions — no risk of splitting a relevant passage across chunks.
- The model can attend to any part of the context simultaneously.
- Works well when the relevant content is unknown in advance (you cannot know what to retrieve).

**In favor of retrieval over long context:**
- Very long contexts are expensive (attention cost is quadratic in sequence length).
- Models do not uniformly use all context equally. Research has documented a "lost in the middle" effect: models attend more strongly to the beginning and end of long contexts, with middle content being underweighted.
- Retrieval provides an auditable trace of what information the model used.
- For large knowledge bases (millions of documents), retrieval is more practical than including everything.

The practical answer depends on scale. For knowledge bases that fit in context at affordable cost, long-context may be simpler. For large knowledge bases or tight latency/cost constraints, retrieval remains necessary.

### The grounding problem

**Grounding** is the property of model outputs being traceable to specific, verifiable information sources rather than generated from parametric memory. A grounded answer cites specific retrieved passages; an ungrounded answer may be factually correct (drawing on pretraining) or fabricated.

The challenge: models trained to be helpful will generate confident-sounding answers even when the retrieved context is insufficient, irrelevant, or absent. Ensuring grounding requires:

**Explicit grounding instructions in the system prompt.** "Answer only from the provided CONTEXT. If the context does not contain sufficient information, say so." These reduce but do not eliminate hallucination.

**Grounding evaluation.** Test whether the model correctly abstains when the answer is not in the context. Include queries where the answer is genuinely absent. A model that correctly says "I don't know" on absent-answer queries is grounded; one that generates plausible-sounding answers to everything is not.

**Citation-level verification.** For high-stakes uses, requiring the model to identify specific passages it is drawing from, and checking that those passages support the claim, provides a verifiable audit trail.

*Friction:* "We added tools" does not fix the grounding problem if the model can sound confident when a tool returns nothing. The grounding discipline has to be in the prompting, the evaluation, and the output validation — not just the tool architecture.

### Fine-tuning vs. retrieval for knowledge updates

When knowledge needs to be updated (product information changes, regulations update, research findings shift), the choice between retrieval and fine-tuning recurs:

**Retrieval** is almost always better for knowledge that changes frequently. Fine-tuning snapshots knowledge at training time; retrieval provides current knowledge at query time. Updating a retrieval index is fast; re-fine-tuning a model is slow and expensive.

**Fine-tuning** is better for behavioral changes: teaching the model how to perform a task it was not optimized for, adjusting its output format, or specializing its reasoning style. Fine-tuning does not reliably implant specific facts — it can produce confident wrong answers rather than retrieving correctly.

The common mistake is using fine-tuning to update facts rather than behavior, and retrieval to change behavior rather than knowledge. Match the mechanism to the problem.

### Takeaway

- Parametric memory (in weights) is fast and accessible but stale, unauditable, and subject to hallucination.
- Non-parametric memory (retrieval) is updatable and auditable but requires infrastructure and careful chunking.
- Long context and retrieval are complementary, not competing — the choice depends on knowledge base size, cost constraints, and context utilization patterns.
- Grounding is a discipline requiring explicit instructions, evaluation of absent-answer cases, and optional citation verification.
- Use retrieval for knowledge updates, fine-tuning for behavioral changes.

---

## Chapter 3 — Agents: planning, memory, and multi-step reliability

**An agent demo with five steps is three slides. An agent deployment with five hundred steps is a systems engineering problem.**

Agents — systems where a model takes actions, observes results, and continues until a goal is achieved — represent a qualitative expansion of LLM capability and risk. The same properties that make agents powerful (they can accomplish complex tasks without step-by-step human instruction) make them difficult to evaluate, debug, and control.

### The agent loop

The basic architecture of a tool-using agent:

```
while goal not achieved:
    observe current state
    plan next action
    select and call a tool
    receive tool result
    update state / context
    decide: continue or terminate
```

This loop is simple to describe and complex to get right. Each iteration involves the model making a decision based on potentially noisy or incomplete information, with downstream consequences for subsequent decisions.

### Planning architectures

**Flat planning.** The model receives a goal and makes tool calls directly, without explicit decomposition. Effective for simple tasks; brittle for complex tasks where subgoal tracking matters.

**Chain-of-thought planning.** The model first produces an explicit reasoning trace (a plan), then executes it. This can improve coherence on multi-step tasks and provides a debugging artifact. The plan and the execution can drift.

**ReAct (Reasoning + Acting).** Interleaves reasoning steps and action steps: think → act → observe → think → act. Produces a trace that shows the model's reasoning at each step, which aids debugging.

**Hierarchical planning.** A planning agent decomposes the goal into subgoals and delegates to specialized subagents. Reduces the complexity each model must manage; adds coordination overhead and potential for misalignment between levels.

None of these architectures solves the fundamental reliability problem: each step involves a model that can be wrong, and errors compound over many steps.

### Memory architectures

Agents need memory to maintain context over long task horizons. Four types of memory interact:

**In-context memory.** The current conversation/state is kept in the context window. Simple; runs out as the task grows longer.

**Episodic memory.** A record of past events the agent can retrieve. Allows the agent to reference previous actions without keeping the full history in context. Requires careful retrieval design to avoid missing relevant prior context.

**Semantic memory.** A knowledge store the agent can query. The RAG approach applied to agent memory: the agent can look up facts, procedures, and prior decisions.

**Working memory.** Intermediate results — calculations, partially processed data, notes — kept available during a task. Often implemented as files or structured data in the tool environment.

The tradeoff: more memory types add capability and complexity. The agent must learn when to store, when to retrieve, and when to discard. Memory architecture failures (storing the wrong things, retrieving the wrong things, failing to discard stale information) are a major source of agent reliability problems.

### Failure modes

**Error compounding.** A small mistake in step 3 affects step 4, which affects step 5. By step 20, the original error may have propagated into an irrecoverable state. Errors do not stay small in long-horizon tasks.

**Goal drift.** Over a long task, the model's behavior may drift toward proxies that are easier to achieve than the original goal. This is subtle and difficult to detect without explicit goal tracking.

**Wrong tool arguments.** The model calls a tool with a plausible-sounding argument that is actually incorrect. This is worse in an agent context because tool errors compound. Validation (checking arguments before execution) and human approval for irreversible actions are not optional.

**Looping.** The agent re-performs the same action repeatedly, believing it has not yet succeeded, because it cannot correctly interpret the tool result. Explicit loop detection with a maximum action count is basic safety engineering.

**Out-of-scope actions.** The agent takes actions that were not intended by the user — sending messages, modifying files, making purchases — because the scope of the task was interpreted more broadly than intended.

**Context window exhaustion.** For very long tasks, the agent may run out of context window. Without explicit handling (summarization, retrieval), this causes the agent to "forget" earlier context and make decisions based on incomplete state.

*Direct address:* if your agent demo runs reliably in five steps, it will fail unpredictably at twenty. The debugging surface scales faster than the slide count. Invest in evaluation harnesses that test longer trajectories before deploying.

### Evaluating agents

Single-turn LLM evaluation is already hard. Agent evaluation is harder for several reasons:

**Non-determinism.** Agents make choices at each step; different executions of the same task can take different paths. Evaluation must cover multiple trajectories, not a single fixed output.

**Partial credit.** An agent that completes 8 of 10 required steps correctly is partially successful. Binary success/failure metrics miss this.

**Credit assignment.** When an agent fails, which decision caused it? Tracing the root cause requires step-by-step inspection of the trajectory, not just outcome evaluation.

**Environment fidelity.** Agent evaluation requires a realistic environment for the agent to operate in. A test environment that is easier or harder than production will produce misleading results.

Effective agent evaluation uses:
- Diverse starting states (not just the happy path).
- Adversarial or edge-case scenarios.
- Both outcome metrics (did the task complete?) and process metrics (were intermediate steps reasonable?).
- Failure analysis to identify specific steps where agents consistently go wrong.

### Open problems in agent research

- **Safe interruptibility**: Can an agent be stopped or redirected mid-task without causing harm from partially completed actions?
- **Long-horizon credit assignment**: How should feedback from a task outcome be attributed to individual decisions in a long trajectory?
- **Compositional generalization**: Can agents generalize from training tasks to novel combinations of skills they have not seen together?
- **Alignment under delayed reward**: If the agent's goal is rewarded only at task completion, how do we ensure intermediate actions remain aligned?

These are active research areas, not solved problems.

### Takeaway

- Agents loop: observe, plan, act, update, decide. Each iteration involves a model that can be wrong.
- Planning architectures (flat, CoT, ReAct, hierarchical) trade off simplicity and debuggability.
- Memory architectures (in-context, episodic, semantic, working) add capability and complexity.
- Primary failure modes: error compounding, goal drift, wrong arguments, looping, out-of-scope actions.
- Agent evaluation requires multi-trajectory coverage, partial credit, credit assignment, and realistic environments.
- Invest in evaluation harnesses before deploying agent systems at meaningful scale.

---

## Try it

### Exercise 1 — Multimodal evaluation design

You are building a vision-language feature for a retail product catalog: users upload photos of items and the model identifies the product and answers questions about it. Name two failure modes specific to this visual use case that would not appear in a text-only QA system. For each, describe how you would construct a test case to detect it.

### Exercise 2 — Grounding protocol

Design a grounding evaluation for a retrieval-augmented system: a research assistant that answers questions by retrieving from a corpus of scientific papers. Describe the test cases you would include to verify that the model correctly abstains when the answer is not in the retrieved context, and what you would consider a passing result.

### Exercise 3 — Agent failure trace

Describe a realistic failure scenario for a tool-using agent tasked with "schedule a meeting for next Tuesday with everyone on the project team." Walk through the first five steps the agent might take, identify one specific failure mode, and describe one architectural change (not just a prompt instruction) that would make this agent more robust.

### Exercise 4 — Memory architecture decision

A coding assistant agent needs to remember: (1) the user's code style preferences from previous sessions, (2) the contents of files it edited in the current session, (3) documentation for the libraries it is using. For each of these three memory needs, identify the most appropriate memory type (in-context, episodic, semantic, working) and explain why. If two needs are best served by the same type, note the tradeoff.

---

*End of Part IV. Previous: [Part III — Efficiency: training, inference, and systems](from-models-to-frontiers-part-iii-efficiency-training-inference-and-systems.md) · Next: [Part V — Frontiers and open problems](from-models-to-frontiers-part-v-frontiers-and-open-problems.md) · Or [main volume](from-models-to-frontiers.md).*
