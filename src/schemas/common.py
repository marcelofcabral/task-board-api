from pydantic import ConfigDict


class ResponseSchemaBase:
    model_config = ConfigDict(from_attributes=True)
