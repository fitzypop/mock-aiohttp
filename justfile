default:
    echo 'Hello, world!'

test:
    poetry run pytest -rP .

publish:
    poetry publish --build
