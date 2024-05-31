from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.schemas.offer_schema import OfferInDB, OfferBase, OfferTitleExist
from src.core.models.Offer import Offer
import src.core.controllers.offer_controller as offer_controller
from src.core.config.database import get_db
from .constants import ErrorCode
from src.core.config.security import authentication_mode
from src.api.endpoint.authenticate_endpoint import get_admin_in_token


router = APIRouter()

'''Create a new offer - admin only'''
@router.post("", dependencies=[Depends(get_admin_in_token)], response_model=OfferInDB)
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
async def get_all(db: Session = Depends(get_db), c: str | None = None, orderby: str | None = None):
    """
        Get all offers :
        Can be sorted by column_name c  as /api/offers?c=column_name&orderby=asc|desc
    """
    offer_list = await offer_controller.get_all(db, "all", (c if c is not None else ""), (orderby if orderby is not None else ""))
    return offer_list


'''Get all offers visible'''
@router.get("/visible", response_model=list[OfferInDB])
async def get_all_visible(db: Session = Depends(get_db), c: str | None = None, orderby: str | None = None):
    """
        Get all offers visible :
        Can be sorted by column_name c  as /api/offers/visible?c=column_name&orderby=asc|desc
    """
    
    offer_list = await offer_controller.get_all(db, "visible", (c if c is not None else ""), (orderby if orderby is not None else ""))
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


'''Get a offer by title'''
@router.get("/title/{title}", response_model=OfferTitleExist)
async def get_offer_by_title(title: str, db=Depends(get_db)):
    title_exist = OfferTitleExist(title=title, exist=False)
    
    # Check if the offer exists
    offer = await offer_controller.get_by_title(db, title)
    if offer:
        title_exist.exist = True
    
    # Get the offer
    return title_exist


'''Update a offer - admin only'''
@router.put("/{offer_id}", dependencies=[Depends(get_admin_in_token)], response_model=OfferInDB)
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


'''Update a offer visibility - admin only'''
@router.patch("/{offer_id}/visible", dependencies=[Depends(get_admin_in_token)], response_model=OfferInDB)
async def update_offer_visibility(offer_id: int, db=Depends(get_db)):
    # Check if the offer exists
    offer = db.get(Offer, offer_id)
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.OFFER_NOT_FOUND)
    
    # Update the offer visibility
    offer_return: OfferInDB = await offer_controller.update_visibility(offer, db)
    return offer_return