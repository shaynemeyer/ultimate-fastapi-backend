from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_delivery_partner_access_token,
)
from app.api.schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from app.database.redis import add_jti_to_blacklist

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


### Register a new delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    partner: DeliveryPartnerCreate, service: DeliveryPartnerServiceDep
):
    return await service.add(partner)


### Login a delivery partner
@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}


### Update the delivery partner
@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    return await service.update(partner.sqlmodel_update(update))


### Logout a delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out!"}


### Verify Seller Email
@router.get("/verify")
async def verify_delivery_partner_email(token: str, service: DeliveryPartnerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified"}
