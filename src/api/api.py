from fastapi import APIRouter

from src.api.endpoint import authenticate_endpoint, event_endpoint, user_endpoint
from src.api.endpoint import offer_endpoint

router = APIRouter()

router.include_router(
    event_endpoint.router,
    prefix="/events",
    tags=["Event"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    offer_endpoint.router,
    prefix="/offers",
    tags=["Offer"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    user_endpoint.router,
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    authenticate_endpoint.router,
    prefix="",
    tags=["Login/Signup"],
    responses={404: {"description": "Not found"}},
)