# filename: second_brain_builder/src/web/app.py
# purpose: FastAPI web server - dashboard, build trigger, static Obsidian vault hosting on customizable port

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from config import VAULT_ROOT, DEFAULT_PORT
from src.utils.folder_setup import setup_all_folders
from src.modules.video_processor import process_youtube_links
from src.modules.document_processor import process_report
from src.modules.obsidian_exporter import create_obsidian_structure

app = FastAPI(title="Second Brain Builder")

app.mount("/vault", StaticFiles(directory=str(VAULT_ROOT), html=True), name="vault")

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
<!DOCTYPE html>
<html>
<head><title>Second Brain Builder</title></head>
<body style="font-family:Arial">
<h1>🧠 Second Brain Builder 2026</h1>
<p>Server running on port {DEFAULT_PORT} (customizable via --port or PORT env var)</p>
<button onclick="buildVault()">Build/Update Vault</button>
<p><a href="/vault/index.md" target="_blank">Open Vault (after build)</a></p>
<script>
async function buildVault() {{
    const res = await fetch('/build', {{method:'POST'}});
    const data = await res.json();
    alert(data.message + '\\nOpen /vault/index.md');
}}
</script>
</body>
</html>
"""

@app.post("/build")
async def build_vault():
    setup_all_folders()
    process_youtube_links()
    process_report()
    create_obsidian_structure()
    return {"status": "success", "message": "Vault built successfully - open /vault/index.md", "path": str(VAULT_ROOT)}
