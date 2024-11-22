from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from models.schemas import ChatMessage, ChatResponse, Conversation, MessageRole
from services.chat import ChatService
from typing import List
import json

router = APIRouter()
chat_service = ChatService()

@router.post("/conversations", response_model=Conversation)
async def create_conversation():
    """Crée une nouvelle conversation"""
    try:
        conversation = chat_service.create_conversation()
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Récupère une conversation par son ID"""
    conversation = chat_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/conversations/{conversation_id}/messages")
async def send_message(conversation_id: str, message: ChatMessage):
    """Envoie un message et obtient une réponse"""
    try:
        # Ajouter le message de l'utilisateur
        chat_service.add_message(
            conversation_id=conversation_id,
            content=message.content,
            role=MessageRole.USER
        )
        
        # Générer et renvoyer la réponse
        response = await chat_service.generate_response(conversation_id)
        return ChatResponse(response=response)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversations/{conversation_id}/messages/stream")
async def send_message_stream(conversation_id: str, message: ChatMessage):
    """Envoie un message et obtient une réponse en streaming"""
    try:
        # Ajouter le message de l'utilisateur
        chat_service.add_message(
            conversation_id=conversation_id,
            content=message.content,
            role=MessageRole.USER
        )
        
        # Créer le générateur de streaming
        async def generate():
            try:
                async for chunk in chat_service.generate_stream(conversation_id):
                    # Envoyer chaque chunk au format SSE (Server-Sent Events)
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=List[Conversation])
async def list_conversations():
    """Liste toutes les conversations"""
    return list(chat_service.conversations.values())

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Supprime une conversation"""
    try:
        if conversation_id in chat_service.conversations:
            del chat_service.conversations[conversation_id]
            return {"message": "Conversation deleted successfully"}
        raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 