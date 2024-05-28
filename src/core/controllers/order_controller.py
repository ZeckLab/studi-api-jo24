from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.core.controllers import ticket_controller
from src.core.controllers.utils import create_name_order, create_qrcode_ticket, create_transaction_order
from src.core.models.Ticket import Ticket
from src.core.models.User import User
from src.core.models.Order import Order
from src.core.schemas.order_schema import OrderCreate, Payment
from src.core.schemas.ticket_schema import TicketPublic
from src.core.config.security import get_keygen_order_hash, get_transaction_hash

'''Create a new order in the database'''
async def create(db: Session, order: OrderCreate, user: User) -> TicketPublic:
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
    qrcode_ticket = create_qrcode_ticket(user.keygen, new_order.keygen)
    new_ticket = Ticket(keygen_qrcode= user.keygen+keygen, order_id=new_order.order_id)
    
    await ticket_controller.save(db, new_ticket, order.cart)
    
    # Return the user in a StaffInDB : model Pydantic
    return TicketPublic(qrcode=qrcode_ticket, last_name=user.last_name, first_name=user.first_name, nb_places=order.nb_people)