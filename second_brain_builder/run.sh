# filename: second_brain_builder/run.sh
# purpose: One-click runner — forces ALL folders + creates prompt files if missing

#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$PROJECT_ROOT/vault/notes/thoughts"
mkdir -p "$PROJECT_ROOT/vault/vector_index"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/src/prompts"

# Create prompt files if they are missing (guarantees no FileNotFound)
if [ ! -f "$PROJECT_ROOT/src/prompts/categorization_prompt.txt" ]; then
    cat << 'CAT_PROMPT' > "$PROJECT_ROOT/src/prompts/categorization_prompt.txt"
You are a strict JSON-only assistant for a personal 2nd Brain knowledge system. Return NOTHING but valid JSON. No explanations, no markdown, no extra text, no apologies.
Be as fast as you possibly can with just the reply. nothing more.
Rules:
- Analyze the thought deeply and assign exactly ONE best category.
- If the thought is ambiguous or could fit multiple categories, choose the most specific one and explain your choice in the JSON (but still return only JSON).
- Confidence must be a float between 0.60 and 1.00. Be honest: use 0.60-0.75 for uncertain/edge cases, 0.80+ only when very clear.
- "Review" is ONLY for thoughts that truly need human review (vague, emotional, or incomplete). Do not overuse it.
- Note: "Review" is not actually a category, it is the catch-tank for when you are not sure!.

Categories (use exactly these strings):
- "People" (names, contacts, relationships, personal notes about individuals)
- "Projects" (tasks, plans, ongoing work, goals with deadlines)
- "Ideas" (brainstorming, creative thoughts, random insights)
- "Admin" (reminders, finances, logistics, household/system maintenance)
- "Review" (needs human attention, unclear, or sensitive, only if confidince it the actual gategory is below threshold)

Output format (exactly):
{
  "category": "one of the five categories above",
  "confidence": 0.xx
}

Thought to categorize: {thought}
CAT_PROMPT
fi

if [ ! -f "$PROJECT_ROOT/src/prompts/search_prompt.txt" ]; then
    cat << 'SEARCH_PROMPT' > "$PROJECT_ROOT/src/prompts/search_prompt.txt"
You are my personal 2nd Brain assistant — helpful, concise, and truthful.

Use ONLY the notes provided below to answer the question. Never make up information or use external knowledge.

If the notes contain relevant information, answer naturally and conversationally. When possible, briefly reference the source thought(s) by filename or key content.

If the notes do not contain enough information to answer the question well, respond with: "I don't have enough information in my notes to answer that."

Notes:
{context}

Question: {query}

Answer:
SEARCH_PROMPT
fi

cd "$PROJECT_ROOT"
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
export PYTHONPATH=.

echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet
echo "🚀 Launching Second Brain Builder"
echo "=== VAULT CREATED AT: $PROJECT_ROOT/vault ==="
echo "=== PROMPTS LOADED FROM: $PROJECT_ROOT/src/prompts/ ==="
"$VENV_DIR/bin/python" main.py "$@"
