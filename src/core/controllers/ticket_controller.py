from typing import Tuple
from sqlalchemy import Select
from sqlalchemy.orm import Session

from src.core.controllers.offer_controller import get_by_title
from src.core.models import Offer, Order
from src.core.models.Ticket import OffersTicket, Ticket
from src.core.schemas.offer_schema import OfferOrderView
from src.core.schemas.order_schema import CartItem
from src.core.schemas.ticket_schema import OffersTicketView, TicketPublic
from src.core.utils.qr_code import generate_qrcode

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


'''Get the ticket linked to the order and the offers associated to the ticket'''
async def get_ticket_offers_by_order(db: Session, order: Order) -> Tuple[TicketPublic,list[OffersTicketView],int,float]:
    '''Get the ticket linked to the order and the offers associated to the ticket - summary cart
    :param db: the database session
    :param order: the order
    :return: the ticket to display and a list of offers associated to the ticket
    '''
    statement = Select(Ticket).where(Ticket.order_id == order.order_id)
    ticket: Ticket = db.execute(statement).scalars().first()

    places = 0
    mount = 0.0
    details: list[OffersTicketView] = []
    
    # for each associated offer, get the offer and the quantity
    for ligne in ticket.offers:
        offer_in_view = OfferOrderView(**ligne.offer.__dict__)
        places += ligne.quantity * ligne.offer.nb_people
        mount += ligne.quantity * ligne.offer.price
        details.append(OffersTicketView(quantity=ligne.quantity, offer=offer_in_view))
    
    qrcode = generate_qrcode(ticket.keygen_qrcode)
    ticket_public = TicketPublic(qrcode= qrcode, nb_places= places, last_name= order.user.last_name, first_name= order.user.first_name)
    
    return ticket_public, details, places, mount


'''Get the mount and the number of places on the ticket for the order'''
async def get_mount_places_by_order(db: Session, order: Order) -> Tuple[float, int]:
    '''Get the mount and the number of places on the ticket for the order
    :param db: the database session
    :param order: the order
    :return: the the mount and the number of places on the ticket for the order
    '''
    statement = Select(Ticket).where(Ticket.order_id == order.order_id)
    ticket: Ticket = db.execute(statement).scalars().first()

    places = 0
    mount = 0.0
    
    # for each associated offer, get the offer and the quantity
    for ligne in ticket.offers:
        places += ligne.quantity * ligne.offer.nb_people
        mount += ligne.quantity * ligne.offer.price
    
    return mount, places