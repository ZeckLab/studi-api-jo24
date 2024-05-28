from sqlalchemy.orm import Session

from src.core.controllers.offer_controller import get_by_title
from src.core.models import Offer
from src.core.models.Ticket import OffersTicket, Ticket
from src.core.schemas.order_schema import CartItem

''' Save a ticket in the database and create the association with the offers'''
async def save(db: Session, ticket : Ticket, cart: list[CartItem]) -> Ticket:
    # for each cart item, create a association betwwen the ticket and the offer
    for cart_item in cart:
        offer: Offer = await get_by_title(db, cart_item.offer_name)
        
        new_association = OffersTicket(offer= offer, quantity=cart_item.quantity)
        ticket.offers.append(new_association)
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return ticket