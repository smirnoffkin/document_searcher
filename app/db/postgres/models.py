from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    Integer,
    String,
    text as text_
)
from sqlalchemy.dialects.postgresql import TEXT

from app.db.postgres.connection import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    rubrics = Column(ARRAY(String), nullable=False)
    text = Column(TEXT, nullable=False)
    created_date = Column(
        DateTime,
        nullable=False,
        server_default=text_("now()")
    )
