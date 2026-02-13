run:
    .venv/bin/python main.py
setup:
    .venv/bin/python -m pip install -r requirements.txt
test:
    .venv/bin/python -m pytest -v tests/
install package:
    .venv/bin/python -m pip install {{package}}
uninstall package:
    .venv/bin/python -m pip uninstall {{package}} -y
freeze:
    .venv/bin/python -m pip freeze > requirements.txt
format:
    .venv/bin/python -m ruff format .
lint:
    .venv/bin/python -m ruff check .
lint-fix:
   .venv/bin/python  -m ruff check --fix .