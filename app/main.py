from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.core.engine import SemanticCoverageEngine

app = FastAPI(title="Semantic Coverage API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (okay for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize Engine globally (so we don't reload the model on every request)
engine = SemanticCoverageEngine()

class AnalyzeRequest(BaseModel):
    documents: List[str]
    queries: List[str]

@app.get("/")
def health_check():
    return {"status": "running", "service": "semantic-coverage-api"}

@app.post("/analyze")
def analyze_gap(payload: AnalyzeRequest):
    if not payload.documents or not payload.queries:
        raise HTTPException(status_code=400, detail="Docs and Queries cannot be empty")
    
    try:
        report = engine.analyze(payload.documents, payload.queries)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)