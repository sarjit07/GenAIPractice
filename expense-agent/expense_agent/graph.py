r"""LangGraph wiring for the expense-report pipeline.

Ten nodes, four conditional branch points:

    parse --> rules --(llm_indices empty?)--> metrics --> reconcile --(ok?)--> render --> verify --(ok?)--> finalize --> summary --> END
                   \--> llm ---------------------------/                  \                            \--> halt --> END
    (parse failure) -----------------------------------------------------> halt -------------------------------------> END

The two safety branches (reconcile->halt, verify->halt) are what make "never
render on unreconciled data" and "never leave a leaking report on disk"
structural guarantees of the graph, rather than something a prompt has to
remember to check. Nothing is written to `output_path` until verification of
the fully-rendered HTML (held only in memory up to that point) has passed.
"""

from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

from . import cache as cache_mod
from . import config
from . import llm_client
from . import metrics as metrics_mod
from . import parsing
from . import render
from . import rules
from . import summary as summary_mod
from . import verify as verify_mod


class AgentState(TypedDict, total=False):
    # inputs
    csv_path: str
    holder_name: str | None
    vllm_base_url: str
    vllm_model: str
    no_llm: bool
    cache_path: str
    output_path: str

    # parse -> ...
    account_masked: str
    period: str
    opening_balance: float
    closing_balance: float
    raw_transactions: list          # list[parsing.RawTransaction]

    # rules -> llm
    raw_results: list               # list[rules.CategoryResult], same order/index as raw_transactions
    llm_indices: list               # indices into raw_results still needing resolution
    cache_stats: dict

    # metrics -> reconcile
    categorized: list               # list[metrics_mod.CategorizedTransaction]
    metrics: dict
    reconciliation: dict

    # render -> verify -> finalize
    html: str
    verification: dict

    errors: list
    halted: bool


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def parse_node(state: AgentState) -> AgentState:
    try:
        parsed = parsing.parse_statement_csv(state["csv_path"])
    except parsing.StatementParseError as e:
        return {**state, "errors": state.get("errors", []) + [f"Parse error: {e}"], "halted": True}

    return {
        **state,
        "account_masked": parsed.account_masked,
        "period": parsed.period,
        "opening_balance": parsed.opening_balance,
        "closing_balance": parsed.closing_balance,
        "raw_transactions": parsed.transactions,
    }


def rule_categorize_node(state: AgentState) -> AgentState:
    holder_name = state.get("holder_name")
    # A manual correction (scripts/correct.py) wins over every rule and the
    # LLM, unconditionally — checked first, for every transaction, not just
    # the ones the rules would otherwise send to the LLM.
    mc = cache_mod.MerchantCache(state.get("cache_path", config.DEFAULT_CACHE_PATH))
    results = [
        rules.apply_manual_override(t.narration_masked, mc) or rules.categorize_transaction(t, holder_name)
        for t in state["raw_transactions"]
    ]
    llm_indices = [i for i, r in enumerate(results) if r.needs_llm]
    return {**state, "raw_results": results, "llm_indices": llm_indices}


def llm_categorize_node(state: AgentState) -> AgentState:
    results = list(state["raw_results"])
    indices = state["llm_indices"]

    if state.get("no_llm"):
        for i in indices:
            r = results[i]
            fallback_cat = r.llm_candidate or "Uncategorized"
            results[i] = rules.CategoryResult(
                fallback_cat, "low", "LLM disabled (--no-llm); rule-based best guess only.",
            )
        return {**state, "raw_results": results, "cache_stats": {"hits": 0, "misses": 0, "calls": 0}}

    mc = cache_mod.MerchantCache(state.get("cache_path", config.DEFAULT_CACHE_PATH))
    hits = calls = 0

    for i in indices:
        r = results[i]
        fragment = r.fragment or ""
        cached = mc.get(fragment) if fragment else None
        if cached:
            hits += 1
            results[i] = rules.CategoryResult(cached.category, cached.confidence, cached.reason)
            continue

        if not fragment:
            results[i] = rules.CategoryResult(
                "Uncategorized", "low", "No merchant text available to classify.",
            )
            continue

        calls += 1
        clf = llm_client.classify_merchant(
            fragment, r.llm_candidate,
            base_url=state.get("vllm_base_url"), model=state.get("vllm_model"),
        )
        mc.set(fragment, cache_mod.CachedClassification(
            clf.category, clf.confidence, clf.reason, source="llm",
        ))
        results[i] = rules.CategoryResult(clf.category, clf.confidence, clf.reason)

    mc.save()
    return {
        **state,
        "raw_results": results,
        "cache_stats": {"hits": hits, "misses": len(indices) - hits, "calls": calls},
    }


