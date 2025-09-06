from fastapi import FastAPI

from .database import init_db
from .routers import operators, orders

init_db()

app = FastAPI()

app.include_router(orders.router)
app.include_router(operators.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
