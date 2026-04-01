# Part IV — First steps with prompts

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

You understand what models are, how they generate text, and where they shine or stumble. This part is **hands-on**: how chat interfaces are structured, how to write prompts that actually work, how to recover when the model drifts, and — just as important — **when to stop** and reach for a different tool entirely.

Prompts are not magic spells. They are specifications. A clear specification produces better output than a vague wish, for the same reason that a clear brief produces better work from any collaborator.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 13–16.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Chat interfaces and roles | System vs user, scope, and keeping a prompt library |
| **2** | Writing prompts that work | Goals, audience, format — and few-shot patterns |
| **3** | Common failure modes | Diagnosing vagueness, length, format slips, ignored rules |
| **4** | When not to use an LLM | High stakes, secrets, correctness guarantees — and better fits |

**Contents (plain list — same as table):**

1. Chat interfaces and roles — system vs user; prompt library.
2. Writing prompts that work — goal, audience, format; few-shot.
3. Common failure modes — vagueness, length, format, ignored rules.
4. When not to use an LLM — stakes, privacy, proof.

---

## Chapter 1 — Chat interfaces and roles

**Who is speaking, and to whom?** Most people encounter language models through a simple text box — you type, it responds. But underneath, every conversation has structure that shapes the model's behavior. Understanding that structure is the first step toward using it deliberately rather than hoping for the best.

### Three roles in a chat

In most systems, messages carry one of three roles:

**System**: Instructions that set the rules for the entire conversation. What the model should act as, how it should respond, what it must never do, what format to use. Users typically do not see the system prompt — it is placed before the conversation begins by whoever built or configured the product. When you use a company's internal AI tool, the rules baked into that tool live here.

**User**: What you say. Your questions, instructions, and follow-ups.

**Assistant**: What the model said previously. In a multi-turn conversation, prior model responses are included in the context as assistant turns, so the model can respond coherently to what it already said.

Here is the underlying structure of a simple two-turn conversation:

    System:    You are a plain-language explainer of legal documents.
               Never give legal advice. Always recommend consulting
               a qualified attorney for important decisions.

    User:      What does "indemnification" mean in a contract?

    Assistant: Indemnification means one party agrees to cover
               the costs or losses of another if something goes wrong...

    User:      Can you give me a simple example?

The system message persists for the whole thread. The user and assistant turns accumulate. Everything is text in a sequence — the model sees all of it as one long prompt and generates a continuation.

### What the system message gives you

When you can edit the system message — in a developer context or a configurable tool — treat it as the **contract for the whole thread**. Put things here that you want enforced consistently:

- **Voice and tone**: "Respond in plain language suitable for a non-technical audience."
- **Format rules**: "Use bullet points for lists. Never use more than three levels of nesting."
- **Scope boundaries**: "Only answer questions about our product. If asked about competitors, decline politely."
- **What not to do**: "Do not invent statistics. If you are unsure of a number, say so explicitly."

When you cannot see or edit the system message, you can approximate some of its function by starting your first user message with "For this conversation, please..." — less reliable, but often effective for simple constraints.

### Keeping a prompt library

Good prompts are assets. If you write a system prompt that produces consistently useful results — a tone, a format, a set of rules — save it. Keep a personal library: a plain text file, a note, a document, anything you can search later.

Label entries by **intent**, not by content: "professional email decliner," "extract action items from meeting notes," "explain code to a non-programmer." Add one line of metadata: which product or model you tested it on, and the approximate date. Model updates can change behavior; dated notes tell you when to re-test.

*Friction:* The most common prompting anti-pattern is rebuilding the same system prompt from scratch every session because you never saved the version that worked. The second most common is saving it but not labeling it, so you cannot find it six weeks later.

### Managing drift in long conversations

Models drift during long conversations: they pick up the style of recent turns, chase tangents, or gradually forget instructions given early in the thread. If the thread has gone off course, the fastest fix is usually a **new chat** with a fresh system prompt — not another ten messages trying to redirect the existing one.

*Direct address:* Opening a new chat is not an admission of failure. It is recognizing that the context window has been contaminated with unhelpful patterns and starting from a clean state. This is professional, not impatient.

### Quick takeaway

