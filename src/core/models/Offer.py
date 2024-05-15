from sqlalchemy import CheckConstraint, Column, Float, Integer, String, Text, Boolean
from src.core.config.database import Base

class Offer(Base):
    __tablename__ = "offers"

    offer_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), index=True, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    nb_people = Column(Integer, CheckConstraint("nb_people > 0"), nullable=False)
    price = Column(Float, CheckConstraint("price > 0"), nullable=False)
    visible = Column(Boolean, server_default="false")
    image_url = Column(String(255), nullable=False)