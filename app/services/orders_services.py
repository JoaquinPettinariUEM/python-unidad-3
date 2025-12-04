from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import OrderCreate
from app.dependencies.orders import map_order_to_response

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

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(404, "Not found order")

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id)

    for order_item in order_items:
        db.delete(order_item)
        db.commit()

    db.delete(order)
    db.commit()
    return order
