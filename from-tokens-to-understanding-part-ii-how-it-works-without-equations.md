# Part II — How it works (without equations)

*[From Tokens to Understanding](from-tokens-to-understanding.md) · Volume I*

---

Part I gave you **orientation**: vocabulary, history, and a clear line between fluency and truth. This part turns to **mechanics**—still without equations, but concrete enough that invoices, error messages, and model announcements make sense. You will see how raw text becomes **tokens**, how the model turns a prefix into **probabilities over the next token**, how **training and later tuning** shape behavior, and why **context length** is both a superpower and a hard ceiling.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 5–8.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Text as tokens | Why “token” is the unit of cost and memory, not always “word” |
| **2** | Prediction: the next piece of text | Next-token prediction, randomness, and misplaced confidence |
| **3** | Training and adaptation in one picture | From web-scale pretraining to chatty assistants—in one arc |
| **4** | Context windows and memory | What fits “in view,” and what to do when it does not |

**Contents (plain list — same as table):**

1. Text as tokens — cost and limits in tokens, not always words.  
2. Prediction: the next piece of text — sampling, temperature, confidence.  
3. Training and adaptation in one picture — pretraining to chatty assistants.  
4. Context windows and memory — finite “view,” forgetting in long chats.

---

## Chapter 1 — Text as tokens

Models do not read text the way humans do. They read **tokens**: pieces produced by a fixed procedure called a **tokenizer**. Getting comfortable with tokens saves you from surprises on your bill and from misunderstanding limits in the UI.

### Words, subwords, and strange splits

In English, a token is sometimes a whole word (`"hello"`), sometimes a fragment (`"ing"`, `"un"`). Rare or long words are often cut into several tokens. Punctuation and spaces usually cost tokens too; a newline may be its own token. Different products may use different tokenizers, so the **same sentence** can tokenize slightly differently across systems.

That matters because **price and limits are counted in tokens**, not in words or characters.

### Why the unit is “token,” not “word”

The tokenizer’s job is to turn any allowed text into a sequence of **integer IDs** from a finite vocabulary (often tens or hundreds of thousands of entries). The model’s first layers map those IDs to vectors the rest of the network can process. Using **subwords** keeps the vocabulary manageable: the model can represent rare words by **combining** pieces it has seen often.

You do not need to memorize how byte-pair encoding or SentencePiece work. You need the habit: **paste important text into a token counter** (many providers offer one) when length or cost matters.

### Tokens as the currency of limits

- **Context window** (Part II, Chapter 4) is measured in tokens: how much *input* the model can attend to at once.  
- **Output** is also generated token by token; long answers use more tokens than short ones.  
- **API pricing** is often per million input and output tokens.

So “one prompt” is not one fixed price. A verbose system prompt, a huge pasted PDF, and a chain of earlier messages all **eat the same budget**.

### A helpful analogy

Think of the tokenizer as a **reversible encoding** of text into a standard alphabet the model knows. It is not compression in the file-size sense, but it is **structured**: the model never sees raw bytes the way your editor does; it sees **IDs** that stand for learned pieces of text.

> **In this chapter.** Tokens are the model’s atoms of text; counts drive cost and limits; rare words may split into many tokens.

---

## Chapter 2 — Prediction: the next piece of text

At the core of autoregressive language modeling is a simple loop: given everything so far, assign a **probability** to each possible next token, **pick** one (or take the most likely), append it, and repeat. Everything else—chat tone, “reasoning,” code—is built on top of that loop.

### One step at a time

The model does not emit a full answer in a single gulp. It proposes **one** next token, then conditions the following step on the longer prefix—including the token it just wrote. That is why edits to **early** tokens can change **later** ones: the chain is causal.

### Creativity versus determinism

If the model always picked the single most likely next token, many answers would look repetitive and brittle. Real systems **sample**: they roll the dice using the probability distribution, with knobs—often called **temperature**—that make the distribution sharper (more deterministic) or flatter (more random).

- **Lower temperature**: safer, more “on distribution,” sometimes dull or overconfident in a narrow style.  
- **Higher temperature**: more variety—and more risk of nonsense or drift.

You do not need the formula. You need the idea: **randomness is a design choice**, not a sign of “thinking harder.”

### “Sounds sure” is cheap

The model is trained on mountains of text where confident explanations are common. Its objective rewards **plausible continuation**, not **verified fact**. So it can produce crisp, authoritative prose about things that are false or unknown—without a separate “I am guessing” module unless the system prompt or fine-tuning encourages that habit.

This is the same **fluency ≠ truth** lesson from Part I, now tied to **mechanics**: there is no step labeled “check against reality” inside the next-token loop.

> **In this chapter.** Generation is repeated next-token prediction with sampling; randomness is controlled, not magical; confidence in tone does not imply correctness.

---

## Chapter 3 — Training and adaptation in one picture

Commercial assistants are not only “big neural nets trained on the web.” They are usually **pipelines**: one or more stages after the first round of training teach the model to **follow instructions**, **refuse** some requests, and **match** a house style. You only need a **cartoon** of that pipeline to read announcements and model cards.

### Pretraining: learning language from data

**Pretraining** means training the model to predict tokens on a very large mix of text (and sometimes code). From that pressure alone, the system picks up grammar, facts that appear often in the data, style, and shallow reasoning patterns that show up in written explanations.

Pretraining is expensive and defines much of the model’s **raw capability** and **rough knowledge cutoff** (whatever the training snapshot contained).

### Teaching helpfulness and format

Raw pretrained models are often poor chat partners: they continue text like a book, not like an assistant. Later stages **narrow behavior**:

- **Instruction tuning** (supervised fine-tuning on demonstrations of questions and good answers) teaches format: answer the user, stay on topic, follow simple constraints.  
- **Preference tuning** (learning from human or AI preferences over pairs of answers) nudges the model toward answers people rate as better: clearer, safer, more helpful—by the raters’ lights.

You will see names like **RLHF**, **DPO**, **constitutional AI** in blog posts. For this book, they are all **post-pretraining alignment and style layers**—important, but not something you must implement to use an API well.

### Vocabulary: base, instruct, chat

- **Base** (or “foundation”) often means: after pretraining, **before** heavy chat-oriented tuning—powerful but awkward for dialogue.  
- **Instruction-tuned** / **chat** / **assistant** usually means: further training so the model **behaves** like a product you talk to.

When a provider “updates the model,” behavior can shift because **any** stage changed—not only pretraining.

> **In this chapter.** Pretraining builds broad language skill; later tuning shapes assistant behavior; “base” vs “chat” names real differences in the pipeline.

---

## Chapter 4 — Context windows and memory

The model has no invisible notebook. Everything it “knows” during a reply is whatever sits in the **context**: the tokens you send this turn (system prompt, prior turns, retrieved snippets—if the product adds them). That set is **bounded**.

### A fixed window

A **context window** (or **context length**) is a hard limit on how many tokens can be considered at once—input plus, in many setups, room reserved for the reply. If you exceed it, something must give: the oldest material may be **dropped**, or the request may be **rejected**.

Long documents, long chats, and fat system prompts compete for the same space. **Summarization**, **chunking**, and **retrieval** (choosing only relevant pieces to put in context) are not optional luxuries for serious work—they are strategies for staying inside the window. *From Prompts to Systems* develops those patterns; here, you only need the **constraint**.

### Conversations and “forgetting”

In a chat UI, earlier messages are often concatenated into the prompt each time. When the running total approaches the limit, the product may **truncate** from the top, **summarize** old turns, or ask you to start a new thread. None of that is human memory—it is **bookkeeping** in the prompt builder.

If something important happened twenty turns ago and fell out of the window, the model has **no access** to it unless you paste it back in or the system stores and re-injects it by design.

### Why this connects to cost

Longer context is not “free” for providers either: attention over many tokens costs compute. That is why **long-context** features may be priced differently or rolled out gradually.

> **In this chapter.** Context is finite; everything the model sees must fit in the window; long chats and long docs need deliberate strategies, not hope.

---

## Try it

1. **Token awareness.** Paste a paragraph you wrote (about 100–150 words) into your provider’s **tokenizer** or token counter, if available. Note approximate token count and one word that split into **multiple** tokens.

2. **Same prompt, two temperatures.** Ask a short creative question twice; if the UI exposes **temperature** or “more/less creative,” use low vs high. Compare: which answer would you **trust** for a fact, and which for brainstorming?

---

*End of Part II. Previous: [Part I — Finding your bearings](from-tokens-to-understanding-part-i-finding-your-bearings.md) · Next: [Part III — Capabilities and limits](from-tokens-to-understanding-part-iii-capabilities-and-limits.md) · Or [main volume](from-tokens-to-understanding.md).*
