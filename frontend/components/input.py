from typing import Any, Callable, List, Dict
from idom import html, component
from data.common import Select

class_str = """text-primary-500 placeholder-secondary-400 w-full px-4 py-2.5 mt-2 
                    text-base transition duration-500 ease-in-out transform 
                    border-transparent bg-secondary-300 focus:border-blueGray-500 
                    focus:bg-white dark:focus:bg-secondary-400 focus:outline-none 
                    focus:shadow-outline focus:ring-2 ring-offset-current ring-offset-2 
                    ring-gray-400"""


@component
def Input(
    set_value: Callable,
    label: str = "",
    type: str = "text",
    placeholder: str = "Write here the",
    _class: str = class_str,
):

    return html.input(
        {
            "type": type,
            "placeholder": f"{placeholder} {label}",
            "onChange": lambda event: set_value(event["target"]["value"]),
            "class": _class,
        }
    )


@component
def Selector(
    set_value: Callable,
    placeholder,
    dropdown_list,
    _class: str = class_str,
):
    return html.select(
        {
            "class": _class,
            "onChange": lambda event: set_value(event["target"]["value"]),
        },
        html.option({"value": ""}, placeholder),
        dropdown_list,
    )


@component
def Selector2(
    set_value: Callable,
    data: List[Select],
    _class: str = class_str,
):
    options = []
    for row in data:
        option = html.option({"value": row["value"]}, row["display_value"])
        options.append(option)

    return html.select(
        {
            "class": _class,
            "onChange": lambda event: set_value(event["target"]["value"]),
        },
        options,
    )


def SelectorDropdownKeyValue(rows: List[Any]):
    crows = []
    for row in rows:
        for key in row:
            value = row[key]
            c = html.option({"value": f"{value}"}, key)
            crows.append(c)
    dropdown_list = tuple(crows)
    return dropdown_list


def SelectorDropdownList(rows: List[Any]):
    crows = []
    for n in rows:
        a = html.option({"value": f"{n}"}, n)
        crows.append(a)
    dropdown_list = tuple(crows)
    return dropdown_list


@component
def AutoSelect(
    set_value: Callable,
    option: Any,
    _class: str = class_str,
):
    return html.select(
        {
            "class": _class,
            "onChange": lambda event: set_value(event["target"]["value"]),
        },
        option,
    )
