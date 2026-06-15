import html
import os
import re
from datetime import datetime

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
from greennode_agentbase.memory.models import MemoryRecordSearchRequest
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


# --- Documentation Search Tool (docs/ indexed into long-term memory) ---
# Index docs/ content into the docs namespace ahead of time (see scripts/index_docs.py),
# then this tool searches that namespace for integration support answers.
DOCS_MEMORY_STRATEGY_ID = os.environ.get("DOCS_MEMORY_STRATEGY_ID", "")
DOCS_NAMESPACE = f"/strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/shared"


@tool
def search_docs(query: str) -> str:
    """Search Zalopay integration documentation (docs/) for relevant information.

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
    "- Trich nguon ngan gon ngay sau thong tin lien quan, dang '(Nguon: ten-file.md)', "
    "khong lap lai danh sach nguon o cuoi cau tra loi."
)

agent = create_agent(
    llm,
    tools=[search_docs, remember, recall],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


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
    return {
        "status": "success",
        "response": ai_message.content,
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
    reply_text = result["messages"][-1].content
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
