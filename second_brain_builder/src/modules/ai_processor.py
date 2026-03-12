# filename: second_brain_builder/src/modules/ai_processor.py
# purpose: Ollama client - connects to configured models, lists available models, generates summaries and chat responses with vault context

import logging
import ollama
from pathlib import Path
from typing import List, Dict
from src.config import VAULT_ROOT, OLLAMA_HOST, DEFAULT_OLLAMA_MODEL

logging.basicConfig(filename='logs/ai_processor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OllamaClient:
    def __init__(self):
        ollama.base_url = OLLAMA_HOST  # connects to your running Ollama instance
        self.default_model = DEFAULT_OLLAMA_MODEL

    def list_models(self) -> List[Dict]:
        """Return all models configured in your local Ollama (pull with `ollama pull llama3.2`)."""
        try:
            response = ollama.list()
            return [{"name": m["name"], "size": m["size"]} for m in response.get("models", [])]
        except Exception as e:
            logging.error(f"Ollama not reachable: {e}")
            return []

    def enhance_note(self, note_path: Path) -> str:
        """Generate AI summary for a note using configured model."""
        try:
            content = note_path.read_text(encoding="utf-8")
            prompt = f"Summarize this Second Brain note in 3 bullet points:\n\n{content[:8000]}"
            response = ollama.generate(model=self.default_model, prompt=prompt)
            return response["response"]
        except Exception as e:
            logging.warning(f"Enhance failed: {e}")
            return "AI summary unavailable (Ollama not running)."

    def chat_with_vault(self, user_message: str, model: str = None) -> str:
        """RAG-lite chat: sends vault context + user question to configured Ollama model."""
        model = model or self.default_model
        # Build lightweight context from all notes
        context = "Second Brain Vault contents:\n"
        for root, _, files in Path(VAULT_ROOT).walk():
            for f in files:
                if f.endswith(".md"):
                    try:
                        text = (Path(root) / f).read_text(encoding="utf-8")[:500]
                        context += f"- {f}: {text}\n"
                    except:
                        pass
        if len(context) > 12000:
            context = context[:12000] + "... (truncated)"

        prompt = f"""You are an expert Second Brain assistant. Use the vault knowledge below to answer accurately.

Vault context:
{context}

User question: {user_message}

Answer conversationally and cite note names when possible:"""
        try:
            response = ollama.generate(model=model, prompt=prompt)
            return response["response"]
        except Exception as e:
            logging.error(f"Chat failed: {e}")
            return f"Ollama error: {str(e)}. Is Ollama running on {OLLAMA_HOST}?"

if __name__ == "__main__":
    client = OllamaClient()
    print("Available models:", [m["name"] for m in client.list_models()])
