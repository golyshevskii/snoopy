# System
ROOT_DIR := $(shell powershell -Command "(Get-Location).Path")
ROOT_DIR_MAC := $(shell pwd)

env:
	powershell -Command "Get-ChildItem Env:"

path:
	powershell -Command "$$env:PYTHONPATH='$$env:PYTHONPATH;$(ROOT_DIR)';

mac-path:
	export PYTHONPATH=$(ROOT_DIR_MAC)

# Dependencies
init:
	poetry install --no-root

# Linting & Formatting (CI\CD)
lint:
	cd .github/lint && poetry run black --config pyproject.toml ../../core/
	cd .github/lint && poetry run flake8 --config .flake8 ../../core/

format:
	cd .github/lint && poetry run black --config pyproject.toml ../../core/

check-lint:
	cd .github/lint && poetry run black --config pyproject.toml --check ../../core/
	cd .github/lint && poetry run flake8 --config .flake8 ../../core/

# Docker
up:
	docker-compose up

up-b:
	docker-compose up --build

down:
	docker-compose down
