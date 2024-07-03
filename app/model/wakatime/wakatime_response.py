from dataclasses import dataclass

from .wakatime_data import WakatimeData


@dataclass
class WakatimeResponse:
    data: WakatimeData
