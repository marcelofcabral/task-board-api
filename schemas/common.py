from datetime import datetime

from pydantic import ConfigDict


class ResponseSchemaBase:
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
