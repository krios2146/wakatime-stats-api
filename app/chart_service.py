from functools import reduce
import logging
import re

from . import chart_builder
from . import chart_manager
from .client import github_api_client
from .model.chart.chart_data_type import ChartDataType
from .model.chart.chart_request import ChartRequest
from .model.chart.chart import Chart
from .client import wakatime_api_client
from .model.chart.chart_type import ChartType
from .model.github_language_item import GithubLanguageItem
from .model.wakatime.wakatime_item import WakatimeItem
from .model.wakatime.wakatime_response import WakatimeResponse

log = logging.getLogger(__name__)
log.level = logging.DEBUG


def create_chart(chart_request: ChartRequest) -> Chart | None:
    """
    Creates a chart based on the provided ChartRequest.

    Parameters:
    chart_request (ChartRequest): An object containing all necessary parameters to create the chart.

    Returns:
    Chart | None: A Chart object representing the created chart, or None if the chart could not be created.

    Raises:
    AssertionError: If data is unexpectedly None after processing.

    Notes:
    This function fetches data from external APIs (Wakatime and possibly GitHub) based on chart_request.
    It processes and organizes the data according to the specified parameters in chart_request.
    The created chart is stored and can be retrieved later using its unique uuid with the help of chart_manager.
    """
    log.info(f"Creating chart {chart_request.uuid}")

    response: WakatimeResponse = wakatime_api_client.get_last_7_days(
        chart_request.username
    )

    data: list[WakatimeItem] | None = None
    colors: dict[str, str] | None = chart_request.colors

    match chart_request.chart_data:
        case ChartDataType.LANGUAGES:
            data = response.data.languages
            github_languages = github_api_client.get_github_languages()
            colors = _merge_github_lang_colors(colors, github_languages)

        case ChartDataType.PROJECTS:
            data = response.data.projects

        case ChartDataType.EDITORS:
            data = response.data.editors

    colors = _merge_group_colors(colors, chart_request.group_colors)
    colors = _normalize_colors(colors)

    assert data is not None

    data = _group(data, chart_request.groups)
    data = _hide(data, chart_request.hide)

    match chart_request.chart_type:
        case ChartType.PIE:
            chart_builder.create_pie_chart(
                data,
                chart_request.uuid,
                colors,
                height=chart_request.height,
                width=chart_request.width,
            )

    chart_path: str | None = chart_manager.find_by_uuid(chart_request.uuid)

    if chart_path is None:
        return None

    return Chart(chart_request.uuid, chart_path)


def _merge_github_lang_colors(
    param_colors: dict[str, str] | None, github_languages: list[GithubLanguageItem]
) -> dict[str, str] | None:
    github_colors: dict[str, str] = {
        github_language.name: github_language.color
        for github_language in github_languages
    }

    if param_colors is None:
        return github_colors

    merged_colors = github_colors.copy()

    for github_color_name in github_colors:
        for color_name in param_colors:
            color = param_colors[color_name]

            if github_color_name.lower() == color_name.lower():
                merged_colors[github_color_name] = color
                continue

            merged_colors[color_name] = color

    return merged_colors


def _merge_group_colors(
    colors: dict[str, str] | None, group_colors: dict[str, str] | None
) -> dict[str, str] | None:
    if colors is None:
        return group_colors

    if group_colors is None:
        return colors

    return colors | group_colors


def _normalize_colors(colors: dict[str, str] | None) -> dict[str, str] | None:
    """
    Normalizes color values in a dictionary to ensure they are formatted consistently.

    Parameters:
    colors (dict[str, str] | None): A dictionary mapping keys to color values, or None.

    Returns:
    dict[str, str] | None: A dictionary with normalized color values, or None if colors is None.

    Example:
    colors = {"python": "3572A5", "java": "#B07219"}
    normalized_colors = _normalize_colors(colors)
    # normalized_colors is now {"python": "#3572A5", "java": "#B07219"}

    Notes:
    This function ensures that color values follow a consistent format by checking each value:
    - If a color value is a valid hex code without a leading '#', it adds the '#' prefix.
    - If colors is None, returns None without modification.
    """
    if colors is None:
        return None

    for color_key in colors:
        color = colors[color_key]

        if _is_hex_without_hash(color):
            color = "#" + color
            colors[color_key] = color

    return colors


def _hide(data: list[WakatimeItem], hide: set[str] | None) -> list[WakatimeItem]:
    if hide is None:
        return data

    return _filter(data, hide)


def _group(
    data: list[WakatimeItem], groups: dict[str, set[str]] | None
) -> list[WakatimeItem]:
    if groups is None:
        return data

    grouped_items: list[WakatimeItem] = list()

    for group_name, group_item_names in groups.items():
        non_grouped_items = _filter(data, group_item_names)
        group_items = list(filter(lambda x: x not in non_grouped_items, data))

        if len(group_items) == 0:
            continue

        grouped_item = reduce(_combine_items, group_items)
        grouped_item.name = group_name
        grouped_items.append(grouped_item)

    grouped_items_names = reduce(lambda acc, x: acc | x, groups.values(), set[str]())
    non_grouped_items = _filter(data, grouped_items_names)

    grouped_data = grouped_items + non_grouped_items

    grouped_data.sort(key=lambda x: x.total_seconds, reverse=True)

    return grouped_data


def _filter(items: list[WakatimeItem], item_names: set[str]) -> list[WakatimeItem]:
    filtered_wildcards = _filter_wildcard_items(items, item_names)
    return _filter_items(filtered_wildcards, item_names)


def _filter_items(
    items: list[WakatimeItem], item_names: set[str]
) -> list[WakatimeItem]:
    return list(filter(lambda x: x.name.lower() not in item_names, items))


def _filter_wildcard_items(
    items: list[WakatimeItem], item_names: set[str]
) -> list[WakatimeItem]:
    filtered_items: list[WakatimeItem] = list()

    suffixes = list(
        map(lambda x: x[2:], filter(lambda x: x.startswith("**"), item_names))
    )
    prefixes = list(
        map(lambda x: x[:-2], filter(lambda x: x.endswith("**"), item_names))
    )

    for item in items:
        filtered_out = False

        for prefix in prefixes:
            if item.name.lower().startswith(prefix):
                filtered_out = True
                break

        for suffix in suffixes:
            if item.name.lower().endswith(suffix):
                filtered_out = True
                break

        if not filtered_out:
            filtered_items.append(item)

    return filtered_items


def _combine_items(item_one: WakatimeItem, item_two: WakatimeItem) -> WakatimeItem:
    combined_total_seconds: float = item_one.total_seconds + item_two.total_seconds
    combined_percent: float = item_one.percent + item_two.percent
    combined_hours: int = item_one.hours + item_two.hours
    combined_minutes: int = item_one.minutes + item_two.minutes

    if combined_minutes >= 60:
        hours = combined_minutes // 60
        minutes = combined_minutes % 60

        combined_hours += hours
        combined_minutes = minutes

    combined_digital = f"{combined_hours}:{combined_minutes}"
    combined_decimal = f"{combined_hours}.{combined_minutes // 0.6}"
    combined_text = f"{f"{combined_hours} hrs" if combined_hours != 0 else ""} {combined_minutes} mins"

    return WakatimeItem(
        total_seconds=combined_total_seconds,
        name=item_one.name,
        percent=combined_percent,
        digital=combined_digital,
        decimal=combined_decimal,
        text=combined_text,
        hours=combined_hours,
        minutes=combined_minutes,
    )


def _is_hex_without_hash(color: str) -> bool:
    hex_code_pattern = re.compile(r"^([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")
    return bool(re.match(hex_code_pattern, color))
