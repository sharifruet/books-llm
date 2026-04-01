# Part III — Capabilities and limits

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

You now have a workable picture of **how** a model generates text. This part turns outward: **what these systems are genuinely useful for**, where they **fail or mislead**, how **bias** shows up in outputs, and what **cost, speed, and access** mean in practice.

The aim is proportion. Neither hype ("it can do anything") nor blanket dismissal ("it is only autocomplete") serves you well. You leave this part ready for the hands-on work in Part IV — and with the calibrated skepticism that makes the tools genuinely useful rather than naively trusted.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 9–12.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | What LLMs tend to do well | Real strengths — with an honest account of why they hold |
| **2** | Hallucinations, mistakes, and calibration | Why errors look credible; how to probe and verify |
| **3** | Bias, stereotypes, and fairness | Where skew comes from; why "fixing" it is hard |
| **4** | Speed, cost, access, and the environment | Who can use what, why price varies, a sober footprint note |

**Contents (plain list — same as table):**

1. What LLMs tend to do well — strengths tied to training data patterns.
2. Hallucinations, mistakes, and calibration — credible errors; verification habits.
3. Bias, stereotypes, and fairness — skew; why fixes are incomplete.
4. Speed, cost, access, and the environment — pricing, access gaps, energy in proportion.

---

## Chapter 1 — What LLMs tend to do well

**Which task would you give a tireless colleague who reads fast, writes fluently, and sometimes confidently states something completely wrong?** Not your final legal brief. But your first draft, your brainstorm list, your rephrased email — those are fine. The key to using language models effectively is matching the task to the capability, which requires actually understanding what the capability is.

Large language models are not equally good at everything. Their strengths cluster around tasks that are **pattern-rich in text**: language, format, shallow structure, and information that appears frequently in the training corpus. Knowing the shape of these strengths lets you delegate the right work and reserve human judgment for the rest.

### Drafting, rephrasing, and brainstorming

The single most reliable use of a language model is generating candidate text — not finished text, but starting points that you then edit, select from, or discard.

Ask for three different tones for the same email, and you get three; pick the one that fits and edit from there. Ask for ten headline options for a blog post and you get ten; two of them will be genuinely useful. Ask for an outline before writing and you get a skeleton to rearrange.

**Why this works:** Patterns of tone, structure, and phrasing appear constantly in training data. The model has seen thousands of formal-to-informal transformations, thousands of bullet lists derived from paragraphs, thousands of headlines for thousands of topics. It can generate plausible variations at a speed no human can match.

**The limits:** Faster drafts are not more accurate drafts. "The model wrote it" is not a claim about truth or fitness for purpose — it is a claim about text generation. You remain responsible for the substance.

### Explaining and teaching

Language models are often useful for getting a plain-language explanation of something you do not understand. "Explain how a neural network learns" in ten different ways, at ten different levels of assumed knowledge — the model can do all of them.

**Why this works:** Training data includes enormous amounts of pedagogical text: textbooks, tutorials, explainer articles, Stack Overflow answers, forum threads where experts answer novice questions. The model has learned the shape of "here is a concept explained simply" from millions of examples.

**The limits:** The explanation may be fluent, clear, and subtly wrong. It may omit the crucial caveat that changes the whole picture. It may use an analogy that breaks down in exactly the case you care about. Always check explanations against primary sources when the stakes matter.

### Editing and format transformation

Converting prose to bullet points, bullet points to prose, tables to descriptions, code to documentation — these structural transformations are reliably useful tasks. The model handles format with high consistency.

**Why this works:** Format patterns — markdown, structured lists, JSON shapes, table structures — appear so frequently in training data that the model has a very firm statistical grip on them.

**The limits:** It transforms form, not substance. A factually confused paragraph reformatted into bullet points produces clearly labeled confusion.

### Writing code sketches and debugging hints

For common programming tasks — boilerplate, standard library usage, common API patterns, explaining what an error message might mean — language models are genuinely useful, especially for developers who already know enough to evaluate the output.

**Why this works:** Code represents a large fraction of training data for modern models. The patterns of "here is an error message, here is what it likely means" are well-represented.

**The limits:** The model does not run your code. It does not know your specific library versions, your environment, or your constraints. Treat code suggestions as sketches that require testing, not as solutions that require only copying. For novel problems or tight correctness requirements, the model is much less reliable.

