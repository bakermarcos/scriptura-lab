VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
UVICORN := $(VENV)/bin/uvicorn

.PHONY: help venv api-install web-install install qdrant-up qdrant-down api web ingest test build-web

help:
	@printf "Available targets:\\n"
	@printf "  make venv        Create root Python virtualenv\\n"
	@printf "  make api-install Install FastAPI backend in editable mode\\n"
	@printf "  make web-install Install frontend dependencies\\n"
	@printf "  make install     Install backend and frontend dependencies\\n"
	@printf "  make qdrant-up   Start Qdrant with docker compose\\n"
	@printf "  make qdrant-down Stop Qdrant\\n"
	@printf "  make api         Run FastAPI on port 8000\\n"
	@printf "  make web         Run Vite on port 5173\\n"
	@printf "  make ingest      Index sample Markdown sources\\n"
	@printf "  make test        Run backend tests\\n"
	@printf "  make build-web   Build the frontend\\n"

$(PYTHON):
	python3 -m venv $(VENV)

venv: $(PYTHON)

api-install: $(PYTHON)
	$(PIP) install -e "apps/api[dev]"

web-install:
	cd apps/web && npm install

install: api-install web-install

qdrant-up:
	docker compose up -d

qdrant-down:
	docker compose down

api:
	cd apps/api && ../../$(UVICORN) app.main:app --reload --port 8000

web:
	cd apps/web && npm run dev

ingest:
	$(PYTHON) scripts/ingest/ingest_sample_data.py

test:
	cd apps/api && ../../$(PYTEST)

build-web:
	cd apps/web && npm run build
