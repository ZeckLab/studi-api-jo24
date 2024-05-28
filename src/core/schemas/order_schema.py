from pydantic import BaseModel, ConfigDict

from src.core.schemas.ticket_schema import OffersTicketCreate

class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name : str
    date_time : str

class Payment(BaseModel):
    card_number : str
    card_expiry : str
    card_cvc : str
    mount : float

class CartItem(BaseModel):
    offer_name : str
    quantity : int

class OrderCreate(BaseModel):
    cart : list[CartItem]
    payment : Payment
    nb_people : int
    
class OrderInDB(OrderBase):
    order_id : int
    user_id : int

class OrderTransaction(OrderInDB):
    transaction : str

class OrderKeygen(OrderInDB):
    keygen : str