from sqlalchemy.orm import Session


from src.core.config import security, config
from src.core.models.User import User, Role
from src.core.schemas.user_schema import StaffInDB, UserInDB, UserProfile, UserRegister, StaffCreate, StaffUpdate, RoleBase, RoleInDB, UserUpdate

"""Role Controller"""
'''Get a role by its id in the database'''
async def get_role_by_id(db: Session, id: int) -> RoleInDB:
    # Get the role by its id
    result = db.query(Role).filter(Role.role_id == id).first()
    
    # Return the role in a RoleInDB : model Pydantic
    return RoleInDB.model_validate(result)


'''Get a role by its name in the database'''
async def get_role_by_name(db: Session, name: str) -> Role | None:
    # Get the role by its name
    session_role = db.query(Role).filter(Role.name == name).first()
    
    # Return the role
    return session_role


'''Get all roles in the database'''
async def get_all_roles(db: Session) -> list[RoleInDB]:
    result = []
    
    # Get all the roles
    result = db.query(Role).all()
    
    # Return the list of roles RoleInDB : model Pydantic
    return [RoleInDB.model_validate(row) for row in result]


'''Get all roles of user connected'''
def get_user_roles(user= User) -> list[str]:
    # Get all the roles for user connected
    # Return the list of roles RoleName : model Pydantic
    return [role.name for role in user.roles]


'''Create a role in the database'''
async def create_role(db: Session, role: RoleBase) -> RoleInDB:
    # Create the role object
    new_role = Role(name=role.name, description=role.description)
    
    # Insert the role object in the database
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    # Return the role in a RoleInDB : model Pydantic
    return RoleInDB.model_validate(new_role)


'''Update a role in the database'''
async def update_role(role: Role, role_in: RoleBase, db: Session) -> RoleInDB:
    # Update the role if it exists
    role.name = role_in.name
    role.description = role_in.description
    db.commit()
    db.refresh(role)
    
    # Return the role in a RoleInDB : model Pydantic
    return RoleInDB.model_validate(role)


"""User Controller"""
'''Get a user by its id in the database'''
async def get_user_by_id(db: Session, id: int, staff: bool) -> UserInDB:
    # Get the user by its id
    result = db.query(User).filter(User.user_id == id).first()
    
    model: UserInDB | StaffInDB
    
    if staff:
        # Return the user in a StaffInDB : model Pydantic
        model = StaffInDB.model_validate(result)
    else:
        # Return the user in a UserInDB : model Pydantic
        model = UserInDB.model_validate(result)
    
    # Return the user in a UserInDB | StaffInDB : model Pydantic
    return model


'''Get a user by its email in the database'''
async def get_user_by_email(db: Session, email: str) -> User | None:
    # Get the user by its email
    session_user = db.query(User).filter(User.email == email).first()
    
    # Return the user
    return session_user


'''Get all users (Staff) in the database'''
async def get_all_staff(db: Session) -> list[StaffInDB]:
    result = []
    
    # Get all the staff
    result = db.query(User).filter(User.roles.any(Role.name != "user")).all()
    
    # Return the list of staff StaffInDB : model Pydantic
    return [StaffInDB.model_validate(row) for row in result]


'''Create a user (Staff) in the database'''
async def create_staff(db: Session, staff: StaffCreate) -> StaffInDB:
    # Create the user object
    new_staff = User(email=staff.email, first_name=staff.first_name, last_name=staff.last_name, roles=[Role(name=role.name, description=role.description) for role in staff.roles])
    
    # Insert the user object in the database
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    
    # Return the user in a StaffInDB : model Pydantic
    return StaffInDB.model_validate(new_staff)


'''Update a user (Staff) in the database'''
async def update_staff(staff: User, staff_in: StaffUpdate, db: Session) -> StaffInDB:
    # Update the user if it exists
    staff.email = staff_in.email
    staff.first_name = staff_in.first_name
    staff.last_name = staff_in.last_name
    staff.roles = [Role(name=role.name, description=role.description) for role in staff_in.roles]
    db.commit()
    db.refresh(staff)

    # Return the user in a StaffInDB : model Pydantic
    return StaffInDB.model_validate(staff)


'''Register a user in the database'''
async def register_user(db: Session, user: UserRegister) -> User:
    # the basic user has only one role : 'user' (going to put in a parametrable variable)
    role : Role = await get_role_by_name(db, config.USER_WEB_APPLICATION_NAME_ROLE)
    
    # Create the user object
    new_user = User(email=user.email, first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number,
                    hashed_password=security.get_password_hash(user.password), keygen=security.get_keygen_hash(user.email),
                    roles=[role])
    
    # Insert the user object in the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return the user in a UserInDB : model Pydantic
    return new_user


'''Update a user in the database'''
async def update_user(user: User, user_in: UserUpdate, db: Session) -> User:
    # Update the user if it exists
    user.first_name = user_in.first_name
    user.last_name = user_in.last_name
    user.phone_number = user_in.phone_number
    db.commit()
    db.refresh(user)

    # Return the user
    return user
