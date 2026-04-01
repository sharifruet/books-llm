# Part I — Scale, data, and the pretraining stack

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

To understand why large models behave the way they do — why they are good at some things and brittle on others, why updates sometimes break behavior that was working, why two models with similar parameter counts can perform very differently — you need to understand how they are built. This part covers the scientific and engineering forces that shape modern foundation models: scaling trends, the data pipelines that feed them, the architecture decisions that have survived (and those that are being revisited), and the post-training stages that transform a raw base model into something a team can ship.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 1–4.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Scaling laws and predictable returns | How compute, data, and parameters interact; Chinchilla intuition; limits and domain shifts |
| **2** | Data at scale: curation, contamination, documentation | Web crawls, filtering, deduplication, leakage, datasheets |
| **3** | Architecture variants and inductive biases | Transformers, sparse MoE, long-context methods, state-space hybrids |
| **4** | Post-training: beyond next-token prediction | Instruction tuning, preference optimization, multistage pipelines |

**Contents (plain list — same as table):**

1. Scaling laws — compute-optimal allocation and the limits of power laws.
2. Data at scale — curation, deduplication, contamination, documentation.
3. Architecture variants — transformers, MoE, long-context, state-space models.
4. Post-training — SFT, RLHF/DPO, iterative pipelines.

---

## Chapter 1 — Scaling laws and predictable returns

**A scaling curve is not a roadmap — it is a measurement of what happened under specific conditions, not a promise about what will happen under yours.**

When researchers discovered that language model performance follows smooth power-law relationships — that loss decreases predictably as you increase model size, training data, or compute — it was genuinely exciting. You could, with some care, extrapolate the training loss of a model you had not built yet. You could allocate compute budgets with something better than intuition. The field found a kind of empirical physics for model behavior.

### The Chinchilla result

For most of the early scaling era, larger models were the goal: given a fixed compute budget, use it to train the biggest model you could afford, even if that meant training it on relatively little data. The Chinchilla research (Hoffmann et al., 2022) challenged this by asking: for a fixed compute budget, what is the optimal allocation between model size and training tokens?

The answer was roughly: balance them. Earlier large models were undertrained — too many parameters, not enough tokens. A smaller model trained on more data could match or exceed a larger undertrained model at the same compute cost, and at lower inference cost (since it is smaller).

The practical implications:
- **Compute-optimal training** means running more epochs or collecting more data, not just building a bigger model.
- **Inference economics** matter at planning time. A smaller, well-trained model costs less to serve for every query after training.
- **The specific ratios vary** — the Chinchilla numbers are not universal constants. Recipe, architecture, data domain, and objectives all affect the optimal balance.

Use Chinchilla intuitions as *planning tools*, not commandments. The most important insight is the principle: do not assume that scale in one dimension (parameters) substitutes for scale in another (data).

### Power laws and their limits

Scaling laws describe relationships within a training setup, held roughly constant:
- Same architecture family
- Same data distribution
- Same training objective
- Similar hyperparameter tuning

Change any of these and the curve shifts. This matters because:

**Domain shift breaks naive extrapolation.** A scaling law measured on general web text does not tell you how much data or compute you need for a code model, a biomedical model, or a multilingual model. The domain-specific distribution determines what the model learns from each token.

**Data quality beats raw token count at domain boundaries.** A model trained on 10 billion carefully curated legal documents may outperform one trained on 100 billion noisily filtered general-purpose tokens on legal tasks. The loss curves will not tell you this.

**Benchmark saturation distorts scaling plots.** When a benchmark approaches ceiling performance, the apparent scaling benefit disappears — not because scaling stopped working, but because the metric stopped resolving differences. Scaling results cited on saturated benchmarks are noise.

**Inference and alignment costs may dominate product economics.** Even when training scales efficiently, the cost per query at inference time and the engineering cost of aligning the model for deployment may dwarf training costs once a model is serving millions of users. Scaling training is only part of the cost picture.

*Friction:* "We trained a bigger model" is sometimes a response to what is actually a distribution shift problem, a data quality problem, or a post-training problem. Scaling cannot apologize for the wrong data.

### What scaling laws are actually useful for

Scaling laws give you:
- A principled way to allocate compute between model size and training tokens.
- A way to predict approximate loss at scale before committing a large experiment.
- A framework for understanding why some approaches work better at large scale than small scale (and vice versa).

They do not give you:
- Guarantees about specific downstream task performance.
- Transfer across data distributions.
- Predictions about emergent capabilities that do not appear in the loss curve.

### Takeaway

- Scaling laws are empirical tools for planning experiments and allocating compute — not universal constants.
- Chinchilla-style intuition: for a fixed compute budget, balance model size and training tokens.
- Domain shift, data quality, benchmark saturation, and inference economics all break naive scaling extrapolations.
- Measure on your task and distribution; do not assume the scaling curve generalizes.

