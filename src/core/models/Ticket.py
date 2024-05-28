from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Text
from src.core.config.database import Base
from sqlalchemy.orm import relationship
from src.core.models.Order import Order

class OffersTicket(Base):
    __tablename__ = "offers_ticket"

    ticket_id = Column(Integer, ForeignKey("tickets.ticket_id"), primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.offer_id"), primary_key=True)
    quantity = Column(Integer, CheckConstraint("quantity > 0"), nullable=False)
    
    offer = relationship("Offer")
    
    def __repr__(self):
        return f"Offer: {self.offer.title}  - Quantity: {self.quantity}"

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    keygen_qrcode = Column(Text, nullable=True, unique=True)
    offers = relationship("OffersTicket")
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    
    order = relationship(Order)
    
    def __repr__(self):
        return f"Ticket: {self.keygen_qrcode}"