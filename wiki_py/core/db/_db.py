from pathlib import Path
from typing import List, Optional, TypeAlias, Union
from pydantic import BaseModel
from sqlalchemy import Table
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine.url import URL as URL_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


class URL(BaseModel):
    drivername: str
    username: Optional[str] = None
    password: Optional[Union[str, object]] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None


DBError: TypeAlias = Union[SQLAlchemyError, DBAPIError]


class DataBase:
    def __init__(
        self, url: URL, *, echo: bool, echo_pool: bool, hide_parameters: bool
    ) -> None:
        # * Parameters to tune the SA engine
        self._url = URL_(**url.dict())
        self._echo = echo
        self._echo_pool = echo_pool
        self._hide_parameters = hide_parameters

        # * SA Tables known at the time of execution
        # ? Well do we `need` this? ... Maybe YES
        self._inbound_tables: List[Table] = self.__get_inbound_tables()

        # * SA Engine
        self._engine: Engine = self.__create_engine()

    # * Properties we use in our private methods
    @property
    def url(self):
        return self._url

    @property
    def inbound_tables(self):
        return self._inbound_tables

    @property
    def engine(self):
        return self._engine

    # * Private Methods to create some attributes required

    def __create_engine(self):
        return create_engine(
            self.url,
            echo=self._echo,
            echo_pool=self._echo_pool,
            hide_parameters=self._hide_parameters,
        )

    def __get_inbound_tables(self) -> List[Table]:
        return self.get_inbound_tables()

    # * Methods For Public Usage

    def create_file(self):
        parent_dir = Path(str(self.url.database)).parent.mkdir(parents=True, exist_ok=True)
        if not Path(str(self.url.database)).exists():
            Path(str(self.url.database)).touch()

    # * Table Related Stuffs
    def get_inbound_tables(self) -> Union[List[Table], None]:
        try:
            return SQLModel.metadata.sorted_tables
        except DBError as e:
            return None

    def create_all_tables(self):
        try:
            SQLModel.metadata.create_all(
                bind=self.engine,
                tables=self.inbound_tables,
            )
            return True

        except:  # TODO: Need to log this err
            return False

    def create_tables(
        self, bind: Engine, tables: List[Table], checkfirst: bool
    ) -> bool:
        try:
            SQLModel.metadata.create_all(
                bind=bind, tables=tables, checkfirst=checkfirst
            )
            return True
        except DBError as e:  # TODO: SHould log
            # ! Errors should not pass silently
            return False

    # * Session Related Stuffs
    def get_session(
        self,
        bind: Engine,
        *,
        autoflush: bool = ...,
        autocommit: bool = ...,
    ) -> Session:
        return Session(bind=bind, autoflush=autoflush, autocommit=autocommit)

    # * CRUD Operations
    # * Create Operation
    def insert_row(self, table: SQLModel):
        with self.get_session(self.engine) as session:
            try:
                session.begin()
                session.add(table)
            finally:
                session.commit()
    
    # TODO: Add Following ops for later usage
    # * Read Operation
    # * Update Operation
    # * Delete Operation

    # * Raw SQL
    def execute_sql(self, statement):
        with self.get_session(self.engine) as session:
            return session.execute(statement)