---

## Chapter 2 — Data at scale: curation, contamination, and documentation

**The quality of a foundation model is bounded by the quality of its training data, but "quality" is not a single axis.**

Pretraining a large language model requires data at a scale that makes careful hand-curation impossible. Common English web crawls run to trillions of tokens. The practical question is not "curate everything manually" but "which automated and semi-automated filtering decisions produce a training distribution that leads to capable, reliable, and safe model behavior?"

### The web crawl pipeline

Most large language models are pretrained on derivatives of web crawls (Common Crawl being the most common source), typically combined with curated corpora — books, scientific papers, code repositories, Wikipedia, and licensed datasets. The pipeline from raw crawl to training tokens involves:

**Language filtering.** Identifying and selecting (or weighting) languages. Most pipelines use fastText or similar classifiers. Choice of target languages and their balance shapes multilingual capability significantly.

**Quality filtering.** Removing low-quality content: spam, auto-generated SEO text, very short or very long documents, content with high repetition rates, non-natural-language content. Quality classifiers are often bootstrapped from curated high-quality sources — scoring documents by their similarity to good reference corpora.

**Deduplication.** Exact and near-duplicate removal. This matters for at least two reasons: exact duplicates inflate the effective weight of specific facts and phrasing, and contamination detection (covered below) requires knowing whether benchmark text appeared in training. Near-dedup typically uses MinHash or similar locality-sensitive hashing.

**Toxicity and PII filtering.** Removing or downweighting content that contains slurs, harassment, explicit content, or personally identifiable information. These decisions are imperfect — aggressive filtering removes relevant content, and no filter catches everything.

Each of these decisions involves tradeoffs. Aggressive deduplication can remove useful repetition (concepts that appear frequently benefit from that frequency). Aggressive quality filtering can skew rare languages and domains that produce less English-like writing styles. The pipeline encodes values, whether the team intends it to or not.

### Contamination and benchmark integrity

**Test-set contamination** is the accidental (or deliberate) inclusion of benchmark evaluation examples in training data. When benchmark text appears in the crawl and the model was trained on that crawl, the model has effectively seen the "exam questions" during training. Reported performance on that benchmark is now a measure of memorization, not generalization.

Contamination is hard to detect definitively and easy to overlook. Common signals:
- Performance on a new benchmark is suspiciously higher than closely related tasks.
- The training cutoff predates the benchmark release but the crawl was assembled later.
- Performance drops when evaluated on held-out variations of the benchmark.

Responsible reporting includes a contamination analysis — checking whether benchmark text overlaps with training data — and should be cited when interpreting published results. Benchmarks released after a training cutoff are more trustworthy, but not immune to contamination from later model versions trained on more recent data.

*Memorable detail:* leaderboard jumps have occurred when benchmark text was in the crawl — not because the model "understood" more, but because the exam was accidentally open-book. The model was not cheating intentionally; the pipeline just failed to exclude it.

### Data documentation: datasheets and data statements

**Datasheets for datasets** (Gebru et al., 2018) proposed that datasets should include structured documentation of their motivation, composition, collection process, preprocessing steps, intended uses, and limitations — analogous to product documentation for manufactured components. The concept has been widely endorsed and inconsistently adopted.

For foundation models, meaningful data documentation should include:
- **Provenance**: Where did the data come from? What sources were included and excluded?
- **Time range**: What is the training data cutoff? What temporal biases might this introduce?
- **Language and domain distribution**: How are different languages, registers, and domains represented?
- **Filtering decisions**: What content was removed, and by what criteria?
- **Known limitations and biases**: What groups or topics are underrepresented or skewed?

This documentation is not just for academic completeness. It shapes what practitioners can trust the model to know, where its knowledge cuts off, which domains require supplementary retrieval or fine-tuning, and where claims about model behavior should be interrogated rather than accepted.

*Anchor:* A model's capabilities and biases are downstream of its training data. Understanding the data is part of understanding the model.

### Takeaway

- Web-scale data pipelines involve quality filtering, deduplication, toxicity filtering, and language selection — each a value-laden decision.
- Contamination of benchmark test sets in training data distorts evaluation results. Check for it; report it.
- Datasheets and data documentation are not bureaucracy — they are the infrastructure for honest evaluation and responsible deployment.
- Data quality and distribution matter as much as raw token count for domain-specific capabilities.

---

## Chapter 3 — Architecture variants and inductive biases

**The transformer architecture has dominated language modeling for several years, but "transformer" covers a wide range of variants, and several competing families have developed strong arguments in specific niches.**

Understanding architectures at survey depth — knowing what problem each family addresses and what it trades off — matters for evaluating model releases, understanding capability claims, and making decisions about which model families to build on.

### The transformer baseline

The standard transformer for language modeling uses a decoder-only architecture with causal (autoregressive) attention: each token attends to all previous tokens in the sequence. Key components:

- **Self-attention**: Each token position computes a weighted sum over all previous positions. This is what enables long-range dependency modeling — a word at the end of a paragraph can directly attend to relevant context at the beginning.
- **Feed-forward layers**: Dense transformations applied at each position independently. These have been shown to store factual knowledge and perform position-wise computations.
- **Layer normalization and residual connections**: Stabilize training and enable the deep stacking of many layers.

The computational cost of attention is quadratic in sequence length — a 10x longer sequence requires 100x more attention computation. This is manageable for typical context lengths but becomes a constraint for very long contexts.

### Mixture-of-experts (MoE)

Instead of activating all model parameters for every token, a MoE architecture routes each token to a subset of "expert" feed-forward layers. A small router network decides which experts are active. This allows a model to have a much larger total parameter count (and therefore more total capacity) while activating only a fraction of parameters per forward pass.

The appeal: you can scale total capacity without scaling per-token compute proportionally. The costs: routing overhead, expert load balancing (preventing all tokens from routing to the same few experts), and increased complexity in distributed training.

*Direct address:* When a model release says "2 trillion parameters, activates 220 billion per token" — that is a MoE model. Total parameters and active parameters are different numbers, and both matter for different reasons.

### Long-context methods

Extending the effective context window beyond the length models were trained on requires attention to several problems:

**Positional encoding generalization.** Most transformers encode position with learned or fixed embeddings that may not generalize to positions beyond those seen in training. Techniques like RoPE (rotary position encoding) and ALiBi provide better length generalization, and are now standard in most large models.

**Attention approximations.** For very long contexts, full quadratic attention becomes prohibitively expensive. Approaches include sliding window attention (attending only to nearby tokens), sparse attention patterns (learned or fixed masks), and linear approximations to attention.

**KV cache pressure.** Long contexts require storing large key-value caches during inference (see Part III for detail). This creates memory constraints that affect deployment choices independent of training context length.

### State-space models and hybrids

State-space models (SSMs), particularly the Mamba architecture and its descendants, offer a different approach to sequence modeling: instead of attention, they use recurrent state transitions that scale linearly in sequence length. For long sequences where full attention is expensive, SSMs can be more efficient.

The trade-offs: SSMs process the sequence recurrently and do not have full access to arbitrary earlier positions in the way attention does. This may affect performance on tasks that require attending to very specific positions from early in a long context. Hybrid architectures that combine attention layers with SSM layers attempt to capture both strengths.

### Scale vs prior

An important question for any architecture decision: is a capability the result of scale, or is it built in by architecture and objective choice?

Some capabilities improve predictably with scale in a given architecture. Others are more dependent on architecture design — long-range coherence, for example, depends significantly on how attention is designed. Separating scale effects from architectural priors requires controlled comparisons that vary one dimension at a time, which is expensive and rarely done cleanly in practice.

*Anchor:* Architecture debates are interesting in research. In practice, the question is what measures move on your workload. Evaluate, do not just logos.

### Takeaway

- Decoder-only transformers remain the dominant architecture for language modeling. Most frontier models are variants of this family.
- Mixture-of-experts enables larger total capacity at similar per-token compute; introduces routing complexity.
- Long-context methods (positional encoding, attention approximations) extend usable context but involve tradeoffs.
- State-space and hybrid architectures offer efficient long-context processing; trade-offs in retrieval from arbitrary positions.
- Architecture is a lever; empirical evaluation on your workload is the arbiter.

---

## Chapter 4 — Post-training: beyond next-token prediction

**Pretraining produces a model that is very good at predicting the next token in text that looks like the internet. That is not the same as a model that is helpful, honest, and safe to deploy.**

The post-training pipeline is what transforms a base model into something aligned with user expectations and organizational requirements. It is also where many of the failure modes that practitioners encounter are introduced — and where mitigations can be applied.

### Instruction tuning (supervised fine-tuning)

The first post-training stage for most deployable models is supervised fine-tuning (SFT) on demonstrations of desired behavior. A dataset of (instruction, response) pairs is used to fine-tune the base model so that it follows instructions, responds in dialogue format, and handles common task types.

SFT teaches:
- **Task format**: How to interpret user instructions and structure responses.
- **Dialogue conventions**: Turn-taking, conversation context, how to ask for clarification.
- **Basic refusals**: How to decline obviously harmful requests.

SFT does not fundamentally change what the model knows — that came from pretraining. It changes how the model expresses and applies that knowledge in response to instruction. A model that learned about chemistry during pretraining will still know chemistry after SFT; SFT affects whether it presents that knowledge helpfully, in response to requests, in an appropriate format.

*Important nuance:* Over-tuning on SFT data can lead to "format lock" — the model applies the patterns from the demonstrations even when they do not fit, producing verbose, formulaic responses that hit the template but miss the point.

### Preference optimization

After SFT, models still exhibit behaviors that are subtly wrong: sycophancy (agreeing with users rather than giving accurate information), over-refusal (declining reasonable requests), under-refusal (agreeing to requests they should decline), verbosity, and inconsistency.

**RLHF (reinforcement learning from human feedback)** addresses this by:
1. Collecting human preferences: presenting raters with pairs of model outputs and asking which is better.
2. Training a reward model on these preferences.
3. Using reinforcement learning to fine-tune the policy model to maximize the reward model's score.

**DPO (direct preference optimization)** achieves a similar goal without a separate reward model training stage, by directly optimizing a policy that prefers the "chosen" response over the "rejected" response from the preference dataset.

Both approaches have important limitations:
- **Goodhart's Law**: The model learns to maximize what the reward model measures, which is a proxy for human preference. If the proxy is wrong (e.g., the reward model prefers verbose responses), the model learns to be verbose.
- **Sycophancy as reward hacking**: Human raters often prefer confident, agreeable responses. Models trained to maximize preference scores may learn to be agreeable rather than accurate.
- **Distribution sensitivity**: Preference optimization on one distribution of prompts may not generalize well to different prompt distributions.

*Tiny vignette:* "One more epoch of SFT does not fix a preference-stage failure." If a model is sycophantic, that is usually a preference optimization problem — it learned that agreeable responses score well. Adding more SFT data about being honest does not fix the reward signal that incentivizes agreement.

### Multistage pipelines and iterative refinement

Modern post-training pipelines are not single-stage. A typical sequence:

```
Pretraining
    ↓
SFT (instruction format, basic alignment)
    ↓
Preference optimization (RLHF or DPO)
    ↓
Evaluation gate (quality + safety thresholds)
    ↓
Optional: iterative rounds with updated feedback data
    ↓
Deployment
```

Each stage can shift both capabilities and failure modes. Changes introduced by SFT can interact with preference optimization in unexpected ways. Capability improvements from a pretrained model can regress after post-training if the post-training data is distribution-mismatched.

The practical implications:
- Post-training is not a one-time step — it is an ongoing process as model behavior is monitored and feedback loops close.
- Changes in one stage can have downstream effects in later stages.
- Behavioral regression (something that worked in the base model breaking after SFT) is a real phenomenon that requires careful evaluation.

### Why this matters for practitioners

Understanding the post-training pipeline explains several behaviors that are otherwise mysterious:
- Why models sometimes become *more* cautious and *less* capable after a safety update (over-refusal from miscalibrated preference optimization).
- Why a model is confident but wrong (training on human preferences rewards confidence; being wrong is less penalized than being uncertain).
- Why the same factual question gets different answers depending on how it is framed (SFT taught format templates; a different framing may not trigger the helpful template).
- Why jailbreaks work (they bypass the triggers the SFT and preference optimization stages conditioned on).

### Takeaway

- Instruction tuning (SFT) teaches task format and dialogue conventions; it does not fundamentally change what the model knows.
- Preference optimization (RLHF, DPO) nudges outputs toward human-preferred behavior; vulnerable to reward hacking and proxy failure.
- Post-training is multistage and iterative; changes in one stage affect downstream stages.
- Many observable model behaviors — sycophancy, over-refusal, format lock — are post-training artifacts, not fundamental properties of the architecture.

---

## Try it

### Exercise 1 — Scaling intuition

Explain in two sentences why doubling model parameters without increasing training data may not follow the same scaling curve as a compute-optimal policy. Then extend it: if you were planning a domain-specific model (e.g., legal text, biomedical literature), which factor would you be most uncertain about in a scaling estimate for your domain? Why?

### Exercise 2 — Contamination audit

Pick a benchmark commonly cited in model release announcements. Identify one property of that benchmark that could lead to contamination in a training crawl assembled before the benchmark was released — and one way a research team could reduce that risk in how they report results.

### Exercise 3 — Post-training failure mode

Choose one post-training failure mode (sycophancy, over-refusal, format lock, reward hacking) and trace it back to its most likely training-pipeline cause. Describe one evaluation you could run to detect it in a model you are using. What would a passing response look like, and what would a failing response look like?

### Exercise 4 — Architecture tradeoff

A team is building a customer support system that needs to handle very long conversation histories (50+ turns). They are considering three options: a standard transformer with a 128k token context window, a MoE model with a shorter context window, and a hybrid attention/SSM model. For each option, name one advantage and one risk specific to the long-conversation use case. Which would you start with, and why?

---

*End of Part I. Previous: [From Prompts to Systems — Volume II](../from-prompts-to-systems/from-prompts-to-systems.md) · Next: [Part II — Alignment, safety, and robustness](from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) · Or [main volume](from-models-to-frontiers.md).*
