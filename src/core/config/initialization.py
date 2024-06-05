from sqlalchemy.orm import Session

from src.core.config.database import engine, Base
from src.core.config import config, security
from src.core.models.User import Role, User

def initiate():
    # create the database tables
    Base.metadata.create_all(bind=engine)
    
    with Session(bind=engine) as session:
        # create the web application user role if it does not exist
        role_user = session.query(Role).filter(Role.name == config.USER_WEB_APPLICATION_NAME_ROLE).first()
        if role_user is None:
            role_user = Role(name=config.USER_WEB_APPLICATION_NAME_ROLE, description=config.USER_WEB_APPLICATION_DESC_ROLE)
            session.add(role_user)
            session.commit()
        
        # create the web application admin role if it does not exist
        role_admin = session.query(Role).filter(Role.name == config.ADMIN_WEB_APPLICATION_NAME_ROLE).first()
        if role_admin is None:
            role_admin = Role(name=config.ADMIN_WEB_APPLICATION_NAME_ROLE, description=config.ADMIN_WEB_APPLICATION_DESC_ROLE)
            session.add(role_admin)
            session.commit()

        # create the admin user if it does not exist
        admin = session.query(User).filter(User.email == config.ADMIN_EMAIL).first()
        if admin is None:
            admin = User(email=config.ADMIN_EMAIL,
                        hashed_password=security.get_password_hash(config.ADMIN_PASSWORD),
                        first_name="Admin",
                        last_name="Admin",
                        roles=[role_admin])
            session.add(admin)
            session.commit()