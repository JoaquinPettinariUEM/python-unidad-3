from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import OrderCreate
from app.dependencies.orders import map_order_to_response, build_linked_list

def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return map_order_to_response(order, db)

def get_all_orders(db: Session):
    orders = db.query(Order).all()
    return [map_order_to_response(order, db) for order in orders]


def create_order(db: Session, order_data: OrderCreate):
    order = Order()
    db.add(order)
    db.commit()
    db.refresh(order)
    head_id = build_linked_list(db, order.id, order_data.items)
    if head_id is not None:
        order.head_id = head_id
    db.add(order)
    db.commit()
    db.refresh(order)

    return order

def update_order(db: Session, order_id: int, items: list):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()

    head_id = build_linked_list(db, order_id, items)
    if head_id is not None:
        order.head_id = head_id
    db.add(order)
    db.commit()
    db.refresh(order)

    return order

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(404, "Not found order")

    db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()

    db.delete(order)
    db.commit()
    return order
