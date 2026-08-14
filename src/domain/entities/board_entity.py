from dataclasses import dataclass

from .base_entity import BaseEntity


@dataclass
class BoardEntity(BaseEntity):
    title: str
