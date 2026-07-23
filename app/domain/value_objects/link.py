from dataclasses import dataclass
from urllib.parse import urlparse

from app.domain.exceptions.invalid_url_protocol_error import InvalidUrlProtocolError
from app.domain.exceptions.netloc_not_found_error import NetlocNotFoundError


@dataclass(frozen=True)
class Link:
    address: str

    def __post_init__(self):
        parsed = urlparse(self.address)
        if parsed.scheme.lower() not in ('http', 'https'):
            raise InvalidUrlProtocolError
        if not parsed.netloc:
            raise NetlocNotFoundError
