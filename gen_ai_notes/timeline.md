# GenAI Notes

---

## Timeline of Generative AI

### 2013 — Word2Vec (Google)
**What:** Neural network technique to embed words as dense vectors in continuous space.  
**Why:** Proved that semantic meaning can be captured mathematically — "king - man + woman ≈ queen". Foundational for all future NLP.

### 2014 — GANs — Generative Adversarial Networks (Goodfellow et al.)
**What:** Two networks (Generator + Discriminator) trained adversarially to produce realistic data.  
**Why:** First practical way to generate realistic images from noise. Enabled image synthesis, deepfakes, data augmentation.

### 2014 — Seq2Seq + Attention (Bahdanau et al.)
**What:** Encoder-Decoder architecture for sequence tasks (translation), with soft attention over input tokens.  
**Why:** Solved the bottleneck problem in RNNs — models could now "look back" at input while generating output. Direct precursor to Transformers.

### 2015 — Diffusion Models (theoretical groundwork — Sohl-Dickstein)
**What:** Probabilistic models that learn to reverse a noise process.  
**Why:** Later became the backbone of Stable Diffusion, DALL-E 2, Midjourney. Outperformed GANs in image quality and training stability.

### 2017 — Transformers: "Attention Is All You Need" (Vaswani et al., Google)
**What:** Replaced RNNs entirely with self-attention. Parallelizable, scalable, globally aware.  
**Why:** The most important paper in modern AI. Every major LLM (GPT, BERT, Claude, Gemini) is built on this architecture.

### 2018 — BERT (Google)
**What:** Bidirectional Encoder Representations from Transformers. Trained via masked language modeling (fill in the blank) on massive text.  
**Why:** Showed that pre-training + fine-tuning is a winning paradigm. Dominated NLP benchmarks. Encoder-only, great for understanding tasks.

### 2018 — GPT-1 (OpenAI)
**What:** First Generative Pre-trained Transformer. Decoder-only, trained to predict next token.  
**Why:** Showed unsupervised pre-training transfers to downstream tasks with minimal fine-tuning. Decoder-only = better for generation.

### 2019 — GPT-2 (OpenAI)
**What:** 1.5B parameter model trained on WebText (Reddit outlinks).  
**Why:** OpenAI initially withheld full release citing misuse risk. First public signal that LLMs could generate coherent long-form text — and be dangerous.

### 2020 — GPT-3 (OpenAI) — 175B parameters
**What:** Scaled GPT-2 by ~100x. Introduced "few-shot prompting" — no fine-tuning needed, just show examples in context.  
**Why:** Demonstrated emergent abilities at scale. Launched the era of foundation models and prompt engineering.

### 2021 — CLIP (OpenAI) + DALL-E 1
**What:** CLIP = contrastive learning to align images and text. DALL-E 1 = text-to-image generation.  
**Why:** Enabled zero-shot image classification and text-conditioned image generation. Foundation for multimodal AI.

### 2022 — InstructGPT + RLHF (OpenAI)
**What:** Fine-tuned GPT-3 using Reinforcement Learning from Human Feedback (RLHF) to follow instructions.  
**Why:** Bridged the gap between "predicts next token" and "does what you ask". Made models helpful, harmless, honest. Blueprint for ChatGPT.

### 2022 — Stable Diffusion (Stability AI, open source)
**What:** Open-source latent diffusion model for text-to-image.  
**Why:** Democratized image generation. Running locally, fine-tunable, spawned LoRA, ControlNet, and entire ecosystem of image tools.

### Nov 2022 — ChatGPT (OpenAI)
**What:** InstructGPT + chat interface = ChatGPT. Reached 100M users in 2 months.  
**Why:** Consumer inflection point. Brought LLMs to mainstream. Triggered the AI arms race across Google, Meta, Anthropic, etc.

### 2023 — GPT-4 (OpenAI, March)
**What:** Multimodal, much larger, significantly smarter than GPT-3.5. Details kept secret.  
**Why:** Bar-raiser for reasoning, coding, professional exams (passed BAR, USMLE). Set the benchmark every other lab aimed for.

### 2023 — LLaMA (Meta, Feb) → LLaMA 2 (July)
**What:** Open-weight models (7B–70B). LLaMA 2 openly licensed for commercial use.  
**Why:** Enabled the open-source AI ecosystem. Sparked fine-tunes (Alpaca, Vicuna, Mistral, Mixtral). Showed you don't need GPT-4 scale for many tasks.

### 2023 — Claude 1 → Claude 2 (Anthropic)
**What:** Constitutional AI — trained using AI feedback (RLAIF) and a "constitution" of principles instead of pure human labeling.  
**Why:** Safer, more steerable models. Claude 2 had 100K context window — critical for long documents, codebases.

### 2023 — Agents & Tool Use emerge
**What:** LLMs given access to tools (search, code execution, APIs). AutoGPT, LangChain, ReAct pattern.  
**Why:** Moved LLMs from "answer questions" to "take actions". Enabled multi-step autonomous task completion. Beginning of the agent era.

### 2023 — RAG — Retrieval Augmented Generation (popularized)
**What:** Retrieve relevant documents from a vector store, inject into context, then generate.  
**Why:** Solves the knowledge cutoff problem without retraining. Cost-effective way to give LLMs access to private/recent data.

### 2024 — Gemini 1.0 / 1.5 (Google DeepMind)
**What:** Natively multimodal (text, image, audio, video). Gemini 1.5 Pro: 1M token context window.  
**Why:** 1M context = entire codebases or long videos in one shot. Showed context length itself is a differentiator.

### 2024 — Claude 3 Family (Anthropic, March)
**What:** Haiku, Sonnet, Opus — speed/cost/intelligence tiers. Opus briefly best model on benchmarks.  
**Why:** Introduced the tiered model strategy. Showed Constitutional AI + scale = top-tier reasoning with strong safety properties.

### Sep 2024 — OpenAI o1 (Reasoning Models)
**What:** Models trained to "think before answering" via chain-of-thought reasoning at inference time (not just pre-training).  
**Why:** Major leap in math, coding, science reasoning. Introduced test-time compute scaling as a new axis alongside model size.

### Jan 2025 — DeepSeek R1 (China, open-source)
**What:** Open reasoning model matching o1 performance, trained at a fraction of the cost using RL without SFT warm-up.  
**Why:** Shocked the AI industry. Proved state-of-the-art reasoning is achievable cheaply and open. Triggered market panic (Nvidia stock -17%).

### 2025 — Agentic AI + MCP (Model Context Protocol)
**What:** Standardized protocol (Anthropic's MCP) for LLMs to connect to tools, data sources, and services.  
**Why:** Solving the "tool integration" fragmentation problem. Claude Code, Cursor, and other AI IDEs built on this. Agents become production-grade.

### 2025 — Claude 4 Family (Anthropic)
**What:** Haiku 4.5, Sonnet 4.6, Opus 4.8, Fable 5 — new capability and efficiency tiers.  
**Why:** Continued push on coding, reasoning, and long-context. Sonnet 4.6 became default workhorse for Claude Code.

---

## Visual Timeline

```
2013  2014  2015  2016  2017  2018  2019  2020  2021  2022  2023  2024  2025
 |     |     |     |     |     |     |     |     |     |     |     |     |
 |     |     |     |     |     |     |     |     |     |     |     |     |
W2V   GAN  Diff        TRNSFM BERT  GPT2  GPT3 CLIP  RLHF  GPT4  o1   Claude4
      Seq2             "Attn  GPT1              DALL-E ChatGPT LLaMA DeepR1
      Seq               All"                          Stable  Agents MCP
                                                      Diff    RAG
```

---

## Architecture Evolution

```
RNN Era (pre-2017)                    Transformer Era (2017+)
──────────────────                    ─────────────────────────
                                      
 Input                                 Input Tokens
   │                                      │  │  │
  [t1]──[t2]──[t3]──[t4]            ┌────▼──▼──▼────┐
         ↑ sequential,               │  Embeddings   │
           can't parallelize         └───────┬───────┘
                                             │
                                     ┌───────▼───────┐
                                     │ Self-Attention │ ← every token
                                     │  (all pairs)  │   attends to
                                     └───────┬───────┘   all others
                                             │
                                     ┌───────▼───────┐
                                     │     FFN        │
                                     └───────┬───────┘
                                             │
                                          Output
```

---

## Model Families & Sizes

```
            Parameters
  175B  ┤                                    GPT-3
        │                                      │
   70B  ┤              LLaMA-2-70B ────────────┤  Gemini Pro
        │                                      │
   13B  ┤     LLaMA-13B                        │
        │                                      │
    7B  ┤  LLaMA-7B   Mistral-7B              │
        │                                      │
    1B  ┤                          TinyLLaMA  │
        └──────────────────────────────────────┘
                 Open Weight           Closed
```

---

## Training Stages of a Modern LLM

```
┌─────────────────────────────────────────────────────────────┐
│                    STAGE 1: Pre-training                     │
│                                                              │
│  Massive corpus (internet, books, code) → Predict next token │
│  Goal: Learn language, facts, reasoning patterns             │
│  Cost: $$$$$$ (millions of dollars of compute)               │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 2: Supervised Fine-Tuning (SFT)           │
│                                                              │
│  Human-written (prompt, ideal response) pairs                │
│  Goal: Teach model to follow instructions                    │
│  Cost: $$ (much cheaper)                                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                STAGE 3: RLHF / RLAIF                        │
│                                                              │
│  Humans (or AI) rank model outputs → Train Reward Model      │
│  PPO optimizes policy to maximize reward                     │
│  Goal: Make model helpful, harmless, honest                  │
└─────────────────────────────────────────────────────────────┘
```

---

## GAN Architecture

```
   Random Noise (z)
        │
        ▼
  ┌──────────┐         Generated Image
  │ Generator│ ──────────────────────────────┐
  └──────────┘                               │
                                             ▼
  Real Images ──────────────────────► ┌──────────────┐
                                      │ Discriminator │──► Real / Fake ?
                                      └──────────────┘
                                             │
                         ┌───────────────────┘
                         │  Loss signal
                         ▼
               Generator improves    Discriminator improves
               (fool the judge)      (catch fakes better)
               
               ← Adversarial Training Loop →
```

---

## RAG Architecture

```
                        User Query
                            │
              ┌─────────────▼──────────────┐
              │         Retriever           │
              │  (embed query → search      │
              │   vector store for top-k)   │
              └─────────────┬──────────────┘
                            │ relevant chunks
              ┌─────────────▼──────────────┐
              │       Context Builder       │
              │  [System] + [Retrieved      │
              │   Docs] + [User Query]      │
              └─────────────┬──────────────┘
                            │ augmented prompt
              ┌─────────────▼──────────────┐
              │            LLM             │
              └─────────────┬──────────────┘
                            │
                         Response
                   (grounded in retrieved docs)
```

---

## Agent Loop

```
         User Goal
              │
              ▼
    ┌─────────────────┐
    │   LLM (Brain)   │◄──────────────────┐
    │  Plan next step  │                   │
    └────────┬────────┘                   │
             │ tool call                  │
             ▼                            │
    ┌─────────────────┐           ┌───────┴──────┐
    │   Tool / API    │──result──►│  Observation  │
    │ (search, code,  │           │  added to     │
    │  browser, DB)   │           │  context      │
    └─────────────────┘           └──────────────┘
    
    Repeats until goal reached or max steps hit
```

---

## 2025 Onwards — The Agentic & Multimodal Era

### Mid 2025 — o3 & Reasoning Model Maturity (OpenAI)
**What:** o3 and o3-mini introduced a `reasoning_effort` parameter — let callers trade tokens for accuracy. Smaller models could outperform ones 14x larger when given more compute budget at inference.  
**Why:** Test-time compute emerged as a new scaling axis independent of model size. You don't need a bigger model — you need a smarter inference strategy.

### May 2025 — Veo 3 (Google DeepMind) — Native Audio in Video
**What:** Text-to-video model generating 4K video with synchronized dialogue, background music, and ambient sound — all from one text prompt.  
**Why:** First model to solve the audio-sync problem in video generation. Set the new standard; native audio became table stakes for all video models by 2026.

### Aug 2025 — GPT-5 (OpenAI) — Unified Architecture
**What:** Merged the previously separate "chat" and "reasoning" model lines into one. Ships a real-time internal router between fast and thinking modes. Outperforms o3 while using 50–80% fewer output tokens.  
**Why:** Proved you can have speed and depth in one model. Eliminated the "pick fast or smart" tradeoff users had with GPT-4 vs o1.

### Sep 2025 — Sora 2 (OpenAI)
**What:** Best-in-class physics simulation in video generation. Multi-shot storyboards, cinematic camera control.  
**Why:** Physics coherence (objects bounce, liquids flow, people move naturally) was the last frontier in believable video generation.

### Sep 2025 — Photonic AI Chip (Univ. of Florida)
**What:** Chip that performs AI matrix multiplications using light (photons) instead of electricity.  
**Why:** Moore's law is slowing. Optical computing offers massive bandwidth and energy efficiency gains. Beginning of post-GPU AI hardware era.

### Nov 2025 — AlphaFold 3 & AI for Science (DeepMind)
**What:** Extended AlphaFold to predict structures of all biomolecules (DNA, RNA, ligands, proteins together). Drug-target interaction modeling.  
**Why:** New drug compounds identified and tested in months instead of years. AI became a first-class tool in pharmaceutical R&D and materials science.

### Dec 2025 — GPT-5.2 (OpenAI)
**What:** 400K context window, $1.75/M input tokens, optimized for coding, spreadsheets, and multi-step agentic tasks.  
**Why:** Showed that long-context + agentic reliability + cost reduction all move together. The "daily driver" for enterprise automation.

### 2025 — MCP + A2A Protocols Standardized
**What:** MCP (Model Context Protocol, by Anthropic) = standard for agent-to-tool communication. A2A (Agent-to-Agent) = standard for agents calling other agents.  
**Why:** Solved the integration fragmentation problem. Like HTTP for the web, MCP/A2A created a common layer so any agent can connect to any tool or service. Claude Code, Cursor, and IDE tools all converged on MCP.

### 2025 — AI Math Olympiad Gold (OpenAI + Google)
**What:** Both OpenAI and Google DeepMind systems scored gold medal level at the International Mathematical Olympiad — solving 5/6 problems in natural language under competition conditions.  
**Why:** Proof that frontier AI surpassed human experts at formal mathematical reasoning. A symbolic benchmark for general reasoning capability.

### Early 2026 — Agentic AI Crosses the Chasm
**What:** 79% of organizations reported agentic AI adoption in 2025; 96% planning expansion. Gartner: 40% of enterprise apps will include task-specific agents by end of 2026 (vs <5% in 2025).  
**Why:** Agents moved from experimental to production. The unit of AI value shifted from "chatbot response" to "completed workflow."

### 2026 — Gemini 3 Pro (Google)
**What:** Natively multimodal, Deep Think mode, 1M+ context. Ranked #1 on LMSYS Arena at launch.  
**Why:** Google finally reclaimed the benchmark crown after GPT-4 dominated 2023. Long-context + multimodal as primary differentiators.

### Apr 2026 — Meta Muse Spark (Meta Superintelligence Labs)
**What:** First model from Meta's rebranded AI lab (post-Alexandr Wang acquisition). Native multimodal reasoning, 1M self-managed context, built-in primary-agent + sub-agent orchestration.  
**Why:** Meta's signal that the next competitive axis is native multi-agent architecture baked into the model itself — not a wrapper on top.

### Jun 2026 — Claude Fable 5 / Mythos 5 (Anthropic)
**What:** New capability tier above Opus. Released June 9, briefly suspended June 12–30 under US government export control directive, restored July 1.  
**Why:** Regulatory events (export controls) now directly affect model availability — first major instance of government intervention pausing a model release.

### Jul 2026 — GPT-5.6 Family: Sol, Terra, Luna (OpenAI)
**What:** Three-model family — different cost/speed/capability tiers — now default on ChatGPT.  
**Why:** Tiered model strategy (fast/cheap vs powerful/expensive) became industry standard. Every major lab now ships model families, not single models.

---

## Scaling Laws — Three Axes

```
               SCALE (2018–2022)            REASONING (2024+)
               ─────────────────            ─────────────────
               
  Bigger model ──────────────────►       Think longer at inference
  More data    ──────────────────►       Chain-of-thought at runtime
  More compute ──────────────────►       More tokens = better answer
  
                     +
               
               SPECIALIZATION (2025+)
               ──────────────────────
               
  Post-training refinement dominates
  Small model + domain data = beats giant generalist
  LoRA / RLHF on vertical data = huge wins
  
  All three axes now scale independently
```

---

## Agent-to-Agent Architecture (A2A, 2025)

```
           User Request
                │
                ▼
      ┌──────────────────┐
      │  Orchestrator     │   (Primary Agent — "the manager")
      │  Agent (Claude,   │
      │  GPT-5, etc.)     │
      └──────┬───────────┘
             │ delegates subtasks
    ┌────────┼────────────┐
    ▼        ▼            ▼
┌───────┐ ┌───────┐ ┌───────┐
│Search │ │ Code  │ │ Data  │   Sub-Agents
│ Agent │ │ Agent │ │ Agent │   (specialized workers)
└───┬───┘ └───┬───┘ └───┬───┘
    │         │          │
  Results  Output     Analysis
    └─────────┴──────────┘
                │
      ┌─────────▼──────────┐
      │  Orchestrator       │
      │  synthesizes →      │
      │  Final Response     │
      └─────────────────────┘
      
  MCP = how each agent connects to its tools
  A2A = how agents talk to each other
```

---

## Text-to-Video Evolution

```
2022        2023        2024         2025           2026
 │           │           │            │               │
Gen-1      Runway      Sora 1       Sora 2         Veo 3.1
(Runway)   Gen-2      (OpenAI)    + Veo 3        vs Kling 3
           │          first        first          Native 4K
           short      viral        physics        + Audio
           clips      moment       sim +          + Storyboard
                                   Veo native     + Cinematic
                                   audio          camera work
                                   
Quality: blocky → coherent → photorealistic → broadcast quality
```

---

## Reasoning: Fast vs Slow Thinking

```
       FAST MODE                    SLOW (Reasoning) MODE
       (GPT-4o, Claude Haiku)       (o1, o3, GPT-5 Deep Think)
       ─────────────────────        ──────────────────────────
       
       Input → Answer               Input → [Hidden scratchpad]
         ~1s latency                         Think...
         great for:                          Re-check...
         - chat                              Revise...
         - simple tasks                      Verify...
         - retrieval                        ──────────────
                                     Answer
                                         ~10-60s latency
                                         great for:
                                         - math proofs
                                         - complex coding
                                         - scientific reasoning
       
       GPT-5 routes between them automatically based on query complexity
```

---

## Key Paradigm Shifts

| Shift | When | Before → After |
|---|---|---|
| Embeddings | 2013 | Sparse one-hot → dense semantic vectors |
| Attention | 2017 | RNNs (sequential) → Transformers (parallel, global) |
| Scale | 2020 | Millions of params → Billions → Trillions |
| Alignment | 2022 | Predict text → Follow instructions safely |
| Multimodal | 2021–2023 | Text-only → Text + Image + Audio + Video |
| Agents | 2023 | Respond → Act (tools, memory, planning) |
| Reasoning | 2024 | Single-pass → Think-then-answer (test-time compute) |
| Open Source | 2023–2025 | Closed → Competitive open-weight models |
| Agentic Infra | 2025 | Custom integrations → MCP/A2A standard protocols |
| Video Gen | 2025 | Choppy clips → 4K + physics + sync audio |
| Multi-Agent | 2026 | Single LLM → Orchestrator + specialist sub-agents |
| AI Regulation | 2026 | Self-governed → Government export controls on models |

---

## Next Topics to Cover
- [ ] Transformers Architecture (deep dive)
- [ ] Attention Mechanisms (self, cross, multi-head)
- [ ] Training: Pre-training, SFT, RLHF, RLAIF
- [ ] RAG (Retrieval Augmented Generation)
- [ ] Agents & Tool Use patterns
- [ ] Prompt Engineering techniques
- [ ] Vector Databases
- [ ] Diffusion Models
- [ ] Multimodal Models
- [ ] Fine-tuning (LoRA, QLoRA, PEFT)
- [ ] Reasoning Models & Test-Time Compute

---

## Sources & References

### Foundational Papers
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — Original Transformer paper
- [BERT: Pre-training of Deep Bidirectional Transformers (Devlin et al., 2018)](https://arxiv.org/abs/1810.04805)
- [Language Models are Few-Shot Learners — GPT-3 (Brown et al., 2020)](https://arxiv.org/abs/2005.14165)
- [Training language models to follow instructions with human feedback — InstructGPT / RLHF (Ouyang et al., 2022)](https://arxiv.org/abs/2203.02155)
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (2025)](https://arxiv.org/abs/2501.12948)
- [A Comparative Study on Reasoning Patterns of OpenAI's o1 Model](https://arxiv.org/abs/2410.13639)

### Model Announcements
- [Introducing GPT-5 — OpenAI (Aug 2025)](https://openai.com/index/introducing-gpt-5/)
- [Sora: Creating video from text — OpenAI](https://openai.com/index/sora/)
- [Google's Year in Review: 8 Research Breakthroughs in 2025](https://blog.google/innovation-and-ai/products/2025-research-breakthroughs/)

### Industry Reports & Analysis
- [The 10 AI Developments That Defined 2025 — KDnuggets](https://www.kdnuggets.com/the-10-ai-developments-that-defined-2025)
- [State of AI Agents 2026: Autonomy is Here — Prosus](https://www.prosus.com/news-insights/2026/state-of-ai-agents-2026-autonomy-is-here)
- [What's Next for AI in 2026 — MIT Technology Review](https://www.technologyreview.com/2026/01/05/1130662/whats-next-for-ai-in-2026/)
- [6 AI Breakthroughs That Will Define 2026 — InfoWorld](https://www.infoworld.com/article/4108092/6-ai-breakthroughs-that-will-define-2026.html)
- [AI Trends in 2026: Advancements and Breakthroughs — Trigyn](https://www.trigyn.com/insights/ai-trends-2026-new-era-ai-advancements-and-breakthroughs)
- [Latest AI Breakthroughs in 2026 — Unity Media News](https://unitymedianews.com/2026/05/23/latest-ai-breakthroughs-in-2026/)
- [Generative AI Models in 2026: Top Trends — Refonte Learning](https://www.refontelearning.com/blog/generative-ai-models-in-2026-top-trends-breakthroughs-and-opportunities)

### Agents & Agentic AI
- [Agentic AI in 2026: How AI Evolved from Chatbots to Autonomous Agents — Generative Inc.](https://www.generative.inc/agentic-ai-in-2026-how-ai-went-from-chatting-to-doing)
- [Agentic AI in 2026: The Year Autonomous Agents Crossed the Chasm — Medium](https://medium.com/@mohit15856/agentic-ai-in-2026-the-year-autonomous-agents-crossed-the-chasm-a24b4ace3df7)
- [The State of AI Coding Agents (2026) — Medium](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a)
- [Future of AI Agents: Top Trends in 2026 — Blue Prism](https://www.blueprism.com/resources/blog/future-ai-agents-trends/)
- [International AI Safety Report 2026 — arXiv](https://arxiv.org/pdf/2602.21012)

### Video Generation
- [Veo 3 vs Sora by OpenAI: Side-by-Side Comparison 2026 — Powtoon](https://www.powtoon.com/blog/veo-3-vs-sora/)
- [Text-to-Video AI in 2026: Complete News Guide — Felo](https://felo.ai/blog/text-to-video-ai-in-2026-complete-news-guide-every-tool-breakthrough/)
- [Best AI Video Generator 2026: Veo 3.1 vs Sora 2 vs Kling — Tech Insider](https://tech-insider.org/best-ai-video-generator-2026/)

### Reasoning Models
- [AI Reasoning Models Explained: Test-Time Compute — Taskade](https://www.taskade.com/blog/reasoning-models)
- [Test-Time Scaling in Reasoning Models Is Not Effective for Knowledge-Intensive Tasks Yet — arXiv](https://arxiv.org/html/2509.06861v1)

### Model Trackers (Live)
- [AI Model Release Tracker — AI Flash Report](https://aiflashreport.com/model-releases.html)
- [AI Updates Today — LLM Stats](https://llm-stats.com/llm-updates)
- [Best AI Models July 2026 — FelloAI](https://felloai.com/best-ai-models/)
- [Frontier AI Companies & Labs: Complete List of Models — David Veksler](https://cheatsheets.davidveksler.com/ai-frontier.html)
