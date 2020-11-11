from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class History(BaseModel):
    update_data: Optional[dict] = Field(None, description="Updated Student data")
    update_ts: Optional[datetime] = Field(default_factory=datetime.utcnow)
