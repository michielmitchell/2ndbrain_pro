# filename: second_brain_builder/main.py
# purpose: CLI entry point - supports --serve --port (web now launches full proper GUI dashboard)

import argparse
import sys
import logging
from src.utils.folder_setup import setup_all_folders
from src.modules.video_processor import process_youtube_links
from src.modules.document_processor import process_report
from src.modules.obsidian_exporter import create_obsidian_structure

logging.basicConfig(filename='logs/main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    parser = argparse.ArgumentParser(description="Modular Second Brain Builder - CLI or proper GUI web server")
    parser.add_argument("--serve", action="store_true", help="Start web server with proper Tailwind GUI")
    parser.add_argument("--port", type=int, default=8000, help="Custom port")
    args = parser.parse_args()
    if not setup_all_folders():
        print("Folder setup failed")
        sys.exit(1)
    if args.serve:
        logging.info(f"Starting GUI server on http://0.0.0.0:{args.port}")
        import uvicorn
        from src.web.app import app
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        process_youtube_links()
        process_report()
        create_obsidian_structure()
        print("Vault ready - run with --serve for proper GUI dashboard")

if __name__ == "__main__":
    main()
