from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_schema import ProductBase, ProductResponse
from app.dependencies.utils import get_db
from app.services.products_services import get_products, create_product, get_product_on_tree

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_products_route(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}")
def get_product_by_id(product_id: int):
    return get_product_on_tree(product_id)

@router.post("/", response_model=ProductResponse)
def create_user_route(product: ProductBase, db: Session = Depends(get_db)):
    return create_product(db, product)

