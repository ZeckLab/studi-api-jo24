import psycopg2
import sqlalchemy
from src.core.models.Event import Event
from src.core.config.database import Base, engine, get_db
from sqlalchemy import Row, inspect, text

def test_creation_table_event():
    # Drop table if exists
    #Base.metadata.drop_all(bind=engine, tables=[Event.__table__])
    
    # Recreate table
    #Base.metadata.create_all(
    #    bind=engine,
    #    tables=[Event.__table__],
    #)
    
    inspection = inspect(engine)
    print(inspection.get_table_names())
    
    engine.connect().commit()
    
    assert inspection.has_table("events") == True

# Creation of an event object for the following tests
event = Event(
    event_title="Event 1",
    event_description="Description of event 1",
    event_date="2021-12-31 23:59:59",
    event_capacity=100,
)

def test_creation_event():
    # Check the values of the event object. By default, the event_id is None and event_visible is None
    # because the default value of event_visible is False in database.
    assert event.event_id == None
    assert event.event_title == "Event 1"
    assert event.event_description == "Description of event 1"
    assert event.event_date == "2021-12-31 23:59:59"
    assert event.event_capacity == 100
    assert event.event_visible == None


def test_insert_event_without_attribute_visible():
    insertion_success: bool = False

    # Insert the event object into the database
    with engine.connect() as connection:
        insertion_success = connection.execute(Event.__table__.insert().values(
            event_title=event.event_title,
            event_description=event.event_description,
            event_date=event.event_date,
            event_capacity=event.event_capacity,
        )).is_insert
        connection.commit()
        

    # Check if the insertion was successful
    assert insertion_success == True
    
def test_verifiy_insert_event_without_attribute_visible():
    event_db: Row

    # Insert the event object into the database
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM events WHERE event_title = 'Event 1'"))
        event_db = result.fetchone()
        

    # Check the event_id of the event object. It should be greater than 0.
    # Check the event_visible of the event object. It should be False.
    assert event_db.event_id > 0
    assert event_db.event_visible == False

# Test the insertion of an event object with the same event_title (unique constraint)
def test_insert_same_event_title():
    insertion_success: bool = True

    # Insert the event object into the database
    with engine.connect() as connection:
        try:
            connection.execute(Event.__table__.insert().values(
                event_title=event.event_title,
                event_description=event.event_description,
                event_date=event.event_date,
                event_capacity=event.event_capacity,
            ))
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                insertion_success = False

    # Check if the insertion is failed
    assert insertion_success == False

# Test the insertion of an event object with a null attribute
def test_insert_event_with_null_attribute():
    insertion_success: bool = True

    # Insert the event object into the database
    with engine.connect() as connection:
        try:
            connection.execute(Event.__table__.insert().values(
                event_title="Event 2",
                event_description=None,
                event_date="2021-12-31 23:59:59",
                event_capacity=100,
            ))
            connection.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.NotNullViolation):
                insertion_success = False

    # Check if the insertion is failed
    assert insertion_success == False

# Test the insertion of en event object with a capacity less than 1
def test_insert_event_with_capacity_less_than_1():
    insertion_success: bool = True

    # Insert the event object into the database
    with engine.connect() as connection:
        try:
            connection.execute(Event.__table__.insert().values(
                event_title="Event 3",
                event_description="Description of event 3",
                event_date="2021-12-31 23:59:59",
                event_capacity=0,
            ))
            connection.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, psycopg2.errors.CheckViolation):
                insertion_success = False

    # Check if the insertion is failed
    assert insertion_success == False