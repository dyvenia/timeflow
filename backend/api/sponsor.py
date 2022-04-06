from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, or_
from ..models.client import Client
from ..models.sponsor import Sponsor
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/sponsors", tags=["sponsor"])
session = Session(engine)


@router.post("/")
async def post_sponsor(
    *,
    sponsor: Sponsor,
    session: Session = Depends(get_session),
):
    """
    Post new sponsor.

    Parameters
    ----------
    sponsor : Sponsor
        Sponsor that is to be added to the database.
    session : Session
        SQL session that is to be used to add the sponsor.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Sponsor).where(
        or_(Sponsor.name == sponsor.name, Sponsor.id == sponsor.id)
    )
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(sponsor)
        session.commit()
        session.refresh(sponsor)
        return sponsor


@router.get("/")
async def get_sponsor_list(session: Session = Depends(get_session)):
    """
    Get entire sponsor list (enabled and disabled).

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the sponsors.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Sponsor)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def get_active_sponsor_list(session: Session = Depends(get_session)):
    """
    Get list of active sponsors along with the name of the client.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the sponsors.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Sponsor.id,
            Sponsor.client_id,
            Sponsor.name.label("sponsor_name"),
            Sponsor.short_name.label("sponsor_short_name"),
            Client.name.label("client_name"),
        )
        .join(Client)
        .where(Sponsor.is_active == True)
    )
    results = session.exec(statement).all()
    return results


@router.get("/{sponsor_name}")
async def read_teams(sponsor_name: str = None, session: Session = Depends(get_session)):
    """
    Read the contents of a given sponsor.

    Parameters
    ----------
    sponsor_name : str
        Name of sponsor to be read.
    session : Session
        SQL session that is to be used to read a sponsor.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Sponsor).where(Sponsor.name == sponsor_name)
    try:
        result = session.exec(statement).ones()
        return result
    except NoResultFound:
        msg = f"""There is no sponsor named {sponsor_name}"""


@router.get("/{sponsor_id}/client-name")
async def get_client_name_by_sponsor_id(
    sponsor_id: int, session: Session = Depends(get_session)
):
    """
    Get client name by sponsor id.

    Parameters
    ----------
    sponsor_id : int
        ID of sponsor to pull client name from.
    session : Session
        SQL session that is to be used to get the client name.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Sponsor.id, Client.id, Client.name)
        .join(Client)
        .where(Sponsor.id == sponsor_id)
        .where(Client.is_active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{sponsor_name}/activate")
async def activate_sponsor(
    sponsor_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate a sponsor.

    Parameters
    ----------
    sponsor_name : str
        Name of sponsor to be activated.
    session : Session
        SQL session that is to be used to activate the sponsor.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Sponsor).where(Sponsor.name == sponsor_name)
    sponsor_to_activate = session.exec(statement).one()
    sponsor_to_activate.is_active = True
    sponsor_to_activate.updated_at = datetime.now()
    session.add(sponsor_to_activate)
    session.commit()
    session.refresh(sponsor_to_activate)
    return sponsor_to_activate


@router.put("/{sponsor_name}/deactivate")
async def deactivate_sponsor(
    sponsor_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate a sponsor.

    Parameters
    ----------
    sponsor_name : str
        Name of sponsor to be deactivated.
    session : Session
        SQL session that is to be used to deactivate the sponsor.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Sponsor).where(Sponsor.name == sponsor_name)
    sponsor_to_deactivate = session.exec(statement).one()
    sponsor_to_deactivate.is_active = False
    sponsor_to_deactivate.updated_at = datetime.now()
    session.add(sponsor_to_deactivate)
    session.commit()
    session.refresh(sponsor_to_deactivate)
    return sponsor_to_deactivate


@router.put("/")
async def update_sponsor(
    id: int = None,
    client_id: int = None,
    name: str = None,
    short_name: str = None,
    is_active: bool = None,
    session: Session = Depends(get_session),
):
    """
    Update a sponsor.

    Parameters
    ----------
    id : int
        ID of sponsor to be updated.
    client_id : int
        Updated client ID.
    name : str
        Updated sponsor name.
    short_name : str
        Updated short name of sponsor.
    is_active : bool
        Updated status of sponsor.
    session : Session
        SQL session that is to be used to update the sponsor.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Sponsor).where(or_(Sponsor.name == name, Sponsor.id == id))
    sponsor_to_update = session.exec(statement).one()
    sponsor_to_update.client_id = client_id
    sponsor_to_update.name = name
    sponsor_to_update.short_name = short_name
    sponsor_to_update.is_active = is_active
    session.add(sponsor_to_update)
    sponsor_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(sponsor_to_update)
    return sponsor_to_update
