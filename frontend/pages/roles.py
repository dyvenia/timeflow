import json
from idom import html, use_state, component, event
import requests
from sanic import response
from black import click
from datetime import datetime

from components.input import Input, SelectorDropdownKeyValue, Selector
from components.layout import Row, Column, Container
from components.table import SimpleTable
from components.controls import Button
from config import base_url

from data.roles import to_role, roles_active, role_update


@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    short_name, set_short_name = use_state("")
    submitted_short_name, set_submitted_short_name = use_state("")
    is_updated, set_is_updated = use_state(False)
    deact_role, set_deact_role = use_state("")
    activ_role, set_activ_role = use_state("")
    return Container(
        create_role_form(
            name,
            set_name,
            short_name,
            set_short_name,
            set_submitted_name,
        ),
        Column(
            Row(list_roles(submitted_name, submitted_short_name)),
        ),
        Row(update_role(is_updated, set_is_updated)),
        Row(deactivate_role(set_deact_role), activate_role(set_activ_role)),
    )


@component
def create_role_form(
    name,
    set_name,
    short_name,
    set_short_name,
    set_submitted_name,
):
    """
    Create a form that allows admin to add a new role.

    post endpoint: /api/roles
    schema: {
        "short_name": "string",
        "name": "string",
        "created_at": "2022-03-07T10:56:22.164Z",
        "updated_at": "2022-03-07T10:56:22.164Z",
        "is_active": true
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given role when given event is triggered."""
        to_role(
            short_name=short_name,
            name=name,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
            is_active=True,
        )
        set_submitted_name(name)

    inp_name = Input(set_value=set_name, label="name of the role")
    inp_short_name = Input(set_value=set_short_name, label="short name of the role")

    is_disabled = True
    if name != "" and short_name != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(inp_name, inp_short_name),
        Row(btn),
    )


@component
def list_roles(submitted_name, submitted_short_name):
    """
    Return rows consisting of each role short name along with its full name.

    Obtain a json response from a get request to the client endpoint.
    Return an HTML div that contains the rows in a table.
    """
    rows = roles_active()

    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def update_role(is_updated, set_is_updated):
    """Updates name or/and short_name of a role by required id"""
    role_id, set_role_id = use_state("")
    name_to_update, set_name_to_update = use_state("")
    short_name_to_update, set_short_name_to_update = use_state("")

    @event(prevent_default=True)
    async def handle_update(event):
        """
        Create a form that allows admin to update a new role

        put endpoint: /api/roles
        """
        role_update(
            id=role_id, new_name=name_to_update, new_short_name=short_name_to_update
        )
        if is_updated:
            set_is_updated(False)
        elif is_updated == False:
            set_is_updated(True)

    inp_role_id = Input(set_role_id, label="role id to update")
    inp_name_update = Input(set_name_to_update, label="full name to update")
    inp_short_name_update = Input(
        set_short_name_to_update, label="short name to update"
    )
    is_disabled = True
    if role_id != "" and (name_to_update != "" or short_name_to_update != ""):
        is_disabled = False
    btn_update = Button(is_disabled, handle_submit=handle_update, label="Update")
    return Column(
        Row(inp_role_id, inp_name_update, inp_short_name_update), Row(btn_update)
    )


@component
def deactivate_role(set_deact_role):
    """Deactivate a role without deleting it."""
    role_to_deact, set_role_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given role's is_active column to False."""
        api = f"{base_url}/api/roles/{role_to_deact}/deactivate"
        response = requests.put(api)
        set_deact_role(role_to_deact)
        return True

    inp_deact_role = Input(
        set_value=set_role_to_deact, label="role id to be deactivated"
    )
    is_disabled = True
    if role_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(inp_deact_role), Row(btn))


@component
def activate_role(set_activ_role):
    """Activate an inactivated role"""
    role_to_activ, set_role_to_activ = use_state("")

    def handle_activation(event):
        """Set the given role's is_active column to True."""
        api = f"{base_url}/api/roles/{role_to_activ}/activate"
        response = requests.put(api)
        set_activ_role(role_to_activ)
        return True

    inp_activ_role = Input(set_value=set_role_to_activ, label="role id to be activated")
    is_disabled = True
    if role_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(inp_activ_role), Row(btn))
