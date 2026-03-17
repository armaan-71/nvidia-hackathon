from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import shutil
import os
import tempfile
from retrieval.ingest import DocumentProcessor
from retrieval.vector_store import VectorStoreManager
from agents.orchestrator import AgentOrchestrator
from models import ChatRequest, AgentResponse
from config import get_settings
import session_store

# Load settings
settings = get_settings()

app = FastAPI(
    title="Scout API",
    description="Autonomous funding agent for nonprofits",
    version="0.1.0",
)

# Setup CORS using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
processor = DocumentProcessor()
vector_store = VectorStoreManager()
orchestrator = AgentOrchestrator()

# Ensure temp directory exists
os.makedirs("./temp_uploads", exist_ok=True)

@app.get("/")
@app.get("/health")
async def health():
    return {"status": "Scout API is live", "engine": "NVIDIA NIM / Nemotron", "version": "0.1.0"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a nonprofit document, chunk it, and index it in the RAG pipeline.
    """
    try:
        # Use tempfile to avoid path traversal vulnerabilities
        with tempfile.NamedTemporaryFile(dir="./temp_uploads", delete=False, suffix=f"_{file.filename}") as buffer:
            shutil.copyfileobj(file.file, buffer)
            temp_path = buffer.name
    
        try:
            # Process and chunk
            chunks = processor.process_file(temp_path)
            
            # Add to vector store
            success = vector_store.add_documents(chunks)
            
            if success:
                return {"message": f"Successfully indexed {len(chunks)} chunks from {file.filename}"}
            else:
                raise HTTPException(status_code=500, detail="Failed to generate embeddings via NVIDIA NIM.")
        except Exception as e:
            # Log the error (could use logging here too)
            print(f"Ingestion error: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during document ingestion: {str(e)}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/reset")
async def reset_knowledge_base(session_id: Optional[str] = Query(None)):
    """
    Clears all documents from the RAG vector store and resets session memory.
    """
    try:
        success = vector_store.clear_all_documents()
        session_store.clear_session(session_id)
        if success:
            return {"message": "Knowledge base and session history cleared."}
        else:
            return {"message": "Knowledge base was already empty."}
    except Exception as e:
        print(f"Reset error: {e}")
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.get("/dashboard")
async def get_dashboard_summary(session_id: str = Query(...)):
    """
    Returns aggregated stats and recent activity for the dashboard.
    """
    grants = session_store.get_grants(session_id)
    messages = session_store.get_messages(session_id)
    
    # Calculate stats
    total_grants = len(grants)
    avg_score = 0
    if total_grants > 0:
        # Calculate average match score
        avg_score = sum(round(g.get("score", 0) * 100) for g in grants if "score" in g) // total_grants

    # Extract recent activity (last 2 agent messages)
    activity = []
    agent_msgs = [m for m in messages if m.get("role") == "agent"][-2:]
    for m in agent_msgs:
        activity.append({
            "agent": m.get("agent", "Scout"),
            "action": m.get("content", "")[:100] + "...",
            "timestamp": "Just now"
        })

    return {
        "stats": {
            "opportunities_found": total_grants,
            "avg_match_score": avg_score,
            "upcoming_deadlines": 0 # Placeholder
        },
        "recent_activity": activity
    }

@app.get("/search")
async def search_knowledge(q: str):
    """
    Search the RAG store for relevant context.
    """
    results = vector_store.query(q)
    return {"results": results}

@app.post("/api/agent/chat", response_model=AgentResponse)
async def agent_chat(request: ChatRequest):
    """
    Agentic chat endpoint that orchestrates between specialists.
    """
    try:
        response = await orchestrator.chat(request.message, request.session_id)
        return response
    except Exception as e:
        print(f"Agent Orchestration Error: {e}")
        raise HTTPException(status_code=500, detail=f"Agent failed to respond: {str(e)}")


@app.post("/chat", response_model=AgentResponse)
async def chat(request: ChatRequest):
    """
    Primary chat endpoint. Calls the agent orchestrator and caches any
    discovered grants so they can be retrieved via GET /grants.
    """
    try:
        response = await orchestrator.chat(request.message, request.session_id)

        # Cache grants if the discovery agent returned any
        if response.data and "grants" in response.data:
            grants = response.data["grants"]
            if isinstance(grants, list) and grants:
                session_store.save_grants(request.session_id, grants)

        return response
    except Exception as e:
        print(f"Agent Orchestration Error: {e}")
        raise HTTPException(status_code=500, detail=f"Agent failed to respond: {str(e)}")


@app.get("/grants", response_model=List[Dict[str, Any]])
def get_grants(session_id: str = Query(..., description="Session ID from a previous /chat call")):
    """
    Returns the ranked grant opportunities discovered during a chat session.
    """
    return session_store.get_grants(session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
