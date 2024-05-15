from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.schemas.event_schema import EventInDB, EventBase
import src.core.controllers.event_controller as event_controller
from src.core.config.database import get_db


router = APIRouter()

'''Create a new event'''
@router.post("", response_model=EventInDB)
async def create_event(event: EventBase, db=Depends(get_db)):
    event_in_db : EventInDB = await event_controller.create(db, event)
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
    event = await event_controller.get_by_id(db, event_id)
    return event

'''Update a event'''
@router.put("/{event_id}", response_model=EventInDB | dict)
async def update_event(event_id: int, event: EventBase, db=Depends(get_db)):
    event_return: EventInDB | dict = await event_controller.update(event_id, event, db)
    return event_return

'''Update a event visibility'''
@router.put("/{event_id}/visible", response_model=EventInDB | dict)
async def update_event_visibility(event_id: int, db=Depends(get_db)):
    event_return: EventInDB | dict = await event_controller.update_visibility(event_id, db)
    return event_return