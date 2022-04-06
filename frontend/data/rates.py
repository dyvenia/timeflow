import requests
import json
from config import base_url
from typing import List, Dict, TypedDict
from datetime import datetime


class Rate(TypedDict):
    user_id: int
    client_id: int
    valid_from: str
    valid_to: str
    amount: float
    created_at: datetime
    updated_at: datetime
    is_active: bool


def rate_active_by_user_client(user_id: int, client_id: int) -> List[Dict]:
    api = f"{base_url}/api/rates/users/{user_id}/clients/{client_id}/"
    print(api)
    response = requests.get(api)
    print(response)
    rows = []
    for item in response.json():
        d = {
            "id": item["id"],
            "valid from": item["valid_from"],
            "valid_to": item["valid_to"],
            "amount": item["amount"],
        }
        rows.append(d)
    return rows


def rates_by_user_client_date(user_id: int, client_id: int, date: str) -> List[Dict]:
    if user_id != "" and client_id != "" and date != "":
        api = f"{base_url}/api/rates/users/{user_id}/clients/{client_id}/months/?date={date}"
        response = requests.get(api)
        rows = []
        for item in response.json():
            d = {
                "valid from": item["valid_from"],
                "valid_to": item["valid_to"],
                "amount": item["amount"],
            }
            rows.append(d)
        return rows


def rate_update(rate_id: int, new_amount: float):
    api = f"{base_url}/api/rates/?rate_id={rate_id}&new_amount={new_amount}"
    response = requests.put(api)
    return True


def to_rate(
    user_id: int,
    client_id: int,
    valid_from: str,
    valid_to: str,
    amount: float,
    created_at: str,
    updated_at: str,
    is_active: bool,
) -> bool:
    data = Rate(
        user_id=user_id,
        client_id=client_id,
        valid_from=valid_from,
        valid_to=valid_to,
        amount=amount,
        created_at=created_at,
        updated_at=updated_at,
        is_active=True,
    )
    response = requests.post(
        f"{base_url}/api/rates",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True
