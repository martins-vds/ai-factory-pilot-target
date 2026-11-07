from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TransitEdge:
    voyage_number: str
    from_port: str
    to_port: str
    from_date: datetime
    to_date: datetime
