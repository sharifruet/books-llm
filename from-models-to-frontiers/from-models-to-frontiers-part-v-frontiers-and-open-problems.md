# Part V — Frontiers and open problems

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

The frontier is not only a line where capabilities end. It is also where evaluation fails to keep pace with capability, where scientific explanations lag behind empirical observations, and where honest researchers say "we do not know." This final part covers evaluation at the frontier, the open problems that matter, and how to read a fast-moving field without either being swept away by hype or missing genuinely important progress.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 15–17.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Evaluation at the frontier | Capability vs. process evaluation; dynamic benchmarks; what leaderboards cannot tell you |
| **2** | Open research directions | Reasoning, continual learning, world models, human-AI collaboration |
| **3** | Reading the field and closing the trilogy | arXiv hygiene, sustainable curriculum, what the three volumes built |

**Contents (plain list — same as table):**

1. Evaluation at the frontier — benchmarks, process evaluation, societal lens.
2. Open research directions — reasoning, continual learning, world models.
3. Reading the field — curriculum, sources, trilogy close.

---

## Chapter 1 — Evaluation at the frontier

**The benchmark leaderboard is a video game. High scores can coexist with bad outcomes, and bad scores can hide genuinely useful capabilities.**

Evaluation is not a neutral measurement of capability. It is a claim that the thing being measured corresponds to something important. As model capabilities grow, the mismatch between what benchmarks measure and what matters tends to grow with them — and the stakes of getting this wrong increase.

### Why standard benchmarks go wrong

**Saturation.** A benchmark that most models can nearly ace is no longer measuring meaningful differences. The variance it captures becomes noise rather than signal about capability gaps that matter for deployment. This happens faster than expected: what seemed like a challenging benchmark is often saturated within 18 months of its publication.

**Contamination.** Benchmark examples that appear in training data inflate performance artificially. Responsible evaluation uses held-out or dynamically generated benchmarks, but even held-out benchmarks from past papers eventually appear in web crawls as they accumulate citations and discussions.

**Construct validity.** A benchmark of math problems measures something. But "math problem performance" may not predict the capability that matters for your use case: the model may solve formatted textbook problems well while failing at the informal, multi-step, ambiguous mathematical reasoning in real scientific or engineering work.

**Aggregation hides heterogeneity.** An average score across 100 tasks tells you almost nothing about whether the model is uniformly good at 80/100 tasks or spectacular at 60 and terrible at 40. Two models with the same overall benchmark score can have very different profiles of which tasks they handle well.

**Gaming and optimization pressure.** When benchmarks become industry standards, they attract optimization. Some of this optimization produces genuine capability improvements — models get better at the thing the benchmark measures. Some of it produces benchmark-specific improvements that do not transfer.

### Process evaluation vs. outcome evaluation

**Outcome evaluation** asks: did the model get the right answer? This is easy to automate and scores cleanly. The limitation: a model can get the right answer through wrong reasoning, and get the wrong answer through sound reasoning on a genuinely ambiguous question.

**Process evaluation** asks: was the reasoning process sound? This is harder to automate and does not always have a clean ground truth. The advantage: for tasks where correct reasoning matters (tutoring, medical advice, scientific analysis), a model that gets the right answer via reasoning errors is not a model you want to deploy — even if it passes outcome evaluation.

For high-stakes applications, process evaluation is often more relevant than outcome evaluation. A math tutor that gets the right answer by guessing is not a useful math tutor. A medical information system that reaches a correct recommendation through faulty reasoning cannot be trusted on cases where it is less likely to get lucky.

The practical challenge: process evaluation requires either human judgment or a second model that can evaluate reasoning quality — both of which are expensive and introduce their own biases.

### Dynamic benchmarks

**Dynamic benchmark construction** attempts to create evaluation examples that have not appeared in training data and cannot easily be gamed:

- **Time-gating**: Evaluation examples from events after the training cutoff.
- **Procedural generation**: Generating new examples algorithmically from a specification, so the exact examples have not been seen.
- **Human adversarial data collection**: Having humans specifically try to find questions the model answers incorrectly, then using those as test cases.
- **Live competition benchmarks**: Benchmark examples from ongoing competitions that update continuously.

None of these fully solves the contamination and saturation problems, but they raise the difficulty of gaming and reduce the rate of artificial saturation.

### The societal impact lens

Capability benchmarks measure what models can do. They do not measure what models do when deployed at scale to real users.

The gap matters because:
- The distribution of real user queries is different from the distribution of benchmark questions.
- The distribution of outcomes (who benefits, who is harmed, what behaviors are normalized) depends on the full deployment ecosystem, not model capability in isolation.
- Social and economic impacts from AI systems are determined by deployment decisions, access patterns, and organizational choices, not by benchmark performance.

Occupational impact analysis, audit studies of AI-assisted decisions, longitudinal studies of usage patterns, and community feedback processes are research methodologies for evaluating at the deployment level rather than the model level. These are less developed and less standardized than capability benchmarking — partly because they are harder, and partly because they produce less convenient answers.

*Friction:* the leaderboard is a video game — you get points for winning the levels the game defines. Real deployment is a different game, on different levels, with different scoring. A model that dominates the leaderboard can still fail the people it serves.

### Takeaway

- Standard benchmarks suffer from saturation, contamination, construct validity issues, and aggregation hiding capability heterogeneity.
- Process evaluation is more relevant than outcome evaluation for high-stakes applications where reasoning quality matters.
- Dynamic benchmarks reduce (but do not eliminate) contamination and gaming.
- Capability benchmarks measure potential in lab conditions, not impact under real deployment. Both matter; neither substitutes for the other.

---

## Chapter 2 — Open research directions

**Naming open problems honestly is a form of scientific integrity. The field generates confident claims faster than it generates validated answers.**

This chapter names research directions where the problems are clear and important, the progress is real but incomplete, and bold claims should be interrogated. The goal is not pessimism — progress has been substantial — but calibration. Depth requires distinguishing what is understood from what is asserted.

### Reasoning beyond pattern matching

**The question:** Do current language models reason, or do they pattern-match? Do they compute in a way that generalizes beyond training distribution, or do they find sophisticated statistical shortcuts?

**What is understood:** Models trained on chain-of-thought data produce longer, more structured reasoning traces that correlate with higher accuracy on many reasoning tasks. This is real and useful.

**What is contested:** Whether this constitutes genuine compositional reasoning — the ability to assemble known rules in new ways to solve problems structurally unlike anything in training — or whether it is sophisticated interpolation within the training distribution.

**Why it matters:** If models can generalize compositionally, their capabilities in novel domains may be substantially stronger than their training data directly supports. If they cannot, performance on distribution-shifted problems will be systematically worse than in-distribution evaluation suggests. This directly affects how much you can trust model performance on novel problems.

**Current research directions:** Systematic evaluation on problems designed to require out-of-distribution generalization (novel arithmetic structures, invented logical systems, causal reasoning with new relations), interpretability of reasoning traces, and architectures specifically designed for compositional generalization.

### Continual learning

**The question:** Can a model update its knowledge and behavior in response to new information without degrading its performance on what it already knows?

**The problem:** Standard fine-tuning on new data causes **catastrophic forgetting** — the model overwrites existing knowledge in the process of learning new facts. The parameters that encoded old knowledge and the parameters that need to encode new knowledge overlap, and gradient descent on the new objective modifies both.

**Current approaches:**
- **Parameter isolation**: Reserving specific parameters for new knowledge, either through architectural design or learned parameter masking.
- **Rehearsal**: Including examples of old tasks in the fine-tuning data to prevent forgetting.
- **Low-rank adaptation (LoRA)**: Fine-tuning only a small number of parameters (low-rank weight perturbations), which limits interference with the base model's knowledge.
- **Retrieval as continual learning**: Updating a retrieval index rather than the model weights, so new knowledge is non-parameric.

**Why it matters:** Deployed models need to stay current. The alternative — periodically retraining from scratch on accumulated data — is expensive and introduces instabilities. A model that can incorporate new information without forgetting old knowledge would substantially change the economics and operational complexity of AI deployment.

### World models and physical reasoning

**The question:** Do language models have world models — internal representations of how the world works that support causal inference and planning, not just pattern association?

**What is claimed:** Models that can answer questions about physical systems, predict counterfactuals, and reason about cause and effect. These abilities exist and are useful.

**What is contested:** Whether the underlying representations support genuine causal reasoning (the ability to reason about what would happen under interventions — what if X had been different?) or whether models learn correlational patterns that approximate causal reasoning in in-distribution cases and break on novel causal structures.

**Evidence from the field:** Models succeed reliably at causal questions that have similar structures to training data. Performance degrades significantly on causal questions with novel structural features, or on tasks requiring counterfactual reasoning about physical processes that are unlike anything in text.

**Why it matters:** Planning, simulation, scientific reasoning, and many high-stakes applications require genuine causal inference. If model "understanding" of physical and causal structure is shallow, these applications will fail in predictable ways that benchmark performance does not surface.

### Human-AI collaboration design

**The question:** How should humans and AI systems work together such that the collaboration is reliably better than either alone?

This is both a research question about human-computer interaction and an alignment question about how AI systems should behave in collaborative contexts. Key open problems:

**Appropriate reliance:** Users who over-rely on AI systems can miss errors that they would catch themselves. Users who under-rely fail to benefit from AI capabilities. Calibrating appropriate reliance requires both a well-calibrated AI (confident when right, uncertain when uncertain) and user training. Neither is fully solved.

**AI-induced skill atrophy:** If a professional consistently delegates a skill to an AI tool, does their own ability in that domain degrade? This is plausible for domains where practice maintains skill (writing, mathematical reasoning, judgment under uncertainty). The research is early and contested.

**Collective knowledge effects:** If many people delegate similar thinking to similar AI systems, does the diversity of human thought decrease over time? This is a macro-level question that cannot be studied in short-term individual experiments.

**Disagreement and productive friction:** For AI systems used in decision support, how should disagreement between the AI and the human be handled? A system that always defers to human judgment is not providing useful decision support; a system that pushes too hard on its recommendations undermines human agency.

*Figure-caption aside:* "here be dragons" is not cynicism — it is epistemic humility with a sense of humor. The dragons are the claims we do not yet know how to verify.

### Generalization and emergence

**Emergence** — capabilities that appear at scale without being explicitly trained for — is real in the sense that performance on some benchmarks shows discontinuous jumps as model scale increases. It is contested in several ways:

- Some apparent emergence may be an artifact of evaluation methodology: using a metric that maps nonlinearly onto capability (e.g., exact-match accuracy on problems that require all steps to be correct) can produce apparent discontinuities even when underlying capability is smoothly scaling.
- Some emergent capabilities appear to emerge earlier in smaller models when evaluated with more sensitive metrics.
- The mechanistic explanation of why capabilities emerge at specific scale thresholds is not well understood.

The practical implication: be skeptical of claims that a specific capability will definitely emerge at a specific scale. Monitor empirically for capabilities as scale increases, and design systems to handle both their presence and absence gracefully.

### Takeaway

- Compositional reasoning in novel domains is real but limited; current models may interpolate where we expect them to generalize.
- Continual learning without catastrophic forgetting is an unsolved problem; retrieval is the current practical workaround.
- World models and causal reasoning are present in shallow forms; deep causal reasoning on novel structures remains weak.
- Human-AI collaboration introduces risks (over-reliance, skill atrophy) alongside benefits; these require deliberate design, not just capability.
- Emergence is real but its mechanisms and predictions are contested; measure rather than extrapolate.

---

## Chapter 3 — Reading the field and closing the trilogy

**FOMO is a full-time job. Depth on the threads that matter to your work is how preprint consumption becomes judgment.**

The field moves fast. A sustainable practice for following it requires selectivity, not comprehensiveness. This chapter gives you the reading strategy and then closes the trilogy.

### Evaluating sources

**arXiv** is where most ML research appears first. The advantages: fast, open, comprehensive. The disadvantages: no peer review at the preprint stage, highly variable quality, and a volume that rewards click-optimized abstracts over careful content.

Signals for credibility at arXiv:
- **Reproducibility:** Does the paper release code and evaluation scripts? Reproducibility is not sufficient for correctness, but an unreproducible paper cannot be verified.
- **Related work engagement:** Does the paper engage honestly with prior work and competing approaches, or does it cherry-pick comparisons?
- **Ablations:** Does the paper show what components of the method are actually responsible for the improvement? Results without ablations are claims about a pipeline, not a method.
- **Calibration of claims:** Does the paper distinguish between what the results show and what the authors believe? Overclaiming is common; a paper that acknowledges its limitations is more trustworthy.

**Conference papers** (NeurIPS, ICML, ACL, ICLR, CVPR) have been through peer review, which adds signal but is not infallible. The review process is compressed and relies on overworked reviewers; significant papers are occasionally rejected and weak papers accepted. Use conference acceptance as one signal, not the only one.

**Blog posts and technical reports from labs** are not peer-reviewed but are often the first published account of significant systems. Read them with awareness that they are marketing communications as well as technical writing. The most useful content is often in the methods and evaluation sections, not the headline results.

**Model cards and system cards** are the most directly actionable documents for practitioners. They describe what a model was trained on, how it was evaluated, what its known limitations are, and what uses it is and is not appropriate for. Read these before deploying any model in a production context.

### Building a sustainable reading practice

The goal is not to read everything. The goal is to be well-informed on the threads that matter for your work while maintaining the time and mental bandwidth to think clearly about them.

A practical structure:

**One conference track.** Pick the venue and track most relevant to your work (alignment, systems, NLP, computer vision) and read the accepted papers list when it is published. You do not need to read every paper — the titles and abstracts will show you where to go deeper.

**One or two trusted aggregators.** Annotated paper newsletters (there are several in the ML space) or reading groups that summarize and filter can dramatically reduce the cost of staying current. The value is not just the papers they surface but the context they provide about what is significant.

**One open-model release line.** Follow the release series most relevant to your work (Llama, Mistral, Gemma, or others as they emerge). Read the technical reports, the model cards, and the evaluations. These provide grounded benchmarks for what is currently practical.

**Primary sources for big claims.** When a capability claim is cited enough to affect your decisions (a new reasoning approach, a safety result, a scaling breakthrough), read the original paper rather than the blog post summary. Summaries lose nuance; primary sources let you evaluate the methodology.

*Direct address:* if your list of sources is longer than you can actually read, cut it in half. What you cannot read cannot inform your judgment; it can only produce anxiety. Better to have three sources you read carefully than thirty you skim guilt-ridden.

### What the three volumes built

This trilogy followed one thread from beginning to research depth.

**Volume I — From Tokens to Understanding** built the foundation: what tokens are, how attention works at an intuitive level, what the training process looks like, what models can and cannot do, and how to engage with them responsibly as an everyday user or early practitioner.

**Volume II — From Prompts to Systems** moved from foundation to practice: prompting as engineering discipline, retrieval and adaptation, evaluation, deployment, observability, cost, security, cross-functional teams, and responsible deployment. This is where most of the value is generated — by teams building carefully with the tools that exist.

**Volume III — From Models to Frontiers** stepped behind the API surface: the science of pretraining and scaling, the research foundations of alignment and safety, efficiency for training and serving at scale, multimodal models and agents, and the frontier's open questions. This is where the vocabulary for evaluating the field comes from.

The boundary between volumes is roughly:
- Vol I → II: understanding what models are vs. building reliably with them.
- Vol II → III: building with models vs. understanding or evaluating the models themselves.

You do not need all three volumes to be effective. Most of the value that LLMs generate in the world will come from teams working at the Vol II level — building carefully, measuring honestly, shipping responsibly. Volume III is for the readers whose work requires depth on the science, the safety research, or the research frontier.

### A closing note on uncertainty

This volume named many open problems. That is intentional. The honest account of the field is not one of triumphant progress toward a fully understood technology. It is one of rapid capability growth, contested explanations, improving but imperfect evaluation, and genuine uncertainty about both the potential and the risks.

The researchers and practitioners doing the best work in this field hold two things simultaneously: substantial optimism about what these systems can do, and rigorous skepticism about whether any specific claim about those systems holds up to scrutiny. That combination — optimism paired with skepticism — is the hardest thing to maintain and the most valuable.

The bridge is open, in both directions.

---

## Try it

### Exercise 1 — Benchmark evaluation

Pick a benchmark commonly cited in model release comparisons (MMLU, HumanEval, GSM8K, HellaSwag, or another you have encountered). For that benchmark: identify one way it could be contaminated in a recent training crawl, one task type where it probably overestimates real-world capability, and one task type where it might underestimate. If you cannot find all three, that is informative — note which you could not identify and why.

### Exercise 2 — Process evaluation design

A company uses a large language model to help analysts write investment research reports. The current evaluation measures whether the model's outputs contain specific required sections and passes a factual accuracy check against company databases. Design a process evaluation that would supplement this — what would you evaluate about the reasoning process itself, not just the final output?

### Exercise 3 — Open problem impact

Choose one open research problem from Chapter 2 (compositional reasoning, continual learning, world models, human-AI collaboration, emergence). Describe one specific product or application that currently exists where closing that research gap would change what is practically possible. Be specific about what currently fails and what would become feasible.

### Exercise 4 — Reading list audit

List the sources you currently use to stay current on LLM research. For each source, categorize it: primary (papers, model cards), secondary (summaries, newsletters), or marketing-adjacent (lab blogs, press releases). If more than half are in the marketing-adjacent category, identify one primary or secondary source to add and one marketing-adjacent source to deprioritize. If your list is empty, start with one model card and one conference accepted papers list.

---

*End of Part V — Volume III — From Models to Frontiers. Previous: [Part IV — Beyond text: multimodal models and agents](from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md) · [Trilogy hub — README](../README.md) · Or [main volume](from-models-to-frontiers.md).*
