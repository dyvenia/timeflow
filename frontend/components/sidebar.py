from turtle import heading
from typing import List
from idom import html, component
from components.layout import Container
from config import role
from components.dropdown import Dropdown, ListPages

admin = {
    # 'title': 'page',
    "Users": "Users",
    "Roles": "Roles",
    "Epics": "Epics",
    "Epic Areas": "Epic Areas",
    "Teams": "Teams",
    "Sponsors": "Sponsors",
    "Clients": "Clients",
    "Rates": "Rates",
    "Capacities": "Capacities",
    "Demands": "Demands",
    "Billing": "Billing"
}


aClass = ("text-nav py-2 text-left",)
btnClass = "text-nav py-2 flex"
mainDivClass = (
    "hidden absolute w-screen  h-fit bg-header-bg z-10 xl:w-full xl:block xl:static xl:h-auto",
)
mainDivClassOpen = (
    "absolute w-screen h-fit min-h-screen bg-header-bg z-10 xl:w-full xl:block xl:static xl:h-auto",
)
h1Class = (
    "text-general-heading font-black uppercase text-xl font-black tracking-[2px] my-4",
)
navClass = "flex flex-col pb-4"


@component
def Sidebar(
    current_page,
    set_current_page,
    pages: List[str],
    isOpen,
    set_isOpen,
    title: str = "",
):
    user_role = role()
    page_list = admin
    heading = 'Admin'
    return html.div(
        {
            "class": mainDivClassOpen if isOpen else mainDivClass,
        },
        Container(
            html.h1({"class": h1Class}, title),
            html.nav(
                {"class": navClass},
                ListPages(
                    current_page, set_current_page, set_isOpen, pages=pages, title=title
                ),
                Dropdown(current_page, set_current_page,
                         set_isOpen, heading, page_list)
                if (user_role == "admin" or user_role == None)
                else "",
            ),
        ),
    )
