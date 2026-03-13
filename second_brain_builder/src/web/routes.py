# filename: second_brain_builder/src/web/routes.py
# purpose: All API endpoints (unchanged, uses helpers for stats)

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from src.config import VAULT_ROOT, OLLAMA_HOST
from src.modules.vector_store import vector_store
from src.modules.thought_processor import save_thought_and_reply
from src.modules.prompt_manager import prompt_manager
from src.modules.model_manager import model_manager
from src.modules.ai_processor import OllamaClient
from .helpers import get_vault_stats, extract_slug_and_timestamp
import re
import json
from datetime import datetime
from pathlib import Path
import os

router = APIRouter()
ollama_client = OllamaClient()

@router.get("/api/stats")
async def api_stats():
    return get_vault_stats()

@router.get("/api/models")
async def api_models():
    return JSONResponse(model_manager.get_models())

@router.get("/api/model_config")
async def api_model_config():
    return JSONResponse(model_manager.get_assignment())

@router.post("/api/model_config")
async def save_model_config(data: dict = Body(...)):
    model_manager.save_assignment(data)
    return {"status": "saved"}

@router.get("/api/ollama_status")
async def api_ollama_status():
    try:
        models = model_manager.get_models()
        return {"host": OLLAMA_HOST, "connected": len(models) > 0, "models_count": len(models)}
    except:
        return {"host": OLLAMA_HOST, "connected": False, "models_count": 0}

@router.get("/api/notes")
async def api_notes():
    notes = []
    for root, _, files in os.walk(VAULT_ROOT):
        for fname in files:
            if fname.endswith(".md"):
                full_path = Path(root) / fname
                rel_path = full_path.relative_to(VAULT_ROOT)
                try:
                    with open(full_path, encoding="utf-8") as fp:
                        first_line = fp.readline().strip()
                    thought = first_line.lstrip("# ").strip() if first_line.startswith("#") else fname
                except:
                    thought = fname
                cat_match = re.match(r'^([a-z]+)-', fname)
                cat = cat_match.group(1).capitalize() if cat_match else "Review"
                conf_match = re.search(r'-([0-9.]+)-(?:\d{8}(?:-\d{6})?)\.md$', fname)
                conf = conf_match.group(1) if conf_match else "0.00"
                dt_match = re.search(r'(\d{8}(?:-\d{6})?)\.md$', fname)
                dt_str = dt_match.group(1) if dt_match else ""
                if dt_str:
                    try:
                        if '-' in dt_str:
                            dt = datetime.strptime(dt_str, "%Y%m%d-%H%M%S")
                            formatted_dt = dt.strftime("%Y-%m-%d %H:%M")
                        else:
                            dt = datetime.strptime(dt_str, "%Y%m%d")
                            formatted_dt = dt.strftime("%Y-%m-%d")
                    except:
                        formatted_dt = dt_str
                else:
                    formatted_dt = ""
                notes.append({
                    "path": str(rel_path),
                    "thought": thought[:120] + ("..." if len(thought) > 120 else ""),
                    "category": cat,
                    "confidence": conf,
                    "datetime": formatted_dt
                })
    return JSONResponse(notes)

@router.get("/api/semantic_search")
async def api_semantic_search(query: str = "", category: str = "all", top_k: int = 30):
    hits = vector_store.semantic_search(query, top_k, category if category != "all" else None)
    return JSONResponse(hits)

@router.get("/api/prompts")
async def api_prompts():
    return {
        "categorization": prompt_manager.get_prompt("categorization"),
        "search": prompt_manager.get_prompt("search"),
        "threshold": prompt_manager.get_threshold()
    }

@router.post("/api/save_prompt")
async def api_save_prompt(request: dict = Body(...)):
    key = request.get("key")
    value = request.get("value")
    if key in ["categorization", "search"]:
        prompt_manager.save_prompt(key, value)
    return {"status": "saved"}

@router.post("/api/save_threshold")
async def api_save_threshold(request: dict = Body(...)):
    value = float(request.get("value", 0.60))
    prompt_manager.save_threshold(value)
    return {"status": "saved"}

