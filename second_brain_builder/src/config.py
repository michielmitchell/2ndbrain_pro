# filename: second_brain_builder/src/config.py
# purpose: Central config with all paths and constants - added DB_PATH for SQLite + OLLAMA_HOST env support for custom instances like 192.168.3.237

from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent
VAULT_ROOT = PROJECT_ROOT / "output" / "my_second_brain"
RAW_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

DEFAULT_PORT = 8000

# Ollama connection (supports custom IP like screenshot)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# SQLite persistence for model assignment
DB_PATH = PROJECT_ROOT / "data" / "model_config.db"

# All required subfolders (created via folder_setup)
YOUTUBE_NOTES_DIR = VAULT_ROOT / "youtube_notes"
RAW_DOCS_DIR = VAULT_ROOT / "raw_documents"
CLOUD_DIR = VAULT_ROOT / "notes" / "cloud_platforms"
LOCAL_DIR = VAULT_ROOT / "notes" / "local_storage"
DB_DIR = VAULT_ROOT / "notes" / "databases"
EMERGING_DIR = VAULT_ROOT / "notes" / "emerging"
ATTACHMENTS_DIR = VAULT_ROOT / "attachments"

INPUT_LINKS_FILE = "pasted-text.txt"
INPUT_REPORT_FILE = "Second Brain tools comparison 2026.txt"

# YT URLs hardcoded as fallback if file missing
DEFAULT_YT_LINKS = [
    "https://www.youtube.com/watch?v=0TpON5T-Sw4",
    "https://www.youtube.com/watch?v=_gPODg6br5w"
]
