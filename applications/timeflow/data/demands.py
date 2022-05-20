import requests
import json
from typing import List, TypedDict, Dict
from ..config import base_url
from .common import Select
from ..pages.utils import days_list
from datetime import datetime


class Demand(TypedDict):
    team_id: int
    epic_id: int
    year: int
    month: int
    days: int
    created_at: datetime
    updated_at: datetime
    is_locked: bool


def to_demand(team_id: int, epic_id: int, year_month: str, days: int) -> bool:
    data = Demand(
        team_id=team_id,
        epic_id=epic_id,
        year=int(year_month[:4]),
        month=int(year_month[5:7]),
        days=days,
        created_at=str(datetime.now()),
        updated_at=str(datetime.now()),
        is_locked=False,
    )

    response = requests.post(
        f"{base_url}/api/demands",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def demands_all():
    api = f"{base_url}/api/demands/"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "demand id": item["demand_id"],
            "team": item["team_short_name"],
            "epic": item["epic_name"],
            "year": item["year"],
            "month": item["month"],
            "demand days": item["days"],
        }
        rows.append(d)
    return rows


def demands_by_team(team_id) -> List[Dict]:
    api = f"{base_url}/api/demands/teams/{team_id}/"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "demand id": item["demand_id"],
            "team": item["team_short_name"],
            "epic": item["epic_name"],
            "year": item["year"],
            "month": item["month"],
            "demand days": item["days"],
        }
        rows.append(d)
    return rows


def demands_by_team_epic(team_id, epic_id) -> List[Dict]:
    api = f"{base_url}/api/demands/teams/{team_id}/epics/{epic_id}/"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "demand id": item["demand_id"],
            "team": item["team_short_name"],
            "epic": item["epic_name"],
            "year": item["year"],
            "month": item["month"],
            "demand days": item["days"],
        }
        rows.append(d)
    return rows


def demands_by_epic(epic_id) -> List[Dict]:
    api = f"{base_url}/api/demands/epics/{epic_id}/"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "demand id": item["demand_id"],
            "team": item["team_short_name"],
            "epic": item["epic_name"],
            "year": item["year"],
            "month": item["month"],
            "demand days": item["days"],
        }
        rows.append(d)
    return rows


def demands_by_team_epic_year_month(team_id, epic_id, year_month) -> List[Dict]:
    if team_id != "" and epic_id != "" and year_month != "":
        api = f"{base_url}/api/demands/"
        params = {
            "team_id": team_id,
            "epic_id": epic_id,
            "year": int(year_month[:4]),
            "month": int(year_month[5:7]),
        }

        response = requests.get(api, params=params)
        rows = []
        for item in response.json():
            d = {
                "demand id": item["demand_id"],
                "team": item["team_short_name"],
                "epic": item["epic_short_name"],
                "year": item["year"],
                "month": item["month"],
                "demand days": item["days"],
            }
            rows.append(d)
        return rows


def demand_days() -> List[Dict]:
    days = [Select(value="", display_value="select demand days")]
    for item in days_list(days=20):
        d = Select(value=item, display_value=item)
        days.append(d)
    return days


def demand_deletion(demand_to_delete) -> bool:
    api = f"{base_url}/api/demands/?demand_id={demand_to_delete}"
    response = requests.delete(api)
    return True
