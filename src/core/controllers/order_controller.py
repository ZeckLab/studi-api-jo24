from datetime import datetime, timezone
from sqlalchemy import Select, func
from sqlalchemy.orm import Session

from src.core.controllers import ticket_controller, user_controller
from src.core.controllers.utils import create_name_order, create_transaction_order
from src.core.models.Ticket import Ticket
from src.core.models.User import User
from src.core.models.Order import Order
from src.core.schemas.offer_schema import OfferOrderView
from src.core.schemas.order_schema import OrderBase, OrderCreate, OrderInDB, OrderViewAdmin, OrderViewUser, OrdersView, Payment
from src.core.schemas.ticket_schema import OffersTicketView, TicketPublic
from src.core.config.security import get_keygen_order_hash, get_transaction_hash
from src.core.config import config
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

'''Get order by name'''
async def get_by_name(db: Session, order_name: str) -> Order:
    '''Get the order by name
    :param db: the database session
    :param order_name: the order name
    :return: the order id
    '''
    statement = Select(Order).where(Order.name == order_name)
    order = db.execute(statement).scalars().one()
    
    return order


'''Get all orders'''
async def get_all(db: Session, user: User) -> OrdersView:
    '''Get all orders
    if the user is a user, it will return all orders for the user and the ticket associated
    else, it will return all orders for the back-office
    :param db: the database session
    :param user: the user
    :return: a list of orders with the details of the order and the ticket associated for the user
        and the list of orders for the back-office
    '''
    
    user_role = config.USER_WEB_APPLICATION_NAME_ROLE in user_controller.get_user_roles(user)
    
    count_order_stm = Select(func.count(Order.order_id)).select_from(Order)
    statement = Select(Order)
    
    # if the user is an application user, get all orders for the user
    if user_role:
        count_order_stm = count_order_stm.where(Order.user_id == user.user_id)
        statement = statement.where(Order.user_id == user.user_id)
    
    # order by date_time descending
    statement = statement.order_by(Order.date_time.desc())
    
    count_orders = db.execute(count_order_stm).scalars().one()
    print(count_orders)
    result = db.execute(statement).scalars().all()
    
    orders_user = []
    
    # get the mount and the number of places for each order
    for row in result:
        ticket_public, details, places, mount = await ticket_controller.get_ticket_offers_by_order(db, row)
    
        if user_role:
            order_user = OrderViewUser(name= row.name, date_time= row.date_time, ticket=ticket_public, details= details)
            orders_user.append(order_user)
        else:
            order_user = OrderViewAdmin(name= row.name, date_time= row.date_time, user= f"{row.user.first_name} {row.user.last_name}", mount=mount, places=places)
            orders_user.append(order_user)
    
    return OrdersView(orders=orders_user, count=count_orders)
