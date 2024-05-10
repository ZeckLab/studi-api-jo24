from fastapi import APIRouter

from src.api.endpoint import event_endpoint

router = APIRouter()

router.include_router(
    event_endpoint.router,
    prefix="/events",
    tags=["Event"],
    responses={404: {"description": "Not found"}},
)