import json
import requests

from ..config import base_url
from .common import Select
from datetime import datetime
from typing import List


def epic_area_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/epic_areas/{name_to_activ}/activate"
    response = requests.put(api)
    return True


def epic_area_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/epic_areas/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True


def get_active_epic_area_rows():
    """Get all active epic areas and store them in a list."""
    api = f"{base_url}/api/epic_areas/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Epic": item["epic_name"],
            "Epic Area": item["epic_area_name"],
            "ID": item["id"],
        }
        rows.append(d)
    return rows


def epic_areas_names() -> List[Select]:
    """Gets list of active epics by name and id
    Returns a list of dictionaries
    """
    api_epic_area_name = f"{base_url}/api/epic_areas/active"
    response_epic_name = requests.get(api_epic_area_name)
    epic_area_name_rows = [Select(value="", display_value="select epic area")]
    for item in response_epic_name.json():
        d = Select(value=item["id"], display_value=item["epic_area_name"])
        epic_area_name_rows.append(d)
    return epic_area_name_rows


def epic_areas_names_by_epic_id(epic_id) -> List[Select]:
    api = f"{base_url}/api/epic_areas"
    if epic_id == "":
        epic_id = 0
    params = {"epic_id": epic_id}
    response = requests.get(api, params=params)
    rows = [Select(value="", display_value="select epic area")]
    for item in response.json():
        d = Select(value=item["id"], display_value=item["epic_area_name"])
        rows.append(d)
    return rows


def post_epic_area(epic_id: int, name: str):
    data = {
        "epic_id": epic_id,
        "name": name,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    response = requests.post(
        f"{base_url}/api/epic_areas",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True
