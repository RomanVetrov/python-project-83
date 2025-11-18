import logging
import os
import requests

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from dotenv import load_dotenv

load_dotenv()

from . import db  # noqa: E402
from .services import normalize_url, is_valid_url, parse_seo_data  # noqa: E402

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


INDEX_TEMPLATE = "index.html"
INVALID_URL_MESSAGE = "Некорректный URL"


@app.route("/", methods=["GET"])
def index():
    """Выводит главную страницу с формой добавления URL."""
    return render_template(INDEX_TEMPLATE)


@app.get("/urls")
def urls_index():
    """Показывает список всех URL с датой и кодом последней проверки."""
    app.logger.info("Запрашиваем список URL-адресов")
    urls = db.fetch_urls()
    return render_template("urls/index.html", urls=urls)


@app.get("/urls/<int:url_id>")
def url_show(url_id: int):
    """Отображает карточку URL и историю проверок."""
    app.logger.info("Открываем страницу URL id=%s", url_id)
    url = db.find_url_by_id(url_id)

    if url is None:
        app.logger.warning("URL не найден id=%s", url_id)
        abort(404)

    checks = db.fetch_checks(url_id)
    return render_template("urls/show.html", url=url, checks=checks)


@app.post("/urls")
def urls_create():
    """Обрабатывает создание нового URL."""
    raw_url = request.form.get("url", "").strip()
    app.logger.info("Получен ввод URL='%s'", raw_url)

    if not raw_url:
        flash(INVALID_URL_MESSAGE, "danger")
        return render_template(INDEX_TEMPLATE), 422

    normalized = normalize_url(raw_url)
    app.logger.info("Результат нормализации='%s'", normalized)

    if not normalized:
        flash(INVALID_URL_MESSAGE, "danger")
        return render_template(INDEX_TEMPLATE), 422

    if not is_valid_url(normalized):
        flash(INVALID_URL_MESSAGE, "danger")
        return render_template(INDEX_TEMPLATE), 422

    if len(normalized) > 255:
        flash("URL превышает 255 символов", "danger")
        return render_template(INDEX_TEMPLATE), 422

    existing = db.find_url_by_name(normalized)

    if existing:
        app.logger.info("URL уже существует id=%s", existing["id"])
        flash("Страница уже существует", "info")
        return redirect(url_for("url_show", url_id=existing["id"]))

    try:
        url_id = db.create_url(normalized)
    except Exception:
        app.logger.exception("Не удалось сохранить URL '%s'", normalized)
        flash("Ошибка при добавлении страницы", "danger")
        return redirect(url_for("index"))

    app.logger.info("URL успешно добавлен id=%s", url_id)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("url_show", url_id=url_id))


@app.post("/urls/<int:url_id>/checks")
def url_checks_create(url_id: int):
    """Запускает проверку конкретного URL."""
    app.logger.info("Создаём проверку для URL id=%s", url_id)
    url = db.find_url_by_id(url_id)  # данные ссылки вида {"value": "value"}

    if url is None:
        app.logger.warning(
            "Нельзя создать проверку: URL не найден id=%s",
            url_id,
        )
        abort(404)

    url_name = url["name"]  # достал ссылку

    try:
        response = requests.get(url_name)  # достал объект Response
        response.raise_for_status()  # ловим 4хх-5хх ошибки
    except requests.RequestException:
        app.logger.exception("Не удалось выполнить запрос к URL id=%s", url_id)
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("url_show", url_id=url_id))

    status_code = response.status_code  # достаем HTTP-Code ответа
    seo_data = parse_seo_data(response.text)

    try:
        db.create_check(
            url_id,
            status_code,
            h1=seo_data["h1"],
            title=seo_data["title"],
            description=seo_data["description"],
        )
    except Exception:
        app.logger.exception(
            "Не удалось сохранить результат проверки URL id=%s", url_id
            )
        flash("Не удалось сохранить проверку", "danger")
        return redirect(url_for("url_show", url_id=url_id))

    flash("Страница успешно проверена", "success")
    return redirect(url_for("url_show", url_id=url_id))
