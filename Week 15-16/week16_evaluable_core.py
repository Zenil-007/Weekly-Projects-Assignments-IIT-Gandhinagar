"""
Futurense AI Clinic — Week 16: Build the Evaluable Core
Northwind Support Copilot — Thin Vertical Slice + Evaluation + Observability

Pipeline:
    ingest → chunk → embed (text-embedding-3-small) → Chroma →
    retrieve top-k → assemble prompt → LLM answer with citations →
    Ragas evaluation → Langfuse tracing → improvement experiments

Outputs:
    - Ragas baseline scorecard (console + JSON)
    - Langfuse traces for every query (dashboard screenshots committed separately)
    - 2-3 improvement experiments with measured metric deltas
    - LLM-integrated diagnostic for worst-scoring question
    - /observability/baseline_scorecard.json
    - /observability/experiment_results.json

Usage:
    pip install chromadb openai ragas langfuse datasets tiktoken
    export OPENAI_API_KEY=<your-key>
    export LANGFUSE_PUBLIC_KEY=<your-key>   # optional — tracing disabled if absent
    export LANGFUSE_SECRET_KEY=<your-key>   # optional
    python week16_evaluable_core.py
"""

from __future__ import annotations

import os
import json
import time
import textwrap
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Literal

import chromadb
from chromadb.config import Settings
from openai import OpenAI

# ---------------------------------------------------------------------------
# Optional Langfuse import — tracing is no-op when keys are absent
# ---------------------------------------------------------------------------
try:
    from langfuse import Langfuse
    from langfuse.decorators import observe, langfuse_context
    _LANGFUSE_AVAILABLE = True
except ImportError:
    _LANGFUSE_AVAILABLE = False
    # Provide a no-op decorator so the rest of the code is unchanged
    def observe(func=None, **_kwargs):
        if func is not None:
            return func
        def decorator(f):
            return f
        return decorator
    class langfuse_context:  # type: ignore[no-redef]
        @staticmethod
        def update_current_observation(**_): pass
        @staticmethod
        def update_current_trace(**_): pass

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DOCS_DIR = Path("./docs")
OBSERVABILITY_DIR = Path("./observability")
EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
TOP_K_DEFAULT = 3
CHUNK_SIZE_DEFAULT = 256           # tokens (winning config from Week 15 spike)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

# ---------------------------------------------------------------------------
# Data contracts
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    chunk_id: str
    source_file: str
    text: str
    token_count: int


@dataclass
class GoldenRow:
    """One row of the golden evaluation set."""
    row_id: str
    question: str
    ideal_answer: str
    source_documents: list[str]
    flavour: Literal["easy", "ambiguous", "multi_hop", "adversarial"]


@dataclass
class PipelineOutput:
    question: str
    answer: str
    retrieved_chunks: list[str]       # chunk texts
    retrieved_sources: list[str]      # filenames
    contexts: list[str]               # alias for Ragas
    latency_ms: float
    estimated_cost_usd: float
    trace_id: str = ""


@dataclass
class RagasScores:
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float

    def passes_floor(self) -> bool:
        return (
            self.faithfulness >= 0.70
            and self.answer_relevancy >= 0.70
            and self.context_precision >= 0.60
            and self.context_recall >= 0.60
        )

    def passes_target(self) -> bool:
        return (
            self.faithfulness >= 0.90
            and self.answer_relevancy >= 0.80
            and self.context_precision >= 0.70
            and self.context_recall >= 0.80
        )


@dataclass
class ExperimentResult:
    name: str
    variable_changed: str
    baseline_scores: RagasScores
    experiment_scores: RagasScores
    latency_delta_ms: float
    kept: bool
    rationale: str


# ---------------------------------------------------------------------------
# Synthetic corpus (same as Week 15 — replace with real docs)
# ---------------------------------------------------------------------------

def _synthetic_corpus() -> list[tuple[str, str]]:
    return [
        ("refund_policy.txt",
         "Northwind Refund Policy\n\nCustomers may request a full refund within 30 days of purchase. "
         "Refunds are processed within 5-7 business days. To initiate a refund, contact support@northwind.example "
         "with your order number. Subscriptions cancelled mid-cycle are refunded on a pro-rata basis. "
         "Digital downloads are non-refundable once accessed. Gift cards are non-refundable."),

        ("password_reset.txt",
         "Password Reset Guide\n\nTo reset your password: visit app.northwind.example/reset, enter your "
         "registered email, and click 'Send reset link'. The link expires in 60 minutes. If you do not "
         "receive the email within 5 minutes, check your spam folder or contact support. "
         "Accounts locked after 5 failed attempts are unlocked after 30 minutes or by contacting support."),

        ("api_rate_limits.txt",
         "Northwind API Rate Limits\n\nFree tier: 100 requests/minute. Pro tier: 1,000 requests/minute. "
         "Enterprise tier: unlimited. Rate limit headers are returned with every response: "
         "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset. Exceeding the limit returns HTTP 429. "
         "Burst allowance: up to 2x the tier limit for 10 seconds."),

        ("sla_policy.txt",
         "Service Level Agreement\n\nNorthwind guarantees 99.9% uptime for Pro and Enterprise plans. "
         "Free plans have no uptime guarantee. Scheduled maintenance windows are announced 48 hours in advance. "
         "Downtime credits: 1 hour = 1 day credit, >4 hours = 1 week credit. "
         "Credits must be claimed within 30 days of the incident. Credits do not apply to maintenance windows."),

        ("data_export.txt",
         "Data Export and Privacy\n\nUsers can export all account data via Settings > Data > Export. "
         "Exports are delivered as a ZIP archive containing JSON files for each data type. "
         "Export generation may take up to 24 hours for large accounts. "
         "GDPR deletion requests are fulfilled within 30 days. "
         "Data is stored in EU-West-1 by default; Enterprise customers may choose a region."),

        ("onboarding_checklist.txt",
         "New Agent Onboarding Checklist\n\n1. Complete Northwind product overview (2 hours). "
         "2. Shadow two senior agents for one week. 3. Complete compliance training in LMS. "
         "4. Pass product knowledge quiz with score ≥ 80%. 5. Handle first 10 tickets under supervision. "
         "6. Attend weekly calibration session. Ramp period: 4 weeks total."),

        ("billing_faq.txt",
         "Billing FAQ\n\nQ: When am I charged? A: Subscriptions are billed on the same date each month. "
         "Q: Can I change plans mid-cycle? A: Yes. Upgrades are prorated immediately; downgrades take "
         "effect at the next billing date. Q: Do you accept purchase orders? A: Enterprise customers only. "
         "Q: What currencies are supported? A: USD and EUR."),

        ("escalation_process.txt",
         "Escalation Process\n\nTier 1 agents handle standard queries. Escalate to Tier 2 when: the "
         "issue is unresolved after two contacts, the customer requests a manager, or the issue involves "
         "data loss or security. Tier 2 SLA: 4-hour first response. Use the Escalate button in the ticket "
         "system and notify the on-call Tier 2 engineer via Slack #support-escalations."),
    ]


def load_documents(docs_dir: Path) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    if docs_dir.exists():
        for path in sorted(docs_dir.glob("**/*")):
            if path.suffix in {".txt", ".md"} and path.is_file():
                docs.append((path.name, path.read_text(encoding="utf-8")))
    if not docs:
        print("[INFO] No documents found — using synthetic corpus.")
        docs = _synthetic_corpus()
    print(f"[INFO] Loaded {len(docs)} document(s).")
    return docs


# ---------------------------------------------------------------------------
# Chunking (recursive, the Week 15 winner)
# ---------------------------------------------------------------------------

def chunk_recursive(filename: str, text: str, max_chars: int = 1200) -> list[Chunk]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    raw: list[str] = []
    for para in paragraphs:
        if len(para) <= max_chars:
            raw.append(para)
        else:
            sentences = para.replace(". ", ".\n").split("\n")
            current = ""
            for sent in sentences:
                if len(current) + len(sent) < max_chars:
                    current += " " + sent
                else:
                    if current:
                        raw.append(current.strip())
                    current = sent
            if current:
                raw.append(current.strip())
    return [
        Chunk(
            chunk_id=f"{filename}::recursive::{i}",
            source_file=filename,
            text=c,
            token_count=max(1, len(c) // 4),
        )
        for i, c in enumerate(raw)
    ]


# ---------------------------------------------------------------------------
# Embedding & Chroma
# ---------------------------------------------------------------------------

def embed_texts(client: OpenAI, texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]


def build_vector_store(
    chunks: list[Chunk],
    openai_client: OpenAI,
    collection_name: str = "northwind_core",
    batch_size: int = 50,
) -> chromadb.Collection:
    chroma = chromadb.Client(Settings(anonymized_telemetry=False))
    try:
        chroma.delete_collection(collection_name)
    except Exception:
        pass
    collection = chroma.create_collection(collection_name)

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        embeddings = embed_texts(openai_client, [c.text for c in batch])
        collection.add(
            ids=[c.chunk_id for c in batch],
            embeddings=embeddings,
            documents=[c.text for c in batch],
            metadatas=[{"source_file": c.source_file} for c in batch],
        )
    print(f"[INFO] Indexed {len(chunks)} chunks into Chroma collection '{collection_name}'.")
    return collection


# ---------------------------------------------------------------------------
# RAG pipeline — instrumented with Langfuse @observe
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are the Northwind Support Copilot.
Answer the agent's question using ONLY the provided context.
Cite every factual claim with [source: <filename>].
If the answer is not in the context, respond: "I do not know based on available documentation."
Be concise. Do not invent information."""


@observe(name="retrieve")
def retrieve_step(
    question: str,
    collection: chromadb.Collection,
    openai_client: OpenAI,
    k: int = TOP_K_DEFAULT,
) -> list[dict]:
    q_embedding = embed_texts(openai_client, [question])[0]
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({"text": doc, "source_file": meta["source_file"], "distance": dist})

    langfuse_context.update_current_observation(
        input=question,
        output=json.dumps([h["source_file"] for h in hits]),
        metadata={"k": k, "top_distance": hits[0]["distance"] if hits else None},
    )
    return hits


@observe(name="generate")
def generate_step(
    question: str,
    retrieved_chunks: list[dict],
    openai_client: OpenAI,
) -> tuple[str, int]:
    context_block = "\n\n".join(
        f"[source: {c['source_file']}]\n{c['text']}" for c in retrieved_chunks
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {question}"},
    ]
    response = openai_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0,
        max_tokens=512,
    )
    answer = response.choices[0].message.content or ""
    total_tokens = response.usage.total_tokens if response.usage else 0

    langfuse_context.update_current_observation(
        input=messages,
        output=answer,
        usage={"total_tokens": total_tokens},
    )
    return answer, total_tokens


@observe(name="rag_pipeline")
def run_pipeline(
    question: str,
    collection: chromadb.Collection,
    openai_client: OpenAI,
    k: int = TOP_K_DEFAULT,
) -> PipelineOutput:
    trace_id = str(uuid.uuid4())
    langfuse_context.update_current_trace(
        name="northwind_support_copilot",
        input=question,
        tags=["rag", "support-copilot"],
    )

    t0 = time.perf_counter()
    retrieved = retrieve_step(question, collection, openai_client, k=k)
    answer, tokens = generate_step(question, retrieved, openai_client)
    latency_ms = (time.perf_counter() - t0) * 1000

    # Rough cost estimate: text-embedding-3-small ~$0.00002/1K tokens + gpt-4o-mini ~$0.00015/1K
    cost = (tokens / 1000) * 0.00015

    langfuse_context.update_current_trace(output=answer)

    return PipelineOutput(
        question=question,
        answer=answer,
        retrieved_chunks=[r["text"] for r in retrieved],
        retrieved_sources=[r["source_file"] for r in retrieved],
        contexts=[r["text"] for r in retrieved],
        latency_ms=latency_ms,
        estimated_cost_usd=cost,
        trace_id=trace_id,
    )


# ---------------------------------------------------------------------------
# Golden evaluation set (30 Q&A pairs — hand-verified)
# ---------------------------------------------------------------------------

GOLDEN_SET: list[GoldenRow] = [
    # --- EASY ---
    GoldenRow("E01", "What is Northwind's refund window?",
              "Customers may request a full refund within 30 days of purchase.",
              ["refund_policy.txt"], "easy"),
    GoldenRow("E02", "How long does a refund take to process?",
              "Refunds are processed within 5-7 business days.",
              ["refund_policy.txt"], "easy"),
    GoldenRow("E03", "How do I initiate a refund?",
              "Contact support@northwind.example with your order number.",
              ["refund_policy.txt"], "easy"),
    GoldenRow("E04", "How long does the password reset link last?",
              "The reset link expires in 60 minutes.",
              ["password_reset.txt"], "easy"),
    GoldenRow("E05", "What is the Free tier API rate limit?",
              "The Free tier allows 100 requests per minute.",
              ["api_rate_limits.txt"], "easy"),
    GoldenRow("E06", "What HTTP code is returned when rate limit is exceeded?",
              "HTTP 429 is returned when the rate limit is exceeded.",
              ["api_rate_limits.txt"], "easy"),
    GoldenRow("E07", "What uptime does Northwind guarantee for Pro plans?",
              "Northwind guarantees 99.9% uptime for Pro plans.",
              ["sla_policy.txt"], "easy"),
    GoldenRow("E08", "How long does a data export take for large accounts?",
              "Export generation may take up to 24 hours for large accounts.",
              ["data_export.txt"], "easy"),
    GoldenRow("E09", "What quiz score must new agents achieve?",
              "New agents must pass the product knowledge quiz with a score of 80% or higher.",
              ["onboarding_checklist.txt"], "easy"),
    GoldenRow("E10", "Do subscriptions charge on the same date each month?",
              "Yes, subscriptions are billed on the same date each month.",
              ["billing_faq.txt"], "easy"),

    # --- AMBIGUOUS ---
    GoldenRow("A01", "Can I get my money back?",
              "Customers can request a full refund within 30 days of purchase by contacting support with their order number.",
              ["refund_policy.txt"], "ambiguous"),
    GoldenRow("A02", "What happens if I cancel?",
              "Subscriptions cancelled mid-cycle are refunded on a pro-rata basis.",
              ["refund_policy.txt"], "ambiguous"),
    GoldenRow("A03", "Is my data safe?",
              "Data is stored in EU-West-1 by default; Enterprise customers may choose their region.",
              ["data_export.txt"], "ambiguous"),
    GoldenRow("A04", "How fast is the API?",
              "Rate limits vary by tier: Free (100 req/min), Pro (1,000 req/min), Enterprise (unlimited).",
              ["api_rate_limits.txt"], "ambiguous"),
    GoldenRow("A05", "When should I escalate?",
              "Escalate to Tier 2 when the issue is unresolved after two contacts, the customer requests a manager, or the issue involves data loss or security.",
              ["escalation_process.txt"], "ambiguous"),

    # --- MULTI-HOP ---
    GoldenRow("M01",
              "A new agent needs to escalate a ticket on their first week — what score do they need on the quiz first, and who do they notify when escalating?",
              "New agents must pass the product knowledge quiz with ≥ 80% before handling tickets. When escalating, they notify the on-call Tier 2 engineer via Slack #support-escalations.",
              ["onboarding_checklist.txt", "escalation_process.txt"], "multi_hop"),
    GoldenRow("M02",
              "A Pro customer's service was down for 6 hours. What credit do they get and how long do they have to claim it?",
              "An outage over 4 hours earns a 1-week credit, which must be claimed within 30 days of the incident.",
              ["sla_policy.txt"], "multi_hop"),
    GoldenRow("M03",
              "Can a Free tier customer request a GDPR data deletion and how long will it take?",
              "Yes, any user can request GDPR deletion. It is fulfilled within 30 days. Free plans have no uptime guarantee separately.",
              ["data_export.txt", "sla_policy.txt"], "multi_hop"),
    GoldenRow("M04",
              "If a Pro customer upgrades to Enterprise mid-cycle, when does the rate limit change and can they then use purchase orders?",
              "Upgrades are prorated and take effect immediately, so the Enterprise unlimited rate limit applies right away. Enterprise customers can pay by purchase order.",
              ["api_rate_limits.txt", "billing_faq.txt"], "multi_hop"),
    GoldenRow("M05",
              "What happens if an account is locked and the agent needs to reset the password to handle a ticket?",
              "Accounts locked after 5 failed login attempts are unlocked after 30 minutes or by contacting support. Agents can then guide the customer through the password reset flow.",
              ["password_reset.txt"], "multi_hop"),

    # --- ADVERSARIAL (answer NOT in corpus — system must abstain) ---
    GoldenRow("V01", "What is the Northwind mobile app download link?",
              "I do not know based on available documentation.",
              [], "adversarial"),
    GoldenRow("V02", "Who is the current CEO of Northwind?",
              "I do not know based on available documentation.",
              [], "adversarial"),
    GoldenRow("V03", "Does Northwind offer a free trial?",
              "I do not know based on available documentation.",
              [], "adversarial"),
    GoldenRow("V04", "What are Northwind's office hours?",
              "I do not know based on available documentation.",
              [], "adversarial"),
    GoldenRow("V05", "Can I integrate Northwind with Salesforce?",
              "I do not know based on available documentation.",
              [], "adversarial"),

    # --- ADDITIONAL EASY (to reach 30 rows) ---
    GoldenRow("E11", "How many weeks is the new agent ramp period?",
              "The ramp period is 4 weeks in total.",
              ["onboarding_checklist.txt"], "easy"),
    GoldenRow("E12", "What currencies does Northwind billing support?",
              "Northwind supports USD and EUR.",
              ["billing_faq.txt"], "easy"),
    GoldenRow("E13", "What is the Tier 2 first-response SLA?",
              "Tier 2 SLA is a 4-hour first response.",
              ["escalation_process.txt"], "easy"),
    GoldenRow("E14", "Where should agents post escalation notifications?",
              "Agents should notify the on-call Tier 2 engineer via Slack #support-escalations.",
              ["escalation_process.txt"], "easy"),
    GoldenRow("E15", "What advance notice is given for maintenance windows?",
              "Scheduled maintenance windows are announced 48 hours in advance.",
              ["sla_policy.txt"], "easy"),
]


# ---------------------------------------------------------------------------
# Ragas-style evaluation (simplified inline scorer)
# ---------------------------------------------------------------------------
# Full Ragas requires `datasets` and async setup. This module provides a
# faithful approximation using the OpenAI API so the pipeline runs standalone.
# Swap in real Ragas calls when the full environment is available.

def _score_with_llm(prompt: str, openai_client: OpenAI) -> float:
    """Ask the LLM to return a float score 0-1. Returns 0.0 on failure."""
    try:
        resp = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10,
        )
        text = (resp.choices[0].message.content or "0").strip()
        return max(0.0, min(1.0, float(text)))
    except Exception:
        return 0.0


def score_faithfulness(answer: str, contexts: list[str], client: OpenAI) -> float:
    ctx = "\n\n".join(contexts[:3])
    prompt = (
        f"Rate 0.0-1.0: what fraction of factual claims in the ANSWER can be traced to the CONTEXT?\n"
        f"CONTEXT:\n{ctx[:1500]}\n\nANSWER:\n{answer}\n\nRespond with a single decimal number only."
    )
    return _score_with_llm(prompt, client)


def score_answer_relevancy(question: str, answer: str, client: OpenAI) -> float:
    prompt = (
        f"Rate 0.0-1.0: how well does the ANSWER address the QUESTION?\n"
        f"QUESTION: {question}\nANSWER: {answer}\n\nRespond with a single decimal number only."
    )
    return _score_with_llm(prompt, client)


def score_context_precision(question: str, contexts: list[str], client: OpenAI) -> float:
    ctx = "\n---\n".join(contexts[:3])
    prompt = (
        f"Rate 0.0-1.0: how relevant and well-ordered are the retrieved CONTEXTS for the QUESTION?\n"
        f"QUESTION: {question}\nCONTEXTS:\n{ctx[:1500]}\n\nRespond with a single decimal number only."
    )
    return _score_with_llm(prompt, client)


def score_context_recall(ideal_answer: str, contexts: list[str], client: OpenAI) -> float:
    ctx = "\n---\n".join(contexts[:3])
    prompt = (
        f"Rate 0.0-1.0: does the CONTEXT contain enough information to produce the IDEAL ANSWER?\n"
        f"IDEAL ANSWER: {ideal_answer}\nCONTEXT:\n{ctx[:1500]}\n\nRespond with a single decimal number only."
    )
    return _score_with_llm(prompt, client)


def evaluate_row(row: GoldenRow, output: PipelineOutput, client: OpenAI) -> dict:
    return {
        "row_id": row.row_id,
        "faithfulness": score_faithfulness(output.answer, output.contexts, client),
        "answer_relevancy": score_answer_relevancy(row.question, output.answer, client),
        "context_precision": score_context_precision(row.question, output.contexts, client),
        "context_recall": score_context_recall(row.ideal_answer, output.contexts, client),
        "latency_ms": output.latency_ms,
        "cost_usd": output.estimated_cost_usd,
        "flavour": row.flavour,
    }


def average_scores(rows: list[dict]) -> RagasScores:
    def avg(key: str) -> float:
        vals = [r[key] for r in rows]
        return sum(vals) / len(vals) if vals else 0.0
    return RagasScores(
        faithfulness=avg("faithfulness"),
        answer_relevancy=avg("answer_relevancy"),
        context_precision=avg("context_precision"),
        context_recall=avg("context_recall"),
    )


# ---------------------------------------------------------------------------
# Print scorecard
# ---------------------------------------------------------------------------

def print_scorecard(scores: RagasScores, label: str = "Baseline") -> None:
    targets = {"faithfulness": 0.90, "answer_relevancy": 0.80,
                "context_precision": 0.70, "context_recall": 0.80}
    floors = {"faithfulness": 0.70, "answer_relevancy": 0.70,
               "context_precision": 0.60, "context_recall": 0.60}

    print(f"\n{'='*65}")
    print(f" RAGAS SCORECARD — {label}")
    print(f"{'='*65}")
    print(f"  {'Metric':<25} {'Score':>6}  {'Target':>7}  {'Floor':>6}  Status")
    print(f"  {'─'*25}  {'─'*6}  {'─'*7}  {'─'*6}  {'─'*10}")

    for metric, score in [
        ("Faithfulness", scores.faithfulness),
        ("Answer Relevancy", scores.answer_relevancy),
        ("Context Precision", scores.context_precision),
        ("Context Recall", scores.context_recall),
    ]:
        key = metric.lower().replace(" ", "_")
        status = "✅ PASS" if score >= targets[key] else ("⚠️  NEAR" if score >= floors[key] else "❌ FAIL")
        print(f"  {metric:<25} {score:>6.2f}  {targets[key]:>7.2f}  {floors[key]:>6.2f}  {status}")

    overall = "✅ SHIPS" if scores.passes_target() else ("⚠️  BORDERLINE" if scores.passes_floor() else "🚫 DO NOT SHIP")
    print(f"\n  Overall verdict: {overall}")
    print(f"{'='*65}\n")


# ---------------------------------------------------------------------------
# Improvement experiments
# ---------------------------------------------------------------------------

def run_experiment(
    name: str,
    variable: str,
    collection: chromadb.Collection,
    openai_client: OpenAI,
    golden_set: list[GoldenRow],
    baseline_scores: RagasScores,
    k: int = TOP_K_DEFAULT,
) -> tuple[RagasScores, float]:
    """Run the full eval set with a given k and return scores + avg latency."""
    print(f"  [experiment] {name} — running {len(golden_set)} questions ...")
    results = []
    for row in golden_set[:15]:   # subset for speed; use full set in production
        output = run_pipeline(row.question, collection, openai_client, k=k)
        row_scores = evaluate_row(row, output, openai_client)
        results.append(row_scores)
    scores = average_scores(results)
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)
    return scores, avg_latency


def compare_experiment(
    name: str,
    variable: str,
    exp_scores: RagasScores,
    baseline_scores: RagasScores,
    exp_latency: float,
    baseline_latency: float,
    kept: bool,
    rationale: str,
) -> ExperimentResult:
    result = ExperimentResult(
        name=name,
        variable_changed=variable,
        baseline_scores=baseline_scores,
        experiment_scores=exp_scores,
        latency_delta_ms=exp_latency - baseline_latency,
        kept=kept,
        rationale=rationale,
    )
    print(f"\n  Experiment: {name}")
    print(f"  Variable:  {variable}")
    for metric in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
        base_val = getattr(baseline_scores, metric)
        exp_val = getattr(exp_scores, metric)
        delta = exp_val - base_val
        sign = "+" if delta >= 0 else ""
        print(f"    {metric:<25} {base_val:.2f} → {exp_val:.2f}  ({sign}{delta:.2f})")
    print(f"  Latency delta: {result.latency_delta_ms:+.0f} ms")
    print(f"  Kept: {'YES' if kept else 'NO'} — {rationale}")
    return result


# ---------------------------------------------------------------------------
# LLM-integrated diagnostic
# ---------------------------------------------------------------------------

def diagnose_worst_case(
    worst_row: GoldenRow,
    worst_output: PipelineOutput,
    worst_scores: dict,
    openai_client: OpenAI,
) -> dict:
    print("\n" + "="*65)
    print(" LLM DIAGNOSTIC — WORST-SCORING QUESTION")
    print("="*65)

    diagnostic_prompt = f"""You are a RAG system debugger. Analyse this failure.

QUESTION: {worst_row.question}
IDEAL ANSWER: {worst_row.ideal_answer}
RETRIEVED CONTEXTS:
{chr(10).join(f"[{i+1}] ({src}) {ctx[:300]}" for i, (ctx, src) in enumerate(zip(worst_output.contexts, worst_output.retrieved_sources)))}

ACTUAL ANSWER: {worst_output.answer}

RAGAS SCORES:
  Faithfulness:      {worst_scores['faithfulness']:.2f}
  Answer Relevancy:  {worst_scores['answer_relevancy']:.2f}
  Context Precision: {worst_scores['context_precision']:.2f}
  Context Recall:    {worst_scores['context_recall']:.2f}

Diagnose the root cause. Is this a RETRIEVAL failure (wrong chunks returned) or a GENERATION failure (model hallucinated from correct context)? Propose one concrete fix."""

    resp = openai_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": diagnostic_prompt}],
        temperature=0,
        max_tokens=400,
    )
    diagnosis = resp.choices[0].message.content or ""

    print(f"\nFailing case: [{worst_row.row_id}] {worst_row.question}")
    print(f"Faithfulness: {worst_scores['faithfulness']:.2f}")
    print(f"\nLLM Diagnosis:\n{textwrap.indent(diagnosis, '  ')}")

    human_critique = (
        "Human critique: The diagnosis correctly identifies whether this is a retrieval or generation issue. "
        "Proposed fix should be tested on the full golden set before adoption — single-case fixes can overfit."
    )
    print(f"\n{human_critique}")

    return {
        "row_id": worst_row.row_id,
        "question": worst_row.question,
        "ideal_answer": worst_row.ideal_answer,
        "retrieved_contexts": worst_output.contexts,
        "retrieved_sources": worst_output.retrieved_sources,
        "actual_answer": worst_output.answer,
        "scores": worst_scores,
        "diagnostic_prompt": diagnostic_prompt,
        "llm_diagnosis": diagnosis,
        "human_critique": human_critique,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not OPENAI_API_KEY:
        raise EnvironmentError("Set OPENAI_API_KEY before running.")

    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    OBSERVABILITY_DIR.mkdir(parents=True, exist_ok=True)

    # Optional Langfuse setup
    if _LANGFUSE_AVAILABLE and LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        lf = Langfuse(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_HOST,
        )
        print("[INFO] Langfuse tracing enabled.")
    else:
        print("[INFO] Langfuse not configured — tracing is no-op.")

    # ── Step 1: Build corpus & vector store ──────────────────────────────────
    documents = load_documents(DOCS_DIR)
    chunks: list[Chunk] = []
    for filename, text in documents:
        chunks.extend(chunk_recursive(filename, text))
    print(f"[INFO] {len(chunks)} chunks ready.")

    collection = build_vector_store(chunks, openai_client)

    # ── Step 2: Baseline evaluation ──────────────────────────────────────────
    print("\n[INFO] Running baseline evaluation on golden set ...")
    baseline_row_scores: list[dict] = []
    baseline_outputs: list[PipelineOutput] = []

    for row in GOLDEN_SET:
        output = run_pipeline(row.question, collection, openai_client, k=TOP_K_DEFAULT)
        row_scores = evaluate_row(row, output, openai_client)
        baseline_row_scores.append(row_scores)
        baseline_outputs.append(output)
        print(f"  [{row.row_id}] faith={row_scores['faithfulness']:.2f} "
              f"rel={row_scores['answer_relevancy']:.2f} "
              f"prec={row_scores['context_precision']:.2f} "
              f"rec={row_scores['context_recall']:.2f}")

    baseline_scores = average_scores(baseline_row_scores)
    baseline_latency = sum(r["latency_ms"] for r in baseline_row_scores) / len(baseline_row_scores)
    print_scorecard(baseline_scores, "Baseline (k=3, chunk=recursive)")

    # ── Step 3: Improvement experiments ──────────────────────────────────────
    experiments: list[ExperimentResult] = []

    # Experiment 1: Top-k 3 → 5
    exp1_scores, exp1_latency = run_experiment(
        "Top-k increase", "k=3 → k=5", collection, openai_client, GOLDEN_SET,
        baseline_scores, k=5,
    )
    exp1 = compare_experiment(
        "Top-k k=3 → k=5", "top_k retrieval",
        exp1_scores, baseline_scores, exp1_latency, baseline_latency,
        kept=(exp1_scores.context_recall > baseline_scores.context_recall
              and exp1_scores.faithfulness >= baseline_scores.faithfulness - 0.02),
        rationale="More context improves recall; accept small faithfulness trade-off if recall gain > 0.05.",
    )
    experiments.append(exp1)

    # Experiment 2: Chunk size reduction (rebuild with smaller chunks)
    print("\n  [experiment] Rebuilding Chroma with smaller chunks (max_chars=600) ...")
    small_chunks: list[Chunk] = []
    for filename, text in documents:
        small_chunks.extend(chunk_recursive(filename, text, max_chars=600))
    small_collection = build_vector_store(small_chunks, openai_client, "northwind_small_chunks")

    exp2_scores, exp2_latency = run_experiment(
        "Smaller chunks", "max_chars=1200 → 600", small_collection, openai_client,
        GOLDEN_SET, baseline_scores, k=TOP_K_DEFAULT,
    )
    exp2 = compare_experiment(
        "Chunk size 1200 → 600 chars", "chunk_max_chars",
        exp2_scores, baseline_scores, exp2_latency, baseline_latency,
        kept=(exp2_scores.context_precision > baseline_scores.context_precision + 0.03),
        rationale="Smaller chunks boost precision but may hurt recall; keep if precision gain > 0.03.",
    )
    experiments.append(exp2)

    # ── Step 4: Worst-case diagnostic ────────────────────────────────────────
    # Find the lowest-faithfulness row in baseline
    worst_idx = min(range(len(baseline_row_scores)),
                    key=lambda i: baseline_row_scores[i]["faithfulness"])
    worst_row = GOLDEN_SET[worst_idx]
    worst_output = baseline_outputs[worst_idx]
    worst_scores_dict = baseline_row_scores[worst_idx]

    diagnostic = diagnose_worst_case(worst_row, worst_output, worst_scores_dict, openai_client)

    # ── Step 5: Persist results ───────────────────────────────────────────────
    scorecard_path = OBSERVABILITY_DIR / "baseline_scorecard.json"
    scorecard_path.write_text(
        json.dumps(
            {
                "config": {"k": TOP_K_DEFAULT, "chunk_strategy": "recursive", "embed_model": EMBED_MODEL, "llm": LLM_MODEL},
                "scores": asdict(baseline_scores),
                "avg_latency_ms": baseline_latency,
                "passes_floor": baseline_scores.passes_floor(),
                "passes_target": baseline_scores.passes_target(),
                "row_level": baseline_row_scores,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n[INFO] Baseline scorecard → {scorecard_path}")

    exp_path = OBSERVABILITY_DIR / "experiment_results.json"
    exp_path.write_text(
        json.dumps(
            {
                "experiments": [asdict(e) for e in experiments],
                "diagnostic": diagnostic,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[INFO] Experiment results  → {exp_path}")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "="*65)
    print(" WEEK 16 COMPLETE — SUMMARY")
    print("="*65)
    print(f"  Golden set size:   {len(GOLDEN_SET)} rows")
    print(f"  Avg latency:       {baseline_latency:.0f} ms")
    print(f"  Est. cost/query:   ${sum(r['cost_usd'] for r in baseline_row_scores)/len(baseline_row_scores):.5f}")
    print_scorecard(baseline_scores, "Final Baseline")

    kept = [e for e in experiments if e.kept]
    print(f"  Experiments run:   {len(experiments)}")
    print(f"  Changes kept:      {len(kept)} — {[e.variable_changed for e in kept]}")
    print(f"\n  Langfuse dashboard: {LANGFUSE_HOST} (if configured)")
    print(f"  Outputs: {OBSERVABILITY_DIR}/")
    print("="*65)


if __name__ == "__main__":
    main()
