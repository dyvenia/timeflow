from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel, or_
from sqlalchemy.exc import NoResultFound
from ..models.user import User
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/users", tags=["user"])
session = Session(engine)


@router.post("/")
async def post_user(
    user: User,
    session: Session = Depends(get_session),
):
    """
    Post a new user.

    Parameters
    ----------
    user : User
        User that is to be added to the database.
    session : Session
        SQL session that is to be used to add the user.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(User).where(User.short_name == user.short_name)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.get("/")
async def get_users(
    session: Session = Depends(get_session),
    is_active: bool = None,
    short_name: str = None,
):
    """
    Get list of user(s).

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the users.
        Defaults to creating a dependency on the running SQL model session.
    is_active : bool
        Status of users to be pulled.
    short_name : str
        Short name of user to be pulled.
    """
    statement = select(User)
    if is_active != None:
        statement = select(User).where(User.is_active == is_active)
        if short_name != None:
            statement = (
                select(User)
                .where(User.is_active == is_active)
                .where(User.short_name == short_name)
            )
    result = session.exec(statement).all()
    return result


@router.put("/{user_id}/")
async def update_user(
    user_id: int,
    is_active: Optional[bool] = None,
    new_short_name: Optional[str] = None,
    new_first_name: Optional[str] = None,
    new_last_name: Optional[str] = None,
    new_email: Optional[str] = None,
    new_team_id: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """
    Update a user.

    Parameters
    ----------
    user_id : int
        ID of user to be updated.
    is_active : Optional[bool]
        Updated status of user.
    new_short_name : Optional[bool]
        Updated short name of user.
    new_first_name : Optional[bool]
        Updated first name of user.
    new_last_name : Optional[bool]
        Updated last name of user.
    new_email : Optional[bool]
        Updated email of user
    new_team_id : Optional[bool]
        Updated team id.
    session : Session
        SQL session that is to be used to update the user.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(User).where(User.id == user_id)
    user_to_update = session.exec(statement).one()
    if is_active != None:
        user_to_update.is_active = is_active
    if new_short_name != None:
        user_to_update.short_name = new_short_name
    if new_first_name != None:
        user_to_update.first_name = new_first_name
    if new_last_name != None:
        user_to_update.last_name = new_last_name
    if new_email != None:
        user_to_update.email = new_email
    if new_team_id != None:
        user_to_update.team_id = new_team_id
    user_to_update.updated_at = datetime.now()
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return user_to_update
