from sqlalchemy.dialects.postgresql import TEXT, DATE
from sqlalchemy import Column

from .basic import Base
from .typing_alias import Str


class News(Base):
    __tablename__ = "tab_mosmetro_news"
    news_url = Column(TEXT, primary_key=True, nullable=False)
    news_title = Column(TEXT, nullable=False)  # removed pk, migrate db
    image_url = Column(TEXT, nullable=False)
    parse_date = Column(DATE, nullable=False)
    public_date = Column(DATE, nullable=False)

    def __str__(self) -> Str:
        return "News <{0}>".format(self.news_url)
