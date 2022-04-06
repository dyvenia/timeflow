from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, or_
from ..models.team import Team
from ..models.user import User
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/teams", tags=["team"])
session = Session(engine)


@router.post("/")
async def post_team(
    *,
    team: Team,
    session: Session = Depends(get_session),
):
    """
    Post new team.

    Parameters
    ----------
    team : Team
        Team that is to be added to the database.
    session : Session
        SQL session that is to be used to add the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(or_(Team.name == team.name, Team.id == team.id))
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team


@router.get("/")
async def get_team_list(session: Session = Depends(get_session)):
    """
    Get list of all teams.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the list of teams.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def get_active_team_list(session: Session = Depends(get_session)):
    """
    Get list of active teams.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the active teams.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Team.id,
            Team.lead_user_id,
            Team.name.label("team_name"),
            Team.short_name.label("team_short_name"),
            User.id,
            User.short_name.label("user_name"),
        )
        .join(User)
        .where(Team.is_active == True)
    )
    results = session.exec(statement).all()
    return results


@router.get("/{team_name}")
async def read_teams(team_name: str = None, session: Session = Depends(get_session)):
    """
    Read the contents of a given team.

    Parameters
    ----------
    team_name : str
        Name of team to be read.
    session : Session
        SQL session that is to be used to read the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.name == team_name)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no team named {team_name}"""
        return msg


@router.get("/{team_id}/user-name")
async def get_user_name_by_team_id(
    team_id: int, session: Session = Depends(get_session)
):
    """
    Get user name by team id.

    Parameters
    ----------
    team_id : str
        ID of team to pull user name from.
    session : Session
        SQL session that is to be used to get the user name.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Team.id, User.id, User.name)
        .join(User)
        .where(Team.id == team_id)
        .where(User.active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{team_name}/activate")
async def activate_team(
    team_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate a team.

    Parameters
    ----------
    team_name : str
        Name of team to be activated.
    session : Session
        SQL session that is to be used to activate the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.name == team_name)
    team_to_activate = session.exec(statement).one()
    team_to_activate.is_active = True
    team_to_activate.updated_at = datetime.now()
    session.add(team_to_activate)
    session.commit()
    session.refresh(team_to_activate)
    return team_to_activate


@router.put("/{team_name}/deactivate")
async def deactivate_team(
    team_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate a team.

    Parameters
    ----------
    team_name : str
        Name of team to be deactivated.
    session : Session
        SQL session that is to be used to deactivate the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.name == team_name)
    team_to_deactivate = session.exec(statement).one()
    team_to_deactivate.is_active = False
    team_to_deactivate.updated_at = datetime.now()
    session.add(team_to_deactivate)
    session.commit()
    session.refresh(team_to_deactivate)
    return team_to_deactivate


@router.put("/")
async def update_team(
    id: str = None,
    lead_user_id: str = None,
    name: str = None,
    is_active: bool = None,
    session: Session = Depends(get_session),
):
    """
    Update a team with new values.

    Parameters
    ----------
    id : str
        ID of team to be updated.
    lead_user_id : str
        Updated lead user ID.
    name : str
        Updated name of team.
    is_active : bool
        Updated status of team.
    session : Session
        SQL session that is to be used to update the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(or_(Team.name == name, Team.id == id))
    team_to_update = session.exec(statement).one()
    team_to_update.lead_user_id = lead_user_id
    team_to_update.name = name
    team_to_update.is_active = is_active
    session.add(team_to_update)
    team_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(team_to_update)
    return team_to_update
