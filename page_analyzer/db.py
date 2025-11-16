from __future__ import annotations

import os
from contextlib import contextmanager
import logging

import psycopg2
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


@contextmanager
def get_connection():
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
    logger.info("Выполняем запрос списка URL-адресов")
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    urls.id,
                    urls.name,
                    urls.created_at,
                    (
                        SELECT created_at
                        FROM url_checks
                        WHERE url_id = urls.id
                        ORDER BY id DESC
                        LIMIT 1
                    ) AS last_check
                FROM urls
                ORDER BY id DESC;
                """
            )
            return cursor.fetchall()


def find_url_by_id(url_id: int):
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


def find_url_by_name(name: str):
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


def create_check(url_id: int) -> int:
    logger.info("Создаём проверку для url_id=%s", url_id)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id)
                VALUES (%s)
                RETURNING id
                """,
                (url_id,),
            )
            check_id = cursor.fetchone()[0]
            conn.commit()
            return check_id


def fetch_checks(url_id: int):
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

