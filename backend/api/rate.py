from fastapi import APIRouter, Depends
from ..utils import engine, get_session, far_date, date_str_to_date
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.rate import Rate
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/rates", tags=["rate"])
session = Session(engine)


@router.post("/")
async def rate(
    rate: Rate,
    session: Session = Depends(get_session),
):
    """Post new rate"""
    """
    Post new rate.

    Parameters
    ----------
    rate : Rate
        Rate that is to be added to the database.
    session : Session
        SQL session that is to be used to add the rate.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement1 = (
        select(Rate)
        .where(Rate.user_id == rate.user_id)
        .where(Rate.client_id == rate.client_id)
        .where(Rate.valid_from >= rate.valid_from)
    )

    one_day_delta = timedelta(days=1)
    close_date = rate.valid_from - one_day_delta
    statement2 = (
        select(Rate)
        .where(Rate.user_id == rate.user_id)
        .where(Rate.client_id == rate.client_id)
        .where(Rate.valid_to == far_date)
    )
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        try:
            rate_to_close = session.exec(statement2).one()
            rate_to_close.valid_to = close_date
            rate_to_close.updated_at = datetime.now()
            session.add(rate_to_close)
            session.add(rate)
            session.commit()
            return True
        except NoResultFound:
            session.add(rate)
            session.commit()
            return True


@router.get("/")
async def read_rates(
    session: Session = Depends(get_session),
):
    """
    Get all rates.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the rates.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Rate)
    result = session.exec(statement).all()
    return result


@router.get("/users/{user_id}/clients/{client_id}/")
async def rates_by_user_client(
    user_id: int,
    client_id: int,
    session: Session = Depends(get_session),
):
    """
    Get list of rates using given user ids and clients ids as keys.

    Parameters
    ----------
    user_id : int
        User id that is used to get list of rates.
    client_id : int
        Client id that is used to get the list of rates.
    session : Session
        SQL session that is to be used to read a certain rates.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Rate).where(Rate.user_id == user_id).where(Rate.client_id == client_id)
    )
    result = session.exec(statement).all()
    return result


@router.get("/users/{user_id}/clients/{client_id}/months/")
async def rates_by_user_client_date(
    user_id: int,
    client_id: int,
    date: str,
    session: Session = Depends(get_session),
):
    """
    Get rates from a certain date using a user id and client id as keys.

    Parameters
    ----------
    user_id : int
        User id of user who's rate is in question.
    client_id : int
        Client id of client that's contracting the user.
    date : str
        Date from which the rates are needed.
    session : Session
        SQL session that is to be used to get the rates.
        Defaults to creating a dependency on the running SQL model session.
    """
    month_start_date = date_str_to_date(date)
    statement = (
        select(Rate)
        .where(Rate.user_id == user_id)
        .where(Rate.client_id == client_id)
        .where(Rate.valid_from <= month_start_date)
        .where(Rate.valid_to > month_start_date)
    )
    result = session.exec(statement).all()
    return result


@router.put("/{rate_id}/activate")
async def activate_rate(
    rate_id: str,
    session: Session = Depends(get_session),
):
    """
    Activate a rate using its id as a key.

    Parameters
    ----------
    rate_id : str
        ID of the rate to be activated.
    session : Session
        SQL session that is to be used to activate a rate.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Rate).where(Rate.id == rate_id)
    rate_to_activate = session.exec(statement).one()
    rate_to_activate.is_active = True
    rate_to_activate.updated_at = datetime.now()
    session.add(rate_to_activate)
    session.commit()
    session.refresh(rate_to_activate)
    return rate_to_activate


@router.put("/{rate_id}/deactivate")
async def deactivate_rate_id(
    rate_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate a rate using its id as a key.

    Parameters
    ----------
    rate_id : str
        ID of the rate to be deactivated.
    session : Session
        SQL session that is to be used to deactivate a rate.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Rate).where(Rate.id == rate_id)
    rate_id_to_deactivate = session.exec(statement).one()
    rate_id_to_deactivate.is_active = False
    rate_id_to_deactivate.updated_at = datetime.now()
    session.add(rate_id_to_deactivate)
    session.commit()
    session.refresh(rate_id_to_deactivate)
    return rate_id_to_deactivate


@router.put("/")
async def update_rates(
    rate_id: int = None,
    new_amount: str = None,
    session: Session = Depends(get_session),
):
    """
    Update a rate with new values.

    Parameters
    ----------
    user_id : str
        ID of user to be updated.
    client_id : str
        ID of client to be updated.
    new_amount : str
        Amount to be updated.
    session : Session
        SQL session that is to be used to update the rate.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Rate).where(Rate.id == rate_id)
    rate_to_update = session.exec(statement).one()
    rate_to_update.amount = new_amount
    session.add(rate_to_update)
    session.commit()
    session.refresh(rate_to_update)
    return True
