from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class Message(BaseModel):
    content: str
    role: str = "user"
    timestamp: datetime = datetime.now()

class ChatSession(BaseModel):
    id: Optional[str] = None
    title: str
    pdf_context: Optional[str] = None
    messages: List[Message] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class ChatResponse(BaseModel):
    message: str
    sources: Optional[List[Dict[str, str]]] = None

class PDFUpload(BaseModel):
    filename: str
    file_url: str
    uploaded_at: datetime = datetime.now() 