from fastapi import APIRouter

invoice_router = APIRouter(prefix="/invoice")
nested_router = APIRouter(prefix="/nested")

@nested_router.get("")
async def nested():
    return {"nested": "nested"}

invoice_router.include_router(nested_router)

@invoice_router.get("/{invoice_id}")
async def get_invoice(invoice_id: int):
    return {"id": invoice_id}
