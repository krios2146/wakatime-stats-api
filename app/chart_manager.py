import datetime
import logging
import os
from uuid import UUID
from matplotlib.figure import Figure

PLOTS_DIRECTORY: str = "plots"
DATE_SEPARATOR: str = "_"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def save_chart(figure: Figure, uuid: UUID):
    """
    Saves a matplotlib Figure object as an SVG file with the specified UUID and current date.

    Parameters:
    figure (Figure): A matplotlib Figure object to save.
    uuid (UUID): A unique identifier for the chart.

    Returns:
    None

    Notes:
    - This function saves the plot as an SVG file in the PLOTS_DIRECTORY with the format "{uuid}_{current_date}.svg".
    - Creates the PLOTS_DIRECTORY if it doesn't exist.
    """
    log.debug(f"Saving plot {uuid}")

    date = datetime.datetime.now()
    date = date.strftime("%y-%m-%d")

    if not os.path.exists(PLOTS_DIRECTORY):
        os.makedirs(PLOTS_DIRECTORY)

    figure.savefig(f"{PLOTS_DIRECTORY}/{uuid}{DATE_SEPARATOR}{date}.svg")  # type: ignore[all]


def find_by_uuid(uuid: UUID) -> str | None:
    log.debug(f"Searching plot {uuid}")

    for plot in os.listdir(PLOTS_DIRECTORY):
        if str(uuid) in plot:
            return os.path.join(PLOTS_DIRECTORY, plot)

    return None
