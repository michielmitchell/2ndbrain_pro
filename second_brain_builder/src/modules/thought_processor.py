# filename: second_brain_builder/src/modules/thought_processor.py
# purpose: Thoughts now saved with human-readable filenames based on content (slugified first 60 chars + date) + full logging

import logging
import re
from pathlib import Path
from datetime import datetime
from src.modules.ai_processor import OllamaClient
from src.modules.model_manager import model_manager
from src.config import THOUGHTS_DIR

# === DUAL LOGGING: Console (visible) + File (historical) ===
logger = logging.getLogger("thought_processor")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("🧠 SAVE_LOG | %(asctime)s | %(message)s"))
logger.addHandler(console_handler)

file_handler = logging.FileHandler("logs/thoughts_history.log", mode="a")
file_handler.setFormatter(logging.Formatter("%(asctime)s - THOUGHT_LOG - %(message)s"))
logger.addHandler(file_handler)

ollama_client = OllamaClient()

def slugify(text: str) -> str:
    """Create clean human-readable kebab-case name from thought content"""
    text = text.strip()[:80]  # first ~60-80 chars
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    text = re.sub(r'\s+', '-', text.strip())
    return text[:50] if text else "untitled-thought"

def save_thought_and_reply(thought: str) -> dict:
    if not thought.strip():
        logger.warning("EMPTY thought received - ignored")
        return {"success": False, "reply": "Thought cannot be empty."}

    timestamp = datetime.now().strftime("%Y%m%d")
    readable_name = slugify(thought)
    file_path = THOUGHTS_DIR / f"{readable_name}-{timestamp}.md"

    assignment = model_manager.get_assignment()
    model = assignment.get("primary") or ollama_client.default_model
    exact_prompt = f"As a Second Brain assistant, provide an insightful reply to this thought: {thought}"

    logger.info(f"THOUGHT_RECEIVED | content_preview={thought[:100]}...")
    logger.info(f"GENERATED_FILENAME | {file_path.name}")
    logger.info(f"MODEL_USED | {model}")
    logger.info(f"PROMPT_SENT_TO_OLLAMA | {exact_prompt}")
    logger.info(f"SAVING_FILE | {file_path}")

    content = f"""# {readable_name.replace('-', ' ').title()} - {datetime.now().strftime("%Y-%m-%d")}

{thought}

## AI Reply (pending)
"""
    file_path.write_text(content, encoding="utf-8")
    logger.info(f"FILE_CREATED | path={file_path}")

    reply = ollama_client.chat_with_vault(exact_prompt, model)

    logger.info(f"AI_REPLY_RECEIVED | length={len(reply)} | preview={reply[:150]}...")
    logger.info(f"THOUGHT_SAVE_COMPLETE | file={file_path.name} | model={model}")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n## AI Reply (model: {model})\n{reply}\n")

    return {"success": True, "reply": reply, "filename": file_path.name, "prompt_used": exact_prompt, "model": model}

if __name__ == "__main__":
    result = save_thought_and_reply("This is a test thought about integrating AI with my second brain vault")
    print(result)
