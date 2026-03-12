# filename: second_brain_builder/src/web/app.py
# purpose: Sidebar now correctly highlights the ACTIVE tab with focus (bg-zinc-800 text-white) - Dashboard no longer stuck as always active

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

ollama_client = OllamaClient()

def get_vault_stats():
    stats = {"total_notes": 0, "youtube": 0, "cloud": 0, "local": 0, "db": 0, "emerging": 0}
    for root, _, files in os.walk(VAULT_ROOT):
        for f in files:
            if f.endswith(".md"):
                stats["total_notes"] += 1
                rel = str(Path(root).relative_to(VAULT_ROOT))
                if "youtube_notes" in rel: stats["youtube"] += 1
                elif "cloud_platforms" in rel: stats["cloud"] += 1
                elif "local_storage" in rel: stats["local"] += 1
                elif "databases" in rel: stats["db"] += 1
                elif "emerging" in rel: stats["emerging"] += 1
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
    stats = get_vault_stats()
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
            <a id="tab-link-2" onclick="switchTab(2)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">🧠 Thoughts</a>
            <a id="tab-link-3" onclick="switchTab(3)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">⚙️ Models Config</a>
            <a id="tab-link-4" onclick="switchTab(4)" class="tab-btn flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-zinc-800 text-zinc-400">📝 Prompts Config</a>
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

        <!-- Dashboard Tab -->
        <div id="tab0" class="flex-1 p-8 overflow-auto">
            <div class="grid grid-cols-4 gap-6">
                <div class="bg-zinc-900 rounded-3xl p-6">
                    <div class="text-sm text-zinc-500">Total Thoughts</div>
                    <div id="totalNotes" class="text-5xl font-semibold mt-2">{stats["total_notes"]}</div>
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
            <div id="notesList" class="mt-10 grid grid-cols-3 gap-4"></div>
        </div>

        <!-- AI Chat Tab -->
        <div id="tab1" class="flex-1 hidden flex-col">
            <div class="flex-1 p-8 overflow-auto" id="chatWindow"></div>
            <div class="p-4 border-t border-zinc-800 bg-zinc-900 flex gap-3">
                <input id="chatInput" type="text" class="flex-1 bg-zinc-800 border border-zinc-700 rounded-3xl px-6 py-4 focus:outline-none" placeholder="Ask your Second Brain...">
                <button onclick="sendChat()" class="bg-violet-600 px-8 rounded-3xl font-semibold">Send</button>
            </div>
        </div>

        <!-- Thoughts Tab -->
        <div id="tab2" class="flex-1 p-8 overflow-auto hidden flex flex-col">
            <div class="flex-1 flex flex-col">
                <div class="text-lg font-semibold mb-2">Drop a new thought</div>
                <textarea id="thoughtInput" class="w-full h-32 bg-white text-gray-500 rounded-lg p-4 focus:outline-none focus:border-blue-500 resize-none" placeholder="Type or paste your thought here..."></textarea>
                <button id="saveButton" onclick="saveThought()" class="mt-4 w-40 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg flex items-center justify-center gap-2">
                    <span class="text-sm">💾 Save to 2nd Brain</span>
                </button>
                <div id="replySection" class="mt-6 p-4 bg-blue-100/50 rounded-lg text-blue-800">
                    <div class="text-sm font-semibold mb-1">🤖 2nd Brain Reply:</div>
                    <p>Waiting for your next thought... Drop one and I'll reply instantly! ★</p>
                </div>
            </div>
            <input id="searchInput" type="text" placeholder="Search thoughts..." class="mt-auto bg-zinc-900 border border-zinc-700 rounded-2xl px-4 py-3 w-full" onkeyup="filterThoughts()">
            <div id="thoughtsListFull" class="mt-4 grid grid-cols-2 gap-4"></div>
        </div>

        <!-- Models Config Tab -->
        <div id="tab3" class="flex-1 p-8 overflow-auto hidden">
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
        <div id="tab4" class="flex-1 p-6 overflow-hidden">
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