- Conversations have three roles: system (rules), user (you), assistant (prior model output).
- System messages persist for the whole thread — use them for consistent rules and format.
- Save useful prompts with intent labels and dates.
- When a thread goes wrong, a fresh chat is often faster than repair.

---

## Chapter 2 — Writing prompts that work

**What does "better prompt" mean if you never said what "better" looks like?** The most common prompting mistake is treating prompt quality as a mystery to be intuited rather than a specification to be written. Prompts work better when you make four things explicit: the goal, the audience, the format, and the constraints.

### Goal: what success looks like

Before everything else, state what a successful response actually looks like.

Compare:

**Vague**: "Can you help me with this document?"

**Specific**: "Identify the three most important action items in this document and list them in order of urgency, with one sentence explaining why each matters."

The vague prompt invites the model to define success for you. That is exactly the wrong way around. The model will produce a plausible response to the vague prompt — but plausible and useful are not the same thing.

### Audience: who is reading

Adding an audience constraint changes the response significantly:

- "Explain transformer architecture to a software engineer who has never studied ML."
- "Explain transformer architecture to a business executive who needs to make a budget decision."
- "Explain transformer architecture to a high school student."

The model adjusts vocabulary, analogy choices, depth, and assumed knowledge. "Make it clear" is not an audience. A specific reader with specific background knowledge is.

### Format: what shape the output should take

Specify the **shape** of what you want:

- "Bullet list of no more than five items."
- "A table with columns: Risk, Likelihood, Mitigation."
- "Two paragraphs: first the pros, then the cons. No more than 150 words total."
- "JSON with fields: summary, key_points (array), confidence_level (low/medium/high)."

Leaving format unspecified means the model chooses — and it will choose what appears most common in its training data for that type of question, which may not be what you need.

### Constraints: the guardrails

Constraints tell the model what to avoid and set limits:

- "Do not repeat information from earlier in the document."
- "If you are unsure about a specific number, say so — do not invent it."
- "No preamble. Start your response directly with the answer."
- "At most 200 words."

Constraints also **surface uncertainty**: if the model cannot comply with a constraint (e.g., "cite only peer-reviewed sources" when it has none), that failure is informative — it tells you what the model actually knows.

### Before and after: a worked example

**Before (vague):**
"Summarize this meeting transcript."

**After (specific):**
"From this meeting transcript, extract: (1) the three decisions made, each in one sentence; (2) the action items, each with an owner and deadline where stated; (3) any unresolved questions. If something is ambiguous, flag it rather than guessing."

The second prompt will produce a result you can hand directly to stakeholders. The first will produce a paragraph summary that is readable but may miss the specific structure you needed.

### Few-shot: showing the pattern

**Few-shot prompting** means including short examples of input → desired output in the prompt. The model picks up on format from examples very quickly — often faster than from a paragraph of verbal description.

    Example 1:
    Input: "The meeting was productive and we covered several topics."
    Classification: Vague — no specific outcome stated.

    Example 2:
    Input: "We agreed to delay the launch by two weeks to allow QA time."
    Classification: Specific — clear decision with rationale.

    Now classify this:
    Input: "Leadership discussed the roadmap for next quarter."

Two or three examples usually outperform a long written description for tasks involving classification, extraction, or rigid formatting. Keep examples honest — do not embed false information as demonstrations.

### Chain-of-thought: asking for reasoning steps

For problems that involve reasoning — math, comparisons, multi-step decisions — asking the model to "think through this step by step" or "explain your reasoning before giving your final answer" can improve accuracy.

This works because it makes intermediate steps visible in the token stream, and the model's generation of those steps provides a kind of working memory for the task. It is not magic — it works best for reasoning tasks where the steps are meaningful, and it adds tokens (and therefore cost and latency) to every response.

Use it deliberately, not by default. For simple lookups or direct questions, chain-of-thought adds overhead without benefit.

*Anchor:* Prompting is less like issuing a command and more like briefing a capable contractor. A vague brief produces vague work. A specific brief — goal, audience, format, constraints, examples — produces work you can use.

### Quick takeaway

- State the goal explicitly: what does a successful response look like?
- Name the audience: who is reading this, with what background?
- Specify the format: shape, length, structure.
- Add constraints: what to avoid, what to flag when uncertain.
- Use few-shot examples for classification and rigid formats.
- Use chain-of-thought for reasoning tasks — but not by default.

