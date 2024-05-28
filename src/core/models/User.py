from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from src.core.config.database import Base
from src.core.models.Order import Order

class UserRole(Base):
    __tablename__ = "user_role"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)


class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), index=True, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    users = relationship('User', secondary='user_role', back_populates="roles")


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), index=True, nullable=False, unique=True)
    hashed_password = Column(Text, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20))
    keygen = Column(String(255))
    is_active = Column(Boolean, server_default="true")
    roles = relationship('Role', secondary='user_role', back_populates="users")
    orders = relationship(Order, back_populates="user")
