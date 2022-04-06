from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel, or_
from ..models.epic_area import EpicArea
from ..models.epic import Epic
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/epic_areas", tags=["epic_area"])
session = Session(engine)


@router.post("/")
async def post_epic_area(
    *,
    epic_area: EpicArea,
    session: Session = Depends(get_session),
):
    """
    Post new epic area.

    Parameters
    ----------
    epic_area : EpicArea
        Epic area that is to be added to the database.
    session : Session
        SQL session that is to be used to add the epic area.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement1 = select(EpicArea).where(
        or_(EpicArea.name == epic_area.name, EpicArea.id == epic_area.id)
    )
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        session.add(epic_area)
        session.commit()
        session.refresh(epic_area)
        return epic_area


@router.get("/")
async def get_epic_area_list(session: Session = Depends(get_session)):
    """
    Get list of epic areas.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the epic areas.
        Defaults to creating a dependency on the running SQL model session.
    """

    statement = select(EpicArea)
    results = session.exec(statement).all()
    return results


@router.get("/active")
async def get_active_epic_area_list(session: Session = Depends(get_session)):
    """
    Get list of active epic areas along with the name of their respective epics.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the active epic areas.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            EpicArea.id,
            EpicArea.epic_id,
            EpicArea.name.label("epic_area_name"),
            Epic.id,
            Epic.name.label("epic_name"),
        )
        .join(Epic)
        .where(EpicArea.is_active == True)
    )
    results = session.exec(statement).all()
    return results


@router.get("/{epic_name}")
async def read_epic_areas(
    epic_area_name: str = None, session: Session = Depends(get_session)
):
    """
    Return a single epic area using a given epic area name as a key.

    Parameters
    ----------
    epic_area_name : str
        Name of the epic area to be returned.
    session : Session
        SQL session that is to be used to read the single epic area.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(EpicArea).where(EpicArea.name == epic_area_name)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no epic area named {epic_area_name}"""
        return msg


@router.get("/{epic_area_id}/epic-name")
async def get_epic_name_by_epic_area_id(
    epic_area_id: int, session: Session = Depends(get_session)
):
    """
    Return the epic name using the epic area id as a key.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the name of the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(EpicArea.id, Epic.id, Epic.name)
        .join(Epic)
        .where(EpicArea.id == epic_area_id)
        .where(Epic.is_active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{epic_area_name}/activate")
async def activate_epic_area(
    epic_area_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate an epic area using its name as a key.

    Parameters
    ----------
    epic_area_name : str
        Name of the epic area to be activated
    session : Session
        SQL session that is to be used to activate an epic area.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(EpicArea).where(EpicArea.name == epic_area_name)
    epic_area_to_activate = session.exec(statement).one()
    epic_area_to_activate.is_active = True
    epic_area_to_activate.updated_at = datetime.now()
    session.add(epic_area_to_activate)
    session.commit()
    session.refresh(epic_area_to_activate)
    return epic_area_to_activate


@router.put("/{epic_area_name}/deactivate")
async def deactivate_epic_area(
    epic_area_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate an epic area using its name as a key.

    Parameters
    ----------
    epic_area_name : str
        Name of the epic area to be deactivated
    session : Session
        SQL session that is to be used to deactivate an epic area.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(EpicArea).where(EpicArea.name == epic_area_name)
    epic_area_to_deactivate = session.exec(statement).one()
    epic_area_to_deactivate.is_active = False
    epic_area_to_deactivate.updated_at = datetime.now()
    session.add(epic_area_to_deactivate)
    session.commit()
    session.refresh(epic_area_to_deactivate)
    return epic_area_to_deactivate


@router.put("/")
async def update_epic_area(
    id: str = None,
    epic_id: str = None,
    name: str = None,
    is_active: bool = None,
    session: Session = Depends(get_session),
):
<<<<<<< HEAD
    """
    Update an epic area with new values.

    Parameters
    ----------
    id : str
        ID of epic area to be updated.
    epic_id : str
        Epic ID to be updated.
    epic_area_name : str
        Name of the epic area to be updated.
    is_active : bool
        Change the status of the epic area.
    session : Session
        SQL session that is to be used to deactivate an epic area.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(EpicArea).where(or_(EpicArea.name == name, EpicArea.id == id))
    
=======
    """Update an epic area"""
    statement = select(EpicArea).where(or_(EpicArea.name == name, EpicArea.id == id))
>>>>>>> main
    epic_area_to_update = session.exec(statement).one()
    epic_area_to_update.epic_id = epic_id
    epic_area_to_update.name = name
    epic_area_to_update.is_active = is_active
    session.add(epic_area_to_update)
    epic_area_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(epic_area_to_update)
    return epic_area_to_update