### Multilingual assistance (with significant caveats)

Translation, summarization, and basic conversation in many languages are within reach. High-resource languages (English, Spanish, French, German, Chinese, Japanese) generally work better than low-resource ones.

**Why this works:** The internet, and therefore the training data, includes text in many languages, creating multilingual competence as a side effect.

**The limits:** Performance degrades sharply for low-resource languages, regional dialects, and minority languages. "Works in Spanish" does not imply "works in Nahuatl" or even in every Spanish-speaking regional register. Cultural nuance is harder than linguistic translation. Do not rely on the model for languages you cannot evaluate the output in.

### The recurring theme

All of these strengths are **assistive and draft-quality**. They accelerate iteration. They generate options. They handle the mechanical work of formatting and phrasing so you can focus on substance and judgment. They become most valuable when a human — or a deliberate verification step — can catch errors before they matter.

*Friction:* The organizational risk is not that the model fails obviously. It is that the model succeeds fastwhere you expected it to fail — so teams skip the review step because the output arrived quickly and looked polished. Fast and polished is not the same as accurate and safe.

---

## Chapter 2 — Hallucinations, mistakes, and calibration

**Picture a bibliography in a perfectly formatted academic paper where half the cited studies do not exist.** The author names are plausible. The journal names are almost right. The titles are exactly the kind of titles those journals would publish. But the actual papers — the ones with those exact titles, by those exact authors, in those exact journals — are not real. This is the hallucination problem, and it is not a rare edge case.

### What hallucination actually means

In everyday use, a **hallucination** is a specific, confident, fluent output that is factually false or unsupported. The word comes loosely from psychology — an experience that feels real but has no external basis — but in the LLM context it just means: **the model stated a specific thing as if it were true, and it was not.**

This is distinct from vagueness, uncertainty, or disagreement. A model saying "I'm not certain, but I believe…" is hedging. A model saying "The study by Kovacs et al. (2019) found that…" and inventing the study is hallucinating.

Hallucinations are not rare. They are a **structural property** of how these models work. The training objective rewards plausible continuation, not verified fact. There is no internal fact-checker.

### Four categories where hallucination is most common

**1. Specific numbers and statistics.** Populations, percentages, dates, measurements. The model knows that questions about numbers should be answered with numbers, and it will produce a number — even when it does not have reliable data.

**2. Citations and references.** Ask for academic citations and you are likely to get plausible-looking but nonexistent papers, articles, or rulings. The model knows what citations look like, and it will produce the right shape — with wrong content.

**3. Details about people and organizations.** Job titles, publication histories, biographical facts about real people, details about companies. The model knows that articles about people include these details, so it fills them in.

**4. Events near or after the training cutoff.** The model may generate plausible-sounding details about recent events it has no actual data on.

### Why this happens

Walk through the mechanism. You ask: "What was the population of Lagos in 2022?"

The model has seen thousands of sentences of the form "The population of [city] in [year] was [number]." It knows the shape of this answer. It picks a number that fits that pattern — possibly a real number it saw, possibly a blend of numbers from different years, possibly a confident extrapolation. It has no flag that fires to say "I don't have reliable data for this specific fact." It just produces the most plausible continuation of the question-answer pattern.

The confident tone is not evidence of accuracy. It is evidence of how many confident-sounding answers appear in the training data.

### The verification habit

For any output where factual accuracy matters:

1. **Separate form from substance.** The model may produce beautiful structure around empty or false content. A well-formatted argument is not a correct argument.
2. **Check specific claims.** Numbers, names, dates, citations — any specific claim that would be embarrassing if wrong should be verified from a primary source.
3. **Never treat model citations as real.** If you want citations, find them yourself through a library database or search engine. Use the model to identify *what to look for*, not to provide the reference itself.
4. **Ask for uncertainty signals, but do not rely on them.** Prompting the model to flag things it is unsure about sometimes helps. But the model can also say "I'm fairly confident" about something it is wrong about, and can hedge about things it actually knows. Prompting helps at the margins; it does not solve the structural problem.

*Memorable detail:* A model that is wrong 5% of the time on factual claims sounds reliable until you realize that a 1,000-word document contains dozens of factual claims — and some of them may be wrong in ways that look completely convincing.

