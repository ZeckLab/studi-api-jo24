from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.schemas.event_schema import EventInDB, EventBase
from src.core.models.Event import Event
import src.core.controllers.event_controller as event_controller
from src.core.config.database import get_db
from .constants import ErrorCode


router = APIRouter()

'''Create a new event'''
@router.post("", response_model=EventInDB)
async def create_event(event_in: EventBase, db=Depends(get_db)):
    # Check if the event title already exists
    event_title_exist = await event_controller.get_by_title(db, event_in.title)
    if event_title_exist is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.EVENT_TITLE_ALREADY_EXISTS)
    
    # Create the event
    event_in_db : EventInDB = await event_controller.create(db, event_in)
    return event_in_db

'''Get all events'''
@router.get("", response_model=list[EventInDB])
async def get_all(db: Session = Depends(get_db)):
    event_list = await event_controller.get_all(db, "all")
    return event_list

'''Get all events visible'''
@router.get("/visible", response_model=list[EventInDB])
async def get_all_visible(db: Session = Depends(get_db)):
    event_list = await event_controller.get_all(db, "visible")
    return event_list

'''Get a event by id'''
@router.get("/{event_id}", response_model=EventInDB)
async def get_event(event_id: int, db=Depends(get_db)):
    # Check if the event exists
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.EVENT_NOT_FOUND)
    
    # Get the event
    event_return = await event_controller.get_by_id(db, event_id)
    return event_return

'''Update a event'''
@router.put("/{event_id}", response_model=EventInDB)
async def update_event(event_id: int, event_in: EventBase, db=Depends(get_db)):
    # Check if the event exists
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.EVENT_NOT_FOUND)
    
    # Check if the event title already exists only if the title has changed
    if event_in.title is not None and event_in.title != event.event_title:
        event_title_exist = await event_controller.get_by_title(db, event_in.title)
        if event_title_exist is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.EVENT_TITLE_ALREADY_EXISTS)
    
    # Update the event
    event_return: EventInDB = await event_controller.update(event, event_in, db)
    return event_return

'''Update a event visibility'''
@router.put("/{event_id}/visible", response_model=EventInDB | dict)
async def update_event_visibility(event_id: int, db=Depends(get_db)):
    # Check if the event exists
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.EVENT_NOT_FOUND)
    
    # Update the event visibility
    event_return: EventInDB = await event_controller.update_visibility(event, db)
    return event_return