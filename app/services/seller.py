from fastapi import BackgroundTasks, HTTPException, status

from app.services.user import UserService
from app.utils import generate_access_token

from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService(UserService):
    def __init__(self, session: AsyncSession, tasks: BackgroundTasks):
        super().__init__(Seller, session, tasks)

    async def add(self, seller_create: SellerCreate) -> Seller:
        return await self._add_user(seller_create.model_dump(), router_prefix="seller")

    async def token(self, email, password) -> str:
        return await self._generate_token(email=email, password=password)
