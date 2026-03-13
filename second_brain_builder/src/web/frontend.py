# filename: second_brain_builder/src/web/frontend.py
# purpose: COMPLETE HTML + JS (vertical slider, full table, AI Chat, semantic toggle, all tabs) - 100% working UI

def get_html():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🧠 Second Brain Builder 2026</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        body { font-family: 'Inter', system-ui; }
        input[type="range"][orient="vertical"] {
            writing-mode: bt-lr;
            appearance: slider-vertical;
            -webkit-appearance: slider-vertical;
            height: 280px;
            width: 20px;
            accent-color: rgb(167 139 250);
        }
    </style>
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
            <button onclick="enhanceWithAI()" id="enhanceBtn" class="w-full border border-violet-500 text-violet-400 hover:bg-violet-950 py-3 rounded-3xl flex items-center justify-center gap-2">
                ✨ Enhance with Ollama
            </button>
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
            <div class="bg-zinc-900 rounded-3xl p-4 mb-8 flex gap-6">
                <div class="flex-1 flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <div class="text-lg font-semibold">Drop a new thought</div>
                        <button id="saveButton" onclick="saveThought()" class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-2.5 px-6 rounded-2xl font-medium">
                            <span class="text-xl">📥</span>
                            Save to 2nd Brain
                        </button>
                    </div>
                    <textarea id="thoughtInput" class="flex-1 bg-zinc-800 text-zinc-300 rounded-2xl p-4 focus:outline-none focus:border-violet-500 resize-none h-36" placeholder="Type or paste your thought here..."></textarea>
                </div>
                <div class="flex-1 bg-blue-900/30 rounded-3xl p-6 flex flex-col">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="text-xl">🤖</span>
                        <div class="font-semibold text-blue-200">2nd Brain Reply:</div>
                    </div>
                    <div id="replySection" class="flex-1 text-blue-200 text-sm overflow-auto">
                        Waiting for your next thought... Drop one and I'll reply instantly! ★
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-6 gap-6 mb-8">
                <div onclick="setCategoryFilter('all')" id="card-all" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer border-2 border-violet-500">
                    <div class="text-sm text-zinc-500">Total Thoughts</div>
                    <div class="flex justify-between items-baseline">
                        <div id="totalNotes" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-all">0.00</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('People')" id="card-People" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">People</div>
                    <div class="flex justify-between items-baseline">
                        <div id="peopleCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-People">0.00</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Projects')" id="card-Projects" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Projects</div>
                    <div class="flex justify-between items-baseline">
                        <div id="projectsCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Projects">0.00</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Ideas')" id="card-Ideas" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Ideas</div>
                    <div class="flex justify-between items-baseline">
                        <div id="ideasCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Ideas">0.00</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Admin')" id="card-Admin" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Admin</div>
                    <div class="flex justify-between items-baseline">
                        <div id="adminCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Admin">0.00</span></div>
                    </div>
                </div>
                <div onclick="setCategoryFilter('Review')" id="card-Review" class="category-card bg-zinc-900 hover:bg-zinc-800 rounded-3xl p-6 cursor-pointer">
                    <div class="text-sm text-zinc-500">Review</div>
                    <div class="flex justify-between items-baseline">
                        <div id="reviewCount" class="text-5xl font-semibold">0</div>
                        <div class="text-emerald-400 text-sm font-mono">Avg <span id="avg-Review">0.00</span></div>
                    </div>
                </div>
            </div>
            <div class="bg-zinc-900 rounded-3xl overflow-hidden">
                <div class="px-8 py-5 border-b border-zinc-700 flex items-center justify-between">
                    <h3 id="tableTitle" class="text-lg font-semibold">All Thoughts</h3>
                    <div class="flex items-center gap-4">
                        <input id="thoughtFilter" type="text" placeholder="Filter thoughts..." class="bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-2 text-sm focus:outline-none focus:border-violet-500 w-80">
                        <label class="flex items-center gap-2 text-sm text-zinc-400 cursor-pointer">
                            <input type="checkbox" id="semanticToggle" class="accent-violet-500"> Semantic search
                        </label>
                    </div>
                    <div class="flex items-center gap-6">
                        <div id="bulkActions" class="hidden flex items-center gap-3">
                            <button onclick="deleteSelected()" class="flex items-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-2xl font-medium text-sm">
                                🗑️ Delete Selected
                            </button>
                            <button onclick="bulkEditSelected()" class="flex items-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 text-white rounded-2xl font-medium text-sm">
                                ✏️ Bulk Edit Selected
                            </button>
                            <button onclick="sendForAIReview()" id="reviewButton" class="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-medium text-sm">
                                📤 Send Selected for AI Review
                            </button>
                        </div>
                        <span id="filteredCount" class="text-zinc-400 text-sm font-medium">0 thoughts</span>
                    </div>
                </div>
                <table class="w-full">
                    <thead>
                        <tr class="bg-zinc-800 text-zinc-400 text-sm">
                            <th class="p-4 w-10"><input type="checkbox" id="selectAllHeader" class="accent-violet-500 w-5 h-5" onclick="toggleSelectAll()"></th>
                            <th onclick="sortTable(0)" class="p-4 text-left cursor-pointer hover:text-white">Thought <span id="sort0" class="sort-indicator">↕</span></th>
                            <th onclick="sortTable(1)" class="p-4 text-left cursor-pointer hover:text-white">Category <span id="sort1" class="sort-indicator">↕</span></th>
                            <th onclick="sortTable(2)" class="p-4 text-left cursor-pointer hover:text-white">Confidence <span id="sort2" class="sort-indicator">↕</span></th>
                            <th onclick="sortTable(3)" class="p-4 text-left cursor-pointer hover:text-white">Date & Time <span id="sort3" class="sort-indicator">↕</span></th>
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
        <div id="tab3" class="flex-1 p-6 overflow-hidden hidden">
            <div class="flex gap-6 h-full">
                <div class="w-56 bg-zinc-900 rounded-3xl p-6 flex flex-col items-center">
                    <h3 class="font-semibold text-lg text-center mb-4">AI Review Threshold</h3>
                    <div class="flex flex-col items-center flex-1">
                        <input type="range" id="thresholdSlider" orient="vertical" min="0.60" max="1.00" step="0.01" value="0.65" class="accent-violet-500 h-72" oninput="updateThresholdValue()">
                        <div class="mt-6 text-4xl font-mono text-violet-300" id="thresholdValue">0.65</div>
                    </div>
                    <button onclick="saveThreshold()" class="mt-4 w-full bg-violet-600 hover:bg-violet-700 text-white py-3 rounded-2xl font-semibold">Save Threshold</button>
                </div>
                <div class="flex-1 flex flex-col gap-6">
                    <div class="bg-zinc-900 rounded-3xl p-5 flex-1 flex flex-col">
                        <h3 class="font-semibold text-lg mb-3">Categorization Prompt</h3>
                        <textarea id="categorizationPrompt" class="flex-1 bg-zinc-800 text-zinc-300 p-4 rounded-xl font-mono text-sm focus:outline-none focus:border-violet-500 resize-none"></textarea>
                        <div class="flex gap-3 mt-4">
                            <button onclick="saveCategorizationPrompt()" class="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2">
                                💾 Save
                            </button>
                            <button onclick="resetCategorizationPrompt()" class="px-6 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 py-3 rounded-xl font-medium">🔄 Reset</button>
                        </div>
                    </div>
                    <div class="bg-zinc-900 rounded-3xl p-5 flex-1 flex flex-col">
                        <h3 class="font-semibold text-lg mb-3">Search Prompt</h3>
                        <textarea id="searchPrompt" class="flex-1 bg-zinc-800 text-zinc-300 p-4 rounded-xl font-mono text-sm focus:outline-none focus:border-violet-500 resize-none"></textarea>
                        <div class="flex gap-3 mt-4">
                            <button onclick="saveSearchPrompt()" class="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2">
                                💾 Save
                            </button>
                            <button onclick="resetSearchPrompt()" class="px-6 bg-zinc-700 hover:bg-zinc-600 text-zinc-300 py-3 rounded-xl font-medium">🔄 Reset</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- NOTE MODAL -->
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

<!-- BULK EDIT MODAL -->
<div id="bulkEditModal" class="hidden fixed inset-0 bg-black/80 flex items-center justify-center z-50">
    <div class="bg-zinc-900 rounded-3xl w-full max-w-md shadow-2xl overflow-hidden">
        <div class="px-6 py-4 border-b border-zinc-700 flex items-center justify-between">
            <h3 id="bulkEditTitle" class="font-semibold text-lg">Bulk Edit 0 Thoughts</h3>
            <button onclick="hideBulkEditModal()" class="text-zinc-400 hover:text-white text-2xl">×</button>
        </div>
        <div class="p-6 space-y-6">
            <div>
                <label class="block text-sm text-zinc-400 mb-2">New Category</label>
                <select id="bulkNewCategory" class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-4 py-3 text-zinc-100 focus:outline-none focus:border-violet-500">
                    <option value="keep">Keep current</option>
                    <option value="People">People</option>
                    <option value="Projects">Projects</option>
                    <option value="Ideas">Ideas</option>
                    <option value="Admin">Admin</option>
                    <option value="Review">Review</option>
                </select>
            </div>
            <div>
                <label class="block text-sm text-zinc-400 mb-2">New Confidence</label>
                <input id="bulkNewConfidence" type="number" step="0.01" min="0.00" max="1.00" class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-4 py-3 text-zinc-100 focus:outline-none focus:border-violet-500 font-mono">
            </div>
            <div class="flex items-center gap-3">
                <input id="bulkSetReview" type="checkbox" class="accent-violet-500 w-5 h-5">
                <label class="text-zinc-300">Set Needs Review</label>
            </div>
        </div>
        <div class="p-4 border-t border-zinc-700 flex gap-3">
            <button onclick="hideBulkEditModal()" class="flex-1 bg-zinc-700 hover:bg-zinc-600 py-3 rounded-2xl font-medium">Cancel</button>
            <button onclick="applyBulkEdit()" class="flex-1 bg-blue-600 hover:bg-blue-700 py-3 rounded-2xl font-medium">Apply to All Selected</button>
        </div>
    </div>
