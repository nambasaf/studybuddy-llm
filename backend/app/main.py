from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uuid
import openai

from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from .llm_service import LLMService

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Enable CORS for the Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,   # allow cookies/headers like auth
    allow_methods=["*"],      # for http meths like GET, POST
    allow_headers=["*"],      # allow custom headers like Content-Type
)

# Initialize services
doc_processor = DocumentProcessor()
vector_store = VectorStore()
llm_service = LLMService()

@app.get("/")
def read_root():
    return {"message": "Studybuddy API is running!"} # confirm api is live

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)): # tells FastAPI to expect a file upload
    """Upload and process a PDF document"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate a unique document ID
        doc_id = str(uuid.uuid4())

        # process document
        chunks = doc_processor.process_document(file.file)

        # Store in vector database
        vector_store.store_chunks(chunks, doc_id)

        return {
            "document_id": doc_id,
            "filename": file.filename,
            "chunks_created": len(chunks),
            "message": "Document uploaded successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Error processing document: {str(e)}")

@app.post("/ask")
async def ask_question(request: dict):
    """Answer a question based on uploaded documents"""
    query = request.get("question")
    complexity = request.get("complexity", "medium")

    if not query:
        raise HTTPException(status_code=400, detail="Question is required")
    
    try:
        # Find relevant chunks for the  question
        similar_chunks = vector_store.search_similar(query, top_k=5)
        context_texts = [chunk["text"] for chunk in similar_chunks]

        # Generate answer
        answer = llm_service.generate_answer(query, context_texts, complexity)
        return {
            "answer": answer,
            "sources_found": len(similar_chunks),
            "confidence_scores": [chunk["score"] for chunk in similar_chunks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
    
@app.post("/generate-quiz")
async def generate_quiz(request: dict):
    """Generate quiz questions based on uploaded documents"""
    topic = request.get("topic", "")
    num_questions = request.get("num_questions", 5)

    try:
        # Search for relevant content
        if topic:
            similar_chunks = vector_store.search_similar(topic, top_k=3)
        else:
            # if no topic is specified, get some random chunks
            similar_chunks = vector_store.search_similar("main concepts", top_k=3)

        context_texts = [chunk["text"] for chunk in similar_chunks]

        # Generate quiz
        questions = llm_service.generate_quiz_questions(context_texts, num_questions)

        return {
            "questions": questions,
            "topic": topic or "General"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

# Starts the backend server so it can accept requests.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)