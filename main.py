from fastapi import FastAPI

from controller import invoice_router, place_router, auth_router

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
    uvicorn.run(app, host="localhost", port=8000)