---

## Chapter 3 — Common failure modes — and simple responses

Even well-intentioned prompts fail. The good news is that failures fall into recognizable patterns. Recognizing the pattern means you change the setup rather than arguing with the model in prose.

### Failure mode 1: Too vague

**Symptom:** The response is generic, hedging, could apply to anything, or asks you twelve clarifying questions.

**Why it happens:** The model is trained to produce plausible responses. A vague prompt has many plausible responses, so it produces the most common one, which is usually the most generic.

**Fix:** Narrow the task. Add a concrete scenario. Request structure. State explicitly what you are and are not asking for.

    Instead of: "Tell me about project management."
    Try: "List the five most common reasons software projects miss deadlines, each with one sentence on how to prevent it."

### Failure mode 2: Too long

**Symptom:** Walls of text, repeated points, a three-paragraph preamble before the actual answer, or the same idea restated five times.

**Why it happens:** The model has seen enormous amounts of writing where thoroughness is rewarded. Without a length constraint, it defaults to thorough.

**Fix:** Cap the length. Ask for the answer first, then elaboration. Request an outline rather than a full draft.

    Add to your prompt: "Maximum 150 words." or "Lead with the direct answer, then explain in at most two sentences."

### Failure mode 3: Wrong format

**Symptom:** You wanted a bullet list and got an essay. You wanted plain text and got markdown that your pipeline cannot parse. You wanted JSON and got JSON wrapped in a paragraph.

**Why it happens:** Without a format specification, the model guesses what format best fits the question type. That guess is often wrong for your specific use case.

**Fix:** State the format in the prompt explicitly and, if possible, include a micro-example.

    "Return only a JSON object with the fields: name, date, summary. No surrounding text, no code fences."

If the model still adds surrounding text, try repeating the format constraint at the end of the prompt — recency in the prompt can help.

### Failure mode 4: Ignored instructions

**Symptom:** You said "do not mention competitor products" and it mentioned them. You said "respond in French" and it responded in English. You said "maximum 100 words" and got 400.

**Why it happens:** This can be a position problem (instructions buried in the middle of a long prompt are attended to less reliably than those at the start), a complexity problem (too many constraints at once), or a context length problem (a long conversation thread has pushed the original instructions out of effective attention range).

**Fix:**

1. Move critical rules to the beginning of the system message or the very start of the user message.
2. Reduce the number of simultaneous constraints — prioritize the most important ones.
3. If the failure happens in a long thread, start a new conversation with the instruction prominently placed.
4. Break the task into explicit steps: "Step 1: Do only X. Wait for my response before proceeding."

*Direct address:* If you are on your fifth "please follow this rule" message in the same thread, you are past the point where prompt tweaks help. The context has accumulated enough noise that a fresh start is faster than repair.

### A diagnostic shortcut

Before trying another prompt variation, ask: **Is this failure prompt-shaped?**

- If the model is producing reasonable-looking text about the wrong thing → prompt is probably too vague.
- If the model is producing exactly what you asked for but it is wrong on the facts → this is a hallucination problem, not a prompt problem. Prompting cannot fix it; verification can.
- If the model is behaving inconsistently across turns → context is the problem; start a new thread.
- If the model refuses to do something safe and reasonable → check whether the system prompt is restricting it, or try rephrasing with more context about why you need it.

### Quick takeaway

- Too vague → narrow the task with concrete scenarios and structure.
- Too long → cap length, ask for the answer first.
- Wrong format → specify it explicitly and give a micro-example.
- Ignored instructions → move rules to the front, reduce complexity, use a fresh thread.
- Distinguish prompt failures from hallucination failures — they need different responses.

---

## Chapter 4 — When not to use an LLM

Competence includes restraint. Knowing when not to reach for a tool is as important as knowing when to use it. Some tasks are genuinely wrong for probabilistic text generators — not because the model is bad at them, but because the **error profile** does not fit the requirement.

### High-stakes decisions without human review

**Medical, legal, financial, and safety-critical** decisions need qualified professionals and authoritative sources. A language model can help you understand a concept, prepare questions for a professional, or draft a summary of information you already have from authoritative sources. It should not be the sole basis for a diagnosis, a legal filing, a financial decision, or any choice where being wrong causes serious harm.

