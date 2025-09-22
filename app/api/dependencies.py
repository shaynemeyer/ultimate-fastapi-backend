from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme_seller, oauth2_scheme_partner
from app.database.models import DeliveryPartner, Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.deliver_partner import DeliveryPartnerService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Access token data dep
async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return data


# Seller access token data
async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
) -> dict:
    return await _get_access_token(token)


# Delivery partner access token data
async def get_delivery_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
) -> dict:
    return await _get_access_token(token)


# Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep,
):
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))

    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )
    return seller


# Logged In Seller
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
    session: SessionDep,
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))

    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )
    return partner


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session, DeliveryPartnerService(session))


# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)


# Delivery partner service dep
def get_delivery_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)


SellerDep = Annotated[Seller, Depends(get_current_seller)]
DeliveryPartnerDep = Annotated[DeliveryPartner, Depends(get_current_partner)]
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService, Depends(get_delivery_partner_service)
]
