import os
from fastapi import *
from sqlmodel import Session, select, SQLModel, text
from sqlalchemy.exc import OperationalError
from .models.timelog import TimeLog
from .models.calendar import Calendar
from .utils import (
    engine,
    create_db,
    tags_metadata,
    execute_sample_sql,
)
from .api import (
    user,
    timelog,
    forecast,
    epic,
    epic_area,
    client,
    rate,
    team,
    role,
    sponsor,
    capacity,
    demand,
)
import csv

app = FastAPI(title="timeflow app API", openapi_tags=tags_metadata)

session = Session(engine)
app.include_router(timelog.router)
app.include_router(forecast.router)
app.include_router(user.router)
app.include_router(epic.router)
app.include_router(epic_area.router)
app.include_router(client.router)
app.include_router(rate.router)
app.include_router(team.router)
app.include_router(role.router)
app.include_router(sponsor.router)
app.include_router(capacity.router)
app.include_router(demand.router)


@app.on_event("startup")
def on_startup():
    if os.getenv("TIMEFLOW_DEV") == "true":
        create_db()
        execute_sample_sql(session)
    elif os.getenv("TIMEFLOW_DEV") == "false":
        try:
            statement = select(TimeLog)
            results = session.exec(statement)
        except OperationalError:
            create_db()


@app.on_event("startup")
def implement_calendar_table():
    try:
        statement = select(Calendar.year_name).where(Calendar.id == 1)
        result = session.exec(statement).one()
    except Exception as e:
        print(e)
        values_sql = f"""INSERT INTO app_db.calendar (date, year_number, year_name, quarter_number, quarter_name
                    , month_number, month_name, week_number, week_name, week_day_number, week_day_name)
                    VALUES """
        with open("backend/calendar.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar="|")
            values_list = []
            for index, row in enumerate(reader):
                if index > 0 and row[0] != "":
                    _row = [f"'{item}'" for item in row]
                    row_sql = ", ".join(_row)
                    values = f"({row_sql}),"
                    values_sql += values
            values_sql += f"({row_sql});"
            with engine.connect() as con:
                con.execute(text(values_sql))
                con.commit()
