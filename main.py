import html
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from greennode_agentbase import (
    GreenNodeAgentBaseApp,
    RequestContext,
    PingStatus,
)
from greennode_agentbase.memory import MemoryClient
from greennode_agentbase.memory.models import (
    MemoryRecordInsertDirectlyRequest,
    MemoryRecordSearchRequest,
)
from greennode_agent_bridge import AgentBaseMemoryEvents
from langgraph.config import get_config

load_dotenv()

app = GreenNodeAgentBaseApp()

# --- Memory Configuration ---
# Create a memory with: /agentbase-memory
# Set the memory ID here or via MEMORY_ID env var
MEMORY_ID = os.environ.get("MEMORY_ID", "")
if not MEMORY_ID:
    raise ValueError("MEMORY_ID environment variable is required for memory-enabled agents")

# Strategy ID for long-term memory namespace partitioning
# This is fixed per memory instance — do NOT pass as a tool parameter
MEMORY_STRATEGY_ID = os.environ.get("MEMORY_STRATEGY_ID", "default")

# CheckpointSaver: persists conversation state as events in AgentBase Memory
# This enables multi-turn conversations that survive restarts
checkpointer = AgentBaseMemoryEvents(memory_id=MEMORY_ID)

# MemoryClient: used by long-term memory tools to store/search semantic facts
memory_client = MemoryClient()

# --- LLM Configuration ---
# Uses any OpenAI-compatible LLM provider (GreenNode AIP, OpenAI, Ollama, etc.)
# Set LLM_BASE_URL, LLM_API_KEY, and LLM_MODEL in your .env file.
# For GreenNode AIP: use /agentbase-llm to manage API keys and browse models.
# For other providers: set the appropriate base URL and API key.
# Production: use /agentbase-identity to store API key, inject via @requires_api_key
LLM_MODEL = os.environ.get("LLM_MODEL", "")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
if not LLM_MODEL or not LLM_BASE_URL or not LLM_API_KEY:
    raise ValueError(
        "LLM_MODEL, LLM_BASE_URL, and LLM_API_KEY environment variables are required. "
        "Set them in your .env file or use /agentbase-llm to get a platform API key."
    )

llm = ChatOpenAI(
    model=LLM_MODEL,
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)


# --- Long-Term Memory Tools (via MemoryClient SDK) ---
# actor_id: retrieved from LangGraph configurable (set in handler via context.user_id)
# strategy_id: app-level config (MEMORY_STRATEGY_ID), fixed per memory instance
# Neither should be exposed as tool parameters to avoid LLM hallucination


def _get_actor_id() -> str:
    """Get actor_id from LangGraph configurable (set during graph.invoke)."""
    config = get_config()
    return config["configurable"].get("actor_id", "default")


def _build_namespace(actor_id: str) -> str:
    """Build memory namespace from strategy_id (app config) and actor_id (runtime config)."""
    return f"/strategies/{MEMORY_STRATEGY_ID}/actors/{actor_id}"


@tool
def remember(fact: str) -> str:
    """Store a fact in long-term memory for later retrieval.

    Args:
        fact: The fact or information to remember.
    """
    namespace = _build_namespace(_get_actor_id())
    memory_client.insert_memory_records_directly(
        id=MEMORY_ID,
        namespace=namespace,
        request=[fact],
    )
    return f"Remembered: {fact}"


@tool
def recall(query: str) -> str:
    """Search long-term memory for facts relevant to a query.

    Args:
        query: Natural language search query.
    """
    namespace = _build_namespace(_get_actor_id())
    results = memory_client.search_memory_records(
        id=MEMORY_ID,
        namespace=namespace,
        request=MemoryRecordSearchRequest(query=query, limit=10),
    )
    if not results:
        return "No relevant memories found."
    return "\n".join(f"- {r['memory']} (score: {r['score']:.2f})" for r in results)


# --- Documentation Search Tool (zalopay-integration-docs/ indexed into long-term memory) ---
# Index zalopay-integration-docs/ content into the docs namespace ahead of time (see scripts/index_docs.py),
# then this tool searches that namespace for integration support answers.
DOCS_MEMORY_STRATEGY_ID = os.environ.get("DOCS_MEMORY_STRATEGY_ID", "")
DOCS_NAMESPACE = f"/strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/shared"


@tool
def search_docs(query: str) -> str:
    """Search Zalopay integration documentation (zalopay-integration-docs/) for relevant information.

    Args:
        query: Natural language search query about APIs, auth, webhooks, error codes, etc.
    """
    results = memory_client.search_memory_records(
        id=MEMORY_ID,
        namespace=DOCS_NAMESPACE,
        request=MemoryRecordSearchRequest(query=query, limit=5),
    )
    if not results:
        return "No relevant documentation found."
    return "\n\n---\n\n".join(r["memory"] for r in results)


