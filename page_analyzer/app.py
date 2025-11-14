import os
from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

