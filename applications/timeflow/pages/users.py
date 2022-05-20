from idom import html, use_state, component, event

from .utils import switch_state
from uiflow.components.input import Input, Selector2
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable
from uiflow.components.controls import Button

from ..data.users import (
    users_active,
    update_user,
    users_names,
    activate_user,
    deactivate_user,
    users_names_inactive,
)
from ..data.roles import roles_id_name
from ..data.teams import teams_id_name
from ..data.common import year_month_dict_list, days_in_month


@component
def page():
    # Used for refreshing page on event
    is_event, set_is_event = use_state(True)
    return html.div(
        {"class": "w-full"},
        Container(
            Column(
                Row(update_users(is_event, set_is_event)),
            ),
            Column(list_users(is_event)),
            Row(
                Column(deactivate_users(is_event, set_is_event)),
                Column(activate_users(is_event, set_is_event)),
            ),
        ),
    )


@component
def list_users(is_event):
    """Calls a list of active users"""
    rows = users_active()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def update_users(is_event, set_is_event):
    new_first_name, set_new_first_name = use_state("")
    new_last_name, set_new_last_name = use_state("")
    new_role_id, set_new_role_id = use_state("")
    new_team_id, set_new_team_id = use_state("")
    update_user_id, set_update_user_id = use_state("")

    # Initializes day state, should be in parent(?), here due to a bug
    day, set_day = use_state("")
    year_month, set_year_month = use_state("")

    ym = year_month
    year = ym[:4]
    month = ym[5:7]
    new_start_date = year + "-" + month + "-" + day

    @event(prevent_default=True)
    def handle_update(event):
        update_user(
            user_id=update_user_id,
            new_team_id=new_team_id,
            new_role_id=new_role_id,
            new_first_name=new_first_name,
            new_last_name=new_last_name,
            new_start_date=new_start_date,
        )
        # Changes state triggering refresh on update event
        switch_state(value=is_event, set_value=set_is_event)

    inp_first_name = Input(
        set_value=set_new_first_name,
        label="first name",
        width="[48%]",
        md_width="[48%]",
    )
    inp_last_name = Input(
        set_value=set_new_last_name, label="last name", width="[48%]", md_width="[48%]"
    )

    selector_user = Selector2(
        set_update_user_id,
        data=users_names(label="select user to update"),
        width="48%",
        md_width="48%",
    )
    selector_team = Selector2(
        set_new_team_id,
        data=teams_id_name(label="select new team"),
        width="48%",
        md_width="48%",
    )
    selector_role = Selector2(
        set_new_role_id,
        data=roles_id_name(),
        width="48%",
        md_width="48%",
    )
    selector_start_month = Selector2(
        set_year_month,
        year_month_dict_list(label="select start month"),
        width="48%",
        md_width="48%",
    )
    selector_start_day = Selector2(
        set_day, days_in_month(label="select start day"), width="48%", md_width="48%"
    )
    is_disabled = False
    btn = Button(is_disabled, handle_update, label="Update")
    return Column(
        Row(selector_user),
        Row(inp_first_name, inp_last_name, justify="justify-between"),
        Row(selector_role, selector_team, justify="justify-between"),
        Row(selector_start_month, selector_start_day, justify="justify-between"),
        Row(btn),
    )


@component
def deactivate_users(is_event, set_is_event):
    """Deactivate an user without deleting it."""
    deactiv_user_id, set_deactiv_user_id = use_state("")

    def handle_deactivation(event):
        """Set the given user's is_active column to False."""
        deactivate_user(deactiv_user_id)
        switch_state(value=is_event, set_value=set_is_event)

        return True

    selector_user = Selector2(
        set_deactiv_user_id,
        data=users_names(label="select user to deactivate"),
        width="96%",
        md_width="96%",
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

    def handle_activation(event):
        """Set the given user's is_active column to False."""
        activate_user(activ_user_id)
        switch_state(value=is_event, set_value=set_is_event)
        return True

    selector_user = Selector2(
        set_activ_user_id,
        data=users_names_inactive(label="select user to activate"),
        width="96%",
        md_width="96%",
    )
    is_disabled = True
    if activ_user_id != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(selector_user, justify="justify-end"), Row(btn))
