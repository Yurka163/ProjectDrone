import dataclasses
from typing import Optional

@dataclasses.dataclass
class DroneDto:
    id: Optional[int] = None
    model: Optional[str] = None
    status: Optional[str] = 'None'

