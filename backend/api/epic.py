from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel, or_
from ..models.epic import Epic
from ..models.client import Client
from ..models.sponsor import Sponsor
from ..models.team import Team
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/epics", tags=["epic"])
session = Session(engine)


@router.post("/")
async def post_epic(
    *,
    epic: Epic,
    session: Session = Depends(get_session),
):
    """
    Post new epic.

    Parameters
    ----------
    epic : Epic
        Epic that is to be added to the database.
    session : Session
        SQL session that is to be used to add the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement1 = select(Epic).where(Epic.name == epic.name)
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        session.add(epic)
        session.commit()
        session.refresh(epic)
        return epic


@router.get("/")
async def get_epic_list(session: Session = Depends(get_session)):
    """
    Get list of epics.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def get_active_epics_list(session: Session = Depends(get_session)):
    """
    Get list of active epics.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the active epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic).where(Epic.is_active == True)
    results = session.exec(statement).all()
    return results


@router.get("/teams/{team_id}/sponsors/{sponsor_id}/")
async def get_epic_by_team_sponsor(team_id: int, sponsor_id: int):
    """
    Get list of epics by team id and sponsor id.

    Parameters
    ----------
    team_id : int
        ID of team to pull epics from.
    sponsor_id : int
        ID of sponsor to pull epics from.
    session : Session
        SQL session that is to be used to pull the epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Epic.id.label("epic_id"),
            Epic.name.label("epic_name"),
            Epic.start_date,
            Team.name.label("team_name"),
            Sponsor.short_name.label("sponsor_short_name"),
        )
        .select_from(Epic)
        .join(Team)
        .join(Sponsor)
        .where(Epic.team_id == team_id)
        .where(Epic.sponsor_id == sponsor_id)
        .where(Epic.is_active == True)
    )
    results = session.exec(statement).all()
    return results


@router.get("/{epic_id}/client-name")
async def get_client_name_by_epic_id(
    epic_id: int, session: Session = Depends(get_session)
):
    """
    Get client name from epic_id.

    Parameters
    ----------
    epic_id : int
        ID of epic to pull client name from.
    session : Session
        SQL session that is to be used to pull the client name.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Client.name.label("client_name"), Client.id.label("client_id"))
        .select_from(Epic)
        .join(Sponsor, isouter=True)
        .join(Client, isouter=True)
        .where(Epic.id == epic_id)
        .where(Client.is_active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{epic_id}/activate")
async def activate_epic(
    epic_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate an epic using its ID as a key.

    Parameters
    ----------
    epic_id : str
        ID of epic to be activated.
    session : Session
        SQL session that is to be used to activate the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic).where(Epic.id == epic_id)
    epic_to_activate = session.exec(statement).one()
    epic_to_activate.is_active = True
    epic_to_activate.updated_at = datetime.now()
    session.add(epic_to_activate)
    session.commit()
    session.refresh(epic_to_activate)
    return epic_to_activate


@router.put("/{epic_id}/deactivate")
async def deactivate_epic(
    epic_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate an epic using its ID as a key.

    Parameters
    ----------
    epic_id : str
        ID of epic to be deactivated.
    session : Session
        SQL session that is to be used to deactivate the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic).where(Epic.id == epic_id)
    epic_to_deactivate = session.exec(statement).one()
    epic_to_deactivate.is_active = False
    epic_to_deactivate.updated_at = datetime.now()
    session.add(epic_to_deactivate)
    session.commit()
    session.refresh(epic_to_deactivate)
    return epic_to_deactivate


@router.put("/")
async def update_epic(
    epic_id: str = None,
    new_short_name: str = None,
    new_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Update an epic.

    Parameters
    ----------
    epic_id : str
        ID of epic to be updated.
    new_short_name : str
        Name of new short name.
    new_name : str
        Name of new name.
    session : Session
        SQL session that is to be used to update the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic).where(Epic.id == epic_id).where(Epic.is_active == True)
    epic_to_update = session.exec(statement).one()
    if new_short_name != None:
        epic_to_update.short_name = new_short_name
    if new_name != None:
        epic_to_update.name = new_name
    session.add(epic_to_update)
    epic_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(epic_to_update)
    return epic_to_update
