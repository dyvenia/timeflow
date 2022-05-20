import requests

from ..config import base_url
from typing import List, Dict, TypedDict
from ..pages.utils import (
    year_month_list,
    hours_list,
    month_start_list,
    days_in_month_list,
)


class Select(TypedDict):
    value: str
    dispay_value: str


def username() -> List[Select]:
    api_username = f"{base_url}/api/users"
    response_username = requests.get(api_username)
    username_rows = [Select(value="", display_value="select username")]
    for item in response_username.json():
        d = Select(value=item["id"], display_value=item["username"])
        username_rows.append(d)
    return username_rows


def year_month_dict_list(label: str = "select month") -> List[Select]:
    ym_dict_list = [Select(value="", display_value=label)]
    for item in year_month_list:
        d = Select(value=item, display_value=item)
        ym_dict_list.append(d)
    return ym_dict_list


def hours() -> List[Dict]:
    hours = [Select(value="", display_value="select hour")]
    for item in hours_list:
        d = Select(value=item, display_value=item)
        hours.append(d)
    return hours


def months_start() -> List[Dict]:
    months = [Select(value="", display_value="select start date")]
    for item in month_start_list:
        d = Select(value=item, display_value=item)
        months.append(d)
    return months


def days_in_month(label: str = "select days") -> List[Dict]:
    days = [Select(value="", display_value=label)]
    for item in days_in_month_list:
        d = Select(value=item, display_value=item)
        days.append(d)
    return days
