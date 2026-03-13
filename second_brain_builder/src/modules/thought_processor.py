# filename: second_brain_builder/src/modules/thought_processor.py
# purpose: Auto-embed every new thought into ChromaDB (parallel layer only)

import json
import re
from datetime import datetime
from pathlib import Path
import logging
from src.config import VAULT_ROOT, DEFAULT_OLLAMA_MODEL
from src.modules.ai_processor import OllamaClient
from src.modules.prompt_manager import prompt_manager
from src.modules.model_manager import model_manager
from src.modules.vector_store import vector_store

logger = logging.getLogger(__name__)
ollama_client = OllamaClient()

def save_thought_and_reply(thought: str):
    try:
        if not thought.strip():
            return {"success": False, "reply": "Empty thought ignored."}
        base_prompt = prompt_manager.get_prompt("categorization")
        threshold = prompt_manager.get_threshold()
        full_prompt = base_prompt.replace("{thought}", thought) + f"\n\nReview Threshold: {threshold:.2f}\nReturn ONLY valid JSON."
        assignment = model_manager.get_assignment()
        primary_model = assignment.get("primary", DEFAULT_OLLAMA_MODEL)
        logger.info(f"[CATEGORIZATION PROMPT SENT TO {primary_model}]")
        raw = ollama_client.chat_with_vault(full_prompt, primary_model)
        logger.info(f"[CATEGORIZATION RAW] {raw}")
        json_match = re.search(r'(\{.*?\})', raw, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(1))
            category = data.get("category", "Review")
            confidence = float(data.get("confidence", 0.75))
        else:
            category = "Review"
            confidence = 0.75
        slug = re.sub(r'[^a-z0-9]+', '-', thought.lower().strip()[:60]).strip('-')
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{category.lower()}-{slug}-{confidence:.2f}-{timestamp}.md"
        thoughts_dir = VAULT_ROOT / "notes" / "thoughts"
        thoughts_dir.mkdir(parents=True, exist_ok=True)
        file_path = thoughts_dir / filename
        content = f"# {thought}\n\n## Metadata\nCategory: {category}\nConfidence: {confidence}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        file_path.write_text(content, encoding="utf-8")
        rel_path = f"notes/thoughts/{filename}"
        vector_store.embed_thought(thought, rel_path, category, confidence, timestamp)
        logger.info(f"[SAVE SUCCESS] {filename} + vector embedded")
        reply = ollama_client.chat_with_vault(f"Give a short, helpful reply to this thought: {thought}", primary_model)
        return {"success": True, "reply": reply, "filename": filename}
    except Exception as e:
        logger.error(f"[SAVE ERROR] {e}")
        return {"success": False, "reply": f"Error: {str(e)}"}
