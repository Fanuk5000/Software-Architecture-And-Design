from DataAccess.DataBase.initDB import get_db
from DataAccess.repository import GenericRepository
from DataAccess.unit_of_work import SqlAlchemyUnitOfWork

#
from fastapi import Depends

#
from Services.booking import BookingService
from Services.certificate import CertificateService
from Services.quest import QuestRoomService
from Services.user import UserService


def _get_uow(db=Depends(get_db)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(
        session_factory=lambda: db,
        repository=GenericRepository,
    )


def get_quest_service(uow: SqlAlchemyUnitOfWork = Depends(_get_uow)) -> QuestRoomService:
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
