from idom import html, use_state, component, event
from idom.backend import fastapi
import requests
from datetime import datetime
from applications.timeflow.config import get_user, fetch_username
from uiflow.components.input import (
    Input,
    Selector2,
    display_value,
)
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable
from uiflow.components.controls import Button
from uiflow.components.heading import H3

from ..data.common import (
    year_month_dict_list,
    hours,
    username,
    days_in_month,
)

from ..data.epics import epics_names
from ..data.epic_areas import epic_areas_names_by_epic_id
from ..data.timelogs import to_timelog, timelog_by_user_id
from ..data.users import get_user_id_by_username

from ..config import base_url
from uiflow.components.controls import TableActions
from uiflow.components.yourTimelog import YourTimelog
from .utils import switch_state


@component
def page(app_role: str, github_username: str):
    """
    Timelogs page.

    Parameters
    ----------
    app_role: str
        Role of user within the app.
    github_username: str
        GitHub username of user.
    """
    year_month, set_year_month = use_state("")
    day, set_day = use_state("")
    user_id, set_user_id = use_state("")
    epic_id, set_epic_id = use_state("")
    epic_area_id, set_epic_area_id = use_state("")
    start_time, set_start_time = use_state("")
    end_time, set_end_time = use_state("")
    is_event, set_is_event = use_state(True)
    deleted_timelog, set_deleted_timelog = use_state("")
    return html.div(
        {"class": "w-full"},
        create_timelog_form(
            year_month,
            set_year_month,
            day,
            set_day,
            user_id,
            set_user_id,
            epic_id,
            set_epic_id,
            epic_area_id,
            set_epic_area_id,
            start_time,
            set_start_time,
            end_time,
            set_end_time,
            is_event,
            set_is_event,
            app_role,
            github_username,
        ),
        Container(
            Column(
                Row(timelogs_table(user_id, is_event, app_role, github_username)),
            ),
            delete_timelog_input(set_deleted_timelog),
        ),
    )


@component
def create_timelog_form(
    year_month,
    set_year_month,
    day,
    set_day,
    user_id,
    set_user_id,
    epic_id,
    set_epic_id,
    epic_area_id,
    set_epic_area_id,
    start_time,
    set_start_time,
    end_time,
    set_end_time,
    is_event,
    set_is_event,
    app_role,
    github_username,
):
    """
    schema:
    {
    "user_id": 0,
    "start_time": "string",
    "end_time": "string",
    "epic_id": 0,
    "epic_area_id": 0,
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

        start_time_post = f"{year}-{month}-{day} {start_time}"
        end_time_post = f"{year}-{month}-{day} {end_time}"

        to_timelog(
            start_time=start_time_post,
            end_time=end_time_post,
            user_id=user_id,
            epic_id=epic_id,
            epic_area_id=epic_area_id,
            month=month,
            year=year,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
        )
        switch_state(is_event, set_is_event)
        set_epic_id("")

    admin = True if app_role == "admin" or app_role == None else False

    if admin == True:
        selector_user = Selector2(set_value=set_user_id, data=username())
    elif admin == False:
        user_id = get_user_id_by_username(github_username)
        selector_user = display_value(user_id, github_username)

    selector_epic_id = Selector2(
        set_value=set_epic_id,
        set_sel_value=set_epic_area_id,
        sel_value="",
        data=epics_names(is_active=True),
    )

    selector_epic_area_id = Selector2(
        set_value=set_epic_area_id,
        data=epic_areas_names_by_epic_id(epic_id),
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
        admin == True
        and user_id != ""
        and epic_id != ""
        and epic_area_id != (0 or "")
        and year_month != ""
        and day != ""
        and start_time != ""
        and end_time != ""
    ):
        is_disabled = False
    elif (
        admin == False
        and epic_id != ""
        and epic_id != ""
        and epic_area_id != (0 or "")
        and year_month != ""
        and day != ""
        and start_time != ""
        and end_time != ""
    ):
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")
    return html.section(
        {"class": "bg-filter-block-bg py-4 text-sm"},
        Container(
            H3("Your current project"),
            html.div(
                {
                    "class": "flex flex-wrap justify-between items-center md:justify-start 2xl:justify-between"
                },
                selector_user,
                selector_epic_id,
                selector_epic_area_id,
                selector_year_month,
                selector_days,
                selector_start_time,
                selector_end_time,
                btn,
            ),
        ),
    )


@component
def timelogs_table(user_id, is_event, app_role, github_username):
    api = f"{base_url}/api/timelogs"
    response = requests.get(api)
    admin = True if app_role == "admin" or app_role == None else False

    if admin == False:
        user_id = get_user_id_by_username(github_username)

    if user_id != "":
        rows = timelog_by_user_id(user_id)
    else:
        rows = []
        for item in response.json():
            d = {
                "timelog id": item["id"],
                "username": item["username"],
                "epic name": item["epic_name"],
                "epic area name": item["epic_area_name"],
                "start time": (item["start_time"]).replace("T", " "),
                "end time": (item["end_time"]).replace("T", " "),
                "count hours": item["count_hours"],
                "count days": item["count_days"],
            }
            rows.append(d)
    return html.div(
        {"class": "w-full"}, YourTimelog(), TableActions(), SimpleTable(rows=rows)
    )


@component
def delete_timelog_input(set_deleted_timelog):
    timelog_to_delete, set_timelog_to_delete = use_state("")

    def handle_delete(event):
        api = f"{base_url}/api/timelogs/{timelog_to_delete}"
        response = requests.delete(api)
        set_deleted_timelog(timelog_to_delete)

    inp_username = Input(
        set_value=set_timelog_to_delete, label="timelog id to delete", width="full"
    )

    return Column(Row(inp_username), Button(False, handle_delete, "Submit"))
