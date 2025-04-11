import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from src.main import app

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


@pytest_asyncio.fixture
async def api_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:80") as client:
        yield client
