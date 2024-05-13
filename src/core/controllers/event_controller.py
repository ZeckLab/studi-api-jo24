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


'''Get an event by its title in the database'''
async def get_by_title(db: Session, title: str) -> Event | None:
    # Get the event by its title
    session_event = db.query(Event).filter(Event.event_title == title).first()
    
    # Return the event
    return session_event


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
async def update(event: Event, event_in: EventBase, db: Session) -> EventInDB:
    # Update the event if it exists
    event.event_title = event_in.title
    event.event_description = event_in.description
    event.event_date = event_in.date
    event.event_capacity = event_in.capacity
    db.commit()
    db.refresh(event)
    
    # Return the event in a EventInDB : model Pydantic
    return EventInDB(id=event.event_id, title=event.event_title, description=event.event_description, date=event.event_date, capacity=event.event_capacity, visible=event.event_visible)

async def update_visibility(event:Event, db: Session) -> EventInDB | dict:
    # Update the event visibility
    event.event_visible = not event.event_visible
    db.commit()
    db.refresh(event)
    
    # Return the event in a EventInDB : model Pydantic
    return EventInDB(id=event.event_id, title=event.event_title, description=event.event_description, date=event.event_date, capacity=event.event_capacity, visible=event.event_visible)
