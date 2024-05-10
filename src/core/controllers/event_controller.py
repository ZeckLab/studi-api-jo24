from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from src.core.models.Event import Event
from src.core.schemas.event_schema import EventInDB, EventBase

'''Get an event by its id in the database'''
async def get_by_id(db: Session, id: int) -> EventInDB:
    # Get the event by its id
    result = db.query(Event).filter(Event.event_id == id).first()
    
    # Return the event in a EventInDB : model Pydantic
    return EventInDB(id=result.event_id, title=result.event_title, description=result.event_description, date=result.event_date, capacity=result.event_capacity, visible=result.event_visible)

'''Get all events in the database or only the visible events in the database'''
async def get_all(db: Session, type: str) -> list[EventInDB]:
    result = []
    
    if type == "visible":
        # Get only the visible events
        result = db.query(Event).filter(Event.event_visible == True).all()
    else:
        # Get all the events
        result = db.query(Event).all()
    
    # Return the list of events EventInDB : model Pydantic
    return [EventInDB(id=row.event_id, title=row.event_title, description=row.event_description,
                date=row.event_date, capacity=row.event_capacity, visible=row.event_visible) for row in result]

'''Create an event in the database'''
async def create(db: Session, event: EventBase) -> EventInDB:
    # Create the event object
    new_event = Event(event_title=event.title, event_description=event.description, event_date=event.date, event_capacity=event.capacity)
    
    # Insert the event object in the database
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    # Return the event in a EventInDB : model Pydantic
    return EventInDB(id=new_event.event_id, title=new_event.event_title, description=new_event.event_description, date=new_event.event_date, capacity=new_event.event_capacity, visible=new_event.event_visible)

'''Update an event in the database'''
async def update(event_id: int, event: EventBase, db: Session) -> EventInDB | dict:
    # Get the event by its id
    result = db.query(Event).filter(Event.event_id == event_id).first()
    
    if result is not None:
        # Update the event if it exists
        result.event_title = event.title
        result.event_description = event.description
        result.event_date = event.date
        result.event_capacity = event.capacity
        db.commit()
        db.refresh(result)
    else:
        # Return an error message if the event does not exist
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = {"message": "Event not found"}).__dict__
    
    # Return the event in a EventInDB : model Pydantic
    return EventInDB(id=result.event_id, title=result.event_title, description=result.event_description, date=result.event_date, capacity=result.event_capacity, visible=result.event_visible)

async def update_visibility(event_id: int, db: Session) -> EventInDB | dict:
    #
    result = db.query(Event).filter(Event.event_id == event_id).first()
    
    if result is not None:
        # Update the event visibility
        result.event_visible = not result.event_visible
        db.commit()
        db.refresh(result)
    else:
        # Return an error message if the event does not exist
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST, content = {"message": "Event not found"}).__dict__
    
    # Return the event in a EventInDB : model Pydantic
    return EventInDB(id=result.event_id, title=result.event_title, description=result.event_description, date=result.event_date, capacity=result.event_capacity, visible=result.event_visible)
