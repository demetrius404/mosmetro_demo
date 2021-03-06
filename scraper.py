import os

import json
import lxml.html as html

import schedule

from datetime import datetime
from datetime import date
from requests import Session
from requests.exceptions import ConnectionError
from lxml.html import Element
from time import sleep

from typing import Dict
from typing import Union

from lib import create_postgres_session
from lib import create_logger
from lib import News
from lib.typing_alias import Str
from lib.typing_alias import Bytes
from lib.typing_alias import Int
from lib.typing_alias import Date

# logging
log = create_logger("scraper")


def parse_news_block(element: Element, basic_url: Str) -> Union[Dict, None]:
    payload = dict()
    try:
        payload["news_title"] = element.xpath(".//span[@class='newslist__text-title']/text()")[0]
        payload["news_url"] = "".join([basic_url, element.xpath("./@href")[0]])
        payload["image_url"] = "".join([basic_url, element.xpath(".//img/@src")[0]])
    except IndexError:
        return None
    return payload


def parse_news_public_date(raw_date: Str) -> Union[Date, None]:
    months = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12
    }
    day, month, year = raw_date.strip().lower().split(" ")
    try:
        return date(int(year), months[month], int(day))
    except (ValueError, TypeError, KeyError):
        return None


def web_session_get(session: Session, url: Str) -> Union[Bytes, None]:
    try:
        log.info("Web session: {0}".format(url))
        response = session.get(url)
    except ConnectionError:
        log.error("connection error")
        return None
    if response.status_code == 200:
        return response.content
    else:
        log.error("status code")
        return None


def scrape_news_list(delay: Int = 2) -> None:

    basic_url = "https://www.mosmetro.ru"

    log.info("create Web session")
    with open("lib/user_agent.json") as f:
        user_agent = json.load(f)
    web_session = Session()
    web_session.headers.update(user_agent)

    log.info("create PostgreSQL session")
    postgres_engine, postgres_connection, postgres_session = create_postgres_session(os.environ["POSTGRES_URL"])

    content = web_session_get(web_session, "".join([basic_url, "/press/news/"]))
    if content:
        dom_news_list = html.fromstring(content)
        for item in dom_news_list.xpath("//a[@class='newslist__link']"):
            payload = parse_news_block(item, basic_url)
            payload["parse_date"] = datetime.today().date()

            log.info("News <{0}>".format(payload["news_url"]))

            where = News.news_url == payload["news_url"]
            news_exists = postgres_session.query(News).filter(where).first()
            if not news_exists:
                # extra public date
                dom_news = html.fromstring(web_session_get(web_session, payload["news_url"]))
                raw_public_date = dom_news.xpath("//div[@class='pagetitle__content-date']/text()")[0]
                payload["public_date"] = parse_news_public_date(raw_public_date)
                log.info("insert")
                postgres_session.add(News(**payload))
                postgres_session.commit()
                log.info("sleep")
                sleep(delay)
            else:
                log.info("exists")

    log.info("close Web session")
    web_session.close()
    log.info("close PostgreSQL session")
    postgres_connection.close()


def init_database(delay: Int = 15):
    log.info("create PostgreSQL session")
    postgres_engine, postgres_connection, postgres_session = create_postgres_session(os.environ["POSTGRES_URL"], delay)
    log.info("create table if required")
    News.__table__.create(postgres_engine, checkfirst=True)
    postgres_connection.close()
    log.info("close PostgreSQL session")
    postgres_connection.close()


if __name__ == "__main__":

    init_database(15)

    log.info("first round")
    scrape_news_list(1)  # step delay 1s

    minutes = 10
    log.info("schedule every {0} minutes".format(minutes))
    schedule.every(10).minutes.do(scrape_news_list, 5)  # step delay 5s

    while True:
        schedule.run_pending()
        sleep(1)


