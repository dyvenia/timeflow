import requests
import json
from typing import TypedDict, List
from datetime import date, datetime
from ..config import base_url
from .common import Select


class User(TypedDict):
    username: str
    first_name: str
    last_name: str
    email: str
    role_id: int
    team_id: int
    start_date: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


def to_user(
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    role_id: str,
    year_month: str,
    day: int,
    created_at: datetime,
    updated_at: datetime,
    team_id: str,
):
    ym = year_month
    year = ym[:4]
    month = ym[5:7]
    start_date = year + "-" + month + "-" + day

    data = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role_id=role_id,
        team_id=team_id,
        start_date=start_date,
        created_at=str(created_at),
        updated_at=str(updated_at),
        is_active=True,
    )
    response = requests.post(
        f"{base_url}/api/users",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )


def users_active():
    api = f"{base_url}/api/users/"
    params = {"is_active": True}
    response = requests.get(api, params=params)
    rows = []
    for item in response.json():
        d = {
            "username": item["username"],
            "first name": item["first_name"],
            "last name": item["last_name"],
            "role": item["role_short_name"],
            "main team": item["main_team"],
            "start date": item["start_date"],
        }
        rows.append(d)
    return rows


def update_user(
    user_id: int,
    new_team_id: int = None,
    new_role_id: int = None,
    new_first_name: str = None,
    new_last_name: str = None,
    new_start_date: date = None,
):
    api = f"{base_url}/api/users/{user_id}/"
    func_params = {
        "new_team_id": new_team_id,
        "new_role_id": new_role_id,
        "new_first_name": new_first_name,
        "new_last_name": new_last_name,
        "new_start_date": new_start_date,
    }

    api_params = func_params.copy()

    # Pop all keys with value of None
    for param in func_params.keys():
        if api_params[param] == None:
            api_params.pop(param)

    response = requests.put(api, params=api_params)
    return True


def activate_user(user_id: int):
    api = f"{base_url}/api/users/{user_id}/"
    params = {"is_active": True}
    response = requests.put(api, params=params)
    return True


def deactivate_user(user_id: int):
    api = f"{base_url}/api/users/{user_id}/"
    params = {"is_active": False}
    response = requests.put(api, params=params)
    return True


def users_names(label="select user") -> List[Select]:
    # Connect to users list endpoint
    api_username = f"{base_url}/api/users"
    params = {"is_active": True}
    response_username = requests.get(api_username, params=params)
    username_rows = [Select(value="", display_value=label)]
    for item in response_username.json():
        d = Select(value=item["id"], display_value=item["username"])
        username_rows.append(d)
    return username_rows


def users_names_inactive(label="select user") -> List[Select]:
    # Connect to users list endpoint
    api_username = f"{base_url}/api/users"
    params = {"is_active": False}
    response_username = requests.get(api_username, params=params)
    username_rows = [Select(value="", display_value=label)]
    for item in response_username.json():
        d = Select(value=item["id"], display_value=item["username"])
        username_rows.append(d)
    return username_rows


def get_user_id_by_username(username):
    """
    Get user id by username.
    """
    api = f"{base_url}/api/users"
    params = {"username": username}
    response = requests.get(api, params=params).json()
    user_id = response[0]["id"]
    return user_id
