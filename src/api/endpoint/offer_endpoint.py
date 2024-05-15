from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.schemas.offer_schema import OfferInDB, OfferBase
from src.core.models.Offer import Offer
import src.core.controllers.offer_controller as offer_controller
from src.core.config.database import get_db
from .constants import ErrorCode


router = APIRouter()

'''Create a new offer'''
@router.post("", response_model=OfferInDB)
async def create_offer(offer_in: OfferBase, db=Depends(get_db)):
    # Check if the offer title already exists
    offer_title_exist = await offer_controller.get_by_title(db, offer_in.title)
    if offer_title_exist is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.OFFER_TITLE_ALREADY_EXISTS)
    
    # Create the offer
    offer_in_db : OfferInDB = await offer_controller.create(db, offer_in)
    return offer_in_db


'''Get all offers'''
@router.get("", response_model=list[OfferInDB])
async def get_all(db: Session = Depends(get_db)):
    offer_list = await offer_controller.get_all(db, "all")
    return offer_list


'''Get all offers visible'''
@router.get("/visible", response_model=list[OfferInDB])
async def get_all_visible(db: Session = Depends(get_db)):
    offer_list = await offer_controller.get_all(db, "visible")
    return offer_list


'''Get a offer by id'''
@router.get("/{offer_id}", response_model=OfferInDB)
async def get_offer(offer_id: int, db=Depends(get_db)):
    # Check if the offer exists
    offer = db.get(Offer, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.OFFER_NOT_FOUND)
    
    # Get the offer
    offer_return = await offer_controller.get_by_id(db, offer_id)
    return offer_return


'''Update a offer'''
@router.put("/{offer_id}", response_model=OfferInDB)
async def update_offer(offer_id: int, offer_in: OfferBase, db=Depends(get_db)):
    # Check if the offer exists
    offer = db.get(Offer, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.OFFER_NOT_FOUND)
    
    # Check if the offer title already exists only if the title has changed
    if offer_in.title is not None and offer_in.title != offer.title:
        offer_title_exist = await offer_controller.get_by_title(db, offer_in.title)
        if offer_title_exist is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.OFFER_TITLE_ALREADY_EXISTS)
    
    # Update the offer
    offer_return: OfferInDB = await offer_controller.update(offer, offer_in, db)
    return offer_return

'''Update a offer visibility'''
@router.put("/{offer_id}/visible", response_model=OfferInDB)
async def update_offer_visibility(offer_id: int, db=Depends(get_db)):
    # Check if the offer exists
    offer = db.get(Offer, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.OFFER_NOT_FOUND)
    
    # Update the offer visibility
    offer_return: OfferInDB = await offer_controller.update_visibility(offer, db)
    return offer_return