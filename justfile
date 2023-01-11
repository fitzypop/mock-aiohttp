default:
    echo 'Hello, world!'

test:
    poetry run pytest -rP test_aiohttp_mock.py
