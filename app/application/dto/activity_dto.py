from dataclasses import dataclass
from datetime import date, time
import uuid


@dataclass
class ActivityDTO:
    title: str
    date: date
    time: time


@dataclass
class ActivityResponseDTO:
    id: uuid.UUID
    title: str
    date: date
    time: time
