from sqlalchemy.orm import Session

from src.core.models.Offer import Offer
from src.core.schemas.offer_schema import OfferInDB, OfferBase

'''Get an offer by its id in the database'''
async def get_by_id(db: Session, id: int) -> OfferInDB:
    # Get the offer by its id
    result = db.query(Offer).filter(Offer.offer_id == id).first()
    
    # Return the offer in a OfferInDB : model Pydantic
    return OfferInDB(offer_id=result.offer_id, title=result.title, description=result.description, nb_people=result.nb_people, price=result.price, image_url = result.image_url, visible=result.visible)


'''Get an offer by its title in the database'''
async def get_by_title(db: Session, title: str) -> Offer | None:
    # Get the offer by its title
    session_offer = db.query(Offer).filter(Offer.title == title).first()
    
    # Return the offer
    return session_offer


'''Get all offers in the database or only the visible offers in the database'''
async def get_all(db: Session, type: str) -> list[OfferInDB]:
    result = []
    
    if type == "visible":
        # Get only the visible offers
        result = db.query(Offer).filter(Offer.visible == True).all()
    else:
        # Get all the offers
        result = db.query(Offer).all()
    
    # Return the list of offers offerInDB : model Pydantic
    return [OfferInDB(offer_id=row.offer_id, title=row.title, description=row.description, nb_people=row.nb_people, price=row.price, image_url = row.image_url,
                    visible=row.visible) for row in result]

'''Create an offer in the database'''
async def create(db: Session, offer: OfferBase) -> OfferInDB:
    # Create the offer object
    new_offer = Offer(title=offer.title, description=offer.description, nb_people=offer.nb_people, price=offer.price, image_url=offer.image_url)
    
    # Insert the offer object in the database
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    
    # Return the offer in a offerInDB : model Pydantic
    return OfferInDB(offer_id=new_offer.offer_id, title=new_offer.title, description=new_offer.description, nb_people=new_offer.nb_people, price=new_offer.price, image_url = new_offer.image_url, visible=new_offer.visible)

'''Update an offer in the database'''
async def update(offer: Offer, offer_in: OfferBase, db: Session) -> OfferInDB:
    # Update the offer if it exists
    offer.title = offer_in.title
    offer.description = offer_in.description
    offer.nb_people = offer_in.nb_people
    offer.price = offer_in.price
    offer.image_url = offer_in.image_url
    db.commit()
    db.refresh(offer)
    
    # Return the offer in a offerInDB : model Pydantic
    return OfferInDB(offer_id=offer.offer_id, title=offer.title, description=offer.description, nb_people=offer.nb_people, price=offer.price, image_url = offer.image_url, visible=offer.visible)

async def update_visibility(offer:Offer, db: Session) -> OfferInDB:
    # Update the offer visibility
    offer.visible = not offer.visible
    db.commit()
    db.refresh(offer)
    
    offer_db = OfferInDB.model_validate(offer)
    print(offer.offer_id)
    print(offer.title)
    
    # Return the offer in a offerInDB : model Pydantic
    return offer_db
