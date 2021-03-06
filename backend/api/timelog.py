from fastapi import APIRouter, Depends
from ..utils import get_session
from sqlmodel import Session, select
from ..models.user import AppUser
from ..models.timelog import TimeLog
from ..models.epic import Epic
from ..models.epic_area import EpicArea

router = APIRouter(prefix="/api/timelogs", tags=["timelog"])


@router.post("/")
async def timelog(*, timelog: TimeLog, session: Session = Depends(get_session)):
    """
    Post new timelog.

    Example: timelog.start_time = "2022-01-19T08:30:00.000Z

    Parameters
    ----------
    timelog : TimeLog
        Timelog that is to be added to the database.
    session : Session
        SQL session that is to be used to add the timelog.
        Defaults to creating a dependency on the running SQL model session.
    """
    # checking overlaping timelogs
    statement1 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.start_time >= timelog.start_time)
        .where(TimeLog.start_time < timelog.end_time)
    )
    statement2 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.end_time > timelog.start_time)
        .where(TimeLog.end_time <= timelog.end_time)
    )
    statement3 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.start_time >= timelog.start_time)
        .where(TimeLog.end_time <= timelog.end_time)
    )
    statement4 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.start_time < timelog.start_time)
        .where(TimeLog.end_time > timelog.end_time)
    )
    # Checking if timelog doesn't procede posted epic's start date
    statement5 = (
        select(Epic)
        .where(Epic.id == timelog.epic_id)
        .where(Epic.start_date > timelog.start_time)
    )

    results1 = session.exec(statement1).all()
    results2 = session.exec(statement2).all()
    results3 = session.exec(statement3).all()
    results4 = session.exec(statement4).all()
    results5 = session.exec(statement5).all()

    if results1 or results2 or results3 or results4:
        return "Currently posted timelog overlaps another timelog"
    elif results5:
        return "epic was created later than timelog's start date"
    else:
        time_delta = timelog.end_time - timelog.start_time
        work_delta_hours = time_delta.total_seconds() / 3600
        work_hours = "{:.3f}".format(work_delta_hours)
        work_delta_days = time_delta.total_seconds() / 3600 / 8
        work_days = "{:.3f}".format(work_delta_days)
        timelog.count_hours = work_hours
        timelog.count_days = work_days
        session.add(timelog)
        session.commit()
        session.refresh(timelog)
        return "Your log has been submitted"


@router.get("/")
async def get_timelogs_all(session: Session = Depends(get_session), month: int = None):
    """
    Get list all timelogs.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the timelogs.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            TimeLog.id,
            AppUser.username.label("username"),
            AppUser.first_name,
            AppUser.last_name,
            AppUser.email.label("user_email"),
            Epic.name.label("epic_name"),
            EpicArea.name.label("epic_area_name"),
            TimeLog.start_time,
            TimeLog.end_time,
            TimeLog.count_hours,
            TimeLog.count_days,
        )
        .join(AppUser)
        .join(EpicArea)
        .join(Epic)
    )
    if month != None:
        statement_final = statement.where(TimeLog.month == month).order_by(
            TimeLog.end_time.desc()
        )
    else:
        statement_final = statement.order_by(TimeLog.end_time.desc())
    results = session.exec(statement_final).all()
    return results


@router.get("/users/{user_id}")
async def get_timelog_by_user_id(
    user_id: int, session: Session = Depends(get_session), month: int = None
):
    statement = (
        select(
            TimeLog.id,
            AppUser.email.label("user_email"),
            AppUser.first_name,
            AppUser.last_name,
            Epic.name.label("epic_name"),
            EpicArea.name.label("epic_area_name"),
            TimeLog.start_time,
            TimeLog.end_time,
            TimeLog.count_hours,
            TimeLog.count_days,
        )
        .join(AppUser)
        .join(EpicArea)
        .join(Epic)
        .where(TimeLog.user_id == user_id)
    )
    if month != None:
        statement_final = statement.where(TimeLog.month == month).order_by(
            TimeLog.end_time.desc()
        )

    else:
        statement_final = statement.order_by(TimeLog.end_time.desc())

    results = session.exec(statement_final).all()
    return results


@router.get("/{timelog_id}")
async def get_timelog_by_id(timelog_id: int, session: Session = Depends(get_session)):
    """
    Get timelog by id.

    Parameters
    ----------
    timelog_id : int
        ID of timelog to be returned.
    session : Session
        SQL session that is to be used to get the timelog.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(TimeLog).where(TimeLog.id == timelog_id)
    result = session.exec(statement).one()
    return result


@router.get("/users/{user_id}/epics/{epic_id}")
async def get_timelog_user_id(
    *,
    user_id: int,
    epic_id: int,
    month: int,
    year: int,
    session: Session = Depends(get_session),
):
    """
    Get list of timelogs by user_id, month.

    Parameters
    ----------
    user_id : str
        ID of user from which to pull timelogs.
    year_month : int
        Month and year from which to pull timelog(s).
    session : Session
        SQL session that is to be used to get the timelogs.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            TimeLog.id,
            AppUser.username.label("username"),
            Epic.name.label("epic_name"),
            EpicArea.name.label("epic_area_name"),
            TimeLog.start_time,
            TimeLog.end_time,
            TimeLog.count_hours,
            TimeLog.count_days,
        )
        .join(AppUser)
        .join(EpicArea)
        .join(Epic)
        .where(TimeLog.user_id == user_id)
        .where(TimeLog.epic_id == epic_id)
        .where(TimeLog.month == month)
        .where(TimeLog.year == year)
        .order_by(TimeLog.end_time.desc())
    )
    results = session.exec(statement).all()
    return results


@router.delete("/{timelog_id}")
async def delete_timelogs(
    *,
    timelog_id: int,
    user_id: int = None,
    session: Session = Depends(get_session),
):
    """
    Delete a timelog.

    Parameters
    ----------
    timelog_id : int
        ID of timelog to be deleted.
    session : Session
        SQL session that is to be used to delete the timelog.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(TimeLog).where(TimeLog.id == timelog_id)
    if user_id != None:
        statement_final = statement.where(TimeLog.user_id == user_id)
    else:
        statement_final = statement
    result = session.exec(statement_final).one()
    timelog_to_delete = result
    session.delete(timelog_to_delete)
    session.commit()
    return True
