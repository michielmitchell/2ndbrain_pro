# filename: second_brain_builder/src/web/helpers.py
# purpose: Shared utilities - full vault stats with correct per-category + overall averages

import re
from datetime import datetime
from pathlib import Path
from src.config import VAULT_ROOT

def get_vault_stats():
    stats = {
        "total_notes": 0,
        "People": 0, "Projects": 0, "Ideas": 0, "Admin": 0, "Review": 0,
        "avg_People": 0.0, "avg_Projects": 0.0, "avg_Ideas": 0.0, "avg_Admin": 0.0, "avg_Review": 0.0,
        "avg_all": 0.0
    }
    sum_conf = {"People": 0.0, "Projects": 0.0, "Ideas": 0.0, "Admin": 0.0, "Review": 0.0}
    total_conf = 0.0
    thoughts_dir = VAULT_ROOT / "notes" / "thoughts"
    if thoughts_dir.exists():
        for f in thoughts_dir.glob("*.md"):
            stats["total_notes"] += 1
            name_lower = f.name.lower()
            conf_match = re.search(r'-([0-9.]+)-(?:\d{8}(?:-\d{6})?)\.md$', f.name)
            conf = float(conf_match.group(1)) if conf_match else 0.0
            total_conf += conf
            cat = None
            if name_lower.startswith("people-"):
                cat = "People"
            elif name_lower.startswith("projects-"):
                cat = "Projects"
            elif name_lower.startswith("ideas-"):
                cat = "Ideas"
            elif name_lower.startswith("admin-"):
                cat = "Admin"
            elif name_lower.startswith("review-"):
                cat = "Review"
            if cat:
                stats[cat] += 1
                sum_conf[cat] += conf
    for cat in ["People", "Projects", "Ideas", "Admin", "Review"]:
        count = stats[cat]
        stats[f"avg_{cat}"] = round(sum_conf[cat] / count, 2) if count > 0 else 0.0
    stats["avg_all"] = round(total_conf / stats["total_notes"], 2) if stats["total_notes"] > 0 else 0.0
    return stats

def extract_slug_and_timestamp(filename: str):
    stem = Path(filename).stem
    date_match = re.search(r'(\d{8}(?:-\d{6})?)$', stem)
    timestamp = date_match.group(1) if date_match else datetime.now().strftime("%Y%m%d-%H%M%S")
    if date_match:
        base = stem[:date_match.start()].strip('-')
    else:
        base = stem
    slug = re.sub(r'^[a-z]+-', '', base)
    slug = re.sub(r'-[0-9.]+$', '', slug)
    slug = re.sub(r'--+', '-', slug).strip('-')
    if not slug:
        slug = "thought"
    return slug, timestamp
