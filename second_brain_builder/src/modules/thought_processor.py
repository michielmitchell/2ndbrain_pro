# filename: second_brain_builder/src/modules/thought_processor.py
# purpose: Processes new thoughts - saves to MD + generates Ollama reply using Primary model

import logging
from pathlib import Path
from datetime import datetime
from src.modules.ai_processor import OllamaClient
from src.modules.model_manager import model_manager
from src.config import THOUGHTS_DIR

logging.basicConfig(filename='logs/thought_processor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ollama_client = OllamaClient()

def save_thought_and_reply(thought: str) -> dict:
    if not thought.strip():
        return {"success": False, "reply": "Thought cannot be empty."}
    
    # Save as MD
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = THOUGHTS_DIR / f"thought_{timestamp}.md"
    content = f"""# New Thought - {timestamp}

{thought}

## AI Reply (pending)
"""
    file_path.write_text(content, encoding="utf-8")
    logging.info(f"Saved thought: {file_path}")

    # Get reply from Primary model
    assignment = model_manager.get_assignment()
    model = assignment.get("primary") or ollama_client.default_model
    prompt = f"As a Second Brain assistant, provide an insightful reply to this thought: {thought}"
    reply = ollama_client.chat_with_vault(prompt, model)  # Reuse chat func for reply

    # Append reply to MD
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n## AI Reply\n{reply}\n")

    return {"success": True, "reply": reply}

if __name__ == "__main__":
    # Test
    result = save_thought_and_reply("Test thought")
    print(result)
