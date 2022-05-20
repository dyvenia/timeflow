from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from ..models.user import AppUser
from ..models.role import Role
from ..models.team import Team
from typing import Optional
from datetime import datetime, date

router = APIRouter(prefix="/api/users", tags=["user"])


@router.post("/")
async def post_user(
    user: AppUser,
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
    statement = select(AppUser).where(AppUser.username == user.username)
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
    username: str = None,
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
    username : str
        Short name of user to be pulled.
    """
    statement = select(AppUser)
    if is_active != None:
        statement = (
            select(
                AppUser.id,
                AppUser.username,
                AppUser.first_name,
                AppUser.last_name,
                Role.short_name.label("role_short_name"),
                Team.short_name.label("main_team"),
                AppUser.start_date,
            )
            .select_from(AppUser)
            .join(Role, AppUser.role_id == Role.id, isouter=True)
            .join(Team, AppUser.team_id == Team.id, isouter=True)
            .where(AppUser.is_active == is_active)
            .order_by(AppUser.start_date.desc())
        )
    elif username != None:
        statement = (
            select(
                AppUser.id,
                AppUser.username,
                AppUser.first_name,
                AppUser.last_name,
                AppUser.start_date,
            )
            .select_from(AppUser)
            .where(AppUser.username == username)
        )
    result = session.exec(statement).all()
    return result


@router.put("/{user_id}/")
async def update_user(
    user_id: int,
    is_active: Optional[bool] = None,
    new_username: Optional[str] = None,
    new_first_name: Optional[str] = None,
    new_last_name: Optional[str] = None,
    new_email: Optional[str] = None,
    new_team_id: Optional[int] = None,
    new_role_id: Optional[int] = None,
    new_start_date: Optional[date] = None,
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
    new_username : Optional[str]
        Updated short name of user.
    new_first_name : Optional[str]
        Updated first name of user.
    new_last_name : Optional[str]
        Updated last name of user.
    new_email : Optional[str]
        Updated email of user
    new_team_id : Optional[int]
        Updated team id.
    new_role_id : Optional[int]
        Updated role id.
    new_start_date : Optional[date]
        Updated start date.
    session : Session
        SQL session that is to be used to update the user.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(AppUser).where(AppUser.id == user_id)
    user_to_update = session.exec(statement).one()
    if is_active != None:
        user_to_update.is_active = is_active
    if new_username != None:
        user_to_update.username = new_username
    if new_first_name != None:
        user_to_update.first_name = new_first_name
    if new_last_name != None:
        user_to_update.last_name = new_last_name
    if new_email != None:
        user_to_update.email = new_email
    if new_team_id != None:
        user_to_update.team_id = new_team_id
    if new_role_id != None:
        user_to_update.role_id = new_role_id
    if new_start_date != None:
        user_to_update.start_date = new_start_date
    user_to_update.updated_at = datetime.now()
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return user_to_update