The risk is not that the model will obviously fail. The risk is that it will confidently produce something that sounds exactly right, passes a quick read, and turns out to be wrong in a way that matters enormously.

### Private or regulated data you should not paste

If putting text into a chat would violate a policy, breach a contract, or cause harm if leaked — do not paste it. Cloud chat tools may log, store, or train on your conversations depending on their terms of service. Customer data, patient records, unpublished research, legally privileged communications, and unreleased financial information all carry obligations that override the convenience of an AI tool.

The practical rule: if you would not forward this text to a stranger's email address without legal review, do not paste it into a chat box without knowing what happens to it. Use approved enterprise tools with clear data-handling terms, or offline models, when working with sensitive material.

### Tasks that need guaranteed correctness

**Formal verification, exact computation, cryptography, regulated compliance output** — these require deterministic tools with auditable processes, not probabilistic text generation. A language model doing arithmetic can get the right answer and the wrong answer on the same problem across different sessions. Code it generates may have subtle security flaws. Legal language it drafts may be invalid in your jurisdiction. For tasks where the standard is "definitely right," the tool needs a verifiability guarantee the model cannot provide.

### Better tools exist

Sometimes the right tool is simply a different one:

| Task | Better tool |
|------|-------------|
| Finding a specific document you wrote | Search engine or file system search |
| Performing exact calculations | Spreadsheet or calculator |
| Looking up current information | Web search with source verification |
| Running a repeatable process reliably | Code, scripts, or automation tools |
| Getting authoritative professional guidance | A qualified professional |
| Storing and retrieving structured data reliably | A database |

The model is strong where **language, structure, and pattern** help. It is weak where **truth, proof, privacy, or exact determinism** is required.

*One-line analogy:* A skilled writer does not use a word processor to calculate compound interest. A word processor is excellent; it is just the wrong tool. Knowing which tool fits which job is the skill.

### Quick takeaway

- High-stakes decisions: use the model to prepare, not to decide.
- Sensitive data: know your provider's data policy before pasting anything regulated.
- Exact correctness requirements: use deterministic tools with auditable outputs.
- Better tools exist for many tasks — match the tool to the error profile required.

---

## Try it

### Exercise 1 — Vague versus structured prompt

Pick a small task you actually need to do — summarize a document, draft a short message, explain a concept to someone. Write two prompts for it:

**Version A**: A one-liner, as vague as feels natural.

**Version B**: A prompt using goal, audience, format, and at least one constraint.

Run both. Compare the outputs. Which would you actually use as-is? Which needs more editing? If Version A was fine, ask yourself whether you were grading on accuracy or on politeness.

### Exercise 2 — Fix one failure mode deliberately

Write a prompt that you expect to produce a specific failure — too long, wrong format, or too vague. Observe the failure. Then rewrite the prompt with exactly one change to address it: a length constraint, a format spec, a concrete example, or a narrowed scope.

Did the fix work? If not, was the failure actually prompt-shaped, or was it a hallucination or a policy limit?

### Exercise 3 — Build a few-shot classifier

Choose a simple classification task: positive vs. negative sentiment, urgent vs. non-urgent, specific vs. vague. Write a prompt with two or three input-output examples, then test it on five new inputs.

How consistent is it? What kinds of edge cases confuse it? This exercise teaches you more about few-shot pattern-matching than any description can.

### Exercise 4 — Find the boundary

Try asking the model to do something that it probably should not — not harmful, but at the edge of what it is designed for. Something like: "Give me the exact legal language I should use to write my own will" or "Diagnose what's wrong with my knee based on this description."

Observe how it responds. Does it refuse? Does it comply with caveats? Does it comply without caveats?

Then ask yourself: what would the right behavior actually be in this situation? The goal is not to evaluate the model — it is to develop your own judgment about when to stop before the model does.

---

*End of Part IV. Previous: [Part III — Capabilities and limits](from-tokens-to-understanding-part-iii-capabilities-and-limits.md) · Next: [Part V — Responsibility in everyday use](from-tokens-to-understanding-part-v-responsibility-in-everyday-use.md) · Or [main volume](from-tokens-to-understanding.md).*
