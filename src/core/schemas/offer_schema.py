from pydantic import BaseModel, ConfigDict, Field

# Offer Schema : Pydantic Model
# By default, the visible attribute is not required because it has a default value in the database.
class OfferBase(BaseModel):
    title: str
    description: str
    nb_people: int = Field(gt=0)
    price: float = Field(gt=0.0)
    image_url: str

# A schema to validate an offer in the database
class OfferInDB(OfferBase):
    model_config = ConfigDict(from_attributes=True)
    
    offer_id: int
    visible: bool

# A schema to view an offer with the minimum of information
class OfferOrderView(BaseModel):
    title: str
    nb_people: int
    price: float


class OfferTitleExist(BaseModel):
    title: str
    exist: bool