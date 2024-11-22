from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import Message, ChatResponse, ChatSession, PDFUpload
from services.chat import ChatService
from services.google_storage import GoogleCloudStorage
from typing import List
import PyPDF2
import io

router = APIRouter()
chat_service = ChatService()
storage_service = GoogleCloudStorage()

@router.post("/chat/simple", response_model=ChatResponse)
async def chat_without_context(message: Message):
    """Chat without RAG context"""
    response = await chat_service.chat_without_rag(message.content)
    return ChatResponse(message=response)

@router.post("/chat/rag", response_model=ChatResponse)
async def chat_with_context(message: Message, session_id: str):
    """Chat with RAG context"""
    # Ici, vous devrez implémenter la récupération du vectorstore associé à la session
    # Pour l'instant, nous utilisons un mock
    vectorstore = None  # À implémenter
    response, sources = await chat_service.chat_with_rag(message.content, vectorstore)
    return ChatResponse(message=response, sources=sources)

@router.post("/upload/pdf", response_model=PDFUpload)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Lire et vérifier le PDF
    pdf_content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Upload to Google Cloud Storage
    file_url = await storage_service.upload_file(
        io.BytesIO(pdf_content),
        file.filename
    )
    
    return PDFUpload(filename=file.filename, file_url=file_url) 