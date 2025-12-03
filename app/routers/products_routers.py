from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_schema import Product
from app.dependencies.utils import get_db
from app.services.products_services import get_products

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[Product])
def get_products_route(db: Session = Depends(get_db)):
    return get_products(db)
