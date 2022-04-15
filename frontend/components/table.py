from typing import Any, Callable, List
from idom import html, component, use_effect, use_state
from components.layout import Column, Row
from components.pagination import PaginationBlock
import math

from components.input import Checkbox
from components.tablebatch_row import TablebatchRow
from components.layout import Container

per_page_list = [
    5,
    10,
    15,
]
thClass = 'w-[176px] text-left text-text-table-head uppercase py-1 leading-5'
trClass = 'border-b-[1px] border-border-table'
tdClassActive = 'w-[176px] pt-4 pb-3'
tdClass = 'w-[176px] pt-4 pb-3'


@component
def SimpleTable(rows: List[Any]):
    checked, set_checked = use_state({})
    try:
        select_per_page, set_select_per_page = use_state(per_page_list[0])
        page_number, set_page_number = use_state(1)
        trs = []
        p = page_number
        m = p - 1
        number_of_visible_rows = int(select_per_page)
        a = m * number_of_visible_rows
        b = a + number_of_visible_rows
        qty_page = math.ceil(len(rows) / number_of_visible_rows)
        count = 0
        for row in rows[a:b]:
            tds = []
            count += 1

            for k in row:
                value = row[k]
                tds.append(html.td({"class": tdClassActive}, value))

            trs.append(TablebatchRow(count, tds, checked, set_checked))

        ths = [html.th({"class": thClass}, header)
               for header in rows[0].keys()]
        thead = html.thead(
            {},
            html.tr(
                {"class": "bg-table-head"},
                html.th(
                    {'class': 'w-6'}
                ),
                ths),
        )
        tbody = html.tbody(
            {},
            trs,
        )
        pages_total = math.ceil(len(rows) / number_of_visible_rows)
        pg_range = range(1, pages_total + 1)
        list_pages_nr = []
        for n in pg_range:
            list_pages_nr.append(n)
        table = html.div(
            {'class': 'overflow-auto py-6 text-xs'},
            html.table({'class': 'w-[905px] mx-auto xl:w-full'}, thead, tbody)
        )

        return html.div(
            {"class": "flex flex-col w-full space-y-2"},
            table,
            Row(
                PaginationBlock(set_page_number, qty_page,
                                set_select_per_page, per_page_list),
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

    ths = [html.th({"class": thClass}, header)
           for header in rows[0].keys()]
    thead = html.thead(
        {"class": ""},
        html.tr({"class": "bg-table-head"}, ths),
    )
    tbody = html.tbody(
        {
            "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
        },
        trs,
    )
    table = html.table({"class": "w-[905px] mx-auto xl:w-full"}, thead, tbody)

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


data_thead = [
    'Client',
    'Epic',
    'Username',
    'Forecasted Days',
    'Billings',
    'Timelogs Days',
    'Billings'
]


@component
def BillingTable():

    ths = [html.th({"class": thClass}, header)
           for header in data_thead]
    thead = html.thead(
        {},
        html.tr(
            {"class": "bg-table-head"},
            ths),
    )

    tbody = html.tbody(
        {},
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'rowspan': '6'},
                'client_a'
            ),
            html.td(
                {'rowspan': '4'},
                'epic_a'
            ),
            html.td(
                {'class': tdClass},
                'user_a'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'class': tdClass},
                'user_a'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'class': tdClass},
                'user_a'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'class': tdClass},
                'user_a'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'rowspan': '2'},
                'epic_b'
            ),
            html.td(
                'user_b'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                'user_b'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table bg-table-head'},
            html.th(
                {'colspan': '3', 'class': 'text-left '},
                'Client total'
            ),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'rowspan': '6'},
                'client_b'
            ),
            html.td(
                {'rowspan': '4'},
                'epic_c'
            ),
            html.td(
                {'class': tdClass},
                'user_a'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'class': tdClass},
                'user_b'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'class': tdClass},
                'user_c'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'class': tdClass},
                'user_d'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                {'rowspan': '2'},
                'epic_d'
            ),
            html.td(
                'user_b'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table'},
            html.td(
                'user_b'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            ),
            html.td(
                {'class': tdClass},
                '(...)'
            )
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table bg-table-head'},
            html.th(
                {'colspan': '3', 'class': 'text-left'},
                'Client total'
            ),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table bg-table-head'},
            html.th(
                {'colspan': '3', 'class': 'text-left '},
                'Grand total'
            ),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
        ),
        html.tr(
            {'class': 'border-b-[1px] border-border-table bg-table-head'},
            html.th(
                {'colspan': '3', 'class': 'text-left '},
                'Country total'
            ),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
            html.td({'class': tdClass}, 'sum'),
        )

    )

    return Container(
        html.div(
            {'class': 'overflow-auto py-6 text-xs'},
            html.table(
                {
                    'class': 'w-[905px] mx-auto xl:w-full'
                },
                thead,
                tbody
            )
        )

    )
