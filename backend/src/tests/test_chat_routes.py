import pytest
from httpx import AsyncClient
from main import app
import json
from models.schemas import MessageRole

@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient):
    """Test la création d'une nouvelle conversation"""
    test_client = await client  # Attendre la coroutine
    response = await test_client.post("/api/chat/conversations")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "messages" in data
    assert isinstance(data["messages"], list)

@pytest.mark.asyncio
async def test_get_conversation(client):
    """Test la récupération d'une conversation"""
    test_client = await client  # Attendre la coroutine
    # Créer d'abord une conversation
    conv_response = await test_client.post("/api/chat/conversations")
    conv_id = conv_response.json()["id"]
    
    # Récupérer la conversation
    response = await test_client.get(f"/api/chat/conversations/{conv_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conv_id

@pytest.mark.asyncio
async def test_send_message(client):
    test_client = await client
    # Créer une conversation
    conv_response = await test_client.post("/api/chat/conversations")
    conv_id = conv_response.json()["id"]
    
    # Envoyer un message
    message = {"content": "Bonjour, comment vas-tu ?"}
    response = await test_client.post(
        f"/api/chat/conversations/{conv_id}/messages",
        json=message
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

@pytest.mark.asyncio
async def test_streaming_message(client):
    test_client = await client
    # Créer une conversation
    conv_response = await test_client.post("/api/chat/conversations")
    conv_id = conv_response.json()["id"]
    
    # Envoyer un message en streaming
    message = {"content": "Compte jusqu'à 3"}
    response = await test_client.post(
        f"/api/chat/conversations/{conv_id}/messages/stream",
        json=message
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

@pytest.mark.asyncio
async def test_list_conversations(client):
    test_client = await client
    # Créer quelques conversations
    await test_client.post("/api/chat/conversations")
    await test_client.post("/api/chat/conversations")
    
    # Récupérer la liste
    response = await test_client.get("/api/chat/conversations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

@pytest.mark.asyncio
async def test_delete_conversation(client):
    test_client = await client
    # Créer une conversation
    conv_response = await test_client.post("/api/chat/conversations")
    conv_id = conv_response.json()["id"]
    
    # Supprimer la conversation
    response = await test_client.delete(f"/api/chat/conversations/{conv_id}")
    assert response.status_code == 200
    
    # Vérifier que la conversation n'existe plus
    response = await test_client.get(f"/api/chat/conversations/{conv_id}")
    assert response.status_code == 404