</div>

<script>
let sortColumn = 0;
let sortAsc = true;
let selectedPaths = new Set();
let currentCategoryFilter = 'all';
let useSemantic = false;
let messages = [];

async function refreshStats() {
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
}

function highlightActiveCard() {
    document.querySelectorAll('.category-card').forEach(c => c.classList.remove('border-violet-500'));
    if (currentCategoryFilter === 'all') {
        document.getElementById('card-all').classList.add('border-violet-500');
    } else {
        const el = document.getElementById(`card-${currentCategoryFilter}`);
        if (el) el.classList.add('border-violet-500');
    }
}

function setCategoryFilter(cat) {
    currentCategoryFilter = cat;
    document.getElementById('tableTitle').textContent = cat === 'all' ? 'All Thoughts' : `${cat} Thoughts`;
    renderTable();
    highlightActiveCard();
}

function updateSortIndicators() {
    document.querySelectorAll('.sort-indicator').forEach(el => el.textContent = '↕');
    const currentIndicator = document.getElementById(`sort${sortColumn}`);
    if (currentIndicator) currentIndicator.textContent = sortAsc ? '↑' : '↓';
}

async function renderTable() {
    const filterText = document.getElementById('thoughtFilter').value.trim();
    let notes;
    if (useSemantic && filterText) {
        const res = await fetch(`/api/semantic_search?query=${encodeURIComponent(filterText)}&category=${currentCategoryFilter}`);
        notes = await res.json();
    } else {
        const res = await fetch('/api/notes');
        notes = await res.json();
        if (filterText) notes = notes.filter(n => n.thought.toLowerCase().includes(filterText.toLowerCase()));
        if (currentCategoryFilter !== 'all') notes = notes.filter(n => n.category.toLowerCase() === currentCategoryFilter.toLowerCase());
    }
    notes.sort((a, b) => {
        let va, vb;
        let multiplier = sortAsc ? 1 : -1;
        switch (sortColumn) {
            case 0: va = a.thought.toLowerCase(); vb = b.thought.toLowerCase(); break;
            case 1: va = a.category.toLowerCase(); vb = b.category.toLowerCase(); break;
            case 2: va = parseFloat(a.confidence) || 0; vb = parseFloat(b.confidence) || 0; break;
            case 3: va = a.datetime || ''; vb = b.datetime || ''; break;
        }
        if (va < vb) return multiplier * -1;
        if (va > vb) return multiplier * 1;
        return 0;
    });
    let html = '';
    notes.forEach(n => {
        const checked = selectedPaths.has(n.path) ? 'checked' : '';
        html += `<tr class="border-t border-zinc-800 hover:bg-zinc-800 cursor-pointer" onclick="if(!event.target.closest('input[type=checkbox]')) showNoteModal('${n.path}')">
            <td class="p-4"><input type="checkbox" class="row-checkbox accent-violet-500 w-5 h-5" data-path="${n.path}" ${checked} onclick="event.stopImmediatePropagation(); toggleRow(this)"></td>
            <td class="p-4 font-medium">${n.thought}</td>
            <td class="p-4">${n.category}</td>
            <td class="p-4 text-emerald-400 font-mono">${n.confidence}</td>
            <td class="p-4 text-zinc-400">${n.datetime}</td>
            <td class="p-4">
                <button onclick="event.stopImmediatePropagation(); deleteNote('${n.path}');" class="text-red-400 hover:text-red-500">🗑️</button>
            </td>
        </tr>`;
    });
    document.getElementById('thoughtsTableBody').innerHTML = html;
    document.getElementById('filteredCount').textContent = `${notes.length} thoughts`;
    updateBulkUI();
    updateSelectAllHeader();
    updateSortIndicators();
}

