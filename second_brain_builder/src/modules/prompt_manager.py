# filename: second_brain_builder/src/modules/prompt_manager.py
# purpose: SQLite persistence for Categorization Prompt, Search Prompt and Confidence Threshold + defaults

import sqlite3
import logging
from pathlib import Path
from src.config import PROMPTS_DB_PATH, DEFAULT_CATEGORIZATION_PROMPT, DEFAULT_SEARCH_PROMPT, DEFAULT_CONFIDENCE_THRESHOLD

logging.basicConfig(filename='logs/prompt_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PromptManager:
    def __init__(self):
        self.db_path = PROMPTS_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        defaults = {
            "categorization": DEFAULT_CATEGORIZATION_PROMPT,
            "search": DEFAULT_SEARCH_PROMPT,
            "threshold": str(DEFAULT_CONFIDENCE_THRESHOLD)
        }
        for k, v in defaults.items():
            cur.execute("INSERT OR IGNORE INTO prompts (key, value) VALUES (?, ?)", (k, v))
        conn.commit()
        conn.close()

    def get_prompt(self, key: str) -> str:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT value FROM prompts WHERE key=?", (key,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else ""

    def save_prompt(self, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("UPDATE prompts SET value=? WHERE key=?", (value, key))
        conn.commit()
        conn.close()

    def get_threshold(self) -> float:
        return float(self.get_prompt("threshold"))

    def save_threshold(self, value: float):
        self.save_prompt("threshold", str(value))

prompt_manager = PromptManager()
