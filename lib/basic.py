from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from typing import Tuple
from .typing_alias import Str


def create_postgres_session(connection_string: Str) -> Tuple:
    postgres_engine = create_engine(name_or_url=connection_string, echo=False)
    postgres_session_maker = sessionmaker(bind=postgres_engine)
    postgres_connection = postgres_engine.connect()
    postgres_session = postgres_session_maker(bind=postgres_connection)
    return postgres_engine, postgres_connection, postgres_session


Base = declarative_base()
