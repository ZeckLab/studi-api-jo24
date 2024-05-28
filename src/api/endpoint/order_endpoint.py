from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.endpoint.authenticate_endpoint import get_current_user
from src.core.schemas.order_schema import OrderInDB, OrderCreate
import src.core.controllers.order_controller as order_controller
from src.core.config.database import get_db
from src.core.config.security import authentication_mode
from src.core.schemas.ticket_schema import TicketPublic


router = APIRouter()

'''Create a new order'''
@router.post("", dependencies=[Depends(authentication_mode)], response_model=TicketPublic)
async def create_offer(offer_in: OrderCreate, db=Depends(get_db), user= Depends(get_current_user)):       
    # Create the order
    ticket_public : TicketPublic = await order_controller.create(db, offer_in, user)
    return ticket_public