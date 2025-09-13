from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    processing = "processing"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    returned = "returned"

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

class Seller(SQLModel, table = True):

    id: int = Field(default=None, primary_key=True)
    name: str
    
    email: EmailStr
    password_hash: str