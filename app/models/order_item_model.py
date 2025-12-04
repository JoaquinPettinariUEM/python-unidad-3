from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer)
    quantity = Column(Integer)

    next_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)

    next = relationship("OrderItem", remote_side=[id], uselist=False)
