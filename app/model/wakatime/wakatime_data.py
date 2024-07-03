from dataclasses import dataclass

from .wakatime_item import WakatimeItem


@dataclass
class WakatimeData:
    projects: list[WakatimeItem]
    languages: list[WakatimeItem]
    editors: list[WakatimeItem]
