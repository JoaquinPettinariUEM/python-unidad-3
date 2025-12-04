from pydantic import BaseModel
from typing import Optional, List

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    next_id: Optional[int] = None


class OrderItem(OrderItemBase):
    id: int

    model_config = {"from_attributes": True}


class OrderItemResponse(OrderItem):
    pass

class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderResponse(BaseModel):
    id: int
    items: List[OrderItemResponse]

    model_config = {"from_attributes": True}
