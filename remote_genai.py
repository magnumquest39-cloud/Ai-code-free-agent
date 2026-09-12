# remote_genai.py
import os
from typing import Optional

try:
    from google import genai
except Exception as e:
    raise ImportError("google-genai SDK is required. Install with: pip install google-genai") from e

API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")


def make_client():
    """Create and return a genai.Client.

    If GEMINI_API_KEY is set, pass it to the client. Otherwise rely on ADC
    (Workload Identity / gcloud auth) which is useful in Codespaces/Actions.
    """
    if API_KEY:
        return genai.Client(api_key=API_KEY)
    return genai.Client()


def generate_text(prompt: str, model: Optional[str] = None, max_tokens: int = 512, temperature: float = 0.2) -> str:
    client = make_client()
    model = model or DEFAULT_MODEL
    # Some SDK variants accept named params differently; keep minimal and robust.
    resp = client.models.generate_content(model=model, contents=prompt)

    # Try multiple common response shapes.
    try:
        candidates = getattr(resp, "candidates", None) or (resp.get("candidates") if isinstance(resp, dict) else None)
        if candidates:
            first = candidates[0]
            content = getattr(first, "content", None) or (first.get("content") if isinstance(first, dict) else None)
            if content and len(content) > 0:
                piece = content[0]
                text = getattr(piece, "text", None) or (piece.get("text") if isinstance(piece, dict) else None)
                if text:
                    return text.strip()
        # Fallbacks
        text = getattr(resp, "output_text", None) or (resp.get("output_text") if isinstance(resp, dict) else None)
        if text:
            return text.strip()
    except Exception:
        pass

    return str(resp)
