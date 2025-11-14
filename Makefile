# ============================
# Установка зависимостей
# ============================
install:
	uv sync


# ============================
# Локальная разработка
# ============================
dev:
	uv run flask --debug --app page_analyzer:app run


# ============================
# Линтер (Ruff)
# ============================
lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .


# ============================
# Продакшен (Gunicorn)
# ============================
PORT ?= 8000

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


# ============================
# Render build
# ============================
build:
	./build.sh
