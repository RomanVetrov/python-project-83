import logging
import os

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
from .services import normalize_url  # noqa: E402

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.get("/urls")
def urls_index():
    app.logger.info("Запрашиваем список URL-адресов")
    urls = db.fetch_urls()
    return render_template("urls/index.html", urls=urls)


@app.get("/urls/<int:url_id>")
def url_show(url_id: int):
    app.logger.info("Открываем страницу URL id=%s", url_id)
    url = db.find_url_by_id(url_id)

    if url is None:
        app.logger.warning("URL не найден id=%s", url_id)
        abort(404)

    return render_template("urls/show.html", url=url)


@app.post("/urls")
def urls_create():
    raw_url = request.form.get("url", "").strip()
    app.logger.info("Получен ввод URL='%s'", raw_url)

    if not raw_url:
        flash("Некорректный URL", "danger")
        return redirect(url_for("index"))

    normalized = normalize_url(raw_url)
    app.logger.info("Результат нормализации='%s'", normalized)

    if not normalized:
        flash("Некорректный URL", "danger")
        return redirect(url_for("index"))

    if len(normalized) > 255:
        flash("URL превышает 255 символов", "danger")
        return redirect(url_for("index"))

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
