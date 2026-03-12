# filename: second_brain_builder/src/web/app.py
# purpose: Checkboxes stay (left column + Select All header). Clicking checkbox ONLY toggles it. Clicking anywhere else on row opens modal. No bulk bar.

import re
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from src.config import VAULT_ROOT, DEFAULT_PORT, OLLAMA_HOST
from src.utils.folder_setup import setup_all_folders
from src.modules.video_processor import process_youtube_links
from src.modules.document_processor import process_report
from src.modules.obsidian_exporter import create_obsidian_structure
from src.modules.ai_processor import OllamaClient
from src.modules.model_manager import model_manager
from src.modules.thought_processor import save_thought_and_reply
from src.modules.prompt_manager import prompt_manager

app = FastAPI(title="Second Brain Builder")
app.mount("/vault", StaticFiles(directory=str(VAULT_ROOT), html=True), name="vault")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/api/note/{path:path}")
async def get_note(path: str):
    full_path = VAULT_ROOT / path
    if full_path.exists() and full_path.is_file():
        content = full_path.read_text(encoding="utf-8")
        return {"filename": Path(path).name, "content": content}
    return {"error": "File not found"}

@app.delete("/api/note/{path:path}")
async def delete_note(path: str):
    full_path = VAULT_ROOT / path
    if full_path.exists() and full_path.is_file():
        full_path.unlink()
        return {"status": "deleted"}
    return {"error": "File not found"}

@app.get("/api/stats")
async def api_stats():
    return get_vault_stats()

ollama_client = OllamaClient()

def get_vault_stats():
    stats = {
        "total_notes": 0, "People": 0, "Projects": 0, "Ideas": 0, "Admin": 0, "Review": 0,
        "avg_People": 0.0, "avg_Projects": 0.0, "avg_Ideas": 0.0, "avg_Admin": 0.0, "avg_Review": 0.0
    }
    sum_conf = {"People": 0.0, "Projects": 0.0, "Ideas": 0.0, "Admin": 0.0, "Review": 0.0}
    total_conf = 0.0
    thoughts_dir = VAULT_ROOT / "notes" / "thoughts"
    if thoughts_dir.exists():
        for f in thoughts_dir.glob("*.md"):
            name_lower = f.name.lower()
            stats["total_notes"] += 1
            conf_match = re.search(r'-([0-9.]+)-\d{8}\.md$', f.name)
            conf = float(conf_match.group(1)) if conf_match else 0.65
            total_conf += conf
            if name_lower.startswith("people-"):
                stats["People"] += 1
                sum_conf["People"] += conf
            elif name_lower.startswith("projects-"):
                stats["Projects"] += 1
                sum_conf["Projects"] += conf
            elif name_lower.startswith("ideas-"):
                stats["Ideas"] += 1
                sum_conf["Ideas"] += conf
            elif name_lower.startswith("admin-"):
                stats["Admin"] += 1
                sum_conf["Admin"] += conf
            elif name_lower.startswith("review-"):
                stats["Review"] += 1
                sum_conf["Review"] += conf
    for cat in ["People", "Projects", "Ideas", "Admin", "Review"]:
        count = stats[cat]
        if count > 0:
            stats[f"avg_{cat}"] = round(sum_conf[cat] / count, 2)
    stats["avg_all"] = round(total_conf / stats["total_notes"], 2) if stats["total_notes"] > 0 else 0.65
    return stats

@app.get("/api/models")
async def api_models():
    return JSONResponse(model_manager.get_models())

@app.get("/api/model_config")
async def api_model_config():
    return JSONResponse(model_manager.get_assignment())

@app.post("/api/model_config")
async def save_model_config(data: dict = Body(...)):
    model_manager.save_assignment(data)
    return {"status": "saved"}

@app.get("/api/ollama_status")
async def api_ollama_status():
    models = model_manager.get_models()
    return {"host": OLLAMA_HOST, "connected": len(models) > 0, "models_count": len(models)}

