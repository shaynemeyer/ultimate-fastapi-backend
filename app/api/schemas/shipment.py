from datetime import datetime
from random import randint
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.database.models import Seller, ShipmentEvent, ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25, ge=1)
    destination: int


class ShipmentRead(BaseShipment):
    id: UUID
    seller: Seller
    timeline: list[ShipmentEvent]
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    client_contact_email: EmailStr
    client_contact_phone: int | None = Field(default=None)


class ShipmentUpdate(BaseModel):
    location: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    description: str | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)


class ShipmentReview(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None)
