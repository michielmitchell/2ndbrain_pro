# filename: second_brain_builder/src/config.py
# purpose: Added THOUGHTS_DIR for new Thoughts tab layout

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

# New for Thoughts tab
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
