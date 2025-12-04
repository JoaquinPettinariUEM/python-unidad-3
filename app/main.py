from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.database import Base, engine, SessionLocal
from app.routers import orders_routers, products_routers
from app.services.products_services import preload_products

load_dotenv()


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        preload_products(db)
        yield
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(products_routers.router)
app.include_router(orders_routers.router)
