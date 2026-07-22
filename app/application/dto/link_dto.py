from dataclasses import dataclass
import uuid


@dataclass
class LinkDTO:
    link: str
    title: str


@dataclass
class LinkResponseDTO:
    id: uuid.UUID
    link: str
    title: str
