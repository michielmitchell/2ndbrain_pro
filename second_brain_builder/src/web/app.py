# filename: second_brain_builder/src/web/app.py
# purpose: Tiny assembly layer - imports the 3 modules, creates FastAPI, mounts everything, keeps root endpoint clean

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.config import VAULT_ROOT
from .routes import router
from .frontend import get_html

app = FastAPI(title="Second Brain Builder")
app.mount("/vault", StaticFiles(directory=str(VAULT_ROOT), html=True), name="vault")

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return get_html()
