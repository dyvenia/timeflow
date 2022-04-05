from idom import html, use_state, component, event
from sanic import response
from black import click

from components.controls import activation_button, deactivation_button, submit_button
from components.input import Input, Selector2
from components.layout import Row, Column, Container
from components.table import SimpleTable

from data.epics import epics_names
from data.epic_areas import (
    epic_area_activation,
    epic_area_deactivation,
    get_active_epic_area_rows,
    post_epic_area,
)


@component
def page():
    epic_id, set_epic_id = use_state("")
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")
    print(name)

    return Container(
        create_epic_area_form(
            epic_id,
            set_epic_id,
            name,
            set_name,
            set_submitted_name,
        ),
        Column(
            Row(list_epic_areas(submitted_name)),
        ),
        Row(deactivate_epic_area(set_deact_name)),
        Row(activate_epic_area(set_activ_name)),
    )


@component
def create_epic_area_form(
    epic_id,
    set_epic_id,
    name,
    set_name,
    set_submitted_name,
):
    """
    Create a form that allows admin to add a new epic area.

    post endpoint: /api/epic_areas
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
        """Call a post request for the given epic area when given event is triggered."""
        post_epic_area(epic_id, name)

        # Change the states
        set_submitted_name(name)

    # Create dropdown of active epics which can then be selected
    selector_epic_id = Selector2(
        set_value=set_epic_id,
        data=epics_names(),
    )

    # Create input field for the name of the epic area
    inp_name = Input(set_value=set_name, label="name")

    # Create submit button
    btn = submit_button(handle_submit, epic_id, name)

    return Column(
        Row(
            selector_epic_id,
            inp_name,
        ),
        Row(btn),
    )


@component
def list_epic_areas(submitted_name):
    """
    Return rows consisting of each epic area along with its epic.

    Obtain a json response from a get request to the active epic areas endpoint.
    Store in rows the names of the epic and epic area, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    rows = get_active_epic_area_rows()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_epic_area(set_deact_name):
    """Deactivate an epic area without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given epic area's active column to False."""
        epic_area_deactivation(name_to_deact)
        set_deact_name(name_to_deact)

    # Create input field for name of epic area to be deactivated
    inp_deact_name = Input(
        set_value=set_name_to_deact, label="epic area to be deactivated"
    )

    # Create the deactivation button
    btn = deactivation_button(name_to_deact, handle_deactivation)

    return Column(Row(inp_deact_name), Row(btn))


@component
def activate_epic_area(set_activ_name):
    """Activate an epic area."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic area's active column to True."""
        epic_area_activation(name_to_activ)
        set_activ_name(name_to_activ)

    # Create input field for name of epic area to be activated
    inp_activ_name = Input(
        set_value=set_name_to_activ, label="epic area to be activated"
    )

    # Create the activation button
    btn = activation_button(name_to_activ, handle_activation)

    return Column(Row(inp_activ_name), Row(btn))
