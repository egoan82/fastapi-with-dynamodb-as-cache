from fastapi import APIRouter

from api.v100.users import users

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
