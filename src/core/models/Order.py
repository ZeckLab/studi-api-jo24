from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text
from src.core.config.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), index=True, nullable=False, unique=True)
    date_time = Column(DateTime, nullable=False)
    transaction = Column(String(256), nullable=False)
    keygen = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    user = relationship("User", back_populates="orders")
    
    def __repr__(self):
        return f"Order: {self.name} - Date: {self.date_time}"