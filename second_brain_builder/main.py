# filename: second_brain_builder/main.py
# purpose: CLI entry point - original build OR web server mode with customizable port (production ready)

import argparse
import sys
import logging
from src.utils.folder_setup import setup_all_folders
from src.modules.video_processor import process_youtube_links
from src.modules.document_processor import process_report
from src.modules.obsidian_exporter import create_obsidian_structure

logging.basicConfig(filename='logs/main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    parser = argparse.ArgumentParser(description="Modular Second Brain Builder - CLI or hosted web server")
    parser.add_argument("--serve", action="store_true", help="Start FastAPI web server")
    parser.add_argument("--port", type=int, default=8000, help="Custom port for server (default 8000)")
    parser.add_argument("--links", default="pasted-text.txt", help="YT links file")
    parser.add_argument("--report", default="Second Brain tools comparison 2026.txt", help="Report file")
    args = parser.parse_args()
    if not setup_all_folders():
        print("Folder setup failed - aborting.")
        sys.exit(1)
    if args.serve:
        logging.info(f"Starting web server on http://0.0.0.0:{args.port}")
        import uvicorn
        uvicorn.run("src.web.app:app", host="0.0.0.0", port=args.port, reload=False)
    else:
        logging.info("Starting CLI modular processing")
        process_youtube_links()
        process_report()
        create_obsidian_structure()
        print("Second Brain vault ready in output/my_second_brain/")
        print("Open in Obsidian or visit http://localhost:8000/vault after running with --serve")

if __name__ == "__main__":
    main()
