from datetime import datetime as datetime
from sqlalchemy import Row
from sqlalchemy.sql import text
from pydantic import ValidationError
from src.core.config.database import Base, engine
from src.core.schemas.event_schema import EventBase, EventInDB
from src.core.models.Event import Event

# create a event schema
# Validation of datas
def test_create_event_by_schema():
    json = {
        "title": "Event 5",
        "description": "Description of event 5",
        "date": "2021-12-31 23:59:59",
        "capacity": 100
    }
    
    event = EventBase(**json)

    assert event.title == "Event 5"
    assert event.description == "Description of event 5"
    assert event.date == datetime.strptime("2021-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    assert event.capacity == 100


# Validation of datas
def test_create_event_by_schema_with_capacity_less_1():
    exception_raised = False
    json = {
        "title": "Event 5",
        "description": "Description of event 5",
        "date": "2021-12-31 23:59:59",
        "capacity": -100
    }
    
    try:
        EventBase(**json);
    except ValidationError:
        exception_raised = True
    
    assert exception_raised == True

# Validation of datas
def test_create_event_by_schema_with_null_attribute():
    exception_raised = False

    json = {
        "title": "Event 5",
        "description": None,
        "date": "2021-12-31 23:59:59",
        "capacity": 100
    }
    
    try:
        EventBase(**json);
    except ValidationError:
        exception_raised = True
    
    assert exception_raised == True

# Validation of datas
def test_create_event_by_schema_with_missing_attribute():
    exception_raised = False

    json = {
        "title": "Event 5",
        "description": "Description of event 5",
        "capacity": 100
    }
    
    try:
        EventBase(**json);
    except ValidationError:
        exception_raised = True
    
    assert exception_raised == True

# Validation of datas
def test_validation_datas_in_db():
    result : Row
    
    Base.metadata.drop_all(bind=engine, tables=[Event.__table__])
    
    # Recreate table
    Base.metadata.create_all(
        bind=engine,
        tables=[Event.__table__],
    )
    
    with engine.connect() as connection:
        connection.execute(Event.__table__.insert().values(
            event_title="Event 5",
            event_description="Description of event 5",
            event_date="2021-12-31 23:59:59",
            event_capacity=100,
        ))
        connection.commit()
        result = connection.execute(text("SELECT * FROM events WHERE event_title = 'Event 5'")).first()
    
    event_db = EventInDB(id=result.event_id, title=result.event_title, description=result.event_description, date=result.event_date, capacity=result.event_capacity, visible=result.event_visible)
    assert event_db.id > 0
    assert event_db.visible == False
    assert event_db.title == "Event 5"
    assert event_db.description == "Description of event 5"
    assert event_db.date == datetime.strptime("2021-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    assert event_db.capacity == 100