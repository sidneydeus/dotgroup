from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class BookFilter(BaseModel):
    title: Optional[str] = Field(None, description="Filter by title (partial match)")
    author: Optional[str] = Field(None, description="Filter by author (partial match)")


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")
    publication_date: date = Field(..., description="Publication date")
    summary: Optional[str] = Field(None, max_length=2000, description="Book summary")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    publication_date: Optional[date] = None
    summary: Optional[str] = Field(None, max_length=2000)


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True