from typing import Any, Callable, List
from idom import html, component


def Container(*args: html):
    return html.div({"class": "w-full"}, args)


def FlexContainer(*args: html):
    return html.div({"class": "flex w-full"}, args)


def Column(*args: html, width: str = "full"):
    return html.div(
        {"class": f"flex flex-col w-{width} space-y-2 pl-2 pr-4 mt-2"}, args
    )


@component
def Row(*args: html, justify: str = None):
    return html.div({"class": f"flex flex-col md:flex-row {justify} space-x-4"}, args)
