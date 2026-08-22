from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

from database import Base


def to_model[M: Base](value_object: object, db_model_cls: type[M]) -> M:
    kwargs_dict = {
        col_name: getattr(value_object, col_name)
        for col_name in db_model_cls.__table__.columns.keys()  # noqa: SIM118 - columns is not a dict
    }

    return db_model_cls(**kwargs_dict)


def apply_patch_to_model(
    db_model: Base, patch_value_object: "DataclassInstance"
) -> None:
    exclude_from_update = ("id", "created_at")

    column_names = db_model.__table__.columns.keys()

    for name in column_names:
        if name in exclude_from_update:
            continue

        attribute_value = getattr(patch_value_object, name)

        setattr(db_model, name, attribute_value)
