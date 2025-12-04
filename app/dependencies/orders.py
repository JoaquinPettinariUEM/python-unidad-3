from typing import Dict, Any
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.models.order_item_model import OrderItem
from app.models.order_model import Order

def map_order_to_response(order: Order, db: Session) -> Dict[str, Any]:
    nodes = []
    current = order.head
    while current:
        nodes.append(current)
        current = current.next

    if not nodes:
        return {"order_id": order.id, "items": []}

    product_ids = [node.product_id for node in nodes]
    products = db.query(Product).filter(Product.id.in_(set(product_ids))).all()
    product_map = {p.id: p for p in products}

    items = []
    for node in nodes:
        product = product_map.get(node.product_id)
        if product:
            items.append({
                "name": product.name,
                "price": product.price
            })
        else:
            items.append({
                "name": None,
                "price": None
            })

    return {
        "order_id": order.id,
        "items": items
    }

def build_linked_list(db: Session, order_id, items: list):
    previous_node = None
    head_node = None

    for item in items:
        node = OrderItem(
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(node)
        db.flush()

        if head_node is None:
            head_node = node
        else:
            if previous_node is not None:
                previous_node.next_id = node.id
            db.add(previous_node)

        previous_node = node

    return head_node.id if head_node else None

