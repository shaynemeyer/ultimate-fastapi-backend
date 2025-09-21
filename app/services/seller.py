from fastapi import HTTPException, status

from app.services.user import UserService
from app.utils import generate_access_token

from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(Seller, session)

    async def add(self, seller_create: SellerCreate) -> Seller:
        return await self._add_user(seller_create.model_dump())

    async def token(self, email, password) -> str:
        return await self._generate_token(email=email, password=password)
