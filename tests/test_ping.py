import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("expected", [
    ({"Ping": "Pong!"})
])
async def test_ping(client: AsyncClient, expected: dict):
    response = await client.get("/ping")
    assert response.status_code == 200
    assert response.json() == expected
