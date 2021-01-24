import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import redirect
from flask import request
from flask import abort

from datetime import datetime
from datetime import timedelta

from lib.typing_alias import Int
from lib.typing_alias import Bool
from lib import create_postgres_session
from lib import create_logger
from lib import News

# logging
log = create_logger("application")

log.info("create PostgreSQL session")
postgres_engine, postgres_connection, postgres_session = create_postgres_session(os.environ["POSTGRES_URL"])
News.__table__.create(postgres_engine, checkfirst=True)
postgres_connection.close()
log.info("close PostgreSQL session")
postgres_connection.close()

log.info("create Flask application")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = False
postgres = SQLAlchemy(app)


def validate_days(days: Int, max_days: Int = 31) -> Bool:
    if 0 <= days <= max_days:
        return True
    else:
        return False


@app.route("/", methods=["GET"])
def index():
    return redirect("/metro/news", code=302)


@app.route("/metro/news", methods=["GET"])
def metro_news():
    days = request.args.get("days", default=5, type=Int)
    if not validate_days(days):
        abort(400)
    period_start = datetime.today().date()
    period_end = period_start - timedelta(days=days)

    items = list()
    desc = News.public_date.desc()
    where = News.public_date >= period_end
    news = postgres.session.query(News).filter(where).order_by(desc).all()
    for item in news:
        _news = {
            "news_title": item.news_title,
            "image_url": item.image_url,
            "public_date": item.public_date.strftime("%Y-%m-%d")
        }
        items.append(_news)
    return jsonify(news=items, period=[period_start.strftime("%Y-%m-%d"), period_end.strftime("%Y-%m-%d")]), 200


@app.before_request
def before_request():
    log.info("{0}".format(request))


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(description="page not found", code=404), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify(description="internal server error", code=500), 500


@app.errorhandler(400)
def bad_request(e):
    return jsonify(description="bad request", code=400), 400
