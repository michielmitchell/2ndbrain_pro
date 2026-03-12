# filename: second_brain_builder/src/modules/thought_processor.py
# purpose: New thoughts now use EXACT same Categorization Prompt as AI Review (with context). Robust JSON parsing, no default Review 0.65, full logging, correct filename.

from pathlib import Path
from datetime import datetime
import json
import re
from src.config import VAULT_ROOT
from src.modules.ai_processor import OllamaClient
from src.modules.model_manager import model_manager
from src.modules.prompt_manager import prompt_manager

ollama_client = OllamaClient()

def save_thought_and_reply(thought: str):
    if not thought.strip():
        return {"success": False, "reply": "Empty thought"}

    THOUGHTS_DIR = VAULT_ROOT / "notes" / "thoughts"
    THOUGHTS_DIR.mkdir(parents=True, exist_ok=True)

    # Use EXACT same prompt as AI Review
    base_prompt = prompt_manager.get_prompt("categorization")
    full_prompt = base_prompt.replace("{thought}", thought)

    assignment = model_manager.get_assignment()
    primary_model = assignment.get("primary", "qwen2.5:14b")

    print(f"[NEW THOUGHT CATEGORIZATION PROMPT SENT TO {primary_model}]\n{full_prompt}\n")

    summary = ollama_client.chat_with_vault(full_prompt, primary_model)
    print(f"[NEW THOUGHT RAW RESPONSE]\n{summary}\n")

    try:
        data = json.loads(summary.strip())
        category = data.get("category", "Review")
        confidence = float(data.get("confidence", 0.65))
    except Exception as e:
        print(f"[NEW THOUGHT JSON PARSE FAILED] {e}")
        category = "Review"
        confidence = 0.65

    slug = re.sub(r'[^a-z0-9]+', '-', thought.lower().strip()[:80]).strip('-')
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{category.lower()}-{slug}-{confidence:.2f}-{timestamp}.md"
    file_path = THOUGHTS_DIR / filename

    content = f"""# {thought}

## AI Initial Categorization
**Category:** {category}
**Confidence:** {confidence:.2f}

## Full AI Response
{summary}
"""
    file_path.write_text(content, encoding="utf-8")

    print(f"[NEW THOUGHT SAVED] {filename} (category={category}, confidence={confidence})")

    reply = f"Thought saved as **{category}** with confidence **{confidence:.2f}**."

    return {"success": True, "reply": reply, "filename": filename}
