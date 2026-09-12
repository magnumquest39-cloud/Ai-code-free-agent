# Web IDE Agent

This simple web UI can be served inside Codespaces or any web IDE where you can run a lightweight HTTP server.

Start with:

pip install -r web_ide_agent/requirements.txt
uvicorn web_ide_agent.app:app --host 0.0.0.0 --port 8080

Open the forwarded port 8080 in Codespaces.
