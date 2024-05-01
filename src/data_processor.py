import matplotlib
import matplotlib.pyplot as plt

from data import Data

matplotlib.use("TkAgg")
custom_font = {
    "font.family": "sans-serif",
    "font.serif": ["Segoe UI"],
}

matplotlib.rcParams.update(custom_font)

GITHUB_BG_COLOR: str = "#0D1117"
GITHUB_FG_COLOR: str = "#C3D1D9"


def show_pie_chart(data_list: list[Data]) -> None:
    box, (left_plot, right_plot) = plt.subplots(1, 2)

    percents: list[float] = [data.percent for data in data_list[:5]]
    names: list[str] = [data.name for data in data_list[:5]]
    hours: list[str] = [data.text for data in data_list[:5]]

    # creating pie based on percents, shape it with wedgeprops
    wedges, autotext = right_plot.pie(percents, wedgeprops=dict(width=0.2, radius=0.95))

    # building left side legend
    labels = [
        f"{editor_name} {percent}% - {hour}"
        for editor_name, percent, hour in zip(names, percents, hours)
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

    plt.show()
