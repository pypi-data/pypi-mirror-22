"""PytSite Form Endpoints.
"""
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def submit(args: dict, inp: dict):
    """Default submit endpoint.
    """
    frm = _api.dispense(inp)

    # Rebuild form
    if not frm.nocache:
        frm.remove_widgets()
        for step in range(1, frm.steps + 1):
            frm.step = step
            frm.setup_widgets(False)

    # Validate the form
    frm.fill(inp, mode='validation').validate()

    # Refill the form in 'normal' mode
    frm.fill(inp)

    # Notify form about submit
    return frm.submit()