@router.post("/api/enhance")
async def enhance_all():
    thoughts_dir = VAULT_ROOT / "notes" / "thoughts"
    enhanced = 0
    if thoughts_dir.exists():
        for p in thoughts_dir.glob("*.md"):
            try:
                await enhance_note({"path": str(p.relative_to(VAULT_ROOT))})
                enhanced += 1
            except:
                pass
    return {"status": "success", "enhanced": enhanced}

@router.post("/api/enhance_note")
async def enhance_note(request: dict = Body(...)):
    path = request.get("path")
    p = VAULT_ROOT / path
    if not (p.exists() and p.is_file()):
        return {"status": "failed"}
    content = p.read_text(encoding="utf-8")
    base_prompt = prompt_manager.get_prompt("categorization")
    threshold = prompt_manager.get_threshold()
    review_prompt = base_prompt.replace("{thought}", content) + f"""

Review Threshold: {threshold:.2f}
If your confidence would be below this threshold, you MUST use category "Review". Be strict.

Return ONLY valid JSON. NO explanations, NO extra text after the closing brace."""
    assignment = model_manager.get_assignment()
    primary_model = assignment.get("primary", "qwen2.5:14b")
    raw = ollama_client.chat_with_vault(review_prompt, primary_model)
    json_match = re.search(r'(\{.*?\})', raw, re.DOTALL)
    if not json_match:
        return {"status": "failed"}
    json_str = json_match.group(1)
    try:
        data = json.loads(json_str)
        new_category = data.get("category", "Review")
        new_confidence = float(data.get("confidence", 0.0))
        slug, timestamp = extract_slug_and_timestamp(p.name)
        new_name = f"{new_category.lower()}-{slug}-{new_confidence:.2f}-{timestamp}.md"
        new_p = p.parent / new_name
        if p != new_p:
            p.rename(new_p)
            p = new_p
        with open(p, "a", encoding="utf-8") as fp:
            fp.write(f"\n\n## AI Review Summary (Ollama)\n{raw}\n")
        return {"status": "enhanced", "new_path": str(new_p.relative_to(VAULT_ROOT)), "summary": raw[:300]}
    except:
        return {"status": "failed"}

@router.post("/api/bulk_edit")
async def bulk_edit(request: dict = Body(...)):
    paths = request.get("paths", [])
    new_category = request.get("new_category", "keep")
    new_confidence = float(request.get("new_confidence", 0.0))
    force_review = request.get("force_review", False)
    for path_str in paths:
        p = VAULT_ROOT / path_str
        if not (p.exists() and p.is_file()):
            continue
        content = p.read_text(encoding="utf-8")
        stem = p.stem
        cat_match = re.match(r'^([a-z]+)-', stem)
        current_cat = cat_match.group(1).capitalize() if cat_match else "Review"
        if force_review:
            new_category = "Review"
        elif new_category == "keep":
            new_category = current_cat
        slug, timestamp = extract_slug_and_timestamp(p.name)
        new_name = f"{new_category.lower()}-{slug}-{new_confidence:.2f}-{timestamp}.md"
        new_p = p.parent / new_name
        if p != new_p:
            p.rename(new_p)
            p = new_p
        with open(p, "a", encoding="utf-8") as fp:
            fp.write(f"\n\n## Bulk Edit Applied (category={new_category}, confidence={new_confidence})\n")
    return {"status": "success"}

@router.post("/api/chat")
async def chat(request: dict = Body(...)):
    msg = request.get("message", "")
    assignment = model_manager.get_assignment()
    model = request.get("model") or assignment.get("primary")
    reply = ollama_client.chat_with_vault(msg, model)
    return {"reply": reply}

@router.post("/api/save_thought")
async def api_save_thought(request: dict = Body(...)):
    thought = request.get("thought", "")
    return save_thought_and_reply(thought)

@router.get("/api/note/{path:path}")
async def get_note(path: str):
    full_path = VAULT_ROOT / path
    if full_path.exists() and full_path.is_file():
        content = full_path.read_text(encoding="utf-8")
        return {"filename": Path(path).name, "content": content}
    return {"error": "File not found"}

@router.delete("/api/note/{path:path}")
async def delete_note(path: str):
    full_path = VAULT_ROOT / path
    if full_path.exists() and full_path.is_file():
        full_path.unlink()
        return {"status": "deleted"}
    return {"error": "File not found"}
