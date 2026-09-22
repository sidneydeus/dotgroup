from sqlalchemy import Column, Integer, String, Text, Date
from app.core.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    publication_date = Column(Date, nullable=False)
    summary = Column(Text, nullable=True)