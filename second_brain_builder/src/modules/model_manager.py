# filename: second_brain_builder/src/modules/model_manager.py
# purpose: Handles dynamic Ollama model loading + Primary/FB1/FB2/FB3 assignment with SQLite persistence + auto-sort

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict
import ollama
from src.config import DB_PATH, OLLAMA_HOST

logging.basicConfig(filename='logs/model_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS model_assignment (
                role TEXT PRIMARY KEY,
                model_name TEXT
            )
        ''')
        roles = ['primary', 'fallback1', 'fallback2', 'fallback3']
        for role in roles:
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
        """Live dynamic load from Ollama instance"""
        try:
            ollama.base_url = OLLAMA_HOST
            resp = ollama.list()
            models = [{"name": m["name"], "size_gb": round(m.get("size", 0) / (1024**3), 2)} for m in resp.get("models", [])]
            return sorted(models, key=lambda x: x["name"])
        except Exception as e:
            logging.error(f"Ollama unreachable at {OLLAMA_HOST}: {e}")
            return []

model_manager = ModelManager()
