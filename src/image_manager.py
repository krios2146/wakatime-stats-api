import datetime
from uuid import UUID
from matplotlib.figure import Figure

PLOTS_DIRECTORY: str = "plots"
DATE_SEPARATOR: str = "_"


def save_plot(figure: Figure, uuid: UUID):
    date = datetime.datetime.now()
    date = date.strftime("%y-%m-%d")

    figure.savefig(f"{PLOTS_DIRECTORY}/{uuid}{DATE_SEPARATOR}{date}.png")
