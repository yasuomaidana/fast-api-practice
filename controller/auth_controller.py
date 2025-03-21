from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from auth import OAuthProvider
from dto.user.create_user_dto import CreateUserDto
from dto.user.login_dto import LoginDto
from service.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
user_service = UserService()


@auth_router.post("/register", status_code=HTTP_201_CREATED,
                  responses={HTTP_400_BAD_REQUEST: {"description": "User already exists"}})
async def register(user: CreateUserDto):
    try:
        user_service.register(user)
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Username or email already registered")


@auth_router.post("/login", status_code=HTTP_200_OK,
                  responses={HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"}})
async def login(login_input: LoginDto):
    user = user_service.find_account(login_input.username)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid username")
    verified = user_service.auth_handler.verify_password(login_input.password, user.password)
    if not verified:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = user_service.auth_handler.encode_token(user.username)
    return {"token": token}


oauth_router = APIRouter(prefix="/oauth", tags=["OAuth2"])
@oauth_router.post("/token")
async def oauth_token(token: Annotated[OAuthProvider().password_request_form, Depends()]):
    print(token.username, token.password)
    return {"token": token}


auth_router.include_router(oauth_router)