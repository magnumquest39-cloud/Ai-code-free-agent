# web_ide_agent/README.md

Web IDE Agent — lightweight chat extension for Codespaces / web IDE

This folder contains a minimal FastAPI-based chat UI that acts as a web IDE "agent extension".
It uses remote_genai.generate_text() to call Gemini (via GEMINI_API_KEY or ADC).

Usage (in Codespace or local dev):

1. Ensure GEMINI_API_KEY is available in environment (or configure ADC/OIDC):
   export GEMINI_API_KEY="your_key_here"

2. Install dependencies:
   python -m pip install -r web_ide_agent/requirements.txt

3. Run server:
   uvicorn web_ide_agent.app:app --host 0.0.0.0 --port 8080

4. Open the forwarded port (8080) in Codespaces or http://localhost:8080 locally.

Security notes:
- Do NOT commit API keys to git. Use Codespaces secrets or GitHub Actions secrets.
- In production prefer Workload Identity Federation (OIDC) and avoid storing long-lived keys.
