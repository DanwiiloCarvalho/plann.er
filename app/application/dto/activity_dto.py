from dataclasses import dataclass
from datetime import date, time


@dataclass
class ActivityDTO:
    title: str
    date: date
    time: time
