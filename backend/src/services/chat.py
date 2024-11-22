from typing import List, Optional, AsyncGenerator
from models.schemas import Message, Conversation, MessageRole
from services.llm_service import LLMService
import uuid
from datetime import datetime

class ChatService:
    def __init__(self):
        self.conversations: dict[str, Conversation] = {}
        self.llm_service = LLMService()
    
    def create_conversation(self, title: Optional[str] = None) -> Conversation:
        """Crée une nouvelle conversation"""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            title=title or f"Conversation {len(self.conversations) + 1}"
        )
        self.conversations[conversation_id] = conversation
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Récupère une conversation par son ID"""
        return self.conversations.get(conversation_id)
    
    def add_message(self, conversation_id: str, content: str, role: MessageRole) -> Message:
        """Ajoute un message à une conversation"""
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        message = Message(role=role, content=content)
        conversation.messages.append(message)
        return message
    
    async def generate_response(self, conversation_id: str) -> str:
        """Génère une réponse pour la conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Formater l'historique pour le LLM
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]
        
        # Obtenir la réponse du LLM
        prompt = self.llm_service.format_chat_prompt(formatted_messages)
        response = await self.llm_service.generate_response(prompt)
        
        # Ajouter la réponse à la conversation
        self.add_message(conversation_id, response, MessageRole.ASSISTANT)
        return response
    
    async def generate_stream(self, conversation_id: str) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]
        
        prompt = self.llm_service.format_chat_prompt(formatted_messages)
        response_chunks = []
        
        async for chunk in self.llm_service.generate_stream(prompt):
            response_chunks.append(chunk)
            yield chunk
        
        # Une fois le streaming terminé, ajouter le message complet à la conversation
        complete_response = "".join(response_chunks)
        self.add_message(conversation_id, complete_response, MessageRole.ASSISTANT)