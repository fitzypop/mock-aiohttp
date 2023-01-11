"""
Mocking aiohttp async, nested, context managers for testing.

Specifically, the request method.

Run the following to get started
pip install --upgrade aiohttp pytest pytest-asyncio
pytest -rP "test_aiohttp_mock.py"
"""
import sys

import pytest


if sys.version_info < (3,8):
    pytest.skip(
        "must use 3.8 or greater",
        allow_module_level=True,
    )


from unittest.mock import AsyncMock, Mock

import aiohttp

class ContextManagerMock:
    async def __aenter__(self):
        pass

    async def __aexit__(self):
        pass

    def request(self):
        pass


@pytest.fixture
def aiomock() -> tuple:
    response = AsyncMock()
    response.json.return_value = {"body": "asdf"}
    response.raise_for_status = Mock(side_effect=aiohttp.ClientError)

    context = AsyncMock(ContextManagerMock)
    context.request.return_value.__aenter__.return_value = response

    session = AsyncMock(ContextManagerMock)
    session.__aenter__.return_value = context
    session.request.return_value.__aenter__.return_value = response

    return (session, context, response)


@pytest.mark.asyncio
async def test_async_mock_works(aiomock):
    session, context, response = aiomock
    with pytest.raises(aiohttp.ClientError):
        async with session:
            async with session.request(
                method="GET", url="https://catfact.ninja/fact"
            ) as _resp:
                _resp.raise_for_status()
                result = await _resp.json()

    session.request.assert_called_once()
    context.request.assert_not_called()
    response.raise_for_status.assert_called_once()
    response.json.assert_not_called()
