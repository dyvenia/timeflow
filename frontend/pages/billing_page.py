from idom import component

from components.table import BillingTable
from components.layout import Container


@component
def page():

    return BillingTable()
