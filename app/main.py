from fastapi import FastAPI

from .routers import orders, operators
from .database import init_db

init_db()

app = FastAPI()

app.include_router(orders.router)
app.include_router(operators.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
