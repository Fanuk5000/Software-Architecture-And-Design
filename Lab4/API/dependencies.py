from datetime import datetime, timedelta
from os import environ as os_environ
from typing import Annotated, Optional

from DataAccess.DataBase.initDB import get_db
from DataAccess.DataBase.models import User as UserModel
from DataAccess.repository import GenericRepository
from DataAccess.unit_of_work import SqlAlchemyUnitOfWork
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

#
from Services.booking import BookingService
from Services.certificate import CertificateService
from Services.quest import QuestRoomService
from Services.user import UserService

load_dotenv()

SECRET_KEY = os_environ.get("SECRET_JWT_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


def _get_uow(db=Depends(get_db)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(
        session_factory=lambda: db,
        repository=GenericRepository,
    )


def get_quest_service(
    uow: SqlAlchemyUnitOfWork = Depends(_get_uow),
) -> QuestRoomService:
    return QuestRoomService(uow)


def get_booking_service(
    uow: SqlAlchemyUnitOfWork = Depends(_get_uow),
) -> BookingService:
    return BookingService(uow)


def get_certificate_service(
    uow: SqlAlchemyUnitOfWork = Depends(_get_uow),
) -> CertificateService:
    return CertificateService(uow)


def get_user_service(uow: SqlAlchemyUnitOfWork = Depends(_get_uow)) -> UserService:
    return UserService(uow)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set in environment variables")

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserService = Depends(get_user_service),
) -> UserModel:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if SECRET_KEY is None:
            raise ValueError("SECRET_KEY is not set in environment variables")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError as e:
        raise credentials_error from e

    user = await service.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_error
    return user


async def get_current_admin_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    return current_user
