import dataclasses
from typing import Optional

@dataclasses.dataclass
class UserDto:
    login: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

