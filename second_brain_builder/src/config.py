# filename: second_brain_builder/src/config.py
# purpose: Added PROMPTS_DB_PATH + default prompts and threshold for Prompts Config tab

from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent
VAULT_ROOT = PROJECT_ROOT / "output" / "my_second_brain"
RAW_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

DEFAULT_PORT = 8000

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://192.168.3.237:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

DB_PATH = PROJECT_ROOT / "data" / "model_config.db"
PROMPTS_DB_PATH = PROJECT_ROOT / "data" / "prompts_config.db"

THOUGHTS_DIR = VAULT_ROOT / "notes" / "thoughts"

YOUTUBE_NOTES_DIR = VAULT_ROOT / "youtube_notes"
RAW_DOCS_DIR = VAULT_ROOT / "raw_documents"
CLOUD_DIR = VAULT_ROOT / "notes" / "cloud_platforms"
LOCAL_DIR = VAULT_ROOT / "notes" / "local_storage"
DB_DIR = VAULT_ROOT / "notes" / "databases"
EMERGING_DIR = VAULT_ROOT / "notes" / "emerging"
ATTACHMENTS_DIR = VAULT_ROOT / "attachments"

INPUT_LINKS_FILE = "pasted-text.txt"
INPUT_REPORT_FILE = "Second Brain tools comparison 2026.txt"

DEFAULT_YT_LINKS = [
    "https://www.youtube.com/watch?v=0TpON5T-Sw4",
    "https://www.youtube.com/watch?v=_gPODg6br5w"
]

# Default prompts for Prompts Config tab
DEFAULT_CATEGORIZATION_PROMPT = """You are a strict JSON-only assistant for a personal 2nd Brain knowledge system. Return NOTHING but valid JSON. No explanations, no markdown, no extra text, no apologies.

Rules:
- Analyze the thought deeply and assign exactly ONE best category.
- If the thought is ambiguous or could fit multiple categories, choose the most specific one and explain your choice in the JSON (but still return only JSON).
- Confidence must be a float between 0.60 and 1.00. Be honest: use 0.60-0.75 for uncertain/edge cases, 0.80+ only when very clear.
- "Review" is ONLY for thoughts that truly need human review (vague, emotional, or incomplete). Do not overuse it.

Categories (use exactly these strings):
- "People" (names, contacts, relationships, personal notes about individuals)
- "Projects" (tasks, plans, ongoing work, goals with deadlines)
- "Ideas" (brainstorming, creative thoughts, random insights)
- "Admin" (reminders, finances, logistics, household/system maintenance)
- "Review" (needs human attention, unclear, or sensitive)

Output format (exactly):
{
  "category": "one of the five categories above",
  "confidence": 0.xx
}

Thought to categorize: {thought}"""

DEFAULT_SEARCH_PROMPT = """You are my personal 2nd Brain assistant — helpful, concise, and truthful.

Use ONLY the notes provided below to answer the question. Never make up information or use external knowledge.

If the notes contain relevant information, answer naturally and conversationally. When possible, briefly reference the source thought(s) by filename or key content.

If the notes do not contain enough information to answer the question well, respond with: "I don't have enough information in my notes to answer that."

Notes:
{context}

Question: {query}

Answer:"""

DEFAULT_CONFIDENCE_THRESHOLD = 0.65
