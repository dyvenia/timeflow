from idom import component, html
from typing import Callable


@component
def Button(is_disabled: bool, handle_submit: Callable, label: str):
    button_status = "text-gray-50  border-secondary-200"
    if is_disabled is False:
        button_status = "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200 hover:bg-gray-50 hover:text-primary-500"
    return html.button(
        {
            "class": f"relative w-fit h-fit px-2 py-1 text-lg border {button_status}",
            "onClick": handle_submit,
            "disabled": is_disabled,
        },
        label,
    )


@component
def submit_button(handle_submit, *fields):
    """Create a submit button that is active when all given fields are filled out"""
    is_disabled = False
    for field in fields:
        if field == "":
            is_disabled = True
    btn = Button(is_disabled, handle_submit, label="Submit")
    return btn


def activation_button(name_to_activ, handle_activation):
    is_disabled = True
    if name_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return btn


def deactivation_button(name_to_deact, handle_deactivation):
    is_disabled = True
    if name_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return btn
