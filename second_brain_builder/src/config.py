# filename: second_brain_builder/src/config.py
# purpose: Central config — now loads default prompts from git-tracked .txt files (no more inline strings)

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Core paths
VAULT_ROOT = PROJECT_ROOT / "vault"
DB_PATH = PROJECT_ROOT / "models.db"
PROMPTS_DB_PATH = PROJECT_ROOT / "prompts.db"

# Ollama
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "qwen2.5:14b"

# Prompt files (git-tracked)
CATEGORIZATION_PROMPT_PATH = PROJECT_ROOT / "src" / "prompts" / "categorization_prompt.txt"
SEARCH_PROMPT_PATH = PROJECT_ROOT / "src" / "prompts" / "search_prompt.txt"

# Load defaults from files
DEFAULT_CATEGORIZATION_PROMPT = CATEGORIZATION_PROMPT_PATH.read_text(encoding="utf-8").strip()
DEFAULT_SEARCH_PROMPT = SEARCH_PROMPT_PATH.read_text(encoding="utf-8").strip()

DEFAULT_CONFIDENCE_THRESHOLD = 0.65
