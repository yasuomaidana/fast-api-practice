from fastapi import APIRouter
from fastapi.params import Depends

from auth import AuthHandler

invoice_router = APIRouter(prefix="/invoice", tags=["Invoice"])
nested_router = APIRouter(prefix="/nested")

@nested_router.get("")
async def nested():
    return {"nested": "nested"}

invoice_router.include_router(nested_router)

@invoice_router.get("/{invoice_id}")
async def get_invoice(invoice_id: int, user=Depends(AuthHandler().auth_wrapper)):
    print(user)
    return {"id": invoice_id}
