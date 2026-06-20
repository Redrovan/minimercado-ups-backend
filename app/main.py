from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routes.productos import router as producto_router

app = FastAPI(
    title="Minimercado UPS"
)

Base.metadata.create_all(bind=engine)

app.include_router(producto_router)


@app.get("/")
def root():

    return {
        "mensaje": "Backend Minimercado UPS"
    }