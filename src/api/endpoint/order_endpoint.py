from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.endpoint.authenticate_endpoint import get_admin_in_token, get_user_in_token
from src.api.endpoint.constants import ErrorCode
from src.core.config import config
from src.core.controllers import ticket_controller
from src.core.schemas.order_schema import OrderInDB, OrderCreate, OrderViewUser, OrdersView, TicketOffers
import src.core.controllers.order_controller as order_controller
from src.core.config.database import get_db
from src.core.config.security import authentication_mode
from src.core.schemas.ticket_schema import TicketPublic


router = APIRouter()

'''Create a new order'''
@router.post("", dependencies=[Depends(authentication_mode)], response_model=OrderInDB)
async def create_order(offer_in: OrderCreate, db=Depends(get_db), user= Depends(get_user_in_token)):
    '''Create a new order
    :param offer_in: the order to create
    :param db: the database session
    :param user: the user who creates the order
    :return: the order created in the database'''
    
    # Create the order
    order_in_db : OrderInDB = await order_controller.create(db, offer_in, user)
    return order_in_db


'''Get all orders'''
@router.get("", dependencies=[Depends(authentication_mode)], response_model=OrdersView)
async def get_orders(db: Session = Depends(get_db), user= Depends(get_user_in_token), skip: int = 0, limit: int = config.LIMIT_DISPLAY_ORDERS):
    '''Get all orders
    if the user is not an admin, it will return all orders for the user
    else, it will return all orders for the back-office
    :param db: the database session
    :param user: the user
    :return: a list of orders
    '''
    
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    orders = await order_controller.get_all(db, user, skip, limit)
    
    return orders


'''Get orders by date'''
@router.get("/date/{order_date}", dependencies=[Depends(get_admin_in_token)], response_model=OrdersView)
async def get_orders_by_date(db: Session = Depends(get_db), order_date: str = None, skip: int = 0, limit: int = config.LIMIT_DISPLAY_ORDERS):
    '''Get all orders by date for the back-office
    :param order_date: the date of the orders
    :param db: the database session
    :return: a list of orders
    '''
    
    date_order = datetime.strptime(order_date, '%Y-%m-%d')
    if(date_order is None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.ORDER_DATE_INVALID)
    
    orders = await order_controller.get_all_by_date(db, date_order, skip, limit)
    
    return orders


@router.get("/{order_name}/details", dependencies=[Depends(get_admin_in_token)], response_model=TicketOffers)
async def get_order_details(order_name: str, db: Session = Depends(get_db)):
    '''Get all orders for the back-office
    :param db: the database session
    :param user: the user
    :return: a list of orders
    '''
        
    order = await order_controller.get_by_name(db, order_name)
    
    order_details = await ticket_controller.get_ticket_offers_by_order(db, order)
    
    return TicketOffers(ticket=order_details[0], details=order_details[1])