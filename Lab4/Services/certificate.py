from DataAccess.DataBase.models import Certificate as CertificateModel
from DataAccess.DataBase.models import User as UserModel
from DataAccess.DataBase.schemas import CreateCertificate
from DataAccess.unit_of_work import SqlAlchemyUnitOfWork


class CertificateService:
    def __init__(self, uow_factory: SqlAlchemyUnitOfWork) -> None:
        self.__uow = uow_factory

    async def get_all_certs(self) -> list[CertificateModel] | list[None]:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            return await certs_repo.get_all()

    async def get_user_certs(self, user_id: int) -> list[CertificateModel] | list:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            return await certs_repo.get_all_by(user_id=user_id)

    async def add_cert(self, cert: CreateCertificate, user_id: int) -> None:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            user_repo = uow.get_repository(UserModel)
            user = await user_repo.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

            user.has_certificate = True
            await user_repo.update(user)
            orm_cert = self.__create_orm_cert(cert)
            await certs_repo.add(orm_cert)
            await uow.commit()

    async def delete_cert(self, cert_id: int, user_id: int) -> None:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            user_repo = uow.get_repository(UserModel)
            cert_to_delete = await certs_repo.get_by_id(cert_id)
            user = await user_repo.get_by_id(user_id)
            if cert_to_delete is None:
                raise ValueError("Certificate not found")
            if user is None:
                raise ValueError("User not found")
            if user_id != cert_to_delete.user_id:
                raise ValueError("Unauthorized to delete this certificate")

            user.has_certificate = False
            await user_repo.update(user)
            await certs_repo.delete(cert_to_delete)
            await uow.commit()

    async def update_cert(self, cert: CreateCertificate) -> None:
        orm_cert = self.__create_orm_cert(cert)

        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            cert_to_update = await certs_repo.get_by_id(orm_cert.id)
            if cert_to_update is None:
                raise ValueError("Certificate not found")
            await certs_repo.update(orm_cert)
            await uow.commit()

    async def use_cert(self, user_id: int) -> int:
        async with self.__uow as uow:
            certs_repo = uow.get_repository(CertificateModel)
            users_repo = uow.get_repository(UserModel)

            cert_to_use: CertificateModel | None = await certs_repo.get_one_by(
                user_id=user_id, is_active=True
            )
            if cert_to_use is None or user_id != cert_to_use.user_id:
                raise ValueError(f"Certificate not found for user {user_id}")

            user = await users_repo.get_by_id(user_id)
            if user is None:
                raise ValueError(f"User not found with id {user_id}")

            if not cert_to_use.is_active and user.has_certificate:
                raise ValueError(f"Certificate not available for user {user_id}")
            user.has_certificate = False
            cert_to_use.is_active = False
            await certs_repo.update(cert_to_use)
            await uow.commit()
            return cert_to_use.discount_percentage

    def __create_orm_cert(self, cert: CreateCertificate) -> CertificateModel:
        orm_cert = CertificateModel(**cert.model_dump())
        return orm_cert
