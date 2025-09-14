from typing import Annotated
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from app.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")
