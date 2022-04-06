from idom import html, run, use_state, component, event, vdom
from idom.web import module_from_url, export
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

from components.layout import Column, Row, FlexContainer
from components.sidebar import Sidebar


@component
def page():

    current_page, set_current_page = use_state("Timelogs")
    pages = ["Timelogs", "Forecasts"]

    print("here", current_page)
    if current_page == "Users":
        current_page_component = users_page(key="users_page")
    if current_page == "Roles":
        current_page_component = roles_page(key="roles_page")
    elif current_page == "Epics":
        current_page_component = epics_page(key="epics_page")
    elif current_page == "Epic Areas":
        current_page_component = epic_areas_page(key="epic_areas_page")
    elif current_page == "Timelogs":
        current_page_component = timelogs_page(key="timelogs_page")
    elif current_page == "Clients":
        current_page_component = clients_page(key="clients_page")
    elif current_page == "Forecasts":
        current_page_component = forecasts_page(key="forecasts_page")
    elif current_page == "Rates":
        current_page_component = rates_page(key="rates_page")
    elif current_page == "Teams":
        current_page_component = teams_page(key="teams_page")
    elif current_page == "Sponsors":
        current_page_component = sponsors_page(key="sponsors_page")
    elif current_page == "Capacities":
        current_page_component = capacities_page(key="capacities_page")
    elif current_page == "Demands":
        current_page_component = demands_page(key="demands_page")
    return html.div(
        {"class": "flex w-full"},
        Sidebar(current_page, set_current_page, pages=pages, title="timeflow UI"),
        FlexContainer(current_page_component),
    )
