from sqlite3.dbapi2 import Timestamp, adapt
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime


class EpicArea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    epic_id: int = Field(foreign_key="epic.id")
    epic_area: str
    active: bool
    created_at: datetime
    updated_at: datetime