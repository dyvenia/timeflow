from idom import html, use_state, component, event
from datetime import datetime

from uiflow.components.input import Input, Selector2
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable, RatesTable
from uiflow.components.controls import Button
from ..data.common import (
    months_start,
    username,
)

from ..data.rates import (
    rate_active_by_user_client,
    rate_update,
    to_rate,
    rates_all,
    rates_active_by_user,
)

from ..data.clients import clients_names

from .utils import month_start_to_str, far_date, date_str_to_date


@component
def page():
    user_id, set_user_id = use_state("")
    client_id, set_client_id = use_state("")
    month_start, set_month_start = use_state("")
    amount, set_amount = use_state("")
    updated_rate, set_updated_rate = use_state("")
    on_submit, set_on_submit = use_state(True)
    return html.div(
        {"class": "w-full"},
        Row(
            Container(
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
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(rates_table(user_id, client_id)),
            ),
            Row(update_rate(set_updated_rate, user_id, client_id, month_start)),
        ),
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

    selector_user_id = Selector2(
        set_value=set_user_id, data=username(), width="24%", md_width="24%"
    )

    selector_client_id = Selector2(
        set_value=set_client_id, data=clients_names(), width="24%", md_width="24%"
    )
    selector_month_start = Selector2(
        set_value=set_month_start, data=months_start(), width="24%", md_width="24%"
    )
    inp_amount = Input(
        set_amount, label="amount in EUR", width="[24%]", md_width="[24%]"
    )

    is_disabled = True
    if user_id != "" and client_id != "" and month_start != "" and amount != "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            selector_user_id,
            selector_client_id,
            selector_month_start,
            inp_amount,
            justify="justify-between",
        ),
        Row(btn),
    )


@component
def rates_table(user_id, client_id):
    select_per_page, set_select_per_page = use_state(per_page_list[0])
    page_number, set_page_number = use_state(1)

    # if (user_id and client_id) != "":
    #     rows = rate_active_by_user_client(user_id, client_id)
    # elif user_id != "":
    #     rows = rates_active_by_user(user_id)
    # else:
    rows = rates_all(1, 15)
    return html.div({"class": "flex w-full"}, RatesTable(rows))


@component
def update_rate(set_updated_rate, user_id, client_id, month_start):
    new_amount, set_new_amount = use_state("")
    rate_id, set_rate_id = use_state(None)

    def handle_submit(event):
        rate_update(rate_id, new_amount)
        set_updated_rate(new_amount)

    inp_rate_id = Input(set_rate_id, label="rate id", width="full")
    inp_amount = Input(set_value=set_new_amount, label="new amount", width="full")
    is_disabled = True
    if rate_id != None and new_amount != "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Update")

    # html.button(
    #     {
    #         "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
    #         "onClick": handle_delete,
    #     },
    #     "Update",
    # )
    return Column(Row(inp_rate_id, inp_amount), Row(btn))
