from uuid import UUID, uuid4

from .chart_type import ChartType
from .chart_data_type import ChartDataType


class ChartRequest:
    uuid: UUID
    chart_type: ChartType
    chart_data: ChartDataType
    username: str
    hide: set[str] | None
    colors: dict[str, str] | None
    groups: dict[str, set[str]] | None
    group_colors: dict[str, str] | None
    width: int | None = None
    height: int | None = None

    def __init__(
        self,
        chart_type: ChartType,
        chart_data: ChartDataType,
        username: str,
        hide: set[str] | None = None,
        colors: dict[str, str] | None = None,
        groups: dict[str, set[str]] | None = None,
        group_colors: dict[str, str] | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        self.uuid = uuid4()
        self.chart_type = chart_type
        self.chart_data = chart_data
        self.username = username
        self.hide = hide
        self.colors = colors
        self.groups = groups
        self.group_colors = group_colors
        self.width = width
        self.height = height
