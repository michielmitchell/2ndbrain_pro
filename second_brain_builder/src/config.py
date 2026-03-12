# filename: second_brain_builder/src/config.py
# purpose: Central config with all paths and constants - ensures subfolder structure is defined

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
VAULT_ROOT = PROJECT_ROOT / "output" / "my_second_brain"
RAW_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

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