function toggleRow(checkbox) {
    const path = checkbox.dataset.path;
    if (checkbox.checked) selectedPaths.add(path);
    else selectedPaths.delete(path);
    updateBulkUI();
    updateSelectAllHeader();
}

function toggleSelectAll() {
    const checked = document.getElementById('selectAllHeader').checked;
    document.querySelectorAll('.row-checkbox').forEach(chk => {
        chk.checked = checked;
        const path = chk.dataset.path;
        if (checked) selectedPaths.add(path);
        else selectedPaths.delete(path);
    });
    updateBulkUI();
}

function updateSelectAllHeader() {
    const header = document.getElementById('selectAllHeader');
    const allCheckboxes = document.querySelectorAll('.row-checkbox');
    if (allCheckboxes.length === 0) {
        header.checked = false;
        return;
    }
    const checkedCount = Array.from(allCheckboxes).filter(chk => chk.checked).length;
    header.checked = checkedCount === allCheckboxes.length;
}

function updateBulkUI() {
    const count = selectedPaths.size;
    const bar = document.getElementById('bulkActions');
    bar.classList.toggle('hidden', count === 0);
}

async function deleteSelected() {
    if (selectedPaths.size === 0 || !confirm(`Delete ${selectedPaths.size} selected thoughts permanently?`)) return;
    for (let path of Array.from(selectedPaths)) {
        await fetch(`/api/note/${path}`, {method: 'DELETE'});
    }
    selectedPaths.clear();
    renderTable();
    refreshStats();
}

function bulkEditSelected() {
    const count = selectedPaths.size;
    if (count === 0) return;
    document.getElementById('bulkEditTitle').textContent = `Bulk Edit ${count} Thoughts`;
    document.getElementById('bulkNewConfidence').value = "0.75";
    document.getElementById('bulkSetReview').checked = false;
    document.getElementById('bulkEditModal').classList.remove('hidden');
    document.getElementById('bulkEditModal').classList.add('flex');
}

function hideBulkEditModal() {
    const modal = document.getElementById('bulkEditModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

async function applyBulkEdit() {
    const paths = Array.from(selectedPaths);
    const newCat = document.getElementById('bulkNewCategory').value;
    const newConf = parseFloat(document.getElementById('bulkNewConfidence').value);
    const forceReview = document.getElementById('bulkSetReview').checked;
    hideBulkEditModal();
    await fetch('/api/bulk_edit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({paths, new_category: newCat, new_confidence: newConf, force_review: forceReview})
    });
    selectedPaths.clear();
    renderTable();
    refreshStats();
    updateBulkUI();
}

async function sendForAIReview() {
    const paths = Array.from(selectedPaths);
    if (paths.length === 0) return;
    const btn = document.getElementById('reviewButton');
    const original = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></span> Reviewing...`;
    for (let path of paths) {
        await fetch('/api/enhance_note', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({path})
        });
    }
    btn.disabled = false;
    btn.innerHTML = original;
    selectedPaths.clear();
    renderTable();
    refreshStats();
    updateBulkUI();
}

async function deleteNote(path) {
    if (!confirm("Delete this thought permanently?")) return;
    await fetch(`/api/note/${path}`, {method: 'DELETE'});
    selectedPaths.delete(path);
    renderTable();
    refreshStats();
}

function sortTable(col) {
    if (sortColumn === col) sortAsc = !sortAsc;
    else { sortColumn = col; sortAsc = true; }
    renderTable();
}

async function showNoteModal(path) {
    const res = await fetch(`/api/note/${path}`);
    const data = await res.json();
    if (data.error) return;
    document.getElementById('modalFilename').textContent = data.filename;
    document.getElementById('modalContent').textContent = data.content;
    document.getElementById('modalOpenObsidian').href = `/vault/${path}`;
    document.getElementById('noteModal').classList.remove('hidden');
    document.getElementById('noteModal').classList.add('flex');
}

function closeModal() {
    const modal = document.getElementById('noteModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

async function enhanceWithAI() {
    const btn = document.getElementById('enhanceBtn');
    const original = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="animate-spin inline-block w-4 h-4 border-2 border-violet-400 border-t-transparent rounded-full mr-2"></span> Enhancing...`;
    const res = await fetch('/api/enhance', {method: 'POST'});
    const data = await res.json();
    btn.disabled = false;
    btn.innerHTML = original;
    if (data.status === "success") {
        alert(`✅ Enhanced ${data.enhanced} thoughts`);
        renderTable();
        refreshStats();
    }
}

function renderChat() {
    const win = document.getElementById('chatWindow');
    win.innerHTML = messages.map(m => `
        <div class="mb-6 ${m.role==='user' ? 'text-right' : ''}">
            <div class="inline-block max-w-lg px-5 py-3 rounded-3xl ${m.role==='user' ? 'bg-violet-600' : 'bg-zinc-800'}">
                ${m.content}
            </div>
        </div>
    `).join('');
    win.scrollTop = win.scrollHeight;
}

async function sendChat() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    messages.push({role: 'user', content: msg});
    renderChat();
    const tempMsg = msg;
    input.value = '';
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: tempMsg})
        });
        const data = await res.json();
        messages.push({role: 'assistant', content: data.reply || "No response from Ollama"});
        renderChat();
    } catch (e) {
        messages.push({role: 'assistant', content: "Error connecting to Ollama"});
        renderChat();
    }
}

