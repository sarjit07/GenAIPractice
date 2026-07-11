# Agentic AI

---

## What Makes AI "Agentic"

An agent is an LLM wrapped in a loop that lets it act, observe results, and decide its own next step toward a goal — rather than producing one response and stopping.

```mermaid
graph TD
    A(("Agentic AI<br/>reason → act → observe"))
    A --> C1["1. Autonomy"]
    A --> C2["2. Planning"]
    A --> C3["3. Tool Use"]
    A --> C4["4. Feedback Loop"]
    A --> C5["5. Memory"]
    A --> C6["6. Multi-step"]
    A --> C7["7. Self-Correction"]
    A --> C8["8. Guardrails"]

    classDef center fill:#fcfcfb,stroke:#0b0b0b,stroke-width:2px,color:#0b0b0b,font-weight:bold;
    classDef c1 fill:#2a78d6,color:#fff,stroke:#184f95,stroke-width:1px;
    classDef c2 fill:#1baf7a,color:#fff,stroke:#128a5e,stroke-width:1px;
    classDef c3 fill:#eda100,color:#fff,stroke:#a87400,stroke-width:1px;
    classDef c4 fill:#008300,color:#fff,stroke:#005c00,stroke-width:1px;
    classDef c5 fill:#4a3aa7,color:#fff,stroke:#332876,stroke-width:1px;
    classDef c6 fill:#e34948,color:#fff,stroke:#a92e2d,stroke-width:1px;
    classDef c7 fill:#e87ba4,color:#fff,stroke:#b5537a,stroke-width:1px;
    classDef c8 fill:#eb6834,color:#fff,stroke:#b04a22,stroke-width:1px;

    class A center;
    class C1 c1;
    class C2 c2;
    class C3 c3;
    class C4 c4;
    class C5 c5;
    class C6 c6;
    class C7 c7;
    class C8 c8;
```

## Key Characteristics

1. **Autonomy** — it decides *what to do next*, not just what to say. Given a goal, it chooses actions without a human specifying each step.
2. **Goal-directed planning** — it decomposes a high-level objective into sub-tasks, often re-planning as it learns new information (vs. a single-shot prompt→response).
3. **Tool use / action-taking** — it can act on the world (call APIs, run code, browse, write files), not just generate text. This is what turns "answering" into "doing."
4. **Observation & feedback loop** — after acting, it reads the result back into context and adjusts (the core of ReAct: Reason → Act → Observe, repeated).
5. **Persistent state / memory** — it tracks progress across many steps (sometimes minutes to hours), which requires managing what stays in context vs. gets summarized or discarded.
6. **Iterative, multi-step execution** — unlike a chatbot turn, an agentic task can run dozens of steps before producing a final result.
7. **Self-correction** — it can notice a failed action or wrong turn and recover (retry, backtrack, ask for help) rather than failing silently.
8. **Bounded but real autonomy** — it typically operates within guardrails (permissions, tool scopes, max-steps) since full unconstrained autonomy is a reliability and safety risk.

---

## Agent vs. Chatbot vs. Plain LLM Call

| | Plain LLM call | Chatbot | Agent |
|---|---|---|---|
| Turns | One prompt → one response | Multi-turn conversation | Multi-step task execution |
| Acts on the world? | No | No (usually) | Yes — tools, APIs, code |
| Decides next step? | No (human decides) | Partially (human drives) | Yes — model drives |
| Has memory of its own actions? | No | Conversation history only | Tracks actions + observations |
| Stops when? | After one response | After one reply | When goal is met or max steps hit |

---

## Key Components of an Agentic AI System

<svg viewBox="0 0 720 780" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="components-title">
  <title id="components-title">Architecture diagram of the key components of an agentic AI system</title>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#898781"/>
    </marker>
  </defs>

  <rect x="1" y="1" width="718" height="778" rx="16" fill="#fcfcfb" stroke="#e1e0d9" stroke-width="2"/>

  <!-- User / Goal -->
  <rect x="260" y="24" width="200" height="56" rx="10" fill="#e1e0d9"/>
  <text x="360" y="58" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="700" fill="#0b0b0b">User / Goal</text>

  <line x1="360" y1="80" x2="360" y2="110" stroke="#898781" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Agent Core -->
  <rect x="210" y="112" width="300" height="90" rx="12" fill="#2a78d6"/>
  <text x="360" y="150" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16" font-weight="700" fill="#ffffff">Agent Core (LLM)</text>
  <text x="360" y="172" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#ffffff">Reasoning &amp; decision-making</text>

  <!-- Memory, bidirectional link to Agent Core -->
  <rect x="550" y="120" width="150" height="76" rx="12" fill="#eda100"/>
  <text x="625" y="152" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="700" fill="#0b0b0b">Memory</text>
  <text x="625" y="170" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#0b0b0b">Short-term + long-term</text>
  <line x1="510" y1="157" x2="550" y2="157" stroke="#898781" stroke-width="2" marker-end="url(#arrow)" marker-start="url(#arrow)"/>

  <line x1="360" y1="202" x2="360" y2="228" stroke="#898781" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Planner -->
  <rect x="260" y="230" width="200" height="70" rx="12" fill="#1baf7a"/>
  <text x="360" y="260" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="700" fill="#0b0b0b">Planner</text>
  <text x="360" y="279" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#0b0b0b">Task decomposition &amp; strategy</text>

  <line x1="360" y1="300" x2="360" y2="370" stroke="#898781" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Guardrails wrapper (dashed, encloses Tool layer) -->
  <rect x="190" y="326" width="340" height="128" rx="14" fill="none" stroke="#e34948" stroke-width="2" stroke-dasharray="8 5"/>
  <text x="210" y="344" font-family="system-ui,sans-serif" font-size="12" font-weight="700" fill="#e34948">Guardrails</text>
  <text x="210" y="358" font-family="system-ui,sans-serif" font-size="9.5" fill="#e34948">permissions · scopes · max-steps</text>

  <!-- Tool / Action Layer -->
  <rect x="220" y="372" width="280" height="70" rx="12" fill="#008300"/>
  <text x="360" y="402" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="700" fill="#ffffff">Tool / Action Layer</text>
  <text x="360" y="421" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#ffffff">APIs · code exec · search · files</text>

  <line x1="360" y1="442" x2="360" y2="480" stroke="#898781" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Environment -->
  <rect x="260" y="482" width="200" height="70" rx="12" fill="#4a3aa7"/>
  <text x="360" y="512" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="700" fill="#ffffff">Environment</text>
  <text x="360" y="531" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#ffffff">External world: web, DB, filesystem</text>

  <!-- Feedback loop back to Agent Core -->
  <path d="M460,517 C630,517 630,190 512,190" fill="none" stroke="#898781" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arrow)"/>
  <text x="644" y="360" text-anchor="middle" font-family="system-ui,sans-serif" font-size="12" fill="#52514e" transform="rotate(-90 644 360)">Observation / feedback</text>

  <!-- legend caption -->
  <text x="360" y="610" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#898781">Solid arrows = control flow · dashed = feedback &amp; guardrail scope</text>
</svg>

- **Agent Core (LLM)** — the reasoning engine. Interprets the goal, consults memory, and decides the next action.
- **Planner** — breaks the goal into sub-tasks and orders them; re-plans when a step fails or new information arrives.
- **Memory** — short-term (current context/scratchpad) and long-term (vector store, files, past runs) that the core reads from and writes to.
- **Tool / Action Layer** — the interface to the outside world: API calls, code execution, search, file I/O (this is what MCP standardizes).
- **Environment** — whatever the tools actually touch: a filesystem, a database, a web page, another service.
- **Guardrails** — permissions, tool scopes, and max-step limits that bound what the core is allowed to do — wraps the action layer, not just a policy on paper.
- **Observation / feedback loop** (dashed) — the result of every action flows back into the core's context, closing the Reason → Act → Observe cycle.

## Next Sections to Write
- [ ] The Agent Loop (ReAct: Reason → Act → Observe) — deep dive
- [ ] Tool Use / Function Calling — how models call tools, schemas, error handling
- [ ] Memory & Context Management — short-term vs long-term, summarization, forgetting
- [ ] Planning strategies — ReAct vs. plan-and-execute vs. tree-of-thought
- [ ] Multi-Agent Orchestration — orchestrator + sub-agents, when to delegate
- [ ] MCP (Model Context Protocol) — agent-to-tool standard
- [ ] A2A (Agent-to-Agent Protocol) — agent-to-agent standard
- [ ] Failure modes — infinite loops, tool misuse, hallucinated actions, guardrails
- [ ] Evaluating agents — success criteria beyond single-turn accuracy
