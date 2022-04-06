import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
import requests
from sanic import Sanic, response
from datetime import datetime

from pages.utils import switch_state
from components.input import Input, Selector2
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import Button
from config import base_url

from data.users import (
    to_user,
    users_active,
    update_user,
    users_names,
    activate_user,
    deactivate_user,
)
from data.roles import roles_id_name
from data.teams import teams_id_name
from data.common import year_month_dict_list, days_in_month


@component
def page():
    short_name, set_short_name = use_state("")
    first_name, set_first_name = use_state("")
    last_name, set_last_name = use_state("")
    email, set_email = use_state("")
    role_id, set_role_id = use_state("")
    team_id, set_team_id = use_state(None)
    # Used for refreshing page on event
    is_event, set_is_event = use_state(True)
    return Container(
        Row(
            create_user_form(
                short_name,
                set_short_name,
                first_name,
                set_first_name,
                last_name,
                set_last_name,
                email,
                set_email,
                role_id,
                set_role_id,
                team_id,
                set_team_id,
                is_event,
                set_is_event,
            )
        ),
        Column(list_users(is_event)),
        Column(
            Row(update_users(is_event, set_is_event)),
        ),
        Row(
            Column(deactivate_users(is_event, set_is_event)),
            Column(activate_users(is_event, set_is_event)),
        ),
    )


@component
def create_user_form(
    short_name,
    set_short_name,
    first_name,
    set_first_name,
    last_name,
    set_last_name,
    email,
    set_email,
    role_id,
    set_role_id,
    team_id,
    set_team_id,
    is_event,
    set_is_event,
):
    """
        endpoint: /api/users
        schema: {
      "short_name": "string",
      "first_name": "string",
      "last_name": "string",
      "email": "string",
      "role_id": 0,
      "team_id": 0,
      "start_date": "2022-03-10",
      "created_at": "2022-03-10T13:11:49.625Z",
      "updated_at": "2022-03-10T13:11:49.625Z",
      "is_active": true
    }"""
    # Initializes day state, should be in parent(?), here due to a bug
    day, set_day = use_state("")
    year_month, set_year_month = use_state("")

    @event(prevent_default=True)
    async def handle_submit(event):
        print("post select team is", team_id)
        # Bypass of a bug, selector not able to set a value=None
        if team_id is "":
            set_team_id(None)
        to_user(
            short_name=short_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role_id=role_id,
            team_id=team_id,
            year_month=year_month,
            day=day,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        # switches state triggering page refresh
        switch_state(is_event, set_is_event)

    inp_short_name = Input(set_value=set_short_name, label="short name")
    inp_first_name = Input(set_value=set_first_name, label="first name")
    inp_last_name = Input(set_value=set_last_name, label="last name")
    inp_email = Input(set_value=set_email, label="email")
    selector_role = Selector2(set_role_id, roles_id_name())
    selector_team = Selector2(set_team_id, teams_id_name(no_team=True))
    selector_start_month = Selector2(
        set_year_month, year_month_dict_list(label="select start month")
    )
    selector_start_day = Selector2(set_day, days_in_month(label="select start day"))

    # is_disabled = True
    # if username != "" and name != "" and surname != "" and email != "":
    is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(inp_short_name, inp_first_name, inp_last_name, inp_email),
        Row(
            selector_role,
            selector_team,
            selector_start_month,
            selector_start_day,
        ),
        Row(btn),
    )


@component
def list_users(is_event):
    """Calls a list of active users"""
    rows = users_active()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def update_users(is_event, set_is_event):
    new_team_id, set_new_team_id = use_state("")
    update_user_id, set_update_user_id = use_state("")

    @event(prevent_default=True)
    def handle_update(event):
        update_user(user_id=update_user_id, new_team_id=new_team_id)
        # Changes state triggering refresh on update event
        switch_state(value=is_event, set_value=set_is_event)

    selector_user = Selector2(
        set_update_user_id, data=users_names(label="select user to update")
    )
    selector_team = Selector2(
        set_new_team_id, data=teams_id_name(label="select new team")
    )
    is_disabled = False
    btn = Button(is_disabled, handle_update, label="Update")
    return Column(Row(selector_user, selector_team), Row(btn))


@component
def deactivate_users(is_event, set_is_event):
    """Deactivate an user without deleting it."""
    deactiv_user_id, set_deactiv_user_id = use_state("")
    print("deactiv iser id is", deactiv_user_id)

    def handle_deactivation(event):
        """Set the given user's is_active column to False."""
        deactivate_user(deactiv_user_id)
        switch_state(value=is_event, set_value=set_is_event)

        return True

    selector_user = Selector2(
        set_deactiv_user_id, data=users_names(label="select user to deactivate")
    )
    is_disabled = True
    if deactiv_user_id != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(selector_user), Row(btn))


@component
def activate_users(is_event, set_is_event):
    """Activate an user without deleting it."""
    activ_user_id, set_activ_user_id = use_state("")
    print("activ iser id is", activ_user_id)

    def handle_activation(event):
        """Set the given user's is_active column to False."""
        activate_user(activ_user_id)
        switch_state(value=is_event, set_value=set_is_event)

        return True

    selector_user = Selector2(
        set_activ_user_id, data=users_names(label="select user to activate")
    )
    is_disabled = True
    if activ_user_id != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(selector_user), Row(btn))
