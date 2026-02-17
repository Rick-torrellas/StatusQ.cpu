# Justfile for CPU monitoring application
# Provides standardized commands for development, testing, and deployment

# --- Application Execution ---
run:
	# Execute the main application in production mode with production environment variables
	uv run --env-file .env.prod main.py

prod:
	# Alias for run command - starts production instance
	uv run --env-file .env.prod main.py

dev:
	# Execute the main application in development mode with development environment variables
	uv run --env-file .env.dev main.py

test:
	# Run the test suite with verbose output using pytest
	uv run pytest -v tests/ --log-file=tests/test.log --log-file-level=DEBUG

# --- Project Initialization & Setup ---
init:
	# Initialize a new Python project using uv
	uv init

setup:
	# Synchronize project dependencies according to pyproject.toml/uv.lock
	uv sync

# --- Package Management ---
install package:
	# Add a new Python package to the project dependencies
	# Usage: make install package=requests
	uv add {{package}}

uninstall package:
	# Remove an existing Python package from project dependencies
	# Usage: make uninstall package=requests
	uv remove {{package}} 

# # Legacy freeze command - commented out for reference
# # Generates requirements.txt from current virtual environment
# freeze:
#    .venv/bin/python -m pip freeze > requirements.txt

# --- Code Quality & Formatting ---
check: format-check lint-check
	# Run all code quality checks (formatting and linting)

format-check:
	# Check code formatting compliance without making changes
	# Exits with non-zero status if formatting issues are found
	uv run ruff format --check .

format:
	# Automatically format code according to ruff rules
	uv run ruff format .

lint-check:
	# Run linting checks to identify code quality issues without fixing
	uv run ruff check .
    
lint:
	# Run linting checks and automatically fix issues where possible
	uv run ruff check --fix .

# --- Docker Commands ---
build:
	# Build Docker containers using docker-compose
	# Use this before starting containers when changes are made to Dockerfile
	docker-compose up --build

up:
	# Start Docker containers in detached mode with production environment variables
	docker-compose --env-file .env.prod up -d

docker-down:
	# Stop and remove all running Docker containers defined in docker-compose
	docker-compose down

docker-shell:
	# Open an interactive bash shell in a new container instance
	# Useful for debugging and inspecting the container environment
	docker-compose run --env-file .env.prod --rm --entrypoint /bin/bash statusq-cpu

changelog:
	# Generate a changelog from git commit history using git-chglog
	# Output is saved to CHANGELOG.md
	uv run gitchangelog > CHANGELOG.md