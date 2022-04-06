from idom import html, use_state, component, event
from sanic import response
from black import click

from components.controls import activation_button, deactivation_button, submit_button
from components.input import Input, Selector2
from components.layout import Row, Column, Container
from components.table import SimpleTable

from data.teams import (
    team_deactivation,
    team_activation,
    post_team,
    get_active_team_rows,
)
from data.users import users_names


@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    short_name, set_short_name = use_state("")
    submitted_short_name, set_submitted_short_name = use_state("")
    lead_user_id, set_lead_user_id = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return Container(
        create_team_form(
            name,
            set_name,
            short_name,
            set_short_name,
            lead_user_id,
            set_lead_user_id,
            set_submitted_name,
            set_submitted_short_name,
        ),
        Column(
            Row(list_teams(submitted_name, submitted_short_name)),
        ),
        Row(deactivate_team(set_deact_name)),
        Row(activate_team(set_activ_name)),
    )


@component
def create_team_form(
    name,
    set_name,
    short_name,
    set_short_name,
    lead_user_id,
    set_lead_user_id,
    set_submitted_name,
    set_submitted_short_name,
):
    """
    Create a form that allows admin to add a new team.

    post endpoint: /api/teams
    schema: {
        "epic_id": "int",
        "name": "string,
        "is_active": True
        "created_at": "2022-02-17T15:31:39.103Z",
        "updated_at": "2022-02-17T15:31:39.103Z"
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given team when given event is triggered."""
        post_team(name, short_name, lead_user_id)

        # Change the states
        set_submitted_name(name)
        set_submitted_short_name(short_name)

    # Create input field for the name of the team
    inp_name = Input(set_value=set_name, label="name of the team")

    # Create input field for the short name of the team
    inp_short_name = Input(set_value=set_short_name, label="short name of the team")

    # Create a dropdown of users which can then be selected
    selector_lead_user_id = Selector2(
        set_value=set_lead_user_id,
        data=users_names(label="select user lead"),
    )

    # Create submit button
    btn = submit_button(handle_submit, name, short_name, lead_user_id)

    return Column(
        Row(
            inp_name,
            inp_short_name,
            selector_lead_user_id,
        ),
        Row(btn),
    )


@component
def list_teams(submitted_name, submitted_short_name):
    """
    Return rows consisting of each team along with its leader (user).

    Obtain a json response from a get request to the users endpoint.
    Store in rows the names of the user and team, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    rows = get_active_team_rows()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_team(set_deact_name):
    """Deactivate a team without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given team's active column to False."""
        team_deactivation(name_to_deact)
        set_deact_name(name_to_deact)

    # Create input field for name of team to be deactivated
    inp_deact_name = Input(set_value=set_name_to_deact, label="team to be deactivated")

    # Create the deactivation button
    btn = deactivation_button(name_to_deact, handle_deactivation)

    return Column(Row(inp_deact_name), Row(btn))


@component
def activate_team(set_activ_name):
    """Activate a team."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic are'a active column to True."""
        team_activation(name_to_activ)
        set_activ_name(name_to_activ)

    # Create input field for name of team to be activated
    inp_activ_name = Input(set_value=set_name_to_activ, label="team to be activated")

    # Create the activation button
    btn = activation_button(name_to_activ, handle_activation)

    return Column(Row(inp_activ_name), Row(btn))
