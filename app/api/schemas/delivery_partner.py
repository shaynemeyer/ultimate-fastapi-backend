from pydantic import BaseModel, EmailStr


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseDeliveryPartner):
    pass


class DeliveryPartnerUpdate(BaseModel):
    serviceable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str
