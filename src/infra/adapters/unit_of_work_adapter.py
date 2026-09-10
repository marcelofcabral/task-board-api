from sqlalchemy.orm import Session

from application.ports.unit_of_work_port import UnitOfWorkPort


class UnitOfWorkAdapter(UnitOfWorkPort):
    def __init__(self, db: Session) -> None:
        self.db = db

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