@app.get("/api/notes")
async def api_notes():
    notes = []
    for root, _, files in os.walk(VAULT_ROOT):
        for f in files:
            if f.endswith(".md"):
                rel_path = Path(root).relative_to(VAULT_ROOT) / f
                notes.append({"path": str(rel_path), "name": f})
    return JSONResponse(notes)

@app.get("/api/prompts")
async def api_prompts():
    return {
        "categorization": prompt_manager.get_prompt("categorization"),
        "search": prompt_manager.get_prompt("search"),
        "threshold": prompt_manager.get_threshold()
    }

@app.post("/api/save_prompt")
async def api_save_prompt(request: dict = Body(...)):
    key = request.get("key")
    value = request.get("value")
    if key in ["categorization", "search"]:
        prompt_manager.save_prompt(key, value)
    return {"status": "saved"}

@app.post("/api/save_threshold")
async def api_save_threshold(request: dict = Body(...)):
    value = float(request.get("value", 0.65))
    prompt_manager.save_threshold(value)
    return {"status": "saved"}

@app.post("/build")
async def build_vault():
    setup_all_folders()
    process_youtube_links()
    process_report()
    create_obsidian_structure()
    return {"status": "success"}

@app.post("/api/enhance")
async def enhance_all():
    enhanced = 0
    for root, _, files in os.walk(VAULT_ROOT):
        for f in files:
            if f.endswith(".md"):
                p = Path(root) / f
                summary = ollama_client.enhance_note(p)
                if summary and "unavailable" not in summary:
                    with open(p, "a", encoding="utf-8") as fp:
                        fp.write(f"\n\n## AI Summary (Ollama)\n{summary}\n")
                    enhanced += 1
    return {"enhanced": enhanced}

@app.post("/api/chat")
async def chat(request: dict = Body(...)):
    msg = request.get("message", "")
    assignment = model_manager.get_assignment()
    model = request.get("model") or assignment.get("primary")
    reply = ollama_client.chat_with_vault(msg, model)
    return {"reply": reply}