*Direct address:* If you are using a language model for anything involving health, legal advice, financial decisions, or any domain where being wrong hurts someone — treat every specific claim as a hypothesis to verify, not a fact to cite.

---

## Chapter 3 — Bias, stereotypes, and fairness

Language models learn from human-generated text. That corpus encodes centuries of human bias: stereotypes about demographic groups, uneven representation of different communities' voices, historical prejudice baked into what was written down and what was not, and gaps in whose knowledge and perspective was digitized. The model does not learn to *understand* bias — it learns to *reproduce the patterns in text*, including the biased ones.

### What "bias" means in this context

In this chapter, **bias** means **systematic skew**: outputs that favor one demographic group, language variety, or worldview over others in ways that are unjustified and often harmful. This is not the same as having a point of view on a contested issue. It is about unfair regularities: consistent under-representation, caricature, or degradation of specific groups.

### Three concrete examples

**Demographic defaults in generated scenarios.** If you ask a model to write a story about a doctor, it may default to a male doctor. If you ask for a story about a nurse, it may default to a female nurse. These defaults reflect the statistical distribution of how doctors and nurses are described in text — and reinforcing those defaults in AI outputs compounds the representational problem.

**Dialect quality judgments.** Language models trained primarily on edited, formal, standard English prose may evaluate or continue African American Vernacular English (AAVE) or other dialects as lower quality, produce corrections when none were requested, or treat non-standard grammar as errors rather than as valid linguistic variation. This is not a deliberate design decision — it is the model reflecting patterns in what "good writing" looks like in its training data.

**Western-centric cultural defaults.** Concepts of family structure, political systems, professional norms, food, clothing, and historical events will skew toward Western European and American perspectives in models trained on English-dominant internet text. A question about "traditional marriage" will produce an answer shaped by that corpus. A question about historical events may center perspectives that dominated the text sources.

### How bias enters the system

The pipeline has three stages where bias can compound:

**Training data.** If the data over-represents certain groups, perspectives, and time periods, the model learns those patterns more deeply. What is not well-represented is learned less reliably.

**Training objective.** The next-token prediction objective does not distinguish between "the text accurately represents group X" and "this is how X is most commonly described in text." Both generate the same training signal.

**Post-training tuning.** Preference tuning and safety filtering reduce some harmful outputs — but they can also shift bias rather than eliminate it, introduce new inconsistencies (over-refusing for some groups, under-refusing for others), or suppress surface expressions of bias while leaving deeper patterns intact.

### Why "fixing" this is an open challenge

Technical mitigations help at the margins: filtering training data for known harmful content, fine-tuning on more representative examples, using classifiers to catch problematic outputs. But these approaches involve difficult tradeoffs — between accuracy and fairness, between free expression and harm reduction — and they can shift bias without removing it.

The deeper problem is that "fair" is not a single, technically specified standard. It requires answering questions like: whose representation counts, by what measure, according to whose cultural standards? Those are social and political questions that engineering alone cannot resolve.

*Direct address:* Do not treat the model as a neutral arbiter of anything involving people, history, or culture. It is not neutral. Nothing trained on human text can be.

For high-stakes outputs — decisions that affect hiring, lending, medical triage, content moderation — bias testing against specific demographic groups should be a requirement, not an afterthought.

---

## Chapter 4 — Speed, cost, access, and the environment

These are not secondary concerns. They are the constraints that shape **who gets to use these tools**, **what they can do with them**, and what real-world resources their use consumes. A short, honest account is more useful than either mystery or moral theater.

### Free tiers, paid APIs, and what "bigger" costs

Most providers offer a free or low-cost tier for casual use. Serious volume — building a feature, running evaluations, processing large documents — usually means paid API access or an enterprise contract.

**Pricing is almost always per token**, for both input and output. The rough intuition:

- A 1,000-word document is approximately 1,300 tokens.
- A mid-tier model API might charge $0.003–$0.015 per 1,000 input tokens.
- A frontier model might cost 5–10x more.
- Output tokens are often priced higher than input tokens.

So a single 500-word answer to a 200-word question, on a mid-range model, costs roughly a fraction of a cent. One million such exchanges costs thousands of dollars. That arithmetic matters quickly when you are building a product.

**Larger models cost more per token** because they require more compute to run. The tradeoff is not always worth it — for many tasks, a smaller, cheaper model is adequate, and the cost difference allows 10x more queries for the same budget.

*Memorable detail:* A simple-looking product can become unexpectedly expensive if the system prompt is 2,000 tokens, retrieval injects another 3,000 tokens of documents per request, and you have 100,000 users per day. You pay for every token the model reads — not just the clever sentence at the end of the prompt.

### Who can access what

Access to frontier AI tools is not uniform. Several axes constrain it:

**Geography and payment infrastructure.** Many frontier model providers are based in the United States and Europe. Payment via credit card or certain banking systems is required. Users in countries with limited credit card access or under payment-system restrictions face barriers that are invisible from within those markets.

**Language coverage.** High-resource languages work better. Users working in lower-resource languages — even in languages spoken by hundreds of millions of people — may see significantly worse quality, more hallucinations, and poorer cultural fit.

**Hardware requirements.** Open-weight models that run locally require capable hardware. A laptop with a current GPU is sufficient for smaller models; larger ones require dedicated workstations or cloud compute, which costs money and technical expertise.

**Organizational access.** Enterprise agreements with privacy guarantees, dedicated capacity, and regulatory compliance (like HIPAA in healthcare or GDPR compliance in Europe) are available — at prices that favor large organizations over individuals and small nonprofits.

None of this is a reason to avoid these tools. It is a reason to be honest about who "we" includes when people say "we all have access to this."

### Energy and environment: a proportionate view

Training a frontier model from scratch uses significant energy — comparable in some estimates to the annual electricity consumption of dozens of homes, or hundreds of round-trip transatlantic flights. This is a legitimate environmental concern.

Inference — each individual query — is much cheaper per request, but adds up at scale. A billion daily queries across a major consumer product is a non-trivial compute load.

The honest environmental stance for this book is: **awareness and proportionality, not performative guilt or greenwashing**. Use these tools where they provide genuine value. Support providers who are transparent about their energy use and working toward lower-carbon infrastructure. Avoid treating a one-time training cost as if it is incurred per query, and avoid treating per-query costs as negligible when running at scale.

### Quick takeaway

- Pricing is per token; larger models cost more; system prompts and retrieved documents contribute to cost.
- Access is uneven by geography, language, hardware, and organizational capacity — this matters for equity.
- Energy use from training is real; per-query use adds up at scale; proportionality beats theater in both directions.

---

## Try it

### Exercise 1 — Hallucination probe

Ask the model a question that has a specific, checkable answer — something like "Who won the [obscure award] in [specific year]?" or "What is the exact founding date of [small organization]?"

Find the actual answer through a search engine or official source. Compare:
- Was the model right or wrong?
- How did it sound? Confident or hedged?
- If it was wrong, was the wrong answer *plausible*? Would you have caught it without checking?

Bonus: ask the model to "cite sources" for its answer and check whether the citations are real.

### Exercise 2 — Strengths vs. limits

Pick one task the model does well for you and one it does poorly. Write one sentence for each explaining *why* the difference exists in terms of what you learned in Chapter 1 (pattern richness in training data). Avoid generic explanations like "AI is not perfect" — connect it specifically to the mechanism.

### Exercise 3 — Observe a bias default

Ask the model to write a short paragraph about a professional — a doctor, a lawyer, an engineer, a nurse, a teacher — without specifying any demographic details.

What defaults did it choose? Now ask again, explicitly specifying a demographic that goes against the common pattern (a female engineer, a male nurse, a young retiree). Does the model handle it naturally or introduce awkwardness?

You are not grading the model here. You are observing what the statistical defaults in training data look like.

### Exercise 4 — Cost intuition

Find the pricing page for a model API you might use. Calculate the approximate token cost for a workflow you actually do or are considering:

- How many input tokens per request (system prompt + context + question)?
- How many output tokens per response?
- How many requests would you run per day or month?

What is the estimated cost? Does that change which model you would pick?

---

*End of Part III. Previous: [Part II — How it works (without equations)](from-tokens-to-understanding-part-ii-how-it-works-without-equations.md) · Next: [Part IV — First steps with prompts](from-tokens-to-understanding-part-iv-first-steps-with-prompts.md) · Or [main volume](from-tokens-to-understanding.md).*