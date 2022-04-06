from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.client import Client
from ..models.epic import Epic
from datetime import datetime

router = APIRouter(prefix="/api/clients", tags=["client"])
session = Session(engine)


@router.post("/")
async def post_client(*, client: Client, session: Session = Depends(get_session)):
    """
    Post a new client.

    Parameters
    ----------
    client : Client
        Client that is to be added to the database.
    session : Session
        SQL session that is to be used to add the client.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.name == client.name)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(client)
        session.commit()
        session.refresh(client)
        return client


@router.get("/")
async def read_clients(session: Session = Depends(get_session)):
    """
    Get a list of all clients.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the clients.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def read_clients(session: Session = Depends(get_session)):
    """
    Get a list of all active clients.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of all of the active clients.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.is_active == True)
    results = session.exec(statement).all()
    return results


@router.get("/{client_id}")
async def read_clients(
    *, client_id: int = None, session: Session = Depends(get_session)
):
    """
    Get a client by client_id.

    Parameters
    ----------
    client_id : int
        ID of client that is to be read.
    session : Session
        SQL session that is to be used to read a client.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.id == client_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no client with id = {client_id}"""
        return msg


@router.get("/names/{name}")
async def read_clients_by_name(
    *, name: str = None, session: Session = Depends(get_session)
):
    """
    Get a client by client_name.

    Parameters
    ----------
    name : str
        Name of client to be read.
    session : Session
        SQL session that is to be used to read a client.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.name == name)
    result = session.exec(statement).one()
    return result


@router.get("/{client_id}/epics/")
async def read_clients_epics(
    client_id: int = None, session: Session = Depends(get_session)
):
    """
    Get epics from a client_id.

    Parameters
    ----------
    client_id : int
        ID of client that is to be used to pull epics from.
    session : Session
        SQL session that is to be used to pull the epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Client.id, Client.name, Epic.name)
        .select_from(Client)
        .join(Epic)
        .where(Client.id == client_id)
    )
    results = session.exec(statement).all()
    return results


# @router.put("/{client_id}/deactivate-client")
# async def update_clients(
#     *,
#     client_id: int,
#     session: Session = Depends(get_session),
# ):
#     """Deactivate a client"""
#     statement = select(Client).where(Client.id == client_id)
#     client_to_update = session.exec(statement).one()
#     client_to_update.active = False
#     statement2 = select(Epic).join(Clinet)
#     client_to_update = session.exec(statement).one()
#     client_to_update.active = False

#     session.add(client_to_update)
#     session.commit()
#     session.refresh(client_to_update)
#     return client_to_update


@router.put("/{client_id}/activate")
async def activate_clients(
    *,
    client_id: int,
    session: Session = Depends(get_session),
):
    """
    Activate a client using its id as a key.

    Parameters
    ----------
    client_id : int
        ID of the client to be activated.
    session : Session
        SQL session that is to be used to activate a client.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    client_to_update.is_active = True
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)
    session.commit()
    session.refresh(client_to_update)
    return client_to_update


@router.put("/{client_id}/deactivate")
async def deactivate_clients(
    *,
    client_id: int,
    session: Session = Depends(get_session),
):
    """
    Deactivate a client using its id as a key.

    Parameters
    ----------
    client_id : int
        ID of the client to be deactivated.
    session : Session
        SQL session that is to be used to deactivate a client.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    client_to_update.is_active = False
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)

    session.commit()
    session.refresh(client_to_update)
    return client_to_update


@router.put("/{client_id}/deactivate-epics")
async def update_clients_and_epics(
    *,
    client_id: int,
    session: Session = Depends(get_session),
):
    """Deactivate a client and its epics"""
    """
    Deactivate a client and its epics using the client's ID as a key.

    Parameters
    ----------
    client_id : int
        ID of the client to deactivate.
    session : Session
        SQL session that is to be used to deactivate the client and its respective epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement1 = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement1).one()
    client_to_update.is_active = False
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)
    statement2 = select(Epic).where(Epic.client_id == client_id)
    epics_to_update = session.exec(statement2).all()
    for epic in epics_to_update:
        epic.is_active = False
        session.add(epic)
    session.commit()
    return True


@router.put("/{client_id}/new-name")
async def update_clients(
    *,
    client_id: int = None,
    new_client_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Update a client from a client_id.

    Parameters
    ----------
    client_id : int
        ID of the client to update.
    new_client_name : str
        New name of the client.
    session : Session
        SQL session that is to be used to update a client.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Client).where(Client.id == client_id)
    client_to_update = session.exec(statement).one()
    client_to_update.name = new_client_name
    client_to_update.updated_at = datetime.now()
    session.add(client_to_update)
    session.commit()
    session.refresh(client_to_update)
    return client_to_update
