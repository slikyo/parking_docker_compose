import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime

from src.common.database import Database


@dataclass
class Spot(object):
    loc: list
    speed: float = field(default=80.00)
    space_length: float = field(default=6.0)
    space_depth: float = field(default=5.0)
    upload_time: str = field(default_factory=lambda: datetime.utcnow())
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def save_to_mongo(self):
        Database.insert('spots', asdict(self))




