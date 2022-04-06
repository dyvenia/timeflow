import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click
from components.input import (
    Input,
    Selector,
    SelectorDropdownList,
    SelectorDropdownKeyValue,
    Selector2,
)
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import Button

from data.common import (
    year_month_dict_list,
    username,
    hours,
    days_in_month,
)

from data.timelogs import Timelog, to_timelog
from data.epics import epics_names

from config import base_url


@component
def page():
    year_month, set_year_month = use_state("")
    day, set_day = use_state("")
    user, set_user = use_state("")
    epic_id, set_epic_id = use_state("")
    start_time, set_start_time = use_state("")
    end_time, set_end_time = use_state("")
    deleted_timelog, set_deleted_timelog = use_state("")
    submitted_user, set_submitted_user = use_state("")
    is_true, set_is_true = use_state(True)
    return Container(
        create_timelog_form(
            year_month,
            set_year_month,
            day,
            set_day,
            user,
            set_user,
            epic_id,
            set_epic_id,
            start_time,
            set_start_time,
            end_time,
            set_end_time,
            is_true,
            set_is_true,
        ),
        Column(
            Row(timelogs_table(is_true)),
        ),
        Row(delete_timelog_input(set_deleted_timelog)),
    )


@component
def create_timelog_form(
    year_month,
    set_year_month,
    day,
    set_day,
    user,
    set_user,
    epic_id,
    set_epic_id,
    start_time,
    set_start_time,
    end_time,
    set_end_time,
    is_true,
    set_is_true,
):
    """
    schema:
    {
    "user_id": 0,
    "start_time": "string",
    "end_time": "string",
    "epic_id": 0,
    "count_hours": 0,
    "count_days": 0,
    "month": 0,
    "year": 0
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        a = year_month
        year = a[:4]
        month = a[5:7]

        # year_int = int(year)
        # month_int = int(month)
        start_time_post = f"{year}-{month}-{day} {start_time}"
        end_time_post = f"{year}-{month}-{day} {end_time}"

        to_timelog(
            start_time=start_time_post,
            end_time=end_time_post,
            user_id=user,
            epic_id=epic_id,
            count_hours=0,
            count_days=0,
            month=month,
            year=year,
        )
        if is_true:
            set_is_true(False)
        else:
            set_is_true(True)

    selector_user = Selector2(set_value=set_user, data=username())

    selector_epic_id = Selector2(
        set_value=set_epic_id,
        data=epics_names(),
    )
    selector_year_month = Selector2(
        set_value=set_year_month,
        data=year_month_dict_list(),
    )
    selector_days = Selector2(
        set_value=set_day,
        data=days_in_month(),
    )

    selector_start_time = Selector2(
        set_value=set_start_time,
        data=hours(),
    )
    selector_end_time = Selector2(
        set_value=set_end_time,
        data=hours(),
    )
    is_disabled = True
    if (
        user != ""
        and epic_id != ""
        and year_month != ""
        and day != ""
        and start_time != ""
        and end_time != ""
    ):
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Submit")
    return Column(
        Row(
            selector_user,
            selector_epic_id,
            selector_year_month,
            selector_days,
            selector_start_time,
            selector_end_time,
        ),
        Row(btn),
    )


@component
def timelogs_table(is_true):
    api = f"{base_url}/api/timelogs"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "timelog id": item["id"],
            "start_time": item["start_time"],
            "end_time": item["end_time"],
            "count_hours": item["count_hours"],
            "count_days": item["count_days"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_timelog_input(set_deleted_timelog):
    timelog_to_delete, set_timelog_to_delete = use_state("")

    def handle_delete(event):
        api = f"{base_url}/api/timelogs/{timelog_to_delete}"
        response = requests.delete(api)
        set_deleted_timelog(timelog_to_delete)

    inp_username = Input(
        set_value=set_timelog_to_delete,
        label="timelog id to delete",
    )
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_delete,
        },
        "Submit",
    )
    return Column(Row(inp_username), Row(btn))