async function saveThought() {
    const input = document.getElementById('thoughtInput');
    const thought = input.value.trim();
    if (!thought) return;
    const btn = document.getElementById('saveButton');
    const original = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>Saving...`;
    const res = await fetch('/api/save_thought', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify({thought})});
    const data = await res.json();
    btn.disabled = false;
    btn.innerHTML = original;
    if (data.success) {
        document.getElementById('replySection').innerHTML = `<p>${data.reply}</p>`;
        input.value = '';
        renderTable();
        refreshStats();
    }
}

/* ==================== MODELS TAB JS ==================== */
async function loadModels() {
    const res = await fetch('/api/models');
    modelsData = await res.json();
}
async function loadModelConfig() {
    const res = await fetch('/api/model_config');
    return await res.json();
}
async function loadOllamaStatus() {
    const res = await fetch('/api/ollama_status');
    return await res.json();
}
async function renderModelTable() {
    const status = await loadOllamaStatus();
    let assignment = await loadModelConfig();
    const statusEl = document.getElementById('ollamaStatus');
    const color = status.connected ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400';
    const icon = status.connected ? '✅' : '❌';
    statusEl.innerHTML = `
        <span class="px-3 py-1 rounded-full text-xs font-medium ${color}">
            ${icon} ${status.connected ? 'Connected' : 'Not reachable'}
        </span>
        <span class="font-mono text-xs">Host: ${status.host} • ${status.models_count} models loaded</span>
    `;
    if (modelsData.length === 0) {
        document.getElementById('modelTable').classList.add('hidden');
        document.getElementById('emptyState').classList.remove('hidden');
        return;
    }
    document.getElementById('modelTable').classList.remove('hidden');
    document.getElementById('emptyState').classList.add('hidden');
    const priority = [assignment.primary, assignment.fallback1, assignment.fallback2, assignment.fallback3];
    modelsData.sort((a, b) => {
        const pa = priority.indexOf(a.name);
        const pb = priority.indexOf(b.name);
        if (pa === -1 && pb === -1) return 0;
        if (pa === -1) return 1;
        if (pb === -1) return -1;
        return pa - pb;
    });
    let html = `<table class="w-full border-collapse text-sm"><thead><tr class="bg-zinc-800 text-zinc-400"><th class="p-4 text-left">Model Name</th><th class="p-4 text-center">Primary</th><th class="p-4 text-center">Fallback 1</th><th class="p-4 text-center">Fallback 2</th><th class="p-4 text-center">Fallback 3</th></tr></thead><tbody>`;
    modelsData.forEach(m => {
        html += `<tr class="border-t border-zinc-800 hover:bg-zinc-800"><td class="p-4 font-medium">${m.name} <span class="text-xs text-zinc-500">(${m.size_gb} GB)</span></td>`;
        html += `<td class="p-4 text-center"><input type="radio" name="primary" value="${m.name}" ${assignment.primary===m.name?'checked':''} onchange="updateAssignment(this)"></td>`;
        html += `<td class="p-4 text-center"><input type="radio" name="fallback1" value="${m.name}" ${assignment.fallback1===m.name?'checked':''} onchange="updateAssignment(this)"></td>`;
        html += `<td class="p-4 text-center"><input type="radio" name="fallback2" value="${m.name}" ${assignment.fallback2===m.name?'checked':''} onchange="updateAssignment(this)"></td>`;
        html += `<td class="p-4 text-center"><input type="radio" name="fallback3" value="${m.name}" ${assignment.fallback3===m.name?'checked':''} onchange="updateAssignment(this)"></td></tr>`;
    });
    html += `</tbody></table>`;
    document.getElementById('modelTable').innerHTML = html;
}
async function updateAssignment(el) {
    let assignment = {};
    ['primary','fallback1','fallback2','fallback3'].forEach(role => {
        const checked = document.querySelector(`input[name="${role}"]:checked`);
        assignment[role] = checked ? checked.value : '';
    });
    await fetch('/api/model_config', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify(assignment)});
    await renderModelTable();
}
async function refreshModels() {
    await loadModels();
    await renderModelTable();
}

/* ==================== PROMPTS TAB JS ==================== */
async function loadPrompts() {
    const res = await fetch('/api/prompts');
    const data = await res.json();
    document.getElementById('categorizationPrompt').value = data.categorization;
    document.getElementById('searchPrompt').value = data.search;
    currentThreshold = data.threshold;
    document.getElementById('thresholdSlider').value = currentThreshold;
    document.getElementById('thresholdValue').textContent = currentThreshold.toFixed(2);
}
async function saveCategorizationPrompt() {
    const value = document.getElementById('categorizationPrompt').value;
    await fetch('/api/save_prompt', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify({key:"categorization", value})});
}
async function resetCategorizationPrompt() {
    if (confirm("Reset to default?")) {
        await fetch('/api/save_prompt', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify({key:"categorization", value:""})});
        loadPrompts();
    }
}
async function saveSearchPrompt() {
    const value = document.getElementById('searchPrompt').value;
    await fetch('/api/save_prompt', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify({key:"search", value})});
}
async function resetSearchPrompt() {
    if (confirm("Reset to default?")) {
        await fetch('/api/save_prompt', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify({key:"search", value:""})});
        loadPrompts();
    }
}
function updateThresholdValue() {
    currentThreshold = parseFloat(document.getElementById('thresholdSlider').value);
    document.getElementById('thresholdValue').textContent = currentThreshold.toFixed(2);
}
async function saveThreshold() {
    await fetch('/api/save_threshold', {method:'POST', headers:{"Content-Type":"application/json"}, body:JSON.stringify({value: currentThreshold})});
}

function switchTab(n) {
    document.querySelectorAll('#tab0,#tab1,#tab2,#tab3').forEach((el,i)=>el.classList.toggle('hidden', i!==n));
    document.getElementById('tabTitle').textContent = ['Dashboard','AI Chat','Models Config','Prompts Config'][n];
    document.querySelectorAll('.tab-btn').forEach((el,i)=>el.classList.toggle('bg-zinc-800', i===n));
    if (n===0) { renderTable(); refreshStats(); }
    if (n===2) { loadModels().then(() => renderModelTable()); }
    if (n===3) { loadPrompts(); }
}

document.getElementById('thoughtFilter').addEventListener('keyup', () => renderTable());
document.getElementById('semanticToggle').addEventListener('change', (e) => {
    useSemantic = e.target.checked;
    renderTable();
});

window.onload = () => {
    refreshStats();
    renderTable();
    switchTab(0);
    highlightActiveCard();
}
</script>
</body>
</html>
"""
