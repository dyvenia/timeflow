from idom import component, html, use_state

from components.sidebar import Sidebar


@component
def Header(current_page, set_current_page, pages, title):

    isOpen, set_isOpen = use_state(False)

    def handleOpenSidebar(event):
        set_isOpen(not isOpen)

    return html.div(
        html.header(
            {'class': "bg-header-bg xl:w-60 xl:h-screen xl:px-6 xl:fixed"},
            html.div(
                {'class': 'w-full px-4 flex justify-between items-center py-4 xl:px-0 xl:py-6'},
                html.img({'src': '../static/img/svg/logo.svg'}),
                html.a(
                    {
                        'href': 'javascript:void(0)',
                        'class': "xl:hidden",
                        'onClick': handleOpenSidebar
                    },
                    html.img(
                        {'src': '../static/img/svg/Burger.svg', 'class': "w-8"}
                    )
                )
            ),
            Sidebar(current_page, set_current_page,
                    pages, isOpen, set_isOpen, title)
        )
    )
