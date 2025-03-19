from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_201_CREATED

from dto.user.create_user_dto import CreateUserDto
from service.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", status_code=HTTP_201_CREATED, responses={400: {"description": "User already exists"}})
async def register(user: CreateUserDto):
    user_service = UserService()
    try:
        user_service.register(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already registered")
