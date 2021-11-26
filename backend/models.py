from typing import Optional
from sqlmodel import Field, SQLModel, Field, create_engine

con_str = f"sqlite:///database.sqlite"
engine = create_engine(con_str, echo=True)


class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_initials: str
    start_time: str
    end_time: str
    client_name: str
    epic_name: str
    work_hours: Optional[float]
    month: Optional[int]
    year: Optional[int]

class Forecast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_initials: str
    epic_name: str
    work_hours: int
    month: int
    year: int

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_initials: str
    user_name: str
    user_surname: str
    user_email: str


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: str


class Epic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    epic_name: str


def create_db():
    SQLModel.metadata.create_all(engine)
