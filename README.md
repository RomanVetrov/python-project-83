# Page Analyzer

[![Actions Status](https://github.com/RomanVetrov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/RomanVetrov/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=RomanVetrov_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=RomanVetrov_python-project-83)

Веб‑приложение, которое сохраняет пользовательские URL‑адреса, выполняет их проверки и отображает историю SEO‑метрик (HTTP‑статус, `<title>`, `<h1>`, `meta description`).

## Технологический стек

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat-square)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white&style=flat-square)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white&style=flat-square)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?logo=gunicorn&logoColor=white&style=flat-square)
![Render](https://img.shields.io/badge/Render-1F1F1F?logo=render&logoColor=white&style=flat-square)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=white&style=flat-square)
![SonarCloud](https://img.shields.io/badge/SonarCloud-F3702A?logo=sonarcloud&logoColor=white&style=flat-square)
![uv](https://img.shields.io/badge/uv-121212?logo=readthedocs&logoColor=white&style=flat-square)

## Основные возможности

- добавление сайтов с валидацией, нормализацией и защитой от дублей;
- выполнение проверок и сохранение результатов в PostgreSQL;
- отображение истории проверок и статуса каждого сайта;
- flash‑сообщения и аккуратный Bootstrap‑интерфейс;
- логирование ключевых операций;
- CI: GitHub Actions + SonarCloud (linters, покрытие, security hotspots).

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

Скопируйте пример переменных окружения и отредактируйте его под себя:

```bash
cp .env.example .env
```

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
