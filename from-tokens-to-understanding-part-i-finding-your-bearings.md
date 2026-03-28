# Part I — Finding your bearings

*Sharif Uddin*

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

Before you touch a chat window or an API, it helps to know **what you are looking at**. This part sets expectations: how the trilogy is meant to be read, how “AI” and “machine learning” relate to language models, what an LLM actually *is* (and what it only resembles), and how we got from simple word counts to the large models people talk about today. None of that requires equations—only patience and a willingness to separate **fluency** from **truth**.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 1–4.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | How to use this book | Scope of this volume, pace, and study habits |
| **2** | AI, machine learning, and language models | Vocabulary for the landscape; why language modeling is different |
| **3** | What an LLM is—and what it is not | Mechanics in one picture; common misconceptions |
| **4** | A short history to the present | N-grams → neural nets → transformers → scale, intuitively |

**Contents (plain list — same as table, for readers or tools that do not render tables well):**

1. How to use this book — scope, pace, study habits.  
2. AI, machine learning, and language models — vocabulary; why language is a different prediction problem.  
3. What an LLM is—and what it is not — statistical model; not a DB, person, or web search by default.  
4. A short history to the present — n-grams through scale, intuitively.

---

## Chapter 1 — How to use this book

This volume is a **map**, not a sprint. It exists to give you a stable picture of what large language models are, what they are good for, and where they fail—so you can use them without treating polished prose as proof.

### What you will find here

You get short explanations in plain language; mental models you can reuse when reading the news or a product page; prompts you can try in any major chat assistant; and steady reminders about privacy, bias, and verification. Where a topic really needs a full course—calculus, distributed training, alignment theory—this book **points forward** to *From Prompts to Systems* and *From Models to Frontiers* instead of cramming everything into a single chapter.

### What you will not find here

Do not expect step-by-step **training** of a model from scratch; formal **derivations** of loss functions or attention; a **complete architecture survey**; or **vendor-specific** walkthroughs that go stale when a settings screen moves. Those belong in courses, documentation, or the later volumes, depending on depth.

### How to read and practice

Work in **short sessions**: read a section, pause, then try **one** thing—a single prompt, or checking a claim against another source. When the book suggests an exercise, treat it as optional but **useful**; “muscle memory” for how models behave beats skimming.

Keep a **scratch file** (paper or digital) for prompts that worked, terms you looked up, and questions to carry into Volume II. When you pick the book up after a break, skim the **contents** at the start of each part so you remember where you are in the arc: orientation, then mechanics, then responsibility.

> **In this chapter.** You now know what this volume promises, what it deliberately omits, and a sustainable way to read it.

---

## Chapter 2 — AI, machine learning, and language models in plain language

Headlines use “AI” to mean many different things. Sorting the vocabulary early saves confusion later.

### Artificial intelligence and machine learning

**Artificial intelligence** is a broad label: systems that do tasks we associate with human judgment—classifying, ranking, generating, planning—often under uncertainty. Not every AI system **learns from data**. A chess engine built from hand-written rules (“if the opponent does X, play Y”) counts as AI in a loose sense, but it does not *learn* from examples the way modern models do.

**Machine learning** means adjusting a system using **data** so that its performance on a task improves without someone coding every special case. You supply inputs (and usually desired outputs); the system finds **patterns** that generalize to new inputs. That process is **statistical**: it works when training data resembles what you will see in deployment, and it can fail when the world shifts or the data is skewed or biased.

### Why language is a different kind of problem

Many tasks attach **one label** to **one object**—for example, an image gets “cat” or “dog.” Language does not work that way. Text unfolds **one piece at a time** in a huge space of possible continuations, and meaning depends on **context**: earlier words in the sentence, the document, or the conversation.

A language model is therefore not merely classifying; it is **modeling a distribution** over sequences—what word or fragment is plausible next, given what came before. That is why **local** coherence can be so strong: the model is very good at continuing in a way that *sounds* right.

It does **not** follow that the model has **beliefs**, a **memory of facts**, or **direct access to the world** the way a person does. Those are separate questions, taken up in the next chapter.

### Where LLMs sit among other tools

The same broad ML ideas show up across domains:

- **Vision** models map images or video to labels, boxes, or captions.  
- **Speech** systems map audio to text, or text to speech.  
- **Robotics** often combines perception, planning, and control.

A **large language model** focuses on **text** (and in multimodal systems, text *together with* other inputs—but this volume starts from the text core). When headlines say “AI” in **recent years**, they often mean an LLM, or a product that **wraps** an LLM with search, tools, or other components. Keeping those layers distinct saves you from expecting one stack to solve every problem.

> **In this chapter.** AI is a wide umbrella; machine learning learns patterns from data; language modeling is sequential and contextual; LLMs are one powerful species in a larger zoo.

---

## Chapter 3 — What an LLM is—and what it is not

Once the vocabulary is in place, you can state plainly what “LLM” names—and what it does **not** name.

### What the acronym names

In the usual technical sense, a **large language model** is a **learned function** that assigns probabilities to possible next pieces of text (**tokens**), given everything you have fed it so far. **Large** refers to scale—billions of parameters is unremarkable now—which affects capability and cost, but the core idea remains **conditional probability over sequences**.

### What it is

An LLM is a **statistical model of language**. It absorbs regularities in how people write—grammar, tone, genre, argument shape, code formatting—because it was trained on enormous amounts of text. When you “ask a question,” you supply a **prefix**; the model continues in ways that *look* like plausible answers in that situation. That behavior is useful for drafting, brainstorming, rephrasing, and exploring ideas—when you treat it as assistance, not oracles.

### What it is not

**Not a database of facts.** The model does not “look up” your answer in a table of truths. If something *like* lookup happens, it is because a **separate** system—retrieval, tools, browser integration—was added on purpose. Even then, the LLM can misread or blend what it receives.

**Not a person.** It has no life history, no conscience, and no human accountability. Calling it “she,” “he,” or “they” is a metaphor for conversation design, not a claim about inner life.

**Not the open web by default.** A standard chat model’s factual picture is **frozen** at training time (with a stated knowledge cutoff) unless the product adds **live** retrieval. Treat “searching the web” as a **feature**, not a property of “being an LLM.”

Mixing up these roles—oracle, friend, search engine—invites **over-trust**.

### Why fluent text can still be wrong

The model is trained to produce answers that *look like* good answers: clear structure, confident tone, plausible detail. None of that requires the content to be **true**. A false statement can be dressed in the same statistical clothing as a true one.

There is no internal guarantee that output matches reality—only that it resembles answers common in training. Later parts of Volume I return to **hallucination**, **verification**, and **when not to use** a model at all.

> **Remember.** Fluency is a style; truth is a separate question. **Fluency ≠ truth.**

---

## Chapter 4 — A short history to the present

You do not need to be a historian to use a model today. You *do* need a rough sense of why the last decade felt like a step change—which this chapter supplies in broad strokes, without architecture deep dives.

### N-grams: statistics over short spans

Before modern deep learning, the simplest language models were **n-grams**: counts of short word sequences in a corpus. If “the cat sat on the” appears constantly, “mat” gets a higher score than “theorem.” That works for spell-checking and crude autocomplete and is easy to reason about.

N-grams **do not generalize** well. They struggle with rare phrases, with long-distance dependencies (“the scientist … later … proved the conjecture”), and with anything that depends on **meaning** beyond nearby word habits.

### Neural language models: learned context

**Neural** models replaced giant tables of counts with **learned representations**. Words become vectors in a high-dimensional space; the network learns which contexts cluster together. Similar words **share** statistical support, which helps fluency and rare words.

For a long time, though, models were **small** by current standards, and capturing very long structure remained difficult.

### Transformers, attention, and depth

**Transformers** with **attention** made it practical to stack many layers and train on parallel hardware. A usable mental image of attention: when predicting the next token, the model learns **which earlier tokens to weight heavily**. That supports **much longer context**—thousands of tokens in mature systems.

The exact wiring matters for specialists. For this book, the important part is the **consequence**: researchers could add **data**, **compute**, and **parameters** and often see **smooth gains** in capability—until they hit data, compute, or fundamental limits.

### Scale and what changed in practice

As models moved from millions toward **billions** of parameters and trained on large slices of public text, they began to **imitate** not only grammar but **genres**: explanations, code, dialogue, translation. Behaviors that look like “following instructions” or “sketching a proof” emerged **without** hand-written rules for each trick.

That does **not** mean the system **understands** in a human sense. It means that the training objective, at sufficient scale, encourages **broad statistical mimicry** of human text—including text that *looks* expert.

The next parts of Volume I leave history behind and turn to **mechanics**: tokens, prediction step-by-step, and context windows—so you can use that mimicry without mistaking it for magic, or for a promise of correctness.

> **In this chapter.** Local word statistics gave way to neural sequences, then to deep attention-based models at scale. Scale unlocked surprising mimicry; it did not quietly solve truth or meaning.

---

## Try it

1. **Book vs oracle.** In any chat tool, ask: *Explain in three bullets what this book says an LLM is not (database, person, web search).* Compare the answer to Chapter 3 of this part. Note anything the model **added** that the book did not claim.

2. **Fluency check.** Ask the model for a **specific fact** you can verify in two minutes (e.g. a date, a citation, a number). Verify it elsewhere. If it was wrong, rewrite one sentence you will remember: what went wrong?

---

*End of Part I. Previous: [main volume — introduction](from-tokens-to-understanding.md) · Next: [Part II — How it works (without equations)](from-tokens-to-understanding-part-ii-how-it-works-without-equations.md).*
