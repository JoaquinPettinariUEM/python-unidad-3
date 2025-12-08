from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_schema import ProductBase, ProductResponse
from app.dependencies.utils import get_db
from app.services.products_services import get_products, create_product, get_product_on_tree, update_product, delete_product

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

@router.put("/{product_id}")
def update_product_route(
    product_id: int,
    product: ProductBase,
    db: Session = Depends(get_db)
):
    return update_product(
        db,
        product_id,
        name=product.name,
        price=product.price
    )

@router.delete("/{product_id}")
def delete_product_router(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)
