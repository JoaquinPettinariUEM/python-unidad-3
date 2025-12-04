from fastapi import HTTPException
from sqlalchemy.orm import Session
import json

from app.schemas.product_schema import ProductBase
from app.models.product_model import Product
from app.structures.tree import Tree

tree = Tree()
PRODUCTS_PATH = "app/data/products.json"

def get_products(db: Session):
  return db.query(Product).all()

def create_product(db: Session, product: ProductBase):
  db_product = Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  product_dict = {
      "id": db_product.id,
      "name": db_product.name,
      "price": db_product.price,
  }

  write_product_in_json(product_dict)

  return db_product

def get_product_on_tree(product_id: int):
    product = tree.search(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return product

def preload_products(db: Session, path=PRODUCTS_PATH):
    try:
        with open(path, "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        print("No products.json found.")
        return

    print("🔄 Preloading products...")

    for p in products:
        existing = db.query(Product).filter(Product.id == p["id"]).first()
        if not existing:
            obj = Product(**p)
            db.add(obj)

        tree.insert(p)

    db.commit()
    print("✅ Products loaded into DB and BST")



def write_product_in_json(product_data: dict):
    tree.insert(product_data)

    try:
        with open(PRODUCTS_PATH, "r") as file:
            products = json.load(file)
    except FileNotFoundError:
        products = []

    products.append(product_data)

    try:
      with open(PRODUCTS_PATH, "w") as file:
          json.dump(products, file, indent=4)

    except FileNotFoundError:
        products = []
    return product_data
