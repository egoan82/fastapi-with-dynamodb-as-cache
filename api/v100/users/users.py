from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from api.v100.schemas.users import UserRead, UserCreate, UserUpdate
from businesslogic.users import BusinessLogicUsers
from db.database import get_session

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
async def list(
        logic: BusinessLogicUsers = Depends(BusinessLogicUsers),
        session: Session = Depends(get_session),
):
    return logic.list(db=session)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def get_one(
        id: UUID,
        logic: BusinessLogicUsers = Depends(BusinessLogicUsers),
        session: Session = Depends(get_session),
):
    user_db = logic.get_one(db=session, id=id)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    return user_db


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
async def create(
        user: UserCreate,
        logic: BusinessLogicUsers = Depends(BusinessLogicUsers),
        session: Session = Depends(get_session),
):
    return logic.create(db=session, user=user)


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def update(
        id: UUID,
        user: UserUpdate,
        logic: BusinessLogicUsers = Depends(BusinessLogicUsers),
        session: Session = Depends(get_session),
):
    return logic.update(db=session, id=id, user=user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
        id: UUID,
        logic: BusinessLogicUsers = Depends(BusinessLogicUsers),
        session: Session = Depends(get_session),
):
    return logic.delete(db=session, id=id)
