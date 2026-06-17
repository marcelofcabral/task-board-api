import store
from deps.users import get_user_or_404
from fastapi import APIRouter, Depends, status
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])


# Read all users
@router.get("", response_model=list[UserResponse])
async def read_all_users():
    return store.users


# Read user
@router.get("/{id}", response_model=UserResponse)
async def read_user(user=Depends(get_user_or_404)):
    return user


# Create user
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    new_user = UserResponse(**user.model_dump(), id=store.next_user_id)
    store.users[store.next_user_id] = new_user

    store.next_user_id = store.next_user_id + 1

    return new_user


# Update user
@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserResponse, _=Depends(get_user_or_404)):
    store.users[id] = user

    return user


# Delete user
@router.delete("/{id}", response_model=UserResponse)
async def delete_user(id: int, _=Depends(get_user_or_404)):
    user = store.users[id]
    del store.users[id]

    return user
