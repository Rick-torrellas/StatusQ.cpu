run:
    uv run --env-file .env.prod main.py
prod:
    uv run --env-file .env.prod main.py
dev:
    uv run --env-file .env.dev main.py
test:
    uv run pytest -v tests/
setup:
    uv sync
install package:
    uv add {{package}}
uninstall package:
    uv remove {{package}} 
# freeze:
#    .venv/bin/python -m pip freeze > requirements.txt
format:
    uv ruff format .
lint:
    uv run ruff check .
lint-fix:
   uv run ruff check --fix .