from typing import Annotated

from fastapi import Depends, HTTPException, status

from deps.board_member import get_board_member_or_403
from deps.service_factories import get_board_service
from models import BoardMemberModel, BoardModel
from services import BoardService


# authorize first using get_board_member_or_403 and only then check if board exists and return it
# this avoids leaking board IDs that exist or don't exist in the DB
def get_authorized_board_or_404(
    board_id: int,
    _: Annotated[BoardMemberModel, Depends(get_board_member_or_403)],
    service: Annotated[BoardService, Depends(get_board_service)],
) -> BoardModel:
    board = service.get_board(board_id)

    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    return board


def get_all_boards(
    service: Annotated[BoardService, Depends(get_board_service)],
) -> list[BoardModel]:
    return service.list_boards()
