from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    head_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)

    head = relationship("OrderItem", foreign_keys=[head_id], post_update=True)
