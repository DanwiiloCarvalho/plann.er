from dataclasses import dataclass

from pydantic_core.core_schema import str_schema


@dataclass
class EmailToInviteDTO:
    fullname: str
    email: str_schema
