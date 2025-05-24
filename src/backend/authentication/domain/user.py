from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class User:
    email: str = field(repr=False)
    hashed_password: str = field(repr=False)
    id: UUID = field(default_factory=uuid4)