def metrics_node(state: AgentState) -> AgentState:
    categorized = [
        metrics_mod.build_categorized(t, r)
        for t, r in zip(state["raw_transactions"], state["raw_results"])
    ]
    computed = metrics_mod.compute_metrics(
        state["account_masked"], state["period"],
        state["opening_balance"], state["closing_balance"], categorized,
    )
    return {**state, "categorized": categorized, "metrics": computed}


def reconcile_node(state: AgentState) -> AgentState:
    ok, detail = metrics_mod.reconcile(
        state["opening_balance"], state["closing_balance"], state["categorized"],
    )
    reconciliation = {"ok": ok, "detail": detail}
    if not ok:
        return {
            **state, "reconciliation": reconciliation,
            "errors": state.get("errors", []) + [detail], "halted": True,
        }
    return {**state, "reconciliation": reconciliation}


def render_node(state: AgentState) -> AgentState:
    html = render.render_html(state["metrics"])
    return {**state, "html": html}


def verify_node(state: AgentState) -> AgentState:
    ok, findings = verify_mod.verify_html(state["html"])
    verification = {"ok": ok, "findings": findings}
    if not ok:
        return {
            **state, "verification": verification,
            "errors": state.get("errors", []) + findings, "halted": True,
        }
    return {**state, "verification": verification}


def finalize_node(state: AgentState) -> AgentState:
    out_path = Path(state.get("output_path") or "outputs/statement-report.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(state["html"])
    return {**state, "output_path": str(out_path)}


def halt_node(state: AgentState) -> AgentState:
    return {**state, "halted": True}


def summary_node(state: AgentState) -> AgentState:
    summary_mod.print_summary(state)
    return state


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def _route_after_parse(state: AgentState) -> str:
    return "halt" if state.get("halted") else "rules"


def _route_after_rules(state: AgentState) -> str:
    return "llm" if state.get("llm_indices") else "metrics"


def _route_after_reconcile(state: AgentState) -> str:
    return "render" if state["reconciliation"]["ok"] else "halt"


def _route_after_verify(state: AgentState) -> str:
    return "finalize" if state["verification"]["ok"] else "halt"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("parse", parse_node)
    g.add_node("rules", rule_categorize_node)
    g.add_node("llm", llm_categorize_node)
    g.add_node("metrics", metrics_node)
    g.add_node("reconcile", reconcile_node)
    g.add_node("render", render_node)
    g.add_node("verify", verify_node)
    g.add_node("finalize", finalize_node)
    g.add_node("halt", halt_node)
    g.add_node("summary", summary_node)

    g.set_entry_point("parse")
    g.add_conditional_edges("parse", _route_after_parse, {"rules": "rules", "halt": "halt"})
    g.add_conditional_edges("rules", _route_after_rules, {"llm": "llm", "metrics": "metrics"})
    g.add_edge("llm", "metrics")
    g.add_edge("metrics", "reconcile")
    g.add_conditional_edges("reconcile", _route_after_reconcile, {"render": "render", "halt": "halt"})
    g.add_edge("render", "verify")
    g.add_conditional_edges("verify", _route_after_verify, {"finalize": "finalize", "halt": "halt"})
    g.add_edge("finalize", "summary")
    g.add_edge("halt", END)
    g.add_edge("summary", END)

    return g.compile()


def run_pipeline(
    csv_path: str,
    holder_name: str | None = None,
    no_llm: bool = False,
    vllm_base_url: str | None = None,
    vllm_model: str | None = None,
    cache_path: str | None = None,
    output_path: str | None = None,
) -> AgentState:
    graph = build_graph()
    initial: AgentState = {
        "csv_path": csv_path,
        "holder_name": holder_name,
        "no_llm": no_llm,
        "vllm_base_url": vllm_base_url or config.DEFAULT_VLLM_BASE_URL,
        "vllm_model": vllm_model or config.DEFAULT_VLLM_MODEL,
        "cache_path": cache_path or config.DEFAULT_CACHE_PATH,
        "output_path": output_path or "outputs/statement-report.html",
        "errors": [],
        "halted": False,
    }
    return graph.invoke(initial)
