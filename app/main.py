from fastapi import FastAPI
from dotenv import load_dotenv

from app.database import Base, engine
from app.routers import orders_routers, products_routers


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products_routers.router)
# app.include_router(orders_routers.router)
