from pydantic import BaseModel, ConfigDict

from src.core.schemas.offer_schema import OfferInDB

class OffersTicketBase(BaseModel):
    quantity: int

class OffersTicketCreate(OffersTicketBase):
    offer : OfferInDB
    quantity : int

class Ticket(BaseModel):
    keygen_qrcode: str
    offers: list[OffersTicketBase]

class TicketInDB(Ticket):
    ticket_id: int

class TicketPublic(BaseModel):
    qrcode: str
    last_name: str
    first_name: str
    nb_places: int