from pydantic import BaseModel, ConfigDict

from src.core.schemas.order_schema import OrderBase

# Role Schema : Pydantic Model
class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    description: str | None = None

class RoleInDB(RoleBase):
    role_id: int


# User Role Schema : Pydantic Model
class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


# User Schema : Pydantic Model
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: str
    first_name: str
    last_name: str
    phone_number: str | None = None

class UserEmailExist(BaseModel):
    email: str
    exist: bool

class UserLogin(BaseModel):
    email: str
    password: str

class StaffCreate(UserBase):
    password: str
    role_names: list[str] = []

class StaffUpdate(UserBase):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role_names: list[str] = []

class UserRegister(UserBase):
    password: str
    phone_number: str

class UserProfile(UserBase):
    phone_number: str

class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

class StaffInDB(UserBase):
    user_id: int
    hashed_password: str

class UserOrders(UserBase):
    orders: list["OrderBase"] | None = []

class UserInDB(UserBase):
    user_id: int
    phone_number: str
    is_active: bool

class UserInResponse(UserInDB):
    roles: list["RoleInDB"]