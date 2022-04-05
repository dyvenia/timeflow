import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click
from datetime import datetime

from components.input import Input, Selector, Selector2
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import Button
from data.common import (
    months_start,
    username,
)

from data.rates import (
    rates_by_user_client_date,
    rate_active_by_user_client,
    rate_update,
    to_rate,
)

from data.clients import clients_names

from pages.utils import month_start_to_str, far_date, date_str_to_date
from config import base_url


@component
def page():
    user_id, set_user_id = use_state("")
    client_id, set_client_id = use_state("")
    month_start, set_month_start = use_state("")
    amount, set_amount = use_state("")
    updated_rate, set_updated_rate = use_state("")
    on_submit, set_on_submit = use_state(True)
    return Container(
        Row(
            create_rates_form(
                user_id,
                set_user_id,
                client_id,
                set_client_id,
                month_start,
                set_month_start,
                amount,
                set_amount,
                on_submit,
                set_on_submit,
            )
        ),
        Column(
            Row(rates_table(user_id, client_id, month_start)),
        ),
        Row(update_rate(set_updated_rate, user_id, client_id, month_start)),
    )


@component
def create_rates_form(
    user_id,
    set_user_id,
    client_id,
    set_client_id,
    month_start,
    set_month_start,
    amount,
    set_amount,
    on_submit,
    set_on_submit,
):
    @event(prevent_default=True)
    async def handle_submit(event):
        """
        schema:
        {
        "user_id": 0,
        "client_id": 0,
        "valid_from": "2022-03-03",
        "valid_to": "2022-03-03",
        "amount": 0,
        "created_at": "2022-03-03T16:02:57.934Z",
        "updated_at": "2022-03-03T16:02:57.934Z",
        "is_active": true
        }
        """
        ms_str = month_start_to_str(month_start)
        selected_date = date_str_to_date(ms_str)
        to_rate(
            user_id=user_id,
            client_id=client_id,
            valid_from=ms_str,
            valid_to=str(far_date),
            amount=amount,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
            is_active=True,
        )
        if on_submit:
            set_on_submit(False)
        else:
            set_on_submit(True)

    selector_user_id = Selector2(set_value=set_user_id, data=username())

    selector_client_id = Selector2(
        set_value=set_client_id,
        data=clients_names(),
    )
    selector_month_start = Selector2(
        set_value=set_month_start,
        data=months_start(),
    )
    inp_amount = Input(set_amount, label="amount in EUR")

    is_disabled = True
    if user_id != "" and client_id != "" and month_start != "" and amount != "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(selector_user_id, selector_client_id, selector_month_start, inp_amount),
        Row(btn),
    )


@component
def rates_table(user_id, client_id, month_start):
    # Get list of rates by selected user and client containing selected date
    ms_str = month_start_to_str(month_start)
    if user_id != "" and client_id != "" and month_start != "":
        rows = rates_by_user_client_date(
            user_id=user_id, client_id=client_id, date=ms_str
        )
        return html.div({"class": "flex w-full"}, SimpleTable(rows))

    # Get list of active rate by user and client
    elif user_id != "" and client_id != "" and month_start == "":
        rows = rate_active_by_user_client(user_id, client_id)
        return html.div({"class": "flex w-full"}, SimpleTable(rows))


@component
def update_rate(set_updated_rate, user_id, client_id, month_start):
    new_amount, set_new_amount = use_state("")

    def handle_submit(event):
        rate_update(user_id, client_id, new_amount)
        set_updated_rate(new_amount)

    inp_rate = Input(
        set_value=set_new_amount,
        label="new amount for current rate",
    )
    is_disabled = True
    if user_id != "" and client_id != "" and month_start == "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Update")

    # html.button(
    #     {
    #         "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
    #         "onClick": handle_delete,
    #     },
    #     "Update",
    # )
    return Column(Row(inp_rate), Row(btn))
