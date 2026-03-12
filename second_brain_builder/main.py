# filename: second_brain_builder/main.py
# purpose: CLI entry point - runs folder setup then all modules in order (production ready)

import argparse
import sys
from pathlib import Path
from src.utils.folder_setup import setup_all_folders
from src.modules.video_processor import process_youtube_links
from src.modules.document_processor import process_report
from src.modules.obsidian_exporter import create_obsidian_structure
import logging

logging.basicConfig(filename='logs/main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    """Orchestrator: setup folders first, then process inputs, export vault."""
    parser = argparse.ArgumentParser(description="Modular Second Brain Builder - replaces bash script")
    parser.add_argument("--links", default="pasted-text.txt", help="YT links file")
    parser.add_argument("--report", default="Second Brain tools comparison 2026.txt", help="Report file")
    args = parser.parse_args()
    if not setup_all_folders():
        print("Folder setup failed - aborting.")
        sys.exit(1)
    logging.info("Starting modular processing")
    process_youtube_links()
    process_report()
    create_obsidian_structure()
    print("Second Brain vault ready in output/my_second_brain/")
    print("Open in Obsidian for full graph + search.")

if __name__ == "__main__":
    main()
