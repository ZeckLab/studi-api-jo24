from src.core.config.database import engine

from src.core.models.User import User, Role
from src.core.models.Order import Order
from src.core.models.Ticket import Ticket, OffersTicket, Base
from src.core.models.Offer import Offer




def test_insert_ticket_with_offers():
    Base.metadata.create_all(bind=engine, tables=[Ticket.__table__, OffersTicket.__table__])
    
    from sqlalchemy.orm import Session
    with Session(bind=engine) as session:
        # Insert a user
        role = session.query(Role).filter(Role.name == "user").first()
        user = User(email='pouet6@test.com', first_name="Pouet", last_name="Pouet", phone_number="+33 1234567890", hashed_password="pouet", keygen='pouet6', roles=[role])
        
        session.add(user)
        session.commit()
        
        user_pouet = session.query(User).filter(User.email == "pouet5@test.com").first()
        
        # Insert an order
        order_pouet = Order(user_id=user_pouet.user_id, name="Order Pouet6", date_time="2021-01-01 00:00:00", transaction="pouet", keygen="pouet6")
        session.add(order_pouet)
        session.commit()
        
        order_pouet = session.query(Order).filter(Order.name == "Order Pouet6").first()
                            
        ticket1 = Ticket(keygen_qrcode="854922r2545aa", order_id=order_pouet.order_id)
        offers_ticket1 = OffersTicket(quantity=3)
        offers_ticket2 = OffersTicket(quantity=2)
        offers_ticket3 = OffersTicket(quantity=1)

        offer1 = session.query(Offer).filter(Offer.title == "Duo").first()
        offer2 = session.query(Offer).filter(Offer.title == "Quatro").first()
        offer3 = session.query(Offer).filter(Offer.title == "Solo").first()
        offers_ticket1.offer = offer1
        offers_ticket2.offer = offer2
        offers_ticket3.offer = offer3
        ticket1.offers.append(offers_ticket1)
        ticket1.offers.append(offers_ticket2)
        ticket1.offers.append(offers_ticket3)
        session.add_all([ticket1, offers_ticket1, offers_ticket2, offers_ticket3])
        session.commit()
        
        ticket_db = session.query(Ticket).filter(Ticket.keygen_qrcode == "854922r2545aa").first()
        offers_ticket_db = session.query(OffersTicket).filter(OffersTicket.ticket_id == ticket_db.ticket_id).all()
        print("Ticket", ticket_db)
        for offer in ticket_db.offers:
            print("Offer", offer.offer.title, "Quantity", offer.quantity)

    # Check if the insertion was successful
    assert user_pouet is not None
    assert order_pouet is not None
    assert ticket1 is not None
    assert ticket_db is not None
    assert len(offers_ticket_db) == 3
    assert len(ticket_db.offers) == 3