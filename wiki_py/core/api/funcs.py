from pathlib import Path
from wiki_py.core.wiki import searcher
from wiki_py.core.db import _db as db
from wiki_py.core.db.models import WikiSearch

def get_contents(db: db.DataBase,title: str) -> searcher.WikiContent:
    content:searcher.WikiContent = searcher.get_wiki(title, searcher.PageReturnables.ALL) # type: ignore
    db.insert_row(WikiSearch(search_keyword=title, **content.dict()))
    return content
    