from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import tempfile
from retrieval.ingest import DocumentProcessor
from retrieval.vector_store import VectorStoreManager

app = FastAPI(title="Scout: Autonomous Funding Agent API")

# Setup CORS - In production, replace "*" with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
processor = DocumentProcessor()
vector_store = VectorStoreManager()

# Ensure temp directory exists
os.makedirs("./temp_uploads", exist_ok=True)

@app.get("/")
async def root():
    return {"status": "Scout API is live", "engine": "NVIDIA NIM / Nemotron"}

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

@app.get("/search")
async def search_knowledge(q: str):
    """
    Search the RAG store for relevant context.
    """
    results = vector_store.query(q)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
