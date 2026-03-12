# filename: second_brain_builder/src/web/app.py
# purpose: FastAPI server with proper modern Tailwind GUI frontend for Second Brain (dashboard, stats, live note list, build button, sidebar explorer)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from src.config import VAULT_ROOT, DEFAULT_PORT
from src.utils.folder_setup import setup_all_folders
from src.modules.video_processor import process_youtube_links
from src.modules.document_processor import process_report
from src.modules.obsidian_exporter import create_obsidian_structure

app = FastAPI(title="Second Brain Builder")

app.mount("/vault", StaticFiles(directory=str(VAULT_ROOT), html=True), name="vault")

def get_vault_stats():
    stats = {"total_notes": 0, "youtube": 0, "cloud": 0, "local": 0, "db": 0, "emerging": 0}
    for root, _, files in os.walk(VAULT_ROOT):
        for f in files:
            if f.endswith(".md"):
                stats["total_notes"] += 1
                rel = str(Path(root).relative_to(VAULT_ROOT))
                if "youtube_notes" in rel:
                    stats["youtube"] += 1
                elif "cloud_platforms" in rel:
                    stats["cloud"] += 1
                elif "local_storage" in rel:
                    stats["local"] += 1
                elif "databases" in rel:
                    stats["db"] += 1
                elif "emerging" in rel:
                    stats["emerging"] += 1
    return stats

@app.get("/api/notes")
async def api_notes():
    notes = []
    for root, _, files in os.walk(VAULT_ROOT):
        for f in files:
            if f.endswith(".md"):
                rel_path = Path(root).relative_to(VAULT_ROOT) / f
                notes.append({"path": str(rel_path), "name": f})
    return JSONResponse(notes)

@app.get("/", response_class=HTMLResponse)
async def root():
    stats = get_vault_stats()
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🧠 Second Brain Builder 2026</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        function initTailwind() {{
            tailwind.config = {{ content: [], theme: {{ extend: {{}} }} }}
        }}
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        body {{ font-family: 'Inter', system-ui; }}
    </style>
</head>
<body class="bg-zinc-950 text-zinc-100">
<div class="flex h-screen">
    <!-- Sidebar -->
    <div class="w-72 bg-zinc-900 border-r border-zinc-800 p-6 flex flex-col">
        <div class="flex items-center gap-3 mb-10">
            <div class="w-9 h-9 bg-violet-600 rounded-xl flex items-center justify-center text-white font-bold">B</div>
            <div>
                <h1 class="text-2xl font-semibold tracking-tight">Second Brain</h1>
                <p class="text-xs text-zinc-500">2026 Vault</p>
            </div>
        </div>
        
        <nav class="flex-1 space-y-1">
            <a href="#" onclick="switchTab(0)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl bg-zinc-800 text-white font-medium">
                <span>📊</span> Dashboard
            </a>
            <a href="#" onclick="switchTab(1)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">
                <span>🎥</span> YouTube Notes
            </a>
            <a href="#" onclick="switchTab(2)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">
                <span>☁️</span> Cloud Platforms
            </a>
            <a href="#" onclick="switchTab(3)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">
                <span>💾</span> Local Storage
            </a>
            <a href="#" onclick="switchTab(4)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">
                <span>🧬</span> AI Databases
            </a>
            <a href="#" onclick="switchTab(5)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">
                <span>🚀</span> Emerging AI
            </a>
        </nav>
        
        <div class="pt-6 border-t border-zinc-800">
            <button onclick="buildVault()" id="buildBtn"
                class="w-full bg-violet-600 hover:bg-violet-700 transition-colors text-white font-semibold py-4 rounded-3xl flex items-center justify-center gap-2">
                <span id="btnText">🚀 Build / Update Vault</span>
            </button>
        </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
        <!-- Top bar -->
        <div class="h-16 border-b border-zinc-800 bg-zinc-900 px-8 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <h2 class="text-xl font-semibold">Dashboard</h2>
                <span id="status" class="px-3 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400">Ready</span>
            </div>
            <div class="flex items-center gap-6 text-sm">
                <a href="/vault/index.md" target="_blank" class="text-zinc-400 hover:text-white transition-colors">Open in Obsidian</a>
                <div class="text-zinc-500">Port: {DEFAULT_PORT}</div>
            </div>
        </div>

        <!-- Dashboard -->
        <div class="flex-1 p-8 overflow-auto" id="mainContent">
            <div class="grid grid-cols-5 gap-6">
                <!-- Stats Cards -->
                <div class="bg-zinc-900 rounded-3xl p-6">
                    <div class="text-sm text-zinc-500">Total Notes</div>
                    <div id="totalNotes" class="text-5xl font-semibold mt-2">{stats["total_notes"]}</div>
                </div>
                <div class="bg-zinc-900 rounded-3xl p-6">
                    <div class="text-sm text-zinc-500">YouTube Transcripts</div>
                    <div id="ytCount" class="text-5xl font-semibold mt-2">{stats["youtube"]}</div>
                </div>
                <div class="bg-zinc-900 rounded-3xl p-6">
                    <div class="text-sm text-zinc-500">Cloud Platforms</div>
                    <div id="cloudCount" class="text-5xl font-semibold mt-2">{stats["cloud"]}</div>
                </div>
                <div class="bg-zinc-900 rounded-3xl p-6">
                    <div class="text-sm text-zinc-500">Local Storage</div>
                    <div id="localCount" class="text-5xl font-semibold mt-2">{stats["local"]}</div>
                </div>
                <div class="bg-zinc-900 rounded-3xl p-6">
                    <div class="text-sm text-zinc-500">AI Databases</div>
                    <div id="dbCount" class="text-5xl font-semibold mt-2">{stats["db"]}</div>
                </div>
            </div>

            <!-- Note List -->
            <div class="mt-10">
                <div class="flex justify-between mb-4">
                    <h3 class="font-semibold text-lg">Vault Notes</h3>
                    <input id="searchInput" type="text" placeholder="Search notes..." 
                        class="bg-zinc-900 border border-zinc-700 rounded-2xl px-4 py-2 text-sm w-72 focus:outline-none focus:border-violet-500"
                        onkeyup="filterNotes()">
                </div>
                <div id="notesList" class="grid grid-cols-2 gap-4"></div>
            </div>
        </div>
    </div>
</div>

<script>
    let allNotes = [];
    function loadNotes() {{
        fetch('/api/notes')
            .then(r => r.json())
            .then(data => {{
                allNotes = data;
                renderNotes(data);
            }});
    }}
    function renderNotes(notes) {{
        const container = document.getElementById('notesList');
        container.innerHTML = notes.map(n => `
            <a href="/vault/${{n.path}}" target="_blank"
                class="block bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 rounded-3xl p-6 transition-all group">
                <div class="text-sm text-violet-400 mb-1">📄</div>
                <div class="font-medium text-white group-hover:text-violet-300 transition-colors">{{n.name}}</div>
                <div class="text-xs text-zinc-500 mt-1">{{n.path}}</div>
            </a>
        `).join('');
    }}
    function filterNotes() {{
        const term = document.getElementById('searchInput').value.toLowerCase();
        const filtered = allNotes.filter(n => n.name.toLowerCase().includes(term));
        renderNotes(filtered);
    }}
    async function buildVault() {{
        const btn = document.getElementById('buildBtn');
        const txt = document.getElementById('btnText');
        txt.innerHTML = 'Building... <span class="animate-spin inline-block ml-2">⟳</span>';
        btn.disabled = true;
        try {{
            await fetch('/build', {{method: 'POST'}});
            const stats = await fetch('/api/notes').then(r => r.json());
            document.getElementById('totalNotes').textContent = stats.length || 0;
            loadNotes();
        }} catch(e) {{}}
        setTimeout(() => {{
            txt.textContent = '🚀 Build / Update Vault';
            btn.disabled = false;
            document.getElementById('status').textContent = 'Updated';
        }}, 800);
    }}
    function switchTab(n) {{
        document.querySelectorAll('.tab-btn').forEach((el,i) => {{
            el.classList.toggle('bg-zinc-800', i===n);
            el.classList.toggle('text-white', i===n);
            el.classList.toggle('text-zinc-400', i!==n);
        }});
    }}
    // Init
    window.onload = () => {{
        initTailwind();
        loadNotes();
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
    return {"status": "success", "message": "Vault built - refresh dashboard"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=DEFAULT_PORT)
