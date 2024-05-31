from datetime import datetime, timezone
from sqlalchemy import Select
from sqlalchemy.orm import Session

from src.core.controllers import ticket_controller
from src.core.controllers.utils import create_name_order, create_transaction_order
from src.core.models.Ticket import Ticket
from src.core.models.User import User
from src.core.models.Order import Order
from src.core.schemas.offer_schema import OfferOrderView
from src.core.schemas.order_schema import OrderCreate, OrderInDB, OrderViewUser, Payment
from src.core.schemas.ticket_schema import OffersTicketView, TicketPublic
from src.core.config.security import get_keygen_order_hash, get_transaction_hash
from typing import Tuple

from src.core.utils.qr_code import generate_qrcode

'''Create a new order in the database'''
async def create(db: Session, order: OrderCreate, user: User) -> OrderInDB:
    '''Create a new order in the database
    :param db: the database session
    :param order: the order to create
    :param user: the user who creates the order
    :return: the order created in the database
    '''
    # Create the order object
    date_time_now = datetime.now(tz=timezone.utc)
    name_order = create_name_order(date_time_now, user)
    transaction = get_transaction_hash(create_transaction_order(Payment.model_validate(order.payment)))
    keygen = get_keygen_order_hash(date_time_now.strftime('%Y%m%d%H%M%S'))
    new_order = Order(name=name_order, date_time=date_time_now, transaction=transaction, keygen=keygen, user_id=user.user_id)
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Create the order ticket
    new_ticket = Ticket(keygen_qrcode= user.keygen+keygen, order_id=new_order.order_id)
    
    await ticket_controller.save(db, new_ticket, order.cart)
    
    # Return the user in a StaffInDB : model Pydantic
    return OrderInDB.model_validate(new_order)

'''Get all orders of the current user'''
async def get_all_for_user(db: Session, user: User) -> list[OrderViewUser]:
    '''Get all orders of the current user with the details of the order
    :param db: the database session
    :param user: the user
    :return: a list of orders with the details of the order and the ticket associated
    '''
    
    # prepare the query statement
    statement = Select(Order).where(Order.user_id == user.user_id).order_by(Order.date_time.desc())
    result = db.execute(statement).scalars().all()
    
    orders_user : list[OrderViewUser] = []
    
    # get the mount and the number of places for each order
    for row in result:
        ticket_public, details = await get_details(db, row.order_id)
        ticket_public.last_name= user.last_name;
        ticket_public.first_name= user.first_name;
        order_user = OrderViewUser(name= row.name, date_time= row.date_time, ticket=ticket_public, details= details)
        orders_user.append(order_user)
    
    return orders_user


'''Get the ticket linked to the order and the offers associated to the ticket'''
async def get_details(db: Session, order_id: int) -> Tuple[TicketPublic,list[OffersTicketView]]:
    '''Get the ticket linked to the order and the offers associated to the ticket - summary cart
    :param db: the database session
    :param order_id: the order id
    :return: the ticket to display and a list of offers associated to the ticket
    '''
    statement = Select(Ticket).where(Ticket.order_id == order_id)
    ticket: Ticket = db.execute(statement).scalars().first()

    places = 0
    details: list[OffersTicketView] = []
    
    # for each associated offer, get the offer and the quantity
    for ligne in ticket.offers:
        offer_in_view = OfferOrderView(**ligne.offer.__dict__)
        places += ligne.quantity * ligne.offer.nb_people
        details.append(OffersTicketView(quantity=ligne.quantity, offer=offer_in_view))
    
    qrcode = generate_qrcode(ticket.keygen_qrcode)
    ticket_public = TicketPublic(qrcode= qrcode, nb_places= places, last_name= "", first_name= "")
    
    return ticket_public, details
