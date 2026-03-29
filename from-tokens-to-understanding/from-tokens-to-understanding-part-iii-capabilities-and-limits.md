# Part III — Capabilities and limits

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

You now have a workable picture of **how** a model generates text. This part turns outward: **what these systems are genuinely useful for**, where they **fail or mislead**, how **social bias** shows up in outputs, and what **speed, money, and access** mean in practice. The aim is proportion: neither hype (“it can do anything”) nor blanket dismissal (“it is only autocomplete”). You leave ready for Part IV’s hands-on prompting—and for Volume II’s deeper treatment of evaluation and deployment.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 9–12.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | What LLMs tend to do well | Real strengths—without mistaking fluency for reliability |
| **2** | Hallucinations, mistakes, and calibration | Why errors look credible; how to probe and verify |
| **3** | Bias, stereotypes, and fairness | Where skew comes from; why “fixing” it is hard |
| **4** | Speed, cost, access, and the environment | Who can use what, why price varies, a sober footprint note |

**Contents (plain list — same as table):**

1. What LLMs tend to do well — strengths without mistaking fluency for reliability.  
2. Hallucinations, mistakes, and calibration — credible errors; verification.  
3. Bias, stereotypes, and fairness — skew; why fixes are hard.  
4. Speed, cost, access, and the environment — pricing, access, energy in proportion.

---

## Chapter 1 — What LLMs tend to do well

Large language models are not equally good at every task. Their strengths line up with **pattern-rich text**: language, format, and shallow structure that appears often in training data. Knowing the sweet spots helps you **delegate** the right work to the model—and reserve human judgment for the rest.

### Drafting, brainstorming, and rephrasing

When you need **many candidate wordings**—email tones, headlines, outlines, alternate explanations—a model can accelerate iteration. It is often strong at **following format**: bullet lists, tables (as text), simple templates, “make this shorter,” “make this more formal.” That is **stylistic and structural** help, not a guarantee that the *content* is accurate for your domain.

### Format-following and light structure

Models that have seen huge amounts of code and markup often produce **plausible-looking** snippets: JSON-shaped objects, small functions, configuration examples. Treat these as **sketches** to be checked in a compiler, linter, or runtime. The same goes for legal or medical *style*: the format may look right while the substance is wrong.

### Simple coding and shell sketches

For **boilerplate**, common APIs, and debugging hints (“what might this error mean?”), LLMs can save time—especially when you already know enough to **spot** mistakes. They are weaker when the problem is **novel**, requires **exact library versions**, or depends on **unstated constraints** in your codebase.

### Multilingual exposure (with caveats)

Training data includes many languages, so models can **translate**, **summarize**, or **chat** in languages beyond English—unevenly. High-resource languages often work better; low-resource or dialectal settings may see more errors or **cultural blind spots**. Do not assume parity with a professional translator or a fluent human editor.

### The recurring theme

These strengths are **assistive**. They are most valuable when a human—or a separate verification step—can catch errors before they matter.

> **In this chapter.** LLMs shine at language-heavy, pattern-rich tasks: drafting, reformatting, brainstorming, and rough code—always subject to review when stakes rise.

---

## Chapter 2 — Hallucinations, mistakes, and calibration

A **hallucination** in common usage means: the model asserted something **specific** (a fact, a citation, a number) that is **false or unsupported**—often while sounding confident. Understanding *why* this happens keeps you from “prompt engineering” your way to perfect truth.

### Confident errors

The training objective rewards **plausible** continuation. Explanations in the training data often sound sure. So the model can produce **well-phrased nonsense**: fake studies, wrong dates, made-up URLs, or subtle numerical slips. This is not a occasional bug; it is a **structural** risk of unconstrained generation.

### When to verify from another source

Verify **whenever** mistakes would hurt someone: health, money, law, reputation, safety. Verify **before** you repeat a claim in public or in code you ship. Primary sources, official documentation, and subject-matter experts still matter. The model is a **starting point**, not an authority.

### Asking for uncertainty (and its limits)

You can ask the model to **flag uncertainty**, **list assumptions**, or **avoid inventing citations**. That sometimes helps; it is not reliable. The model can say “I might be wrong” and still be wrong, or sound tentative while fabricating. **Prompting** cannot replace **checks** on high-stakes facts.

### Citations and “look it up”

If you ask for references, you may get **plausible-looking** titles and authors that do not exist or do not say what the model claims. Unless the system is **wired to retrieval** (search, databases) and you trust that pipeline, treat citations as **suggestions to verify**, not proof.

### A useful habit

Separate **form** from **substance**. The model may produce beautiful structure around empty or false content. Your job is to supply **substance**—or to validate it elsewhere.

> **In this chapter.** Hallucination is confident-sounding error; prompts alone do not fix it; verify when it matters, and never trust ungrounded citations.

---

## Chapter 3 — Bias, stereotypes, and fairness (introduction)

Language models learn from **human-generated** text—books, forums, code, social media. That corpus encodes **biases** of many kinds: stereotypes about groups, uneven representation, historical prejudice, and gaps in whose voices were written down. The model can **reproduce** or **amplify** those patterns, even when later tuning tries to suppress the worst outputs.

### What “bias” means here

In this chapter, **bias** means **systematic skew**: answers that favor one demographic, language variety, or worldview over others without justification; or that **erase** or **caricature** people. It is not the same as having an opinion in a debate—it is about **unfair or harmful regularities** in behavior.

### Harmful or skewed outputs

You may see **stereotyping**, **denigration**, or **overconfidence** about groups the training data treated badly. Safety layers in products **reduce** but do not **eliminate** these failures; adversarial prompts, edge cases, and multilingual settings still surface problems.

### Why “fixing” this is an open challenge

**Technical** fixes—filtering data, fine-tuning on “good” answers, classifiers—help but trade off with other goals (accuracy, nuance, free expression) and can **shift** bias rather than remove it. **Social** questions—who decides what is fair, in which culture—do not have single engineering answers.

Later volumes return to **evaluation**, **alignment**, and **governance**. For now: **notice** when outputs feel off; **do not** treat the model as a neutral arbiter of people or history.

> **In this chapter.** Training data carries society’s biases; models can echo them; mitigation is partial; fairness is partly technical, partly social—and unfinished.

---

## Chapter 4 — Speed, cost, access, and the environment

Capability is not the only axis. **Latency** shapes user experience; **price** shapes who can build what; **access** shapes who benefits from the technology. A short, honest look avoids both **mystery** and **moral theater**.

### Free tiers, APIs, and “bigger costs more”

Many vendors offer **free** or **cheap** tiers for small usage. Serious volume usually means **paid APIs** or **enterprise** contracts. Pricing is often **per token** (Part II): longer prompts and longer answers cost more. **Larger** models generally cost more per token than **smaller** ones; **long-context** or **premium** features may carry a surcharge.

Rough intuition: you pay for **compute** the provider spends to serve you—plus their margin, support, and compliance overhead.

### Who can access what

Access varies by **region**, **payment method**, **organization type**, and **policy** (e.g. age limits, acceptable-use rules). Open-weight models and local inference change the picture: more **control** and **privacy** for those with the **hardware** and skills to run them—still not equally distributed.

Do not assume everyone has the same chatbot, the same model version, or the same legal context.

### Environment and energy (in proportion)

Training large models from scratch uses **a lot** of energy; **inference** (each query) uses less per request but adds up at scale. Exact numbers depend on **hardware**, **utilization**, and **electricity mix**; beware headlines that compare “one chat” to exotic units without context.

The balanced stance for this book: **awareness**, not performative guilt or greenwashing. Efficiency matters; so do **useful** applications and **who** gets to define tradeoffs.

> **In this chapter.** Cost tracks tokens and model size; access is uneven; environmental impact is real and context-dependent—worth knowing, not obsessing over without numbers.

---

## Try it

1. **Hallucination probe.** Ask the model for a **very specific** fact (invent a constraint: “the exact founding year of a small organization you can look up”). Verify online. If wrong, note the **tone** of the wrong answer—confident or hedged?

2. **Strengths vs limits.** Pick one task the model does **well** (e.g. rewrite a paragraph) and one it does **poorly** for you (e.g. exact arithmetic). Write one sentence each: *why* the difference, in terms of this part.

---

*End of Part III. Previous: [Part II — How it works (without equations)](from-tokens-to-understanding-part-ii-how-it-works-without-equations.md) · Next: [Part IV — First steps with prompts](from-tokens-to-understanding-part-iv-first-steps-with-prompts.md) · Or [main volume](from-tokens-to-understanding.md).*
