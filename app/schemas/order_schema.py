from pydantic import BaseModel

class OrderBase(BaseModel):
  next_id: int

class OrderBaseResponse(OrderBase):
  pass

class Order:
  id: int
