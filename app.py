"""Local-only Gemini Pro subscription assistant dashboard.

Does not collect passwords, payment-card details, TOTP secrets or cookies.
"""
from __future__ import annotations

import json
import os
import secrets
import threading
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
STATE_PATH = DATA / "notes.json"
DATA.mkdir(mode=0o700, parents=True, exist_ok=True)
TOKEN = secrets.token_urlsafe(32)
PORT = int(os.getenv("GEMINI_ASSISTANT_PORT", "8765"))
ORIGIN = f"http://127.0.0.1:{PORT}"

OFFICIAL = {
    "google_one": "https://one.google.com/",
    "google_play": "https://play.google.com/store/account/subscriptions",
    "google_account": "https://myaccount.google.com/",
}

app = FastAPI(
    title="Gemini Pro Subscription Assistant",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

class Note(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    plan: str = Field(default="Unknown", max_length=100)
    expiry: str = Field(default="", max_length=40)
    remark: str = Field(default="", max_length=300)

class OpenRequest(BaseModel):
    page: Literal["google_one", "google_play", "google_account"]

def load_notes() -> list[dict]:
    if not STATE_PATH.exists():
        return []
    try:
        content = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return content if isinstance(content, list) else []
    except (OSError, ValueError):
        return []

def save_notes(notes: list[dict]) -> None:
    target = STATE_PATH.with_suffix(".tmp")
    target.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
    target.replace(STATE_PATH)

def require_local(request: Request, x_session_token: str | None) -> None:
    if request.client is None or request.client.host not in {"127.0.0.1", "::1"}:
        raise HTTPException(403, "Local requests only")
    origin = request.headers.get("origin", "")
    if origin != ORIGIN:
        raise HTTPException(403, "Origin rejected")
    if not secrets.compare_digest(x_session_token or "", TOKEN):
        raise HTTPException(403, "Invalid session token")

@app.get("/", response_class=HTMLResponse)
def home():
    html = (BASE / "templates" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html.replace("__TOKEN__", TOKEN))

@app.get("/api/state")
def state(request: Request):
    if request.client is None or request.client.host not in {"127.0.0.1", "::1"}:
        raise HTTPException(403, "Local requests only")
    return {"notes": load_notes(), "official": OFFICIAL}

@app.post("/api/note")
def add_note(note: Note, request: Request, x_session_token: str | None = Header(default=None)):
    require_local(request, x_session_token)
    notes = load_notes()
    notes.append({"id": secrets.token_hex(8), "created": datetime.now(timezone.utc).isoformat(), **note.model_dump()})
    save_notes(notes)
    return {"ok": True}

@app.post("/api/open")
def open_official(body: OpenRequest, request: Request, x_session_token: str | None = Header(default=None)):
    require_local(request, x_session_token)
    url = OFFICIAL[body.page]
    # Only a hard-coded allowlist of HTTPS Google URLs is ever opened.
    threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()
    return {"ok": True, "url": url}

@app.get("/api/report")
def report(request: Request):
    if request.client is None or request.client.host not in {"127.0.0.1", "::1"}:
        raise HTTPException(403, "Local requests only")
    # Notes are manually entered, not scraped from authenticated Google pages.
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "notes": load_notes()}

if __name__ == "__main__":
    import uvicorn
    print(f"Open {ORIGIN} — local machine only", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=PORT, access_log=False)
