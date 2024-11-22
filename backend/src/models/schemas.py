from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ChatMessage(BaseModel):
    content: str

class ChatResponse(BaseModel):
    response: str
    
class Conversation(BaseModel):
    id: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    title: Optional[str] = None 

    model_config = ConfigDict(arbitrary_types_allowed=True) 