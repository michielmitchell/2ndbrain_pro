# filename: second_brain_builder/src/modules/thought_processor.py
# purpose: Save to 2nd Brain now produces RICH visible console logs + historical file (exact thought, FULL prompt sent to Ollama, model, reply, file path)

import logging
from pathlib import Path
from datetime import datetime
from src.modules.ai_processor import OllamaClient
from src.modules.model_manager import model_manager
from src.config import THOUGHTS_DIR

# === DUAL LOGGING: Console (visible in terminal) + File (historical) ===
logger = logging.getLogger("thought_processor")
logger.setLevel(logging.INFO)

# Console handler (so user sees everything live)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "🧠 SAVE_LOG | %(asctime)s | %(message)s"
))
logger.addHandler(console_handler)

# File handler for permanent history
file_handler = logging.FileHandler("logs/thoughts_history.log", mode="a")
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - THOUGHT_LOG - %(message)s"
))
logger.addHandler(file_handler)

ollama_client = OllamaClient()

def save_thought_and_reply(thought: str) -> dict:
    if not thought.strip():
        logger.warning("EMPTY thought received - ignored")
        return {"success": False, "reply": "Thought cannot be empty."}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = THOUGHTS_DIR / f"thought_{timestamp}.md"

    # === MODEL & EXACT PROMPT ===
    assignment = model_manager.get_assignment()
    model = assignment.get("primary") or ollama_client.default_model
    exact_prompt = f"As a Second Brain assistant, provide an insightful reply to this thought: {thought}"

    # === RICH CONSOLE + FILE LOGS ===
    logger.info(f"THOUGHT_RECEIVED | timestamp={timestamp} | thought_preview={thought[:150]}...")
    logger.info(f"MODEL_USED | {model}")
    logger.info(f"PROMPT_SENT_TO_OLLAMA | {exact_prompt}")
    logger.info(f"SAVING_FILE | {file_path}")

    # Write initial markdown
    content = f"""# New Thought - {timestamp}

{thought}

## AI Reply (pending)
"""
    file_path.write_text(content, encoding="utf-8")
    logger.info(f"FILE_CREATED | path={file_path}")

    # Call Ollama
    reply = ollama_client.chat_with_vault(exact_prompt, model)

    # Log reply
    logger.info(f"AI_REPLY_RECEIVED | length={len(reply)} | preview={reply[:200]}...")
    logger.info(f"THOUGHT_SAVE_COMPLETE | file={file_path} | model={model}")

    # Append reply to file
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n## AI Reply (model: {model})\n{reply}\n")

    return {"success": True, "reply": reply, "prompt_used": exact_prompt, "model": model}

if __name__ == "__main__":
    result = save_thought_and_reply("Test thought for logging verification")
    print(result)
