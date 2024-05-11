from uuid import UUID
import matplotlib
import matplotlib.pyplot as plt
import datetime

from data_node.github_language_data_node import GithubLanguageDataNode
from data_node.wakatime_data_node import WakatimeDataNode

matplotlib.use("TkAgg")
custom_font = {
    "font.family": "sans-serif",
    "font.serif": ["Segoe UI"],
}

matplotlib.rcParams.update(custom_font)

GITHUB_BG_COLOR: str = "#0D1117"
GITHUB_FG_COLOR: str = "#C3D1D9"
PLOTS_DIRECTORY: str = "plots"
DATE_SEPARATOR: str = "_"


def create_pie_chart(
    data_list: list[WakatimeDataNode],
    uuid: UUID,
    langs_data: list[GithubLanguageDataNode] | None = None,
) -> None:
    box, (left_plot, right_plot) = plt.subplots(1, 2)

    percents: list[float] = [data.percent for data in data_list[:5]]
    names: list[str] = [data.name for data in data_list[:5]]
    hours: list[str] = [data.text for data in data_list[:5]]

    colors = None

    # colorize data based on languages names
    if langs_data is not None:
        colors = []
        defaultColors = plt.get_cmap("tab10")

        for index, name in enumerate(names):
            found = False
            for lang in langs_data:

                if lang.name.lower() == name.lower():
                    _ = colors.append(lang.color)
                    found = True
                    break

            # use default colors for missing langs
            if not found:
                _ = colors.append(defaultColors(index))

    # creating pie based on percents, shape it with wedgeprops
    wedges, autotext = right_plot.pie(
        percents, colors=colors, wedgeprops=dict(width=0.2, radius=0.95)
    )

    # building left side legend
    labels = [
        f"{name} {percent}% - {hour}"
        for name, percent, hour in zip(names, percents, hours)
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

    date = datetime.datetime.now()
    date = date.strftime("%y-%m-%d")

    plt.savefig(f"{PLOTS_DIRECTORY}/{uuid}{DATE_SEPARATOR}{date}.png")
