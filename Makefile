VENV ?= venv
PY = python3

.PHONY: help deps run build docker lint test

help:
	@echo "Available targets: deps, run, build, docker, test"

deps:
	$(PY) -m pip install -r log_analyzer/requirements.txt

run:
	$(PY) app.py

build:
	docker build -t log-analyzer .

docker:
	docker run --rm -p 5000:5000 log-analyzer

test:
	$(PY) -m pytest -q
