import pytest
from httpx import AsyncClient, ASGITransport
from main import app

pytest_plugins = ['pytest_asyncio']

# Configuration explicite du scope de la boucle asyncio
def pytest_configure(config):
    config.option.asyncio_mode = "strict"
    pytest.asyncio_fixture_scope = "function"

@pytest.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async_client = AsyncClient(transport=transport, base_url="http://test")
    return async_client 