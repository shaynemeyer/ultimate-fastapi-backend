from enum import Enum
from random import randint
from pydantic import BaseModel, Field


def random_destination():
    return randint(11000, 11999)


class ShipmentStatus(str, Enum):
    placed = "placed"
    processing = "processing"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class BaseShipment(BaseModel):
    content: str = Field(
        description="Content of the shipment", max_length=150, min_length=8
    )
    weight: float = Field(
        description="Weight of the shipment in kilograms (kg)", le=25, ge=1
    )
    destination: int | None = Field(
        description="Destination zipcode. If not provided will be sent off to a random location",
        default_factory=random_destination,
    )


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25)
    destination: int | None = Field(default=None)
    status: ShipmentStatus
