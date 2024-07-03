import logging
from uuid import UUID
import matplotlib
import matplotlib.pyplot as plt

from . import chart_manager
from .model.wakatime.wakatime_item import WakatimeItem

custom_font = {
    "font.family": "sans-serif",
    "font.serif": ["Segoe UI"],
}

matplotlib.rcParams.update(custom_font)

GITHUB_BG_COLOR: str = "#0D1117"
GITHUB_FG_COLOR: str = "#C3D1D9"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def create_pie_chart(
    data_list: list[WakatimeItem],
    uuid: UUID,
    colors_data: dict[str, str] | None,
    height: int | None,
    width: int | None,
) -> None:
    """
    Creates a pie chart using Matplotlib based on the provided data.

    Parameters:
    data_list (list[WakatimeItem]): A list of WakatimeItem objects containing data for the pie chart.
    uuid (UUID): A unique identifier for the chart.
    colors_data (dict[str, str] | None): A dictionary mapping item names to colors. If None, default colors are used.
    height (int | None): Height of the chart in inches. If None, uses default size.
    width (int | None): Width of the chart in inches. If None, uses default size.

    Returns:
    None

    Notes:
    - This function creates a pie chart with the top 5 items from data_list based on percent.
    - If colors_data is provided, it maps colors to corresponding items; otherwise, default colors are used.
    - The chart is saved using chart_manager.save_chart() with the provided uuid.
    """
    log.info(f"Creating pie chart {uuid}")
    box, (left_plot, right_plot) = plt.subplots(1, 2)  # type: ignore[all]

    percents: list[float] = [data.percent for data in data_list[:5]]
    names: list[str] = [data.name for data in data_list[:5]]
    hours: list[int] = [data.hours for data in data_list[:5]]
    minutes: list[int] = [data.minutes for data in data_list[:5]]

    colors = _map_colors(colors_data, data_list)

    # creating pie based on percents, shape it with wedgeprops
    wedges, autotext = right_plot.pie(
        percents,
        colors=colors,
        wedgeprops=dict(width=0.22, radius=1.2),
        startangle=90,
        counterclock=False,
    )

    # building left side legend {percent}%
    labels = [
        f"{name} - {hour}h {minunte}m"
        for name, hour, minunte in zip(names, hours, minutes)
    ]

    # hiding legend text on the pie
    for text in autotext:
        text.set_alpha(0)

    # associate data from the pie (wedges) to the labels
    legend = left_plot.legend(wedges, labels, loc="center", frameon=False)
    left_plot.axis("off")

    for text in legend.get_texts():
        text.set_color(GITHUB_FG_COLOR)

    # setting background for the entire box (figure)
    box.patch.set_facecolor(GITHUB_BG_COLOR)

    if height is not None and width is not None:
        box.set_size_inches(w=width / 100, h=height / 100)

    box.subplots_adjust(right=0.95, left=0.1)

    chart_manager.save_chart(box, uuid)


def _map_colors(
    item_colors: dict[str, str] | None, items: list[WakatimeItem]
) -> list[str | tuple[float, float, float, float]] | None:
    if item_colors is None:
        return None

    colors: list[str | tuple[float, float, float, float]] = []
    defaultColors = plt.get_cmap("tab10")

    for index, item in enumerate(items):
        found = False
        for key in item_colors:
            if key.lower() == item.name.lower():
                _ = colors.append(item_colors[key])
                found = True
                break

        # use default colors for missing langs
        if not found:
            _ = colors.append(defaultColors(index))

    return colors
