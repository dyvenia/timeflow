from config import role
from idom import html, use_state, component
from pages.users import page as users_page
from pages.clients import page as clients_page
from pages.epics import page as epics_page
from pages.epic_areas import page as epic_areas_page
from pages.timelogs import page as timelogs_page
from pages.forecasts import page as forecasts_page
from pages.rates import page as rates_page
from pages.teams import page as teams_page
from pages.sponsors import page as sponsors_page
from pages.roles import page as roles_page
from pages.capacities import page as capacities_page
from pages.demands import page as demands_page

from components.layout import FlexContainer, Container
from components.header import Header

from idom.server import fastapi


@component
def BreadCrambs(current_page):
    return Container(
        html.ul(
            {'class': 'breadcrumb my-4'},
            html.li(
                html.a(
                    {'href': '#'},
                    html.i(
                        {'class': 'icon icon-home'}
                    )
                ),
            ),
            html.li(
                html.a(
                    {'href': '#'},
                    current_page
                ),
            )
        )
    )


@component
def page():
    # Get role of user
    user_role = role()

    current_page, set_current_page = use_state("Timelogs")
    pages = ["Timelogs", "Forecasts"]

    print("here", current_page)
    if current_page == "Users":
        if user_role == "admin" or user_role == None:
            current_page_component = users_page(key="users_page")
    elif current_page == "Roles":
        if user_role == "admin" or user_role == None:
            current_page_component = roles_page(key="roles_page")
    elif current_page == "Epics":
        if user_role == "admin" or user_role == None:
            current_page_component = epics_page(key="epics_page")
    elif current_page == "Epic Areas":
        if user_role == "admin" or user_role == None:
            current_page_component = epic_areas_page(key="epic_areas_page")
    elif current_page == "Timelogs":
        current_page_component = timelogs_page(key="timelogs_page")
    elif current_page == "Clients":
        if user_role == "admin" or user_role == None:
            current_page_component = clients_page(key="clients_page")
    elif current_page == "Forecasts":
        current_page_component = forecasts_page(key="forecasts_page")
    elif current_page == "Rates":
        if user_role == "admin" or user_role == None:
            current_page_component = rates_page(key="rates_page")
    elif current_page == "Teams":
        if user_role == "admin" or user_role == None:
            current_page_component = teams_page(key="teams_page")
    elif current_page == "Sponsors":
        if user_role == "admin" or user_role == None:
            current_page_component = sponsors_page(key="sponsors_page")
    elif current_page == "Capacities":
        if user_role == "admin" or user_role == None:
            current_page_component = capacities_page(key="capacities_page")
    elif current_page == "Demands":
        if user_role == "admin" or user_role == None:
            current_page_component = demands_page(key="demands_page")
    return html.div(
        {"class": "xl:flex w-full"},
        html.link({"href": "../static/css/styles.css", "rel": "stylesheet"}),
        html.link({"href": "../static/css/custom.css", "rel": "stylesheet"}),
        html.link(
            {"href": "//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css", "rel": "stylesheet"}),
        Header(current_page, set_current_page,
               pages=pages, title="timeflow UI"),
        FlexContainer(
            html.div(
                {'class': 'w-full'},
                BreadCrambs(current_page),
                current_page_component
            )
        ),
    )
