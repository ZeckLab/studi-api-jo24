from datetime import datetime

from src.core.models.User import User
from src.core.schemas.order_schema import Payment
from src.core.utils.qr_code import generate_qrcode


def create_name_order(date_time_now: datetime, user: User) -> str:
    # Return the name of the order : YYYYMMDD-{initials of the user}{id of the user}-HHMMSS
    return f"{date_time_now.strftime('%Y%m%d')}-{user.first_name[0]}{user.last_name[0]}{user.user_id}-{date_time_now.strftime('%H%M%S')}"

def create_transaction_order(payment: Payment) -> str:
    # Return the transaction number
    return f"{payment.card_number}{payment.card_expiry}{payment.card_cvc}{datetime.now().strftime('%Y%m%d%H%M%S')}"

def create_qrcode_ticket(keygen_user: str, keygen_order: str) -> str:
    # Return the name of the order : YYYYMMDD-{initials of the user}{id of the user}-HHMMSS
    return generate_qrcode(f"{keygen_user}{keygen_order}")