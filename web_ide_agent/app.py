from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from remote_genai import generate_text

app = FastAPI(title="Web IDE Agent Chat")

# Allow web IDEs / Codespaces frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (index.html + app.js) from this directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


class ChatRequest(BaseModel):
    message: str
    model: str | None = None
    temperature: float | None = 0.2
    max_tokens: int | None = 512


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.message or req.message.strip() == "":
        raise HTTPException(status_code=400, detail="Empty message")

    # Simple pass-through to Gemini wrapper
    reply = generate_text(req.message, model=req.model, max_tokens=req.max_tokens, temperature=req.temperature)
    return {"reply": reply}
