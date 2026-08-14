from pydantic import ConfigDict


class ResponseDTOBase:
    model_config = ConfigDict(from_attributes=True)
