from typing import Any, Callable, List
from idom import html, component, use_state
from components.layout import Column, Row
import math


@component
def SimpleTable(rows: List[Any]):
    try:
        page_number, set_page_number = use_state(1)
        trs = []
        p = page_number
        m = p - 1
        number_of_visible_rows = 5
        a = m * number_of_visible_rows
        b = a + number_of_visible_rows

        for row in rows[a:b]:
            tds = []
            for k in row:
                value = row[k]
                tds.append(html.td({"class": "p-4 w-full"}, value))
            trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

        ths = [html.th({"class": "p-4 w-full"}, header) for header in rows[0].keys()]
        thead = html.thead(
            {"class": "flex bg-secondary-400 text-white w-full"},
            html.tr({"class": "flex w-full mb-4"}, ths),
        )
        tbody = html.tbody(
            {
                "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
            },
            trs,
        )
        pages_total = math.ceil(len(rows) / number_of_visible_rows)
        pg_range = range(1, pages_total + 1)
        list_pages_nr = []
        for n in pg_range:
            list_pages_nr.append(n)

        table = html.table({"class": "text-left"}, thead, tbody)

        a = 1
        b = 2
        c = 3

        return html.div(
            {"class": "flex flex-col w-full space-y-2"},
            table,
            Row(
                Row(
                    PaginationButton(set_page_number, page_number, button_page=a),
                    PaginationButton(set_page_number, page_number, button_page=b),
                    PaginationButton(set_page_number, page_number, button_page=c),
                ),
                justify="justify-end",
            ),
        )
    except TypeError:
        return False
    except IndexError:
        return False


@component
def SubmitTable(rows: List[Any]):
    trs = []
    for row in rows[-5:]:
        tds = []
        for k in row:
            value = row[k]
            tds.append(html.td({"class": "p-4 w-full"}, value))
        trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

    ths = [html.th({"class": "p-4 w-full"}, header) for header in rows[0].keys()]
    thead = html.thead(
        {"class": "flex bg-secondary-400 text-white w-full"},
        html.tr({"class": "flex w-full mb-4"}, ths),
    )
    tbody = html.tbody(
        {
            "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
        },
        trs,
    )
    table = html.table({"class": "text-left"}, thead, tbody)

    return html.div(
        {"class": "flex flex-col w-full space-y-2"},
        table,
    )


@component
def HiddenButton(is_hidden, set_is_hidden):
    text, set_text = use_state("hide table")

    def show_page(event):
        if is_hidden:
            set_is_hidden(False)
            set_text("hide table")
        else:
            set_is_hidden(True)
            set_text("show table")

    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": show_page,
        },
        text,
    )

    return btn


@component
def PaginationButton(set_page_number, page_number, button_page):
    def select_page_number(event):
        set_page_number(button_page)

    pgn_btn = html.button(
        {
            "class": "flex px-4 py-2 text-black bg-white rounded-md hover:bg-black hover:text-white",
            "onClick": select_page_number,
        },
        button_page,
    )

    return pgn_btn
