import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class WikiSearch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    searched_on: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)
    search_keyword: str = Field(default=None)
    page_id: Optional[int] = Field(default=None)
    original_title: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    images: Optional[str] = Field(default=None)
    links: Optional[str] = Field(default=None)
    references: Optional[str] = Field(default=None)
    coordinates: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    html: Optional[str] = Field(default=None)