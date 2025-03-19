from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_403_FORBIDDEN

from auth import AuthHandler

invoice_router = APIRouter(prefix="/invoice", tags=["Invoice"])
nested_router = APIRouter(prefix="/nested", tags=["Invoice", "Nested"])

nested_secured_router = APIRouter(prefix="/nested_secured", tags=["Invoice", "Nested", "Secured"],
                                  dependencies=[Depends(AuthHandler().auth_wrapper)],
                                  responses={HTTP_403_FORBIDDEN: {"description": "Forbidden"}})


@nested_router.get("")
async def nested():
    return {"nested": "nested"}


@nested_secured_router.get("")
async def nested_secured():
    return {"nested": "Hey there"}

@nested_secured_router.get("/message")
async def nested_secured(user=Depends(AuthHandler().auth_wrapper)):
    return user


invoice_router.include_router(nested_router)
invoice_router.include_router(nested_secured_router)


@invoice_router.get("/{invoice_id}")
async def get_invoice(invoice_id: int, user=Depends(AuthHandler().auth_wrapper)):
    print(user)
    return {"id": invoice_id}
