from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
import sys

# Ensure backend modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from code_generator_module import generate_code
from code_explainer_module import explain_code
from model_loader import load_models

app = FastAPI()

class CodeRequest(BaseModel):
    prompt: str
    language: str
    model: str = "gemma"

class ExplainRequest(BaseModel):
    code: str
    style: str
    model: str = "deepseek"

@app.on_event("startup")
async def startup_event():
    print("Starting up model server...")
    # Pre-load models on startup
    load_models()

@app.post("/generate")
async def generate(request: CodeRequest):
    try:
        result = generate_code(request.prompt, request.language, request.model)
        return {"code": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain")
async def explain(request: ExplainRequest):
    try:
        result = explain_code(request.code, request.style, request.model)
        return {"explanation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
