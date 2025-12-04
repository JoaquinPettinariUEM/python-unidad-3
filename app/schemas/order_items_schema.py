from pydantic import BaseModel

class OrderItemsBase(BaseModel):
  order_id: int
  product_id: int
  quantity: int

class OrderItemsResponse(OrderItemsBase):
  pass

class OrderItems:
  id: int
