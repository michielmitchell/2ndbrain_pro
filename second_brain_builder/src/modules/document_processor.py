# filename: second_brain_builder/src/modules/document_processor.py
# purpose: Parses comparison report into category-specific MD files + raw copy

import logging
import re
from pathlib import Path
from config import RAW_DOCS_DIR, CLOUD_DIR, LOCAL_DIR, DB_DIR, EMERGING_DIR, INPUT_REPORT_FILE

logging.basicConfig(filename='logs/document_processor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_report() -> None:
    """Read full report, copy raw, split into 4 category files using regex on known headers."""
    report_path = Path(INPUT_REPORT_FILE)
    if not report_path.exists():
        logging.error(f"Missing report: {INPUT_REPORT_FILE}")
        return
    content = report_path.read_text(encoding="utf-8")
    # Raw backup
    (RAW_DOCS_DIR / "full_comparison_2026.md").write_text(content, encoding="utf-8")
    # Extract sections
    categories = {
        "cloud": re.search(r"#### Category 1: Top 10 Leading Cloud Platforms(.*?)(?=#### Category 2:|$)", content, re.DOTALL),
        "local": re.search(r"#### Category 2: Top 10 Local Storage Platforms(.*?)(?=#### Category 3:|$)", content, re.DOTALL),
        "db": re.search(r"#### Category 3: Top 10 Database Options with AI Support(.*?)(?=#### Category 4:|$)", content, re.DOTALL),
        "emerging": re.search(r"#### Category 4: Top 10 New or Up-and-Coming AI Solutions(.*?)(?=$)", content, re.DOTALL),
    }
    for cat_key, match in categories.items():
        text = match.group(1).strip() if match else "Section not parsed."
        target_dir = {
            "cloud": CLOUD_DIR,
            "local": LOCAL_DIR,
            "db": DB_DIR,
            "emerging": EMERGING_DIR,
        }[cat_key]
        note_path = target_dir / f"{cat_key}_tools.md"
        note_path.write_text(f"""# {cat_key.capitalize()} Tools 2026

{text}

**Imported from original comparison report.**
""", encoding="utf-8")
        logging.info(f"Created category note: {note_path}")

if __name__ == "__main__":
    process_report()
