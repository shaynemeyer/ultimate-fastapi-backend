from uuid import UUID
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.templating import Jinja2Templates

from app.api.dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix="/shipment", tags=["Shipment"])

templates = Jinja2Templates(TEMPLATE_DIR)


### Read a shipment by id
@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: UUID, _: SellerDep, service: ShipmentServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


### Tracking details of shipment
@router.get("/track")
async def get_tracking(request: Request, id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request, name="track.html", context=context
    )


### Create a new shipment with content and weight
@router.post("/", response_model=ShipmentRead)
async def submit_shipment(
    seller: SellerDep, shipment: ShipmentCreate, service: ShipmentServiceDep
):
    return await service.add(shipment, seller)


### Update fields of a shipment
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDep,
):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    return await service.update(id, shipment_update, partner)


### Cancel a shipment by id
@router.get("/cancel", response_model=ShipmentRead)
async def cancel_shipment(id: UUID, seller: SellerDep, service: ShipmentServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return await service.cancel(id, seller)
