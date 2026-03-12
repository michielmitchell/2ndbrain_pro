# filename: second_brain_builder/src/modules/thought_processor.py
# purpose: Every thought is now auto-categorized by AI (People/Projects/Ideas/Admin/Review) + filename prefixed with category + full logging

import logging
import re
import json
from pathlib import Path
from datetime import datetime
from src.modules.ai_processor import OllamaClient
from src.modules.model_manager import model_manager
from src.modules.prompt_manager import prompt_manager
from src.config import THOUGHTS_DIR

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
    text = text.strip()[:80]
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    text = re.sub(r'\s+', '-', text.strip())
    return text[:50] if text else "untitled"

def save_thought_and_reply(thought: str) -> dict:
    if not thought.strip():
        logger.warning("EMPTY thought received")
        return {"success": False, "reply": "Thought cannot be empty."}

    # === AI CATEGORIZATION ===
    cat_prompt = prompt_manager.get_prompt("categorization").replace("{thought}", thought)
    assignment = model_manager.get_assignment()
    model = assignment.get("primary") or ollama_client.default_model
    try:
        resp = ollama.generate(model=model, prompt=cat_prompt)
        cat_data = json.loads(resp["response"])
        category = cat_data.get("category", "Review")
        confidence = cat_data.get("confidence", 0.65)
        logger.info(f"CATEGORIZED | category={category} | confidence={confidence}")
    except Exception as e:
        category = "Review"
        confidence = 0.60
        logger.warning(f"Categorization failed, defaulted to Review: {e}")

    timestamp = datetime.now().strftime("%Y%m%d")
    readable_name = slugify(thought)
    file_path = THOUGHTS_DIR / f"{category.lower()}-{readable_name}-{timestamp}.md"

    exact_prompt = f"As a Second Brain assistant, provide an insightful reply to this thought: {thought}"

    logger.info(f"THOUGHT_RECEIVED | preview={thought[:100]}... | category={category}")
    logger.info(f"FILENAME | {file_path.name}")

    content = f"""# {readable_name.replace('-', ' ').title()} - {datetime.now().strftime("%Y-%m-%d")}

{thought}

## Category: {category} (confidence: {confidence:.2f})

## AI Reply (pending)
"""
    file_path.write_text(content, encoding="utf-8")

    reply = ollama_client.chat_with_vault(exact_prompt, model)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n## AI Reply (model: {model})\n{reply}\n")

    logger.info(f"THOUGHT_SAVE_COMPLETE | file={file_path.name} | category={category}")
    return {"success": True, "reply": reply, "filename": file_path.name, "category": category}
