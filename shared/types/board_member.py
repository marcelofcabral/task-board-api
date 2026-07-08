import enum


class BoardMemberRole(str, enum.Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
