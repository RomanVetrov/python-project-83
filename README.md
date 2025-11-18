# Page Analyzer

[![Actions Status](https://github.com/RomanVetrov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/RomanVetrov/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=RomanVetrov_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=RomanVetrov_python-project-83)

Веб‑приложение, которое сохраняет пользовательские URL‑адреса, выполняет их проверки и отображает историю SEO‑метрик (HTTP‑статус, `<title>`, `<h1>`, `meta description`). Проект создавался по программе Hexlet, но аккуратно переупакован, чтобы им было не стыдно делиться с потенциальными работодателями.

## Основные возможности

- добавление сайтов с валидацией, нормализацией и защитой от дублей;
- выполнение проверок и сохранение результатов в PostgreSQL;
- отображение истории проверок и статуса каждого сайта;
- flash‑сообщения и Bootstrap‑интерфейс, повторяющий демо Hexlet;
- логирование ключевых операций;
- CI: GitHub Actions + SonarCloud (linters, покрытие, security hotspots).

## Технологический стек

- Python 3.12, Flask 3, Gunicorn 23
- PostgreSQL + psycopg2
- Bootstrap 5
- uv (управление зависимостями и виртуальной средой)
- GitHub Actions, SonarCloud, Render.com

## Требования

- Python ≥ 3.12
- PostgreSQL 14+
- [uv](https://docs.astral.sh/uv/) установлен в систему

## Установка и запуск

```bash
git clone https://github.com/RomanVetrov/python-project-83.git
cd python-project-83
make install            # установка зависимостей через uv
```

Создайте `.env` в корне:

```dotenv
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db>
SECRET_KEY=<любая_строка>
```

Подготовьте БД (создайте таблицы):

```bash
psql -d "$DATABASE_URL" -f database.sql
```

Запустить локально:

```bash
make dev
# приложение по умолчанию доступно на http://127.0.0.1:5000
```

## Полезные команды

| Команда        | Назначение                                    |
| -------------- | --------------------------------------------- |
| `make install` | установка зависимостей                        |
| `make dev`     | запуск Flask в режиме разработки              |
| `make lint`    | проверка стиля (Ruff)                         |
| `make lint-fix`| автоисправление замечаний Ruff                |
| `make build`   | скрипт сборки для Render (`build.sh`)         |

## Тесты и качество кода

- `make lint` — основной линтинг (Ruff).
- `uv run pytest --cov=page_analyzer --cov-report=xml:coverage.xml` — прогон тестов (при их наличии) и генерация покрытия для SonarCloud.
- GitHub Actions (`.github/workflows/python.yml`) автоматически запускают линтер, pytest и SonarCloud Scan при каждом push.

## Деплой

Проект развёрнут на [Render.com](https://render.com/) и доступен по адресу:  
https://python-project-83-1w25.onrender.com

### Команда запуска в продакшене

`make render-start` (использует `.venv/bin/gunicorn -b 0.0.0.0:<port>`).

## Структура проекта

```
page_analyzer/
├── app.py                # Flask-приложение
├── db.py                 # работа с PostgreSQL
├── services.py           # вспомогательные функции
└── templates/            # Jinja2-шаблоны
database.sql              # актуальная схема БД
build.sh                  # скрипт сборки/миграций для Render
```

## Лицензия

Проект распространяется на условиях MIT License. Используйте, форкните, дорабатывайте и присылайте PR'ы.
