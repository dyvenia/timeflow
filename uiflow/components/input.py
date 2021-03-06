from typing import Any, Callable, List, Dict
from idom import html, component, event

# from data.common import Select

class_str = """text-primary-500 bg-transparent placeholder-secondary-400 w-full px-4 py-2.5 mt-2 
                    text-base transition duration-500 ease-in-out transform 
                    border-transparent focus:border-blueGray-500 
                    focus:bg-white dark:focus:bg-secondary-400 focus:outline-none 
                    focus:shadow-outline focus:ring-2 ring-offset-current ring-offset-2 
                    ring-gray-400"""

inputWrapperClass = "w-full md:w-1/2 flex justify-between items-center border-input-border border-[1px] rounded-[3px] py-2 px-4 xl:max-w-[401px]"
selectClass = (
    "w-full border-select-border py-3 pl-3 border-[1px] rounded-[3px] appearance-none"
)
selectWrapperClass = "block relative w-full sm:w-[48%] md:w-[121px] md:mr-2 my-4 before:content-[''] before:border-[6px] before:border-[transparent] before:border-t-appearance before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute xl:w-{width} 2xl:mr-0"
checkboxTd = "w-6 pr-4 pt-4 pb-3"


@component
def Input(
    set_value: Callable,
    label: str = "",
    type: str = "text",
    placeholder: str = "Write here the",
    _class: str = class_str,
    width: str = "[401px]",
    md_width: str = "1/2",
):

    return html.div(
        {
            "class": f"w-full my-4 md:w-{md_width} flex justify-between items-center bg-nav border-input-border border-[1px] rounded-[3px] py-2 px-4 xl:max-w-{width} xl:w-full"
        },
        html.input(
            {
                "type": type,
                "placeholder": f"{placeholder} {label}",
                "onChange": lambda event: set_value(event["target"]["value"]),
                "class": _class,
            }
        ),
    )


@component
def SearchInput(input_value, set_input_value):
    def handle_click(event):
        set_input_value("")

    return html.div(
        {"class": inputWrapperClass},
        html.img({"src": "../static/img/svg/search.svg"}),
        html.input(
            {
                "type": "text",
                "placeholder": "Search your timelog here",
                "value": input_value,
                "onChange": lambda event: set_input_value(event["target"]["value"]),
                "class": "w-10/12 outline-none",
            },
        ),
        html.img(
            {
                "class": "cursor-pointer",
                "src": "../static/img/svg/cross.svg",
                "onClick": handle_click,
            }
        ),
    )


@component
def Selector(
    set_value: Callable,
    data: List,
    width: str = "14%",
    md_width: str = "121px",
    set_sel_value: Callable = None,
    sel_value: Any = None,
    set_sel_value2: Callable = None,
    sel_value2: Any = None,
    key_attr: str = None,
):
    options = []
    for row in data:
        option = html.option({"value": row["value"]}, row["display_value"])
        options.append(option)

    @event()
    async def on_change(event):
        set_value(event["target"]["value"])
        if (set_sel_value and sel_value) != None:
            set_sel_value(sel_value)
        if (set_sel_value2 and sel_value2) != None:
            set_sel_value2(sel_value2)
        return True

    # changing key_attr value reloads the component
    return html.div(
        {
            "class": f"block relative w-full sm:w-[48%] md:w-[{md_width}] md:mr-2 my-4 before:content-[''] before:border-[6px] before:border-[transparent] before:border-t-appearance before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute xl:w-[{width}] 2xl:mr-0",
            "key": key_attr,
        },
        html.select(
            {
                "class": selectClass,
                "onChange": on_change,
            },
            options,
        ),
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


@component
def SelectPerPage(set_select_per_page, per_page_list, set_page_number):
    dropdown = [html.option({"value": el}, el) for el in per_page_list]

    def onChange(event):
        set_select_per_page(event["target"]["value"])
        set_page_number(1)

    return html.div(
        {
            "class": "block w-[176px] shrink-0 relative md:mr-2 my-4 before:content-["
            "] before:border-[6px] before:border-[transparent] before:border-t-appearance before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute 2xl:mr-0"
        },
        html.select(
            {
                "class": selectClass,
                "onChange": onChange,
            },
            dropdown,
        ),
    )


@component
def Checkbox(value_checkbox, handle_change):
    return html.td(
        {
            "class": checkboxTd,
        },
        html.input(
            {
                "class": "w-4 h-4",
                "checked": value_checkbox,
                "onChange": lambda event: handle_change(event),
                "type": "checkbox",
            }
        ),
    )


@component
def InputDateTime(
    set_value,
    set_sel_value: Callable = None,
    sel_value: Any = None,
):
    @event()
    async def on_change(event):
        set_value(event["target"]["value"])
        if (set_sel_value and sel_value) != None:
            set_sel_value(sel_value)
        return True

    return html.input(
        {
            "class": "py-3 pl-3 w-full border-[1px] sm:w-[48%] md:w-[121px] bg-nav rounded-[3px] md:mr-2 my-4 before:content-[''] before:border-[6px] before:border-[transparent] before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute xl:w-[14%]",
            "type": "datetime-local",
            "onChange": on_change,
        },
    )


@component
def InputDate(set_value):
    return html.input(
        {
            "class": "py-3 pl-3 w-full border-[1px] sm:w-[48%] md:w-[121px] bg-nav rounded-[3px] md:mr-2 my-4 before:content-[''] before:border-[6px] before:border-[transparent] before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute xl:w-[14%]",
            "type": "date",
            "onChange": lambda event: set_value(event["target"]["value"]),
        },
    )


@component
def InputMonth(
    set_value,
    set_sel_value: Callable = None,
    sel_value: Any = None,
):
    @event()
    async def on_change(event):
        set_value(event["target"]["value"])
        if (set_sel_value and sel_value) != None:
            set_sel_value(sel_value)
        return True

    return html.input(
        {
            "class": "py-3 pl-3 w-full border-[1px] sm:w-[48%] md:w-[121px] bg-nav rounded-[3px] md:mr-2 my-4 before:content-[''] before:border-[6px] before:border-[transparent] before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute xl:w-[14%]",
            "type": "month",
            "onChange": on_change,
        },
    )


@component
def display_value(id, value):
    """
    Display a value in a selector-like style.

    Parameters
    ----------
    id: int
        Id of the value to be displayed
    """
    return html.div(
        {
            "class": "py-3 pl-3 w-full border-[1px] sm:w-[48%] md:w-[121px] bg-nav rounded-[3px] md:mr-2 my-4 before:content-[''] before:border-[6px] before:border-[transparent] before:top-1/2 before:right-5 before:-translate-y-0.5 before:absolute xl:w-[14%]",
        },
        html.h3(
            {"value": id},
            value,
        ),
    )
