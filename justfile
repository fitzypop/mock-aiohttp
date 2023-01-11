default:
    echo 'Thanks for cloning!'

test:
    poetry run pytest -rP .

publish:
    poetry publish --build