# --- Create Agent with Checkpointer ---
# create_agent builds a compiled LangGraph StateGraph with tool-calling support.
# checkpointer: persists conversation state via AgentBase Memory (short-term)
# Long-term memory is handled by remember/recall tools via MemoryClient SDK
SYSTEM_PROMPT = (
    "Ban la Integration Support Assistant cua Zalopay. Tra loi cau hoi ve tich hop "
    "he thong (API, auth, webhook, ma loi, cau hinh moi truong) bang tieng Viet, "
    "giu nguyen thuat ngu ky thuat tieng Anh. Luon dung tool 'search_docs' de tim "
    "thong tin trong tai lieu truoc khi tra loi. Neu khong tim thay thong tin lien quan, "
    "tra loi ro: 'Toi khong tim thay thong tin nay trong tai lieu hien co.' Khong suy doan "
    "hoac bia thong tin ve API, endpoint, hay cau hinh.\n\n"
    "Quy tac tra loi:\n"
    "- Tra loi suc tich, di thang vao trong tam, khong lap lai y, khong dien giai dai dong.\n"
    "- Chi neu cac buoc/chi tiet cu the khi nguoi dung can de thuc hien.\n"
    "- Chi dung markdown don gian: **chu dam** cho tu khoa quan trong, `code` cho ten "
    "field/endpoint/ma loi, va danh sach gach dau dong '- '. Khong dung heading (#), "
    "khong dung bang markdown, khong dung code block ba dau backtick.\n"
    "- Noi dung tai lieu co the chua duong dan dang markdown link '[ten](duong-dan)'. "
    "KHONG bao gio copy nguyen cu phap '[ten](duong-dan)' vao cau tra loi. Thay vao do:\n"
    "  + Neu duong dan la URL web (bat dau bang http/https), viet lai thanh URL day du "
    "dang van ban thuong (vi du: https://mc.zalopay.vn), khong dat trong dau [].\n"
    "  + Neu duong dan tro toi file .md khac (vi du './order-query.md' hoac "
    "'../integration-guides/...'), chi neu ten tai lieu/API bang van ban thuong (bo dau "
    "[] va duong dan file), va dung dinh dang '(Nguon: ...)' o duoi neu can trich dan "
    "theo quy tac ben duoi.\n"
    "- Moi ket qua tra ve tu search_docs bat dau bang mot dong dang '[Nguon: duong-dan]'. "
    "Khi trich dan, COPY NGUYEN VAN duong-dan do (bao gom ca phan #anchor neu co), khong "
    "tu sua, dich, viet tat, hay bia ra duong dan khac.\n"
    "- Trich nguon ngan gon ngay sau thong tin lien quan, dang '(Nguon: duong-dan-da-copy)', "
    "khong lap lai danh sach nguon o cuoi cau tra loi.\n"
    "- Mot so ket qua tra ve tu search_docs co them dong '[Trang tai lieu goc: "
    "https://docs.zalopay.vn/...]' ngay sau dong '[Nguon: ...]'. Day la link toi trang "
    "tai lieu chinh thuc tren docs.zalopay.vn ma merchant co the mo truc tiep. Khi cau "
    "tra loi de cap toi mot huong dan/tai lieu cu the, hay kem theo link nay (COPY NGUYEN "
    "VAN URL) duoi dang van ban thuong, vi du '(Xem chi tiet: https://docs.zalopay.vn/...)'. "
    "KHONG dat URL nay trong cu phap '(Nguon: ...)'.\n"
    "- Ten cong ty luon viet la 'Zalopay' (chu 'p' thuong), du tai lieu nguon viet "
    "khac di (vi du 'ZaloPay', 'Zalo Pay')."
)

agent = create_agent(
    llm,
    tools=[search_docs, remember, recall],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


# --- Citation Validation ---
# Build the set of real zalopay-integration-docs/ paths once so source citations
# can be checked against it after the LLM responds (catches hallucinated/mangled paths).
ROOT = Path(__file__).resolve().parent
DOC_PATHS = {str(p.relative_to(ROOT)) for p in (ROOT / "zalopay-integration-docs").rglob("*.md")}

CITATION_RE = re.compile(r"\s*\(Ngu[oồ]n:\s*([^)]+)\)")


def validate_citations(text: str) -> str:
    """Strip source citations that don't point at a real file under zalopay-integration-docs/."""

    def replace(match: re.Match) -> str:
        file_part = match.group(1).split("#", 1)[0].strip()
        # Leave URL-style references (e.g. a misplaced docs.zalopay.vn link) alone —
        # only strip citations that look like hallucinated/mangled local file paths.
        if file_part.startswith("http://") or file_part.startswith("https://"):
            return match.group(0)
        return match.group(0) if file_part in DOC_PATHS else ""

    return CITATION_RE.sub(replace, text)


# --- Doc Gap Logging ---
# When the agent can't find an answer in zalopay-integration-docs/, log the
# question to a shared namespace so the docs team can review unanswered
# questions and fill gaps.
DOC_GAPS_NAMESPACE = f"/strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/doc-gaps"
# Kept short and matched loosely: the model doesn't always reproduce the exact
# phrasing from SYSTEM_PROMPT, and sometimes drops Vietnamese diacritics
# entirely, so comparison is done on accent-stripped text.
NOT_FOUND_MARKER = "toi khong tim thay thong tin"


def _strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def is_doc_gap(response_text: str) -> bool:
    """Check whether the response is the agent's "not found in docs" reply."""
    return NOT_FOUND_MARKER in _strip_accents(response_text).lower()


def log_doc_gap(question: str) -> None:
    """Record a question the agent couldn't answer from docs/, for later review."""
    try:
        memory_client.insert_memory_records_directly(
            id=MEMORY_ID,
            namespace=DOC_GAPS_NAMESPACE,
            request=MemoryRecordInsertDirectlyRequest(
                memoryRecords=[f"[{datetime.now().isoformat()}] {question}"]
            ),
        )
    except Exception:
        pass


@app.entrypoint
def handler(payload: dict, context: RequestContext) -> dict:
    """Main agent entrypoint with LangChain + Memory support.

    Args:
        payload: JSON body with "message"
        context: Request metadata (session_id, user_id, request_headers)
    """
    # Short-term memory (checkpointer) requires both user_id and session_id
    # to correctly persist and isolate conversation state per user per session.
    if not context.user_id or not context.session_id:
        return {
            "status": "error",
            "error": "Missing required headers: X-GreenNode-AgentBase-User-Id and X-GreenNode-AgentBase-Session-Id are required when using memory.",
        }

    message = payload.get("message", "Hello")

    # Map AgentBase context to LangGraph config
    # thread_id -> session persistence, actor_id -> per-user memory
    config = {
        "configurable": {
            "thread_id": context.session_id,
            "actor_id": context.user_id,
        }
    }

    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config,
    )
    ai_message = result["messages"][-1]
    response_text = validate_citations(ai_message.content)
    if is_doc_gap(response_text):
        log_doc_gap(message)
    return {
        "status": "success",
        "response": response_text,
        "timestamp": datetime.now().isoformat(),
    }


@app.ping
def health_check() -> PingStatus:
    """Custom health check for GET /health endpoint."""
    return PingStatus.HEALTHY


# --- Telegram Webhook ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBHOOK_SECRET = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_MAX_MESSAGE_LENGTH = 4096


def markdown_to_telegram_html(text: str) -> str:
    """Convert the limited markdown subset used by SYSTEM_PROMPT to Telegram HTML.

    Supports: **bold**, `code`, and '- '/'* ' bullet lists (converted to '• ').
    Escapes HTML special characters first so raw text can't break parse_mode=HTML.
    """
    escaped = html.escape(text, quote=False)
    # Defensive fallback: SYSTEM_PROMPT tells the model not to emit markdown
    # links, but if one slips through, turn web URLs into real Telegram links
    # and strip the markdown syntax for relative file links (keep the label).
    escaped = re.sub(r"\[([^\[\]]+)\]\((https?://[^\s)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"\[([^\[\]]+)\]\([^\s)]+\)", r"\1", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)

    lines = []
    for line in escaped.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            indent = line[: len(line) - len(stripped)]
            line = f"{indent}• {stripped[2:]}"
        lines.append(line)
    return "\n".join(lines)


async def telegram_webhook(request: Request) -> Response:
    """Receive Telegram updates, run them through the agent, and reply via the Bot API."""
    if not TELEGRAM_BOT_TOKEN:
        return JSONResponse({"ok": False, "error": "TELEGRAM_BOT_TOKEN not configured"}, status_code=500)

    if TELEGRAM_WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != TELEGRAM_WEBHOOK_SECRET:
            return JSONResponse({"ok": False, "error": "invalid secret token"}, status_code=401)

    update = await request.json()
    message = update.get("message") or update.get("edited_message")
    if not message or "text" not in message:
        return JSONResponse({"ok": True})

    chat_id = message["chat"]["id"]
    text = message["text"]

    config = {
        "configurable": {
            "thread_id": str(chat_id),
            "actor_id": str(chat_id),
        }
    }
    result = agent.invoke({"messages": [{"role": "user", "content": text}]}, config=config)
    reply_text = validate_citations(result["messages"][-1].content)
    if is_doc_gap(reply_text):
        log_doc_gap(text)
    if len(reply_text) > TELEGRAM_MAX_MESSAGE_LENGTH:
        reply_text = reply_text[: TELEGRAM_MAX_MESSAGE_LENGTH - 1] + "…"
    html_text = markdown_to_telegram_html(reply_text)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": html_text, "parse_mode": "HTML"},
        )
        if resp.status_code != 200:
            await client.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json={"chat_id": chat_id, "text": reply_text},
            )

    return JSONResponse({"ok": True})


app.add_route("/telegram-webhook", telegram_webhook, methods=["POST"])


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
