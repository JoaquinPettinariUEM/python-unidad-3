from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.orders_services import get_all_orders, get_order, create_order
from app.schemas.order_schema import OrderResponse, OrderCreate
from app.dependencies.utils import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def get_products_route(db: Session = Depends(get_db)):
    return get_all_orders(db)

@router.get("/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return get_order(db, order_id)

@router.post("/")
def create_user_route(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

