# filename: second_brain_builder/src/utils/folder_setup.py
# purpose: Guarantees ALL subfolders exist before any processing (called first in main.py)

from pathlib import Path
import logging
from typing import List

logging.basicConfig(filename='logs/setup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_all_folders() -> bool:
    """Create every required subfolder with parents=True and exist_ok=True.
    Raises no exceptions on success; logs everything. Must run before use.
    """
    folders: List[Path] = [
        Path("data"),
        Path("logs"),
        Path("output/my_second_brain/notes/cloud_platforms"),
        Path("output/my_second_brain/notes/local_storage"),
        Path("output/my_second_brain/notes/databases"),
        Path("output/my_second_brain/notes/emerging"),
        Path("output/my_second_brain/youtube_notes"),
        Path("output/my_second_brain/raw_documents"),
        Path("output/my_second_brain/attachments"),
        Path("output/my_second_brain/.obsidian"),
    ]
    try:
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            logging.info(f"Ensured folder: {folder}")
        logging.info("All subfolders created successfully.")
        return True
    except Exception as e:
        logging.error(f"Folder creation failed: {e}")
        return False

if __name__ == "__main__":
    setup_all_folders()
