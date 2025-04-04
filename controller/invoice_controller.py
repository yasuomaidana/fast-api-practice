from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_403_FORBIDDEN

from auth import AuthHandler, OAuthProvider

invoice_router = APIRouter(prefix="/invoice", tags=["Invoice"])
nested_router = APIRouter(prefix="/nested", tags=["Invoice", "Nested"])

nested_secured_router = APIRouter(prefix="/nested_secured", tags=["Invoice", "Nested", "Secured"],
                                  dependencies=[Depends(AuthHandler().auth_wrapper)],
                                  responses={HTTP_403_FORBIDDEN: {"description": "Forbidden"}})


@nested_router.get("")
async def nested():
    return {"nested": "nested"}

@nested_router.get("/oauth_secured")
async def nested_oauth_secured(user=Depends(OAuthProvider().oauth2_scheme)):
    return user


@nested_secured_router.get("")
async def nested_secured():
    """
    Endpoint to get a secured nested message.
    It does not do anything, but needs authentication.
    This endpoint is protected by authentication.
    """
    return {"nested": "Hey there"}

@nested_secured_router.get("/message")
async def nested_secured(user=Depends(AuthHandler().auth_wrapper)):
    """
    Endpoint to get a secured nested message. It retrieves the user from the token.
    """
    return user


invoice_router.include_router(nested_router)
invoice_router.include_router(nested_secured_router)


@invoice_router.get("/{invoice_id}")
async def get_invoice(invoice_id: int, user=Depends(AuthHandler().auth_wrapper)):
    print(user)
    return {"id": invoice_id}