@app.post("/api/save_thought")
async def api_save_thought(request: dict = Body(...)):
    thought = request.get("thought", "")
    return save_thought_and_reply(thought)

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🧠 Second Brain Builder 2026</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap'); body {{ font-family: 'Inter', system-ui; }}</style>
</head>
<body class="bg-zinc-950 text-zinc-100">
<div class="flex h-screen">
    <!-- Sidebar -->
    <div class="w-72 bg-zinc-900 border-r border-zinc-800 p-6 flex flex-col">
        <div class="flex items-center gap-3 mb-8">
            <div class="w-9 h-9 bg-violet-600 rounded-xl flex items-center justify-center text-xl">🧠</div>
            <div><h1 class="text-2xl font-semibold">Second Brain</h1><p class="text-xs text-zinc-500">Ollama Connected</p></div>
        </div>
        <nav class="flex-1 space-y-1">
            <a id="tab-link-0" onclick="switchTab(0)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl bg-zinc-800 text-white">📊 Dashboard</a>
            <a id="tab-link-1" onclick="switchTab(1)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">💬 AI Chat</a>
            <a id="tab-link-2" onclick="switchTab(2)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">⚙️ Models Config</a>
            <a id="tab-link-3" onclick="switchTab(3)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">📝 Prompts Config</a>
        </nav>
        <div class="pt-6">
            <button onclick="buildVault()" class="w-full bg-violet-600 hover:bg-violet-700 py-4 rounded-3xl font-semibold">🚀 Build Vault</button>
            <button onclick="enhanceWithAI()" class="mt-3 w-full border border-violet-500 text-violet-400 hover:bg-violet-950 py-3 rounded-3xl">✨ Enhance with Ollama</button>
        </div>
    </div>

    <!-- Main Area -->
    <div class="flex-1 flex flex-col">
        <div class="h-16 border-b border-zinc-800 bg-zinc-900 px-8 flex items-center justify-between">
            <h2 id="tabTitle" class="text-xl font-semibold">Dashboard</h2>
            <span id="status" class="px-4 py-1 text-xs bg-emerald-500/10 text-emerald-400 rounded-full">Ollama Ready</span>
        </div>

        <!-- Dashboard -->
        <div id="tab0" class="flex-1 p-8 overflow-auto">
            <!-- Drop a thought -->
            <div class="bg-zinc-900 rounded-3xl p-6 mb-8">
                <div class="text-lg font-semibold mb-3">Drop a new thought</div>
                <textarea id="thoughtInput" class="w-full h-32 bg-zinc-800 text-zinc-300 rounded-xl p-4 focus:outline-none focus:border-violet-500 resize-none" placeholder="Type or paste your thought here..."></textarea>
                <button id="saveButton" onclick="saveThought()" class="mt-4 w-40 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl flex items-center justify-center gap-2">
                    <span class="text-sm">💾 Save to 2nd Brain</span>
                </button>
                <div id="replySection" class="mt-6 p-4 bg-blue-900/30 rounded-xl text-blue-200">
                    <div class="text-sm font-semibold mb-1">🤖 2nd Brain Reply:</div>
                    <p>Waiting for your next thought... Drop one and I'll reply instantly! ★</p>
                </div>
            </div>

            <!-- Category Cards with Avg Confidence -->
            <div class="grid grid-cols-6 gap-6 mb-8" id="categoryCards">
                <div onclick="setCategoryFilter('all')" id="card-all" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer border-2 border-violet-500">
                    <div class="text-sm text-zinc-500">Total Thoughts</div>
                    <div class="flex justify-between items-baseline">
                        <div id="totalNotes" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-all">0.65</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('People')" id="card-People" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">People</div>
                    <div class="flex justify-between items-baseline">
                        <div id="peopleCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-People">0.65</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Projects')" id="card-Projects" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Projects</div>
                    <div class="flex justify-between items-baseline">
                        <div id="projectsCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Projects">0.65</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Ideas')" id="card-Ideas" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Ideas</div>
                    <div class="flex justify-between items-baseline">
                        <div id="ideasCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Ideas">0.65</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Admin')" id="card-Admin" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Admin</div>
                    <div class="flex justify-between items-baseline">
                        <div id="adminCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Admin">0.65</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Review')" id="card-Review" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Review</div>
                    <div class="flex justify-between items-baseline">
                        <div id="reviewCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Review">0.65</span></div>
                    </div>
                </div>
            </div>

            <!-- Table with checkboxes (modal only on non-checkbox clicks) -->
            <div class="bg-zinc-900 rounded-3xl overflow-hidden">
                <div class="px-8 py-5 border-b border-zinc-700 flex justify-between items-center">
                    <h3 id="tableTitle" class="text-lg font-semibold">All Thoughts</h3>
                    <span id="filteredCount" class="text-zinc-400 text-sm">0 thoughts</span>
                </div>
                <table class="w-full">
                    <thead>
                        <tr class="bg-zinc-800 text-zinc-400 text-sm">
                            <th class="p-4 w-10"><input type="checkbox" id="selectAllHeader" class="accent-violet-500 w-5 h-5" onclick="toggleSelectAll()"></th>
                            <th onclick="sortTable(0)" class="p-4 text-left cursor-pointer hover:text-white">Filename <span id="sort0">↕</span></th>
                            <th onclick="sortTable(1)" class="p-4 text-left cursor-pointer hover:text-white">Category <span id="sort1">↕</span></th>
                            <th onclick="sortTable(2)" class="p-4 text-left cursor-pointer hover:text-white">Confidence <span id="sort2">↕</span></th>
                            <th onclick="sortTable(3)" class="p-4 text-left cursor-pointer hover:text-white">Date <span id="sort3">↕</span></th>
                            <th class="p-4 w-12"></th>
                        </tr>
                    </thead>
                    <tbody id="thoughtsTableBody" class="text-sm"></tbody>
                </table>
            </div>
        </div>

        <!-- AI Chat Tab -->
        <div id="tab1" class="flex-1 hidden flex-col">
            <div class="flex-1 p-8 overflow-auto" id="chatWindow"></div>
            <div class="p-4 border-t border-zinc-800 bg-zinc-900 flex gap-3">
                <input id="chatInput" type="text" class="flex-1 bg-zinc-800 border border-zinc-700 rounded-3xl px-6 py-4 focus:outline-none" placeholder="Ask your Second Brain...">
                <button onclick="sendChat()" class="bg-violet-600 px-8 rounded-3xl font-semibold">Send</button>
            </div>
        </div>

        <!-- Models Config Tab -->
        <div id="tab2" class="flex-1 p-8 overflow-auto hidden">
            <div id="ollamaStatus" class="mb-6 p-4 bg-zinc-800 rounded-3xl flex items-center gap-3 text-sm"></div>
            <div class="bg-zinc-900 rounded-3xl p-6">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="font-semibold text-lg">Chat Models Assignment</h3>
                    <button onclick="refreshModels()" class="px-6 py-2 bg-violet-600 hover:bg-violet-700 rounded-2xl text-sm font-medium">🔄 Refresh from Ollama</button>
                </div>
                <div id="modelTable" class="overflow-x-auto"></div>
                <div id="emptyState" class="hidden mt-8 text-center py-12">
                    <div class="text-6xl mb-4">🤖</div>
                    <p class="text-xl font-medium mb-2">No models found</p>
                </div>
                <div class="mt-6 text-xs text-zinc-400">Auto-sorted Primary → FB1 → FB2 → FB3</div>
            </div>
        </div>

        <!-- Prompts Config Tab -->
        <div id="tab3" class="flex-1 p-6 overflow-hidden">
            <div class="space-y-6 h-full flex flex-col">
                <div class="bg-zinc-900 rounded-3xl p-5 flex-1 flex flex-col">
                    <h3 class="font-semibold text-lg mb-3">Categorization Prompt</h3>
                    <textarea id="categorizationPrompt" class="flex-1 bg-zinc-800 text-zinc-300 p-4 rounded-xl font-mono text-sm focus:outline-none focus:border-violet-500 resize-none" spellcheck="false"></textarea>
                    <div class="flex gap-3 mt-4">
                        <button onclick="saveCategorizationPrompt()" class="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2">
                            💾 Save Categorization Prompt
                        </button>
                        <button onclick="resetCategorizationPrompt()" class="px-6 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 py-3 rounded-xl font-medium flex items-center gap-2">
                            🔄 Reset
                        </button>
                    </div>
                </div>
                <div class="bg-zinc-900 rounded-3xl p-5 flex-1 flex flex-col">
                    <h3 class="font-semibold text-lg mb-3">Search Prompt</h3>
                    <textarea id="searchPrompt" class="flex-1 bg-zinc-800 text-zinc-300 p-4 rounded-xl font-mono text-sm focus:outline-none focus:border-violet-500 resize-none" spellcheck="false"></textarea>
                    <div class="flex gap-3 mt-4">
                        <button onclick="saveSearchPrompt()" class="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2">
                            💾 Save Search Prompt
                        </button>
                        <button onclick="resetSearchPrompt()" class="px-6 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 py-3 rounded-xl font-medium flex items-center gap-2">
                            🔄 Reset Search Prompt
                        </button>
                    </div>
                </div>
                <div class="bg-zinc-900 rounded-3xl p-5">
                    <h3 class="font-semibold text-lg mb-3">Confidence Threshold</h3>
                    <div class="flex items-center gap-6">
                        <input type="range" id="thresholdSlider" min="0.60" max="1.00" step="0.01" value="0.65" class="flex-1 accent-violet-500" oninput="updateThresholdValue()">
                        <span id="thresholdValue" class="font-mono text-lg w-12 text-right">0.65</span>
                        <button onclick="saveThreshold()" class="bg-violet-600 hover:bg-violet-700 text-white px-8 py-3 rounded-xl font-semibold">Save Threshold</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ELEGANT MARKDOWN MODAL WITH DELETE -->
<div id="noteModal" class="hidden fixed inset-0 bg-black/80 flex items-center justify-center z-50">
    <div class="bg-zinc-900 rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl">
        <div class="flex items-center justify-between px-8 py-5 border-b border-zinc-700">
            <div id="modalFilename" class="font-semibold text-xl text-zinc-100"></div>
            <div class="flex items-center gap-4">
                <a id="modalOpenObsidian" href="#" target="_blank" class="text-violet-400 hover:text-violet-300 text-sm flex items-center gap-1">
                    Open in Obsidian →
                </a>
                <button onclick="closeModal()" class="w-8 h-8 flex items-center justify-center text-zinc-400 hover:text-white text-2xl leading-none">×</button>
            </div>
        </div>
        <div class="flex-1 p-8 overflow-auto">
            <pre id="modalContent" class="whitespace-pre-wrap font-mono text-zinc-200 text-sm leading-relaxed"></pre>
        </div>
        <div class="p-4 border-t border-zinc-700 flex justify-between">
            <button onclick="deleteCurrentNote()" class="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-2xl font-medium flex items-center gap-2">
                🗑️ Delete Note
            </button>
            <button onclick="closeModal()" class="px-8 py-3 bg-zinc-800 hover:bg-zinc-700 text-white rounded-2xl font-medium">Close</button>
        </div>
    </div>
