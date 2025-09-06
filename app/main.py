from fastapi import FastAPI

from .routers import orders, operators, import_excel
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(orders.router)
app.include_router(operators.router)
app.include_router(import_excel.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
