run:
    .venv/bin/python main.py
setup:
    .venv/bin/python -m pip install -r requirements.txt
test:
    .venv/bin/python -m pytest -v tests/