# filename: second_brain_builder/src/modules/video_processor.py
# purpose: Standalone module to fetch titles + full transcripts from YT links and save .md notes

import logging
from pathlib import Path
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from config import YOUTUBE_NOTES_DIR, INPUT_LINKS_FILE, DEFAULT_YT_LINKS

logging.basicConfig(filename='logs/video_processor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_video_id(url: str) -> str:
    """Robust video ID extractor with validation."""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    raise ValueError(f"Invalid YouTube URL: {url}")

def get_video_title(url: str) -> str:
    """Fetch title via yt-dlp (no download)."""
    ydl_opts = {"quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("title", "Untitled Video").replace("/", "-")

def fetch_transcript(video_id: str) -> str:
    """Fetch transcript with full fallback handling."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        return "\n".join([item["text"] for item in transcript_list])
    except (TranscriptsDisabled, NoTranscriptFound):
        return "No transcript available (disabled or missing)."
    except Exception as e:
        logging.warning(f"Transcript fallback for {video_id}: {e}")
        return f"Transcript error: {str(e)}"

def process_youtube_links() -> None:
    """Main entry: read links file or use defaults, create one MD per video."""
    links_path = Path(INPUT_LINKS_FILE)
    if links_path.exists():
        with open(links_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        logging.warning("Using default YT links.")
        urls = DEFAULT_YT_LINKS
    for idx, url in enumerate(urls):
        try:
            title = get_video_title(url)
            video_id = extract_video_id(url)
            transcript = fetch_transcript(video_id)
            md_content = f"""# {title}

URL: {url}

## Transcript
{transcript}

## Note
Imported into Second Brain vault for knowledge graph linking.
"""
            note_file = YOUTUBE_NOTES_DIR / f"video_{idx+1}_{video_id[:8]}.md"
            note_file.write_text(md_content, encoding="utf-8")
            logging.info(f"Saved: {note_file}")
        except Exception as e:
            logging.error(f"Failed video {url}: {e}")

if __name__ == "__main__":
    process_youtube_links()
