from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.core.schemas.ticket_schema import OffersTicketCreate, OffersTicketView, TicketPublic

class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name : str
    date_time : datetime

# A schema to validate a payment during the creation of an order
class Payment(BaseModel):
    card_number : str
    card_expiry : str
    card_cvc : str
    mount : float

# A schema to validate a element of the cart
# during the creation of an order
class CartItem(BaseModel):
    offer_name : str
    quantity : int

# A schema to validate the creation of an order
class OrderCreate(BaseModel):
    cart : list[CartItem]
    payment : Payment
    nb_people : int

# A schema to view an order with the ticket associated
# and the information of the offers associated to the ticket
class OrderViewUser(OrderBase):
    ticket: TicketPublic
    details: list[OffersTicketView]


class OrderInDB(OrderBase):
    order_id : int
    user_id : int

class OrderTransaction(OrderInDB):
    transaction : str

class OrderKeygen(OrderInDB):
    keygen : str