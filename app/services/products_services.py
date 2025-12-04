from sqlalchemy.orm import Session

from app.schemas.product_schema import ProductResponse, ProductBase
from app.models.product_model import Product

def get_products(db: Session):
  return db.query(Product).all()

def create_product(db: Session, product: ProductBase):
  db_product = Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)

  return db_product
