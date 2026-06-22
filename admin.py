from sqladmin import Admin, ModelView

from database import engine
from models import BoardModel, TaskModel, UserModel


class UserModelAdmin(ModelView, model=UserModel):
    pass


class TaskModelAdmin(ModelView, model=TaskModel):
    pass


class BoardModelAdmin(ModelView, model=BoardModel):
    pass


def setup_admin(app):
    admin = Admin(app, engine)
    admin.add_view(UserModelAdmin)
    admin.add_view(TaskModelAdmin)
    admin.add_view(BoardModelAdmin)
