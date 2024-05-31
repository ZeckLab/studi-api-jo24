from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.endpoint.authenticate_endpoint import get_user_in_token
from src.core.schemas.order_schema import OrderInDB, OrderCreate, OrderViewUser
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


'''Get all orders of the current user with the details of the order'''
@router.get("", dependencies=[Depends(authentication_mode)], response_model=list[OrderViewUser])
async def get_orders(db: Session = Depends(get_db), user= Depends(get_user_in_token)):
    '''Get all orders of the current user with the details of the order
    :param db: the database session
    :param user: the user
    :return: a list of orders with the details of the order and the ticket associated
    '''
    
    if(user is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    orders = await order_controller.get_all_for_user(db, user)
    
    return orders
