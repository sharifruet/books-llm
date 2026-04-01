# Part III — Efficiency: training, inference, and systems

*Sharif Uddin*

*[From Models to Frontiers](from-models-to-frontiers.md) · Volume III*

---

Efficiency decides what is affordable. A technique that improves model quality by 5% while doubling inference cost may not be worth deploying. A quantization method that cuts memory usage by 4x while degrading quality by less than 1% on your task may be essential for serving at your scale. This part covers the engineering and research of making large models affordable to train and to serve — at a level of depth that lets you evaluate efficiency claims critically and make informed infrastructure decisions.

---

## Contents of this part

*In the full volume table of contents, these correspond to sections 9–11.*

| | Chapter | What you will take away |
|---|--------|-------------------------|
| **1** | Training efficiency | Mixed precision, parallelism, gradient checkpointing, curriculum, fault tolerance |
| **2** | Inference efficiency | Quantization, distillation, speculative decoding, KV-cache, latency-quality-cost tradeoffs |
| **3** | Specialized hardware and software stacks | GPUs, TPUs, compiler stacks, hosting vs. self-hosting, custom silicon |

**Contents (plain list — same as table):**

1. Training efficiency — precision, parallelism, checkpointing, bottlenecks.
2. Inference efficiency — quantization, distillation, speculative decoding, KV cache.
3. Hardware and stacks — GPU/TPU, compilers, serving decisions.

---

## Chapter 1 — Training efficiency

**When a training run costs hundreds of thousands of dollars and takes weeks, "faster code" is not an abstract goal — it is the difference between a team that can iterate and one that cannot.**

Modern large model training is a distributed systems problem as much as a machine learning problem. The techniques in this chapter address how to use a cluster of accelerators efficiently, how to handle the numerical challenges of training large models, and how to ensure that expensive training runs are recoverable when things go wrong.

### Mixed precision training

Full-precision (float32) arithmetic is expensive in both memory and compute. **Mixed precision training** uses lower-precision representations (float16 or bfloat16) for most computations while maintaining float32 for numerically sensitive operations (gradient accumulation, loss scaling).

**bfloat16** has become the dominant choice for large model training because it has the same dynamic range as float32 (8 exponent bits) but half the memory footprint. This matters because many training instabilities arise from values near the representation limits, and bfloat16 avoids the overflow/underflow issues that float16 encounters with large gradients.

The benefit: roughly 2x memory reduction, and on modern accelerators (A100, H100, TPU v4+), bfloat16 matrix multiplication is 2-4x faster than float32 due to hardware tensor core support.

The catch: some operations — most critically gradient accumulation — must remain in float32 to avoid numerical error accumulation across many steps. The "mixed" in mixed precision is not optional.

### Parallelism strategies

Training a model that does not fit on a single GPU (or TPU chip) requires distributing the computation. Several strategies exist, and large training runs typically combine multiple:

**Data parallelism.** Each accelerator processes a different micro-batch of data with identical model weights. Gradients are averaged across accelerators after each step. This is the simplest form of parallelism and scales well as long as the model fits on a single device.

**Tensor parallelism.** Individual layers (particularly large attention and feed-forward layers) are split across multiple accelerators. The matrix operations within a layer are computed in parallel. This allows training models that would not fit on a single device even for a single layer.

**Pipeline parallelism.** Different layers of the model are assigned to different accelerators. The input passes through layers in sequence across devices. The challenge is "pipeline bubbles" — accelerators that are idle while waiting for inputs from the previous stage.

**ZeRO (Zero Redundancy Optimizer).** Rather than replicating the optimizer states across all data-parallel replicas (which is expensive), ZeRO shards optimizer states, gradients, and model parameters across data-parallel workers. This dramatically reduces per-device memory usage and allows larger model sizes at the same hardware cost.

Large runs commonly use a 3D parallelism approach — combining data, tensor, and pipeline parallelism — with ZeRO optimization on top. The configuration is complex enough that dedicated frameworks (Megatron-LM, DeepSpeed, JAX with GSPMD) exist specifically to manage it.

### Gradient checkpointing

During the forward pass, intermediate activations are stored for use in the backward pass (computing gradients). For a large model, storing all activations simultaneously can require as much memory as the model weights themselves.

**Gradient checkpointing** recomputes activations during the backward pass rather than storing them all. The tradeoff: roughly 33% more compute, in exchange for significantly reduced activation memory. For very large models or very long sequences, this is often essential to fit training in available memory.

### Bottleneck identification

*Friction:* teams building custom training infrastructure often spend time on kernel optimization — writing custom CUDA for specific operations — before profiling their actual bottlenecks. The actual bottlenecks are frequently:

- **I/O**: Data loading is not fast enough to keep accelerators busy. The GPU is waiting for the next batch.
- **Communication overhead**: In distributed training, all-reduce operations (averaging gradients) can become the limiting factor, especially for large model sizes and high gradient update frequencies.
- **Checkpoint I/O**: Writing checkpoints to disk and resuming from them can dominate wall-clock time for large models on long runs.
- **Load imbalance**: Pipeline bubbles, uneven batch sizes, or MoE expert imbalance leave some accelerators idle.

Profile before optimizing. The boring bottleneck beats the clever story about kernel fusion.

### Fault tolerance

Training runs for large models take days to weeks. Hardware failures are not rare events at this scale — they are expected. Effective training infrastructure requires:

- **Frequent checkpointing**: Saving model state at regular intervals so a hardware failure costs at most a few hours rather than days of work.
- **Automatic restart from checkpoint**: The training job should resume from the last checkpoint without manual intervention.
- **Anomaly detection**: Catching numerical instabilities (loss spikes, NaN values) early, before they propagate across many steps.

The economics of fault tolerance: for a 10-day training run with a 1% per-hour hardware failure rate, the expected time before a failure is roughly 4 days. A checkpoint every 30 minutes means at most 30 minutes of lost work. A checkpoint every 4 hours means potentially 4 hours. Checkpoint frequency directly sets the price of hardware failure.

### Takeaway

- Mixed precision (bfloat16) gives roughly 2x memory reduction and faster compute with appropriate care for numerically sensitive operations.
- Large model training combines multiple parallelism strategies: data, tensor, pipeline, plus ZeRO optimizer sharding.
- Gradient checkpointing trades compute for memory.
- Profile for I/O, communication, and load imbalance before optimizing kernels.
- Fault tolerance requires frequent checkpointing and automatic restart. It is not optional for long training runs.

---

## Chapter 2 — Inference efficiency

**Training is a one-time cost. Inference is ongoing — every query, every user, every day. At scale, inference economics dominate training economics within months of launch.**

A model that cost $10M to train but serves 100M queries per day is a system where inference efficiency decisions matter far more than training efficiency decisions. The techniques in this chapter address how to serve large models more cheaply, more quickly, or with a smaller hardware footprint — and what quality tradeoffs those decisions involve.

### Quantization

**Quantization** reduces the numerical precision of model weights (and sometimes activations) from the 16-bit or 32-bit floats used during training to lower-precision formats.

**INT8 quantization** (8-bit integers) can roughly halve model memory with typically small quality degradation on most tasks. The mechanism: map the range of float16 weights onto a 256-value integer scale, with a scale factor to reverse the mapping. The quality degradation comes from rounding error and from the fact that the scale factor is coarse.

**INT4 quantization** (4-bit) further halves memory at higher risk of quality degradation. Whether the degradation is acceptable depends heavily on the task: coding and reasoning tasks tend to be more sensitive than summarization or simple question-answering.

**GPTQ and GGUF** are specific quantization schemes that have become practical standards for running large models on consumer hardware. They use post-training quantization (quantizing after training without retraining) with calibration datasets to minimize error.

The key insight for practitioners: **quantization quality is task-specific, not model-specific**. You cannot evaluate the acceptability of a quantization decision in the abstract — you have to test on your task distribution. A model quantized to INT4 that passes your evaluation on the cases you care about is an acceptable deployment choice. One that fails on specific reasoning chains you need is not, regardless of average benchmark scores.

### Distillation

**Knowledge distillation** trains a smaller "student" model to mimic the behavior of a larger "teacher" model. Rather than training the student on hard labels (correct/incorrect answers), distillation trains on the teacher's output distribution — the student learns from the teacher's uncertainty and the relative probabilities it assigns to different outputs.

Effective distillation can produce smaller models that perform surprisingly close to the teacher on the teacher's specific tasks. The limitations:
- Distillation is task-specific: a student distilled on customer support conversations may outperform the teacher on customer support but perform worse on unrelated tasks.
- The gap between student and teacher grows for complex reasoning tasks where the teacher's outputs require understanding that a small model cannot represent.
- Distillation from a proprietary model raises legal and licensing questions.

### Speculative decoding

**Speculative decoding** uses a small, fast "draft" model to generate candidate tokens, which a large "verifier" model then checks in parallel. If the large model agrees with the draft tokens, they are accepted without additional compute. If it disagrees, it corrects the first wrong token and continues.

The appeal: the large model's output is preserved exactly (it is still the one determining final tokens), but latency is reduced because many draft tokens can be verified in a single forward pass. The speedup depends on how often the draft model agrees with the large model — more agreement means more speedup.

Speculative decoding is most effective when:
- The large model is compute-bound (the bottleneck is computation, not memory bandwidth).
- There is a good small model in the same family as the large model (trained on similar data, so it agrees often).
- Latency is more important than throughput (it does not reduce total compute — it reduces wall-clock time per sequence).

### KV-cache mechanics and memory pressure

During generation, the transformer's attention mechanism computes key and value vectors for every token in the context. Rather than recomputing these on every generation step, the **KV cache** stores them in memory and reuses them.

The memory cost: for a model with H attention heads, each with a key and value dimension of D, and a context of L tokens, the KV cache requires 2 × H × D × L entries per layer. For a 70B parameter model serving long contexts, the KV cache can be comparable in size to the model weights themselves — or larger.

At inference scale, KV cache memory often becomes the binding constraint:
- Longer context windows increase memory usage linearly.
- Many simultaneous users require either more memory or smaller batches.
- Paged attention (managing the KV cache in fixed-size pages, similar to OS memory paging) allows more efficient sharing and reduces fragmentation.

**Attention sinks and context compression** are techniques for reducing effective context length without truncation — identifying which tokens the model "needs" to retain and dropping those it does not. These techniques can substantially reduce KV cache pressure for very long contexts at the cost of potential quality regression on content in dropped context.

### The latency–quality–cost Pareto surface

There is no single "best" deployment configuration. The tradeoffs form a surface:

| Optimization | What you gain | What you risk |
|---|---|---|
| INT8 quantization | 2x memory reduction, faster matrix mul | Small quality degradation on sensitive tasks |
| INT4 quantization | 4x memory reduction | Higher quality risk, especially for reasoning |
| Smaller model | Much lower compute and memory | Quality gap vs. larger model |
| Distilled student | Lower inference cost on target tasks | Weaker generalization off-target |
| Speculative decoding | Lower latency | Added complexity, draft model required |
| Shorter context | Lower KV cache memory | Less available context for tasks that need it |

Product decisions live on this surface. The right operating point depends on your latency SLO, your quality requirement on your specific task distribution, and your cost budget. Measure all three on your task before deciding.

*Anchor:* inference costs amortize training across users. A model trained once but serving 100M queries per day should have its optimization budget allocated to inference, not training. Profile where the money actually goes.

### Takeaway

- Quantization reduces memory and compute at a quality cost that varies by task. Always evaluate on your task distribution.
- Distillation can produce efficient smaller models for specific tasks; generalization beyond the training distribution shrinks.
- Speculative decoding reduces latency for large models by using a draft model, without changing output quality.
- KV cache is the dominant memory cost for long-context inference; paged attention and compression techniques address it.
- Optimize the right stage: for high-query-volume products, inference economics dominate within months.

---

## Chapter 3 — Specialized hardware and software stacks

**Hardware is not neutral. It determines which techniques are practical, which latency targets are achievable, and how your costs scale with usage.**

Understanding the hardware landscape at a decision-maker level — not a chip designer level — lets you evaluate vendor claims, make infrastructure choices with appropriate skepticism, and avoid building on assumptions that hold at one scale and break at another.

### The accelerator landscape

**GPUs** (Graphics Processing Units) are the dominant training and inference accelerator for most organizations. Modern data-center GPUs (NVIDIA H100, H200, A100) provide:
- Large amounts of high-bandwidth memory (80GB–192GB per chip).
- Tensor cores optimized for the matrix multiplications that dominate transformer computation.
- NVLink for fast inter-GPU communication within a node.
- A mature software ecosystem (CUDA, cuDNN, PyTorch, JAX).

**TPUs** (Tensor Processing Units, Google's ASICs) offer strong performance on specific workloads, particularly for models developed within the Google/JAX ecosystem. Less flexible for arbitrary experimentation but very efficient for regular workloads.

**Newer entrants** (AMD MI300, Intel Gaudi, various startup ASICs) are expanding the landscape, typically emphasizing cost-per-token competitiveness for specific workloads.

The practical decision for most organizations: start with GPUs. Depart only when volume and workload stability justify the engineering investment in porting and optimizing for a different platform.

### Compiler stacks and kernel fusion

Modern accelerators do not automatically achieve their theoretical peak performance for arbitrary operations. Getting close requires careful management of:

**Memory bandwidth vs. compute bandwidth.** For most transformer operations, the limiting factor is not compute but memory bandwidth — moving data between high-bandwidth memory and compute units is the bottleneck. Kernel fusion reduces memory round-trips by combining operations that would otherwise each require loading and storing intermediate values.

**Compiler optimization stacks** (XLA for JAX/TPUs, TorchCompile for PyTorch, Triton for custom kernels) automate some of this optimization, fusing operations and optimizing memory layout. The resulting throughput improvement can be substantial — 30-50% is common for well-tuned compilation.

**Flash attention** specifically addresses the attention mechanism's memory bandwidth problem by computing attention without materializing the full attention matrix in high-bandwidth memory. It is now effectively standard for production transformer inference and training.

### Hosting vs. self-hosting

The decision between API access (hosted inference) and running your own models involves several dimensions:

| | Hosted API | Self-hosted |
|---|---|---|
| **Upfront cost** | None | High (hardware, setup) |
| **Marginal cost** | Per-token pricing | Amortized hardware + ops |
| **Latency control** | Provider SLAs; shared infrastructure | Full control |
| **Model choice** | Provider's models | Any model you can run |
| **Data privacy** | Trust provider's handling | Full control |
| **Capacity planning** | Provider handles it | Your problem |
| **Customization** | Limited to provider's fine-tune options | Full control |

Hosted APIs are almost always the right starting point. Self-hosting becomes worth considering when:
- Query volume is high enough that per-token API costs exceed amortized hardware costs.
- Latency requirements are tight enough that provider SLAs are insufficient.
- Data privacy requirements prohibit sending data to an external provider.
- Fine-tuning or model modification requirements exceed what APIs support.

This calculation changes over time as hardware costs fall and as API providers reduce per-token prices. Revisit it periodically rather than treating the initial decision as permanent.

### Custom silicon

**ASICs** (Application-Specific Integrated Circuits) designed for LLM inference can substantially reduce cost-per-token at scale — they trade flexibility for efficiency. The economics become compelling when:
- Token volume is very high (hundreds of millions per day).
- The workload is stable enough that an inflexible but optimized chip is worth the NRE (non-recurring engineering) cost.
- The organization has the engineering resources to port and maintain software stacks on new hardware.

For most organizations, custom silicon is not the current decision. The decision is which vendor's current generation GPU to deploy and how to optimize workloads for it.

*Direct address:* If you are not at the token volumes where custom silicon changes your economics, the right response to custom silicon discussions is to file them under "interesting, not my decision this quarter." Hardware strategy should follow volume and workload stability, not hype.

### Takeaway

- GPUs dominate training and inference; start there. Depart for other hardware only with clear volume and workload justification.
- Compiler stacks, kernel fusion, and flash attention close the gap between theoretical and actual accelerator performance.
- Hosted APIs are almost always the right starting point; self-hosting for volume, latency, privacy, or customization reasons.
- Custom silicon has compelling economics at high volume but requires engineering investment and reduces flexibility.
- Hardware filters which techniques are practical at your scale. Know the constraints of your infrastructure before committing to an optimization strategy.

---

## Try it

### Exercise 1 — Quantization evaluation

You are considering INT4 quantization for a model that handles both customer FAQ retrieval and contract clause extraction. Describe how you would evaluate the acceptability of this quantization decision *specifically for each task* — what test cases would you include that are more challenging for a heavily quantized model than for the full-precision version?

### Exercise 2 — Inference bottleneck

A long-context chat product serves an average context length of 20,000 tokens per conversation and handles 500,000 conversations per day. Is KV-cache memory or model weight memory more likely to be the binding constraint on GPU memory? Show your reasoning. What technique would you investigate first to address the binding constraint?

### Exercise 3 — Hosting decision

A startup is building a specialized medical information assistant using a 70B parameter model. They currently use a hosted API and are considering self-hosting. What information would you need to determine whether self-hosting is economically justified? What would the analysis look like — what numbers matter?

### Exercise 4 — Speculative decoding fit

A team wants to reduce time-to-first-token for a code generation assistant. They are considering speculative decoding using a 7B model as a draft and a 70B model as the verifier. Describe the conditions under which speculative decoding is likely to provide good speedup for this task, and one scenario in which it would provide poor speedup despite having both models available.

---

*End of Part III. Previous: [Part II — Alignment, safety, and robustness](from-models-to-frontiers-part-ii-alignment-safety-and-robustness.md) · Next: [Part IV — Beyond text: multimodal models and agents](from-models-to-frontiers-part-iv-beyond-text-multimodal-models-and-agents.md) · Or [main volume](from-models-to-frontiers.md).*
