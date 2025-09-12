from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment, ShipmentStatus
from app.database.session import create_db_tables, SessionDep

from app.schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)

shipments = {
    12701: {"weight": 0.6, "content": "glassware", "status": "placed"},
    12702: {"weight": 2.3, "content": "books", "status": "shipped"},
    12703: {"weight": 1.1, "content": "electronics", "status": "delivered"},
    12704: {"weight": 3.5, "content": "furniture", "status": "in_transit"},
    12705: {"weight": 0.9, "content": "clothing", "status": "returned"},
    12706: {"weight": 4.0, "content": "appliances", "status": "processing"},
    12707: {"weight": 1.8, "content": "toys", "status": "placed"},
}


### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipments[id]


### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = session.get(Shipment, id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )

    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    session.delete(session.get(Shipment, id))
    session.commit()

    return {"detail": f"Shipment with id #{id} is delete!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
