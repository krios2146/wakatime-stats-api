class WakatimeDataNode:
    total_seconds: int
    name: str
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int

    def __init__(self, raw_data: dict[str, str | float | int]) -> None:
        self.total_seconds = int(raw_data.get("total_seconds", 0))
        self.name = str(raw_data.get("name", "unknown"))
        self.percent = float(raw_data.get("percent", 0))
        self.digital = str(raw_data.get("digital", "unknown"))
        self.decimal = str(raw_data.get("decimal", "unknown"))
        self.text = str(raw_data.get("text", "unknown"))
        self.hours = int(raw_data.get("hours", 0))
        self.minutes = int(raw_data.get("minutes", 0))
