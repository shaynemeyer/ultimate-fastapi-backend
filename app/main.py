from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.api.tag import APITag
from app.core.exceptions import add_exception_handlers
from app.database.session import create_db_tables
from app.api.router import master_router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


description = """
Delivery Management System for sellers and delivery agents

### Seller
- Submit shipment effortlessly
- Share tracking links with customers

### Delivery Agent
- Auto accept shipments
- Track and update shipment status
- Email and SMS notifications
"""

app = FastAPI(
    lifespan=lifespan_handler,
    title="FastShip",
    description=description,
    terms_of_service="https://fastship.com/terms/",
    contact={
        "name": "FastShip Support",
        "url": "https://fastship.com/support",
        "email": "support@fastship.com",
    },
    openapi_tags=[
        {"name": APITag.SHIPMENT, description: "Operations related to shipments."},
        {"name": APITag.SELLER, description: "Operations related to seller."},
        {
            "name": APITag.PARTNER,
            description: "Operations related to delivery partner.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5500"], allow_methods=["*"]
)

app.include_router(master_router)
add_exception_handlers(app)


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
