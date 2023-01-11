default:
    echo 'Hello, world!'

test:
    poetry run pytest -rP mock-aiohttp/test_aiohttp_mock.py
