from sqlalchemy.orm import Session

from src.core.config.database import engine, Base
from src.core.config import config, security
from src.core.models.User import Role, User

def initiate():
    # create the database tables
    Base.metadata.create_all(bind=engine)
    
    with Session(bind=engine) as session:
    # create the first role if it does not exist
        role = session.query(Role).filter(Role.name == "admin").first()
        if role is None:
            role = Role(name="admin", description="Administrator. All permissions.")
            session.add(role)
            session.commit()

        # create the admin user if it does not exist
        admin = session.query(User).filter(User.email == config.ADMIN_EMAIL).first()
        if admin is None:
            admin = User(email=config.ADMIN_EMAIL,
                        hashed_password=security.get_password_hash(config.ADMIN_PASSWORD),
                        first_name="Admin",
                        last_name="Admin",
                        roles=[role])
            session.add(admin)
            session.commit()