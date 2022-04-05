from turtle import title
from typing import List
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
from idom.web import module_from_url, export

from .icons import arrow_down, arrow_up


@component
def Dropdown(current_page, set_current_page):
    is_down, set_value = use_state(True)

    def handle_click(event):
        if is_down:
            set_value(False)
        else:
            set_value(True)

    btn_class = """flex flex-row items-center w-full px-4 py-2 mt-2 text-sm font-semibold text-left bg-transparent 
                    rounded-lg dark-mode:bg-transparent dark-mode:focus:text-white dark-mode:hover:text-white 
                    dark-mode:focus:bg-gray-600 dark-mode:hover:bg-gray-600 md:block hover:text-gray-900 
                    focus:text-gray-900 hover:bg-gray-200 focus:bg-gray-200 focus:outline-none focus:shadow-outline
                    """
    if is_down:
        btn = html.button(
            {"class": btn_class, "onClick": handle_click},
            html.span("Admin"),
            arrow_down,
        )
        return html.div({"class": "relative"}, btn)
    else:
        btn = html.button(
            {"class": btn_class, "onClick": handle_click},
            html.span("Admin"),
            arrow_up,
        )
        aclass = """block px-4 py-2 mt-2 text-sm font-semibold bg-transparent rounded-lg 
                    dark-mode:bg-transparent dark-mode:hover:bg-gray-600 dark-mode:focus:bg-gray-600 
                    dark-mode:focus:text-white dark-mode:hover:text-white dark-mode:text-gray-200 
                    md:mt-0 hover:text-gray-900 focus:text-gray-900 hover:bg-gray-200 focus:bg-gray-200 
                    focus:outline-none focus:shadow-outline
                """
        anchors = []
        for item in [
            "Users",
            "Roles",
            "Epics",
            "Epic Areas",
            "Teams",
            "Sponsors",
            "Clients",
            "Rates",
            "Capacities",
            "Demands",
        ]:
            anchors.append(html.a({"class": aclass}, item))
        pages = [
            "Users",
            "Roles",
            "Epics",
            "Epic Areas",
            "Teams",
            "Sponsors",
            "Clients",
            "Rates",
            "Capacities",
            "Demands",
        ]
        return html.div(
            {"class": "relative"},
            btn,
            html.div(
                {
                    "class": "absolute right-0 w-full mt-2 origin-top-right rounded-md shadow-lg"
                },
                html.div(
                    {
                        "class": "px-2 py-2 bg-white rounded-md shadow dark-mode:bg-gray-800"
                    },
                    ListPages(current_page, set_current_page, pages=pages),
                ),
            ),
        )


@component
def ListPages(current_page, set_current_page, pages: List[str], title: str = ""):
    def btn_class(btn_bg: str):
        btn_class = f"""block px-4 py-2 mt-2 text-sm font-semibold text-gray-900 bg-{btn_bg} rounded-lg 
                dark-mode:bg-transparent dark-mode:hover:bg-gray-600 dark-mode:focus:bg-gray-600 
                dark-mode:focus:text-white dark-mode:hover:text-white dark-mode:text-gray-200 
                hover:text-gray-900 focus:text-gray-900 hover:bg-gray-200 focus:bg-gray-200 
                focus:outline-none focus:shadow-outline
                """
        return btn_class

    @event(prevent_default=True)
    def handle_click(event):
        set_current_page(event["target"]["value"])

    anchors = []
    for page in pages:
        if page == current_page:
            btn_bg = "gray-200"
        else:
            btn_bg = "transparent"
        anchors.append(
            html.button(
                {
                    "class": btn_class(btn_bg),
                    "href": f"#{page}",
                    "value": page,
                    "onClick": handle_click,
                },
                page,
            )
        )

    return html.div(anchors)


@component
def Sidebar(current_page, set_current_page, pages: List[str], title: str = ""):
    return html.div(
        html.link({"href": "/static/_tailwind.css", "rel": "stylesheet"}),
        html.div(  # w-2/12 h-screen justify-between
            {
                "class": "md:flex flex-col md:flex-row md:min-h-screen w-2/12 h-screen justify-between"
            },
            html.div(
                {
                    "class": "flex flex-col w-full md:w-64 text-gray-700 bg-white dark-mode:text-gray-200 dark-mode:bg-gray-800 flex-shrink-0",
                },
                html.div(
                    {
                        "class": "flex-shrink-0 px-8 py-4 flex flex-row items-center justify-between"
                    },
                    html.a(
                        {
                            "class": "text-lg font-semibold tracking-widest text-gray-900 uppercase rounded-lg dark-mode:text-white focus:outline-none focus:shadow-outline",
                            "href": "#",
                        },
                        title,
                    ),
                ),
                html.nav(
                    {
                        "class": "flex-grow md:block px-4 pb-4 md:pb-0 md:overflow-y-auto"
                    },
                    ListPages(current_page, set_current_page, pages=pages, title=title),
                    Dropdown(current_page, set_current_page),
                ),
            ),
        ),
    )
