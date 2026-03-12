# filename: second_brain_builder/src/modules/model_manager.py
# purpose: SUPER ROBUST model name extraction - handles EVERY Ollama Python client version (dict, object, pydantic) + your exact models (qwen3.5:27b etc.)

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict
import ollama
from src.config import DB_PATH, OLLAMA_HOST

logging.basicConfig(filename='logs/model_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelManager:
    def __init__(self):
        ollama.base_url = OLLAMA_HOST
        self.db_path = DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        logging.info(f"Ollama connected to {OLLAMA_HOST}")

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS model_assignment (
                role TEXT PRIMARY KEY,
                model_name TEXT
            )
        ''')
        for role in ['primary', 'fallback1', 'fallback2', 'fallback3']:
            cur.execute("INSERT OR IGNORE INTO model_assignment (role, model_name) VALUES (?, '')", (role,))
        conn.commit()
        conn.close()

    def get_assignment(self) -> Dict[str, str]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT role, model_name FROM model_assignment")
        rows = cur.fetchall()
        conn.close()
        return {r[0]: r[1] for r in rows}

    def save_assignment(self, assignment: Dict[str, str]):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        for role, model in assignment.items():
            cur.execute("UPDATE model_assignment SET model_name = ? WHERE role = ?", (model, role))
        conn.commit()
        conn.close()

    def get_models(self) -> List[Dict]:
        """Extracts REAL names from ANY Ollama response format"""
        try:
            resp = ollama.list()
            # Handle both dict response and object response (current library)
            raw_list = resp.get("models", []) if isinstance(resp, dict) else getattr(resp, "models", [])
            models = []
            for m in raw_list:
                # Try every possible way to get name
                name = None
                if isinstance(m, dict):
                    name = m.get("name") or m.get("model")
                else:
                    name = getattr(m, "name", None) or getattr(m, "model", None)
                if not name:
                    name = "unknown"
                # Size
                size_bytes = 0
                if isinstance(m, dict):
                    size_bytes = m.get("size", 0)
                else:
                    size_bytes = getattr(m, "size", 0)
                size_gb = round(size_bytes / (1024**3), 2) if size_bytes else 0
                models.append({"name": str(name), "size_gb": size_gb})
            models = sorted(models, key=lambda x: x["name"])
            logging.info(f"✅ Loaded {len(models)} REAL models: {[m['name'] for m in models[:5]]}...")
            return models
        except Exception as e:
            logging.error(f"Ollama error at {OLLAMA_HOST}: {e}")
            return []

model_manager = ModelManager()
