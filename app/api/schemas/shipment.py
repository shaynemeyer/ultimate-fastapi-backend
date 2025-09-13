from datetime import datetime
from random import randint
from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25, ge=1)
    destination: int


class ShipmentRead(BaseShipment):
    id: int
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
