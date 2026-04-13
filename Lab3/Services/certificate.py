from DataAccess.DataBase.models import Certificate as CertificateModel
from DataAccess.DataBase.models import User as UserModel
from DataAccess.DataBase.schemas import Certificate
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork


class CertificateService:
    def __init__(self, uow_factory: SqlAlchemyUnitOfWork) -> None:
        self.__uow = uow_factory

    async def get_available_certs(self) -> list[Certificate] | list[None]:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            return await certs_repo.get_all()

    async def add_cert(self, cert: CertificateModel) -> None:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            await certs_repo.add(cert)
            await uow.commit()

    async def delete_cert(self, cert_id: int) -> None:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            cert_to_delete = await certs_repo.get_by_id(cert_id)
            if cert_to_delete is None:
                raise ValueError("Certificate not found")
            await certs_repo.delete(cert_to_delete)
            await uow.commit()

    async def update_cert(self, cert: CertificateModel) -> None:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            cert_to_update = await certs_repo.get_by_id(cert.id)
            if cert_to_update is None:
                raise ValueError("Certificate not found")
            await certs_repo.update(cert)
            await uow.commit()

    async def use_cert(self, cert_id: int, user_id: int) -> int:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            users_repo = uow.get_repository(UserModel)

            cert_to_use: Certificate | None = await certs_repo.get_by_id(cert_id)
            if cert_to_use is None or user_id != cert_to_use.user_id:
                raise ValueError("Certificate not found")

            user = await users_repo.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

            if not cert_to_use.is_active and user.has_certificate:
                raise ValueError("Certificate not available")
            user.has_certificate = False
            cert_to_use.is_active = False
            await certs_repo.update(cert_to_use)
            await uow.commit()
            return await cert_to_use.discount_percentage
