from fastapi import FastAPI
from controller.invoice_controller import invoice_router
from controller.place_controller import place_router
from settings.database_settings import create_db_and_tables

app = FastAPI()
app.include_router(invoice_router)
app.include_router(place_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/wait")
async def wait_message():
    import time
    time.sleep(10)
    return {"message": "I waited for 10 seconds"}


if __name__ == "__main__":
    import uvicorn

    create_db_and_tables()
    uvicorn.run(app, host="localhost", port=8000)
