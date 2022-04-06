from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from ..models.capacity import Capacity
from sqlmodel import Session, select, SQLModel, and_
from sqlalchemy.exc import NoResultFound
from ..models.user import User
from ..models.team import Team

router = APIRouter(prefix="/api/capacities", tags=["capacity"])
session = Session(engine)


@router.post("/")
async def post_capacity(*, capacity: Capacity, session: Session = Depends(get_session)):
    """
    Post new capacity.

    Parameters
    ----------
    capacity : Capacity
        Capacity that is to be added to the database.
    session : Session
        SQL session that is to be used to add the capacity.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Capacity).where(
        and_(
            Capacity.user_id == capacity.user_id,
            Capacity.team_id == capacity.team_id,
            capacity.year == capacity.year,
            Capacity.month == capacity.month,
        )
    )
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(capacity)
        session.commit()
        session.refresh(capacity)
        return capacity


@router.get("/")
async def get_capacities(
    session: Session = Depends(get_session),
    is_locked: bool = None,
    user_id: int = None,
    team_id: int = None,
    month: int = None,
    year: int = None,
):
    """
    Get list of all capacities.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the epic areas.
        Defaults to creating a dependency on the running SQL model session.
    is_locked : bool
        Whether or not the capacity is locked or not.
    user_id : int
        User id of the user in question.
    team_id : int
        Team id of the user's team.
    month : int
        Month of capacity in question.
    year : int
        Year of capacity in question.
    """
    statement = select(Capacity)
    # Select capacity by user_id, team_id, month, year
    if (user_id and team_id and month and year) != None:
        statement = (
            select(
                Capacity.id.label("capacity_id"),
                User.short_name.label("user_short_name"),
                Team.short_name.label("team_short_name"),
                Capacity.year,
                Capacity.month,
                Capacity.days,
            )
            .select_from(Capacity)
            .join(User, Capacity.user_id == User.id)
            .join(Team, Capacity.team_id == Team.id)
            .where(Capacity.user_id == user_id)
            .where(Capacity.team_id == team_id)
            .where(Capacity.month == month)
            .where(Capacity.year == year)
        )

    result = session.exec(statement).all()
    return result


@router.delete("/")
async def delete_capacities(
    capacity_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Delete a capacity

    Parameters
    ----------
    capacity_id : str
        ID of the capacity that is to be removed from the database.
    session : Session
        SQL session that is to be used to delete the capacity.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Capacity).where(
        Capacity.id == capacity_id,
    )

    capacity_to_delete = session.exec(statement).one()
    session.delete(capacity_to_delete)
    session.commit()
    return True