</div>

<script>
let messages = [];
let modelsData = [];
let currentThreshold = 0.65;
let currentNotePath = '';
let currentCategoryFilter = 'all';
let sortColumn = 0;
let sortAsc = true;

async function refreshStats() {{
    const res = await fetch('/api/stats');
    const stats = await res.json();
    document.getElementById('totalNotes').textContent = stats.total_notes;
    document.getElementById('peopleCount').textContent = stats.People;
    document.getElementById('projectsCount').textContent = stats.Projects;
    document.getElementById('ideasCount').textContent = stats.Ideas;
    document.getElementById('adminCount').textContent = stats.Admin;
    document.getElementById('reviewCount').textContent = stats.Review;

    document.getElementById('avg-all').textContent = stats.avg_all.toFixed(2);
    document.getElementById('avg-People').textContent = stats.avg_People.toFixed(2);
    document.getElementById('avg-Projects').textContent = stats.avg_Projects.toFixed(2);
    document.getElementById('avg-Ideas').textContent = stats.avg_Ideas.toFixed(2);
    document.getElementById('avg-Admin').textContent = stats.avg_Admin.toFixed(2);
    document.getElementById('avg-Review').textContent = stats.avg_Review.toFixed(2);
}}

function highlightActiveCard() {{
    document.querySelectorAll('.category-card').forEach(c => c.classList.remove('border-violet-500'));
    if (currentCategoryFilter === 'all') {{
        document.getElementById('card-all').classList.add('border-violet-500');
    }} else {{
        document.getElementById(`card-${{currentCategoryFilter}}`).classList.add('border-violet-500');
    }}
}}

function setCategoryFilter(cat) {{
    currentCategoryFilter = cat;
    document.getElementById('tableTitle').textContent = cat === 'all' ? 'All Thoughts' : `${{cat}} Thoughts`;
    renderTable();
    highlightActiveCard();
}}

async function renderTable() {{
    const res = await fetch('/api/notes');
    let notes = await res.json();

    if (currentCategoryFilter !== 'all') {{
        notes = notes.filter(n => n.name.toLowerCase().startsWith(currentCategoryFilter.toLowerCase() + '-'));
    }}

    notes.sort((a, b) => {{
        let va = a.name, vb = b.name;
        if (sortColumn === 3) {{
            va = va.match(/\\d{{8}}$/) ? va.match(/\\d{{8}}$/)[0] : '0';
            vb = vb.match(/\\d{{8}}$/) ? vb.match(/\\d{{8}}$/)[0] : '0';
        }}
        if (va < vb) return sortAsc ? -1 : 1;
        if (va > vb) return sortAsc ? 1 : -1;
        return 0;
    }});

    let html = '';
    notes.forEach(n => {{
        const catMatch = n.name.match(/^([a-z]+)-/i);
        const cat = catMatch ? catMatch[1].charAt(0).toUpperCase() + catMatch[1].slice(1) : 'Review';
        const confMatch = n.name.match(/-([0-9.]+)-\\d{{8}}\\.md$/);
        const conf = confMatch ? confMatch[1] : '0.65';
        const dateMatch = n.name.match(/(\\d{{8}})\\.md$/);
        const date = dateMatch ? dateMatch[1] : '';
        html += `<tr class="border-t border-zinc-800 hover:bg-zinc-800 cursor-pointer" onclick="if(!event.target.closest('input[type=checkbox]')) showNoteModal('${{n.path}}')">
            <td class="p-4"><input type="checkbox" class="row-checkbox accent-violet-500 w-5 h-5" onclick="event.stopImmediatePropagation()"></td>
            <td class="p-4 font-medium">${{n.name}}</td>
            <td class="p-4">${{cat}}</td>
            <td class="p-4 text-emerald-400 font-mono">${{conf}}</td>
            <td class="p-4 text-zinc-400">${{date}}</td>
            <td class="p-4">
                <button onclick="event.stopImmediatePropagation(); deleteNote('${{n.path}}');" class="text-red-400 hover:text-red-500">🗑️</button>
            </td>
        </tr>`;
    }});

    document.getElementById('thoughtsTableBody').innerHTML = html;
    document.getElementById('filteredCount').textContent = `${{notes.length}} thoughts`;
}}

function toggleSelectAll() {{
    const checked = document.getElementById('selectAllHeader').checked;
    document.querySelectorAll('.row-checkbox').forEach(chk => {{
        chk.checked = checked;
    }});
}}

async function deleteNote(path) {{
    if (!confirm("Delete this thought permanently?")) return;
    await fetch(`/api/note/${{path}}`, {{method: 'DELETE'}});
    renderTable();
    refreshStats();
}}

function sortTable(col) {{
    if (sortColumn === col) sortAsc = !sortAsc;
    else {{ sortColumn = col; sortAsc = true; }}
    renderTable();
}}

async function loadModels() {{
    const res = await fetch('/api/models');
    modelsData = await res.json();
}}
async function loadModelConfig() {{
    const res = await fetch('/api/model_config');
    return await res.json();
}}
async function loadOllamaStatus() {{
    const res = await fetch('/api/ollama_status');
    return await res.json();
}}
async function renderModelTable() {{
    const status = await loadOllamaStatus();
    let assignment = await loadModelConfig();

    const statusEl = document.getElementById('ollamaStatus');
    statusEl.innerHTML = `
        <span class="px-3 py-1 rounded-full text-xs font-medium ${{status.connected ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}}">
            ${{status.connected ? '✅ Connected' : '❌ Not reachable'}}
        </span>
        <span class="font-mono text-xs">Host: ${{status.host}} • ${{status.models_count}} models loaded</span>
    `;

    if (modelsData.length === 0) {{
        document.getElementById('modelTable').classList.add('hidden');
        document.getElementById('emptyState').classList.remove('hidden');
        return;
    }}
    document.getElementById('modelTable').classList.remove('hidden');
    document.getElementById('emptyState').classList.add('hidden');

    const priority = [assignment.primary, assignment.fallback1, assignment.fallback2, assignment.fallback3];
    modelsData.sort((a, b) => {{
        const pa = priority.indexOf(a.name);
        const pb = priority.indexOf(b.name);
        if (pa === -1 && pb === -1) return 0;
        if (pa === -1) return 1;
        if (pb === -1) return -1;
        return pa - pb;
    }});

    let html = `
        <table class="w-full border-collapse text-sm">
            <thead><tr class="bg-zinc-800 text-zinc-400">
                <th class="p-4 text-left">Model Name</th>
                <th class="p-4 text-center">Primary</th>
                <th class="p-4 text-center">Fallback 1</th>
                <th class="p-4 text-center">Fallback 2</th>
                <th class="p-4 text-center">Fallback 3</th>
            </tr></thead>
            <tbody>
    `;
    modelsData.forEach(m => {{
        html += `<tr class="border-t border-zinc-800 hover:bg-zinc-800">
            <td class="p-4 font-medium">${{m.name}} <span class="text-xs text-zinc-500">(${{m.size_gb}} GB)</span></td>
            <td class="p-4 text-center"><input type="radio" name="primary" value="${{m.name}}" ${{assignment.primary===m.name?'checked':''}} onchange="updateAssignment(this)"></td>
            <td class="p-4 text-center"><input type="radio" name="fallback1" value="${{m.name}}" ${{assignment.fallback1===m.name?'checked':''}} onchange="updateAssignment(this)"></td>
            <td class="p-4 text-center"><input type="radio" name="fallback2" value="${{m.name}}" ${{assignment.fallback2===m.name?'checked':''}} onchange="updateAssignment(this)"></td>
            <td class="p-4 text-center"><input type="radio" name="fallback3" value="${{m.name}}" ${{assignment.fallback3===m.name?'checked':''}} onchange="updateAssignment(this)"></td>
        </tr>`;
    }});
    html += `</tbody></table>`;
    document.getElementById('modelTable').innerHTML = html;
}}
async function updateAssignment(el) {{
    let assignment = {{}};
    ['primary','fallback1','fallback2','fallback3'].forEach(role => {{
        const checked = document.querySelector(`input[name="${{role}}"]:checked`);
        assignment[role] = checked ? checked.value : '';
    }});
    await fetch('/api/model_config', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify(assignment)}});
    await renderModelTable();
}}
async function refreshModels() {{
    await loadModels();
    await renderModelTable();
}}
async function showNoteModal(path) {{
    currentNotePath = path;
    const res = await fetch(`/api/note/${{path}}`);
    const data = await res.json();
    if (data.error) return alert(data.error);

    document.getElementById('modalFilename').textContent = data.filename;
    document.getElementById('modalContent').textContent = data.content;
    document.getElementById('modalOpenObsidian').href = `/vault/${{path}}`;
    document.getElementById('noteModal').classList.remove('hidden');
    document.getElementById('noteModal').classList.add('flex');
}}
async function deleteCurrentNote() {{
    if (!currentNotePath) return;
    if (!confirm("Permanently delete this note?")) return;

    const res = await fetch(`/api/note/${{currentNotePath}}`, {{method: 'DELETE'}});
    if ((await res.json()).status === "deleted") {{
        closeModal();
        renderTable();
        refreshStats();
    }}
}}
function closeModal() {{
    const modal = document.getElementById('noteModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    currentNotePath = '';
}}
document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') closeModal();
}});
document.getElementById('noteModal').addEventListener('click', (e) => {{
    if (e.target.id === 'noteModal') closeModal();
}});
async function buildVault() {{
    await fetch('/build', {{method:'POST'}});
    renderTable();
    refreshStats();
}}
async function enhanceWithAI() {{
    await fetch('/api/enhance', {{method:'POST'}});
    alert('All notes enhanced with Ollama summaries!');
    renderTable();
    refreshStats();
}}
async function sendChat() {{
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    messages.push({{role:'user', content:msg}});
    renderChat();
    input.value = '';
    const res = await fetch('/api/chat', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{message:msg}})}});
    const data = await res.json();
    messages.push({{role:'assistant', content:data.reply}});
    renderChat();
}}
function renderChat() {{
    const win = document.getElementById('chatWindow');
    win.innerHTML = messages.map(m => `
        <div class="mb-6 ${{m.role==='user'?'text-right':''}}">
            <div class="inline-block max-w-lg px-5 py-3 rounded-3xl ${{m.role==='user'?'bg-violet-600':'bg-zinc-800'}}">
                ${{m.content}}
            </div>
        </div>
    `).join('');
    win.scrollTop = win.scrollHeight;
}}
async function saveThought() {{
    const input = document.getElementById('thoughtInput');
    const thought = input.value.trim();
    if (!thought) return;

    const btn = document.getElementById('saveButton');
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>Thinking...`;

    const res = await fetch('/api/save_thought', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{thought}})}});
    const data = await res.json();

    btn.disabled = false;
    btn.innerHTML = originalHTML;

    const replySection = document.getElementById('replySection');
    if (data.success) {{
        replySection.innerHTML = `
            <div class="text-sm font-semibold mb-1">🤖 2nd Brain Reply:</div>
            <p>${{data.reply}}</p>
        `;
        input.value = '';
        renderTable();
        refreshStats();
    }} else {{
        replySection.innerHTML = `<p class="text-red-600">Error: ${{data.reply}}</p>`;
    }}
}}
async function loadPrompts() {{
    const res = await fetch('/api/prompts');
    const data = await res.json();
    document.getElementById('categorizationPrompt').value = data.categorization;
    document.getElementById('searchPrompt').value = data.search;
    currentThreshold = data.threshold;
    document.getElementById('thresholdSlider').value = currentThreshold;
    document.getElementById('thresholdValue').textContent = currentThreshold.toFixed(2);
}}
async function saveCategorizationPrompt() {{
    const value = document.getElementById('categorizationPrompt').value;
    await fetch('/api/save_prompt', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{key:"categorization", value}})}});
}}
async function resetCategorizationPrompt() {{
    if (confirm("Reset to default? This is a destructive action.")) {{
        await fetch('/api/save_prompt', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{key:"categorization", value:""}})}});
        loadPrompts();
    }}
}}
async function saveSearchPrompt() {{
    const value = document.getElementById('searchPrompt').value;
    await fetch('/api/save_prompt', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{key:"search", value}})}});
}}
async function resetSearchPrompt() {{
    if (confirm("Reset to default? This is a destructive action.")) {{
        await fetch('/api/save_prompt', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{key:"search", value:""}})}});
        loadPrompts();
    }}
}}
function updateThresholdValue() {{
    currentThreshold = parseFloat(document.getElementById('thresholdSlider').value);
    document.getElementById('thresholdValue').textContent = currentThreshold.toFixed(2);
}}
async function saveThreshold() {{
    await fetch('/api/save_threshold', {{method:'POST', headers:{{"Content-Type":"application/json"}}, body:JSON.stringify({{value: currentThreshold}})}});
}}
function switchTab(n) {{
    document.querySelectorAll('#tab0,#tab1,#tab2,#tab3').forEach((el,i)=>el.classList.toggle('hidden', i!==n));
    document.getElementById('tabTitle').textContent = ['Dashboard','AI Chat','Models Config','Prompts Config'][n];

    document.querySelectorAll('.tab-btn').forEach((el, i) => {{
        if (i === n) {{
            el.classList.add('bg-zinc-800', 'text-white');
            el.classList.remove('text-zinc-400');
        }} else {{
            el.classList.remove('bg-zinc-800', 'text-white');
            el.classList.add('text-zinc-400');
        }}
    }});

    if (n===2) loadModels().then(() => renderModelTable());
    if (n===3) loadPrompts();
    if (n===0) {{ renderTable(); refreshStats(); }}
}}
window.onload = () => {{
    refreshStats();
    renderTable();
    loadPrompts();
    switchTab(0);
    highlightActiveCard();
}}
</script>
</body>
</html>
"""
