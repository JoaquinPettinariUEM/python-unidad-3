from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.product_model import Product

def map_order_to_response(order, db: Session) -> Dict[str, Any]:
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
