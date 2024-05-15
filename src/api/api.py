from fastapi import APIRouter

from src.api.endpoint import event_endpoint
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