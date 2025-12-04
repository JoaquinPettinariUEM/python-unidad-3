from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import OrderCreate

from typing import List, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.models.product_model import Product


def get_order(db: Session, order_id: int) -> List[Dict[str, Any]]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    nodes = []
    current = order.head
    while current:
        nodes.append(current)
        current = current.next

    if not nodes:
        return []

    product_ids = [node.product_id for node in nodes]
    products = db.query(Product).filter(Product.id.in_(set(product_ids))).all()
    product_map = {product.id: product for product in products}

    result: List[Dict[str, Any]] = []
    for node in nodes:
        product = product_map.get(node.product_id)
        if product:
            result.append({"name": product.name, "price": product.price})
        else:
            result.append({"name": None, "price": None})

    return result


def get_all_orders(db: Session):
    return db.query(Order).all()

def create_order(db: Session, order_data: OrderCreate):
    order = Order()
    db.add(order)
    db.commit()
    db.refresh(order)

    previous_node = None
    head_node = None

    for item in order_data.items:
        node = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(node)
        db.commit()
        db.refresh(node)

        if head_node is None:
            head_node = node
        else:
            if(previous_node is not None):
              previous_node.next_id = node.id

        previous_node = node
    if head_node:
      order.head_id = head_node.id
    db.add(order)
    db.commit()
    db.refresh(order)

    return order
