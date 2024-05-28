from src.core.config.database import engine

from src.core.models.Ticket import Ticket, OffersTicket, Base
from src.core.models.Offer import Offer




def test_insert_ticket_with_offers():
    Base.metadata.create_all(bind=engine, tables=[Ticket.__table__, OffersTicket.__table__])
    
    ticket1 = Ticket(qrcode="854922r2545")
    offers_ticket1 = OffersTicket(quantity=3)
    offers_ticket2 = OffersTicket(quantity=2)
    offers_ticket3 = OffersTicket(quantity=1)
    
    from sqlalchemy.orm import Session
    with Session(bind=engine) as session:
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
        
        ticket_db = session.query(Ticket).filter(Ticket.qrcode == "854922r2545").first()
        offers_ticket_db = session.query(OffersTicket).filter(OffersTicket.ticket_id == ticket_db.ticket_id).all()
        print("Ticket", ticket_db)
        for offer in ticket_db.offers:
            print("Offer", offer.offer.title, "Quantity", offer.quantity)

    # Check if the insertion was successful
    assert ticket_db is not None
    assert len(offers_ticket_db) == 3
    assert len(ticket_db.offers) == 3