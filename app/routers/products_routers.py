from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_schema import ProductBase, ProductResponse
from app.dependencies.utils import get_db
from app.services.products_services import get_products, create_product

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_products_route(db: Session = Depends(get_db)):
    return get_products(db)

@router.post("/", response_model=ProductResponse)
def create_user_route(product: ProductBase, db: Session = Depends(get_db)):
    return create_product(db, product)
