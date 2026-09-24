from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

from database import Base

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


def to_entity[M: Base, E: DataclassInstance](db_model: M, entity_cls: type[E]) -> E:
    kwargs_dict = {
        attr.name: getattr(db_model, attr.name) for attr in fields(entity_cls)
    }

    return entity_cls(**kwargs_dict)


def to_entities[M: Base, E: DataclassInstance](
    db_models: list[M], entity_cls: type[E]
) -> list[E]:
    return [to_entity(db_model, entity_cls) for db_model in db_models]
