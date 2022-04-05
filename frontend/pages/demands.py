import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event
import requests
from sanic import Sanic, response
from black import click

from pages.utils import switch_state

from components.input import Input, Selector2
from components.layout import Row, Column, Container

from components.table import SimpleTable
from components.controls import Button

from data.common import year_month_dict_list
from data.demands import (
    demand_days,
    to_demand,
    demands_by_team_epic_year_month,
    demand_deletion,
)
from data.teams import teams_id_name
from data.epics import epics_names


@component
def page():
    """Creates a page for demands"""
    team_id, set_team_id = use_state("")
    epic_id, set_epic_id = use_state("")
    year_month, set_year_month = use_state("")
    days, set_days = use_state("")
    is_event, set_is_event = use_state(False)
    return Container(
        Row(
            create_demand_form(
                team_id,
                set_team_id,
                epic_id,
                set_epic_id,
                year_month,
                set_year_month,
                days,
                set_days,
                is_event,
                set_is_event,
            )
        ),
        Column(
            Row(demands_table(team_id, epic_id, year_month)),
        ),
        Row(delete_demand(is_event, set_is_event)),
    )


@component
def create_demand_form(
    team_id,
    set_team_id,
    epic_id,
    set_epic_id,
    year_month,
    set_year_month,
    days,
    set_days,
    is_event,
    set_is_event,
):
    """Generates demand form to submit demands and filter demand by month epic and team"""

    @event(prevent_default=True)
    async def handle_submit(event):
        """
        schema:
        {
          "team_id": 0,
          "epic_id": 0,
          "year": 0,
          "month": 0,
          "days": 0,
          "created_at": "2022-03-15T15:25:44.266Z",
          "updated_at": "2022-03-15T15:25:44.266Z",
          "is_locked": false
        }"""
        to_demand(
            team_id=team_id,
            epic_id=epic_id,
            year_month=year_month,
            days=days,
        )
        switch_state(is_event, set_is_event)

    selector_team_id = Selector2(
        set_value=set_team_id,
        data=teams_id_name(),
    )
    selector_epic_id = Selector2(set_value=set_epic_id, data=epics_names())
    selector_year_month = Selector2(
        set_value=set_year_month,
        data=year_month_dict_list(),
    )

    selector_days = Selector2(
        set_value=set_days,
        data=demand_days(),
    )

    is_disabled = True
    if team_id != "" and epic_id != "" and year_month != "" and days != "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            selector_team_id,
            selector_epic_id,
            selector_year_month,
            selector_days,
        ),
        Row(btn),
    )


@component
def demands_table(team_id, epic_id, year_month):
    """Generates a table component with demand days by year month epic and team"""
    rows = demands_by_team_epic_year_month(team_id, epic_id, year_month)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_demand(is_event, set_is_event):
    """Generates an input for demand id to delete"""
    demand_to_del, set_demand_to_del = use_state("")

    def handle_delete(event):
        demand_deletion(demand_to_del)
        switch_state(is_event, set_is_event)

    inp_demand = Input(
        set_value=set_demand_to_del,
        label="demand id to delete",
    )
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_delete,
        },
        "Delete",
    )
    return Column(Row(inp_demand), Row(btn))