<!-- ELEGANT MARKDOWN MODAL -->
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
        <div class="p-4 border-t border-zinc-700 flex justify-end">
            <button onclick="closeModal()" class="px-8 py-3 bg-zinc-800 hover:bg-zinc-700 text-white rounded-2xl font-medium">Close</button>
        </div>
    </div>
</div>

<script>
let messages = [];
let modelsData = [];
let currentThreshold = 0.65;

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
async function loadNotes() {{
    const res = await fetch('/api/notes');
    const notes = await res.json();
    const container = document.getElementById('notesList');
    container.innerHTML = notes.slice(0,9).map(n => `
        <div onclick="showNoteModal('${{n.path}}')" class="cursor-pointer block bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-5 border border-zinc-700 transition-all">
            <div class="font-medium">${{n.name}}</div>
        </div>
    `).join('');
}}
async function loadThoughts() {{
    const res = await fetch('/api/notes');
    const notes = await res.json();
    const container = document.getElementById('thoughtsListFull');
    container.innerHTML = notes.filter(n => n.path.includes('thoughts')).slice(0,6).map(n => `
        <div onclick="showNoteModal('${{n.path}}')" class="cursor-pointer block bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-5 border border-zinc-700 transition-all">
            <div class="font-medium">${{n.name}}</div>
        </div>
    `).join('');
}}
async function filterThoughts() {{
    const term = document.getElementById('searchInput').value.toLowerCase();
    const res = await fetch('/api/notes');
    const notes = await res.json();
    const filtered = notes.filter(n => n.path.includes('thoughts') && n.name.toLowerCase().includes(term));
    const container = document.getElementById('thoughtsListFull');
    container.innerHTML = filtered.slice(0,6).map(n => `
        <div onclick="showNoteModal('${{n.path}}')" class="cursor-pointer block bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-5 border border-zinc-700 transition-all">
            <div class="font-medium">${{n.name}}</div>
        </div>
    `).join('');
}}
async function showNoteModal(path) {{
    const res = await fetch(`/api/note/${{path}}`);
    const data = await res.json();
    if (data.error) return alert(data.error);

    document.getElementById('modalFilename').textContent = data.filename;
    document.getElementById('modalContent').textContent = data.content;
    document.getElementById('modalOpenObsidian').href = `/vault/${{path}}`;
    document.getElementById('noteModal').classList.remove('hidden');
    document.getElementById('noteModal').classList.add('flex');
}}
function closeModal() {{
    const modal = document.getElementById('noteModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}}
document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') closeModal();
}});
document.getElementById('noteModal').addEventListener('click', (e) => {{
    if (e.target.id === 'noteModal') closeModal();
}});
async function buildVault() {{
    await fetch('/build', {{method:'POST'}});
    loadNotes();
}}
async function enhanceWithAI() {{
    await fetch('/api/enhance', {{method:'POST'}});
    alert('All notes enhanced with Ollama summaries!');
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
        loadThoughts();
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
    document.querySelectorAll('#tab0,#tab1,#tab2,#tab3,#tab4').forEach((el,i)=>el.classList.toggle('hidden', i!==n));
    document.getElementById('tabTitle').textContent = ['Dashboard','AI Chat','Thoughts','Models Config','Prompts Config'][n];

    // ACTIVE TAB FOCUS - highlight the clicked sidebar item
    document.querySelectorAll('.tab-btn').forEach((el, i) => {{
        if (i === n) {{
            el.classList.add('bg-zinc-800', 'text-white');
            el.classList.remove('text-zinc-400');
        }} else {{
            el.classList.remove('bg-zinc-800', 'text-white');
            el.classList.add('text-zinc-400');
        }}
    }});

    if (n===3) loadModels().then(() => renderModelTable());
    if (n===2) loadThoughts();
    if (n===4) loadPrompts();
    if (n===0) loadNotes();
}}
window.onload = () => {{
    loadNotes();
    loadPrompts();
    switchTab(0);
}}
</script>
</body>
</html>
"""
