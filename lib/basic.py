from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from time import sleep
from typing import Tuple
from .typing_alias import Str
from .typing_alias import Int


def create_postgres_session(postgres_url: Str, delay: Int = 0) -> Tuple:
    sleep(delay)  # delay before create
    postgres_engine = create_engine(name_or_url=postgres_url, echo=False)
    postgres_session_maker = sessionmaker(bind=postgres_engine)
    postgres_connection = postgres_engine.connect()
    postgres_session = postgres_session_maker(bind=postgres_connection)
    return postgres_engine, postgres_connection, postgres_session


Base = declarative_base()
