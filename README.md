# filename: README.md
# purpose: Complete up-to-date README for Second Brain Builder 2026 at current state

# 🧠 Second Brain Builder 2026

A beautiful, fast, local-first personal knowledge system powered by Ollama + Obsidian-compatible vault.

## Current Features (March 2026)

### Web GUI[](http://localhost:8000)
- **Drop a new thought** — type/paste → Save → instant AI reply
- **Live Filter thoughts...** search box (real-time on Thought column)
- **Category cards** with live counts + average confidence
- **Sortable table** (click headers) with checkboxes
- **Bulk actions**: Delete Selected • Bulk Edit Selected • Send Selected for AI Review (live progress)
- **AI Review Threshold** vertical panel in Prompts Config
- **Models Config** tab — dynamic Ollama models with Primary/FB1/FB2/FB3 radios (auto-saved)
- **Prompts Config** tab — edit Categorization & Search prompts + threshold
- **Enhance with Ollama** button — runs AI review on every thought

### CLI Tool
```bash
2b+ "your thought here"
Adds instantly and shows AI reply. Works from anywhere in the project.
Architecture

Thoughts = plain .md files in notes/thoughts/ (Obsidian-ready)
Metadata in filename: category-slug-confidence-YYYYMMDD-HHMMSS.md
Config only in SQLite (models.db) for models + prompts + threshold
Hybrid file-first design

Quick Start
Bashcd ~/2ndbrain_pro
./run.sh --serve --port 8000
Then open http://localhost:8000
CLI usage:
Bash2b+ "my new brilliant idea about mechanical keyboards"
Commands

./run.sh --serve          → start web UI (default port 8000)
2b+ "thought text"        → add thought via terminal
./run.sh                  → start web UI (no flags)

Folders
textsecond_brain_builder/
├── notes/thoughts/           ← all your thoughts (Obsidian vault)
├── logs/                     ← debug logs
├── 2b+                       ← CLI tool
├── run.sh                    ← launcher
└── README.md
Everything is production-ready, fully commented, and ready for git commit.
Made with love for a perfect local second brain.
