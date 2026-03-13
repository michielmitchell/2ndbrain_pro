# filename: second_brain_builder/main.py
# purpose: Entry point - launches the modular FastAPI app (keeps everything working perfectly)

import uvicorn
from src.web.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
