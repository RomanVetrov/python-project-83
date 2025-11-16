from __future__ import annotations

import os
from contextlib import contextmanager
import logging

import psycopg2
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


@contextmanager
def get_connection():
    """Контекстный менеджер, который открывает и автоматически закрывает соединение с БД."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    logger.debug("Открываем соединение с БД")
    conn = psycopg2.connect(database_url)
    try:
        yield conn
    finally:
        logger.debug("Закрываем соединение с БД")
        conn.close()


def fetch_urls():
    """Возвращает список URL-адресов с датой и кодом последней проверки.

    Использую DISTINCT ON с сортировкой по url_checks.id, чтобы Postgres
    за один проход по данным выбрал последнюю проверку для каждого URL без
    дополнительных подзапросов."""
    logger.info("Выполняем запрос списка URL-адресов")
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    urls.created_at,
                    url_checks.created_at AS last_check,
                    url_checks.status_code AS last_status
                FROM urls
                LEFT JOIN url_checks ON url_checks.url_id = urls.id
                ORDER BY urls.id DESC, url_checks.id DESC;
                """
            )
            return cursor.fetchall()


def find_url_by_id(url_id: int) -> DictCursor | None:
    """Возвращает URL по идентификатору или None."""
    logger.info("Ищем URL по id=%s", url_id)
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, name, created_at
                FROM urls
                WHERE id = %s
                """,
                (url_id,),
            )
            return cursor.fetchone()


def find_url_by_name(name: str) -> DictCursor | None:
    """Возвращает URL по имени или None."""
    logger.info("Ищем URL по имени=%s", name)
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, name, created_at
                FROM urls
                WHERE name = %s
                """,
                (name,),
            )
            return cursor.fetchone()


def create_url(name: str) -> int:
    """Создаёт новую запись URL и возвращает её идентификатор."""
    logger.info("Создаём новую запись URL name=%s", name)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO urls (name)
                VALUES (%s)
                RETURNING id
                """,
                (name,),
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            return new_id


def create_check(url_id: int, status_code: int) -> int:
    """Сохраняет результат проверки и возвращает идентификатор проверки."""
    logger.info("Создаём проверку для url_id=%s", url_id)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id, status_code)
                VALUES (%s, %s)
                RETURNING id
                """,
                (url_id, status_code),
            )
            check_id = cursor.fetchone()[0]
            conn.commit()
            return check_id


def fetch_checks(url_id: int) -> list[DictCursor]:
    """Возвращает список проверок для указанного URL."""
    logger.info("Получаем список проверок для url_id=%s", url_id)
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                """,
                (url_id,),
            )
            return cursor.fetchall()
