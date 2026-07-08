from sqladmin import Admin, ModelView

from database import engine
from models import BoardMemberModel, BoardModel, TaskModel, UserModel


class UserModelAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.username,
        UserModel.birth,
        UserModel.created_at,
    ]
    column_details_exclude_list = [UserModel.tasks, UserModel.memberships]


class TaskModelAdmin(ModelView, model=TaskModel):
    column_list = [
        TaskModel.id,
        TaskModel.title,
        TaskModel.description,
        TaskModel.user_id,
        TaskModel.board_id,
        TaskModel.created_at,
    ]


class BoardModelAdmin(ModelView, model=BoardModel):
    column_list = [
        BoardModel.id,
        BoardModel.title,
        BoardModel.created_at,
    ]


class BoardMemberModelAdmin(ModelView, model=BoardMemberModel):
    column_list = [
        BoardMemberModel.user_id,
        BoardMemberModel.board_id,
        BoardMemberModel.role,
    ]


def setup_admin(app):
    admin = Admin(app, engine)
    admin.add_view(UserModelAdmin)
    admin.add_view(TaskModelAdmin)
    admin.add_view(BoardModelAdmin)
    admin.add_view(BoardMemberModelAdmin)
