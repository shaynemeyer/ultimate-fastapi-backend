from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Shipment
from app.database.session import SessionDep
from app.api.schemas.schemas import ShipmentUpdate
from app.services.shipment import ShipmentService

router = APIRouter(prefix="/shipment", tags=["Shipment"])

### Read a shipment by id
@router.get("/", response_model=Shipment)
async def get_shipment(id: int, service: ServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
  return await service.add(shipment)


### Update fields of a shipment
@router.patch("/", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = await service.update(id, shipment_update)

    return shipment

@router.delete("/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is delete!"}
