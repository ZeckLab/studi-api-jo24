from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

# Event Schema : Pydantic Model
# By default, the visible attribute is not required because it has a default value in the database.
class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    capacity: int = Field(gt=0)

class EventInDB(EventBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    visible: bool