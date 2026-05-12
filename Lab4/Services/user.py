import hashlib
from dataclasses import dataclass

from DataAccess.DataBase.models import User as UserModel
from DataAccess.repository import GenericRepository
from DataAccess.unit_of_work import SqlAlchemyUnitOfWork


@dataclass
class UpdateUserRequest:
    username: str | None
    password: str | None
    money: float | None
    is_admin: bool | None
    is_active: bool | None
    has_certificate: bool | None


def _get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return _get_password_hash(plain_password) == hashed_password


class UserService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.__uow = uow

    async def create_user(
        self, username: str, password: str, money: float, is_admin: bool
    ) -> int:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(model=UserModel)  # pyright: ignore[reportAssignmentType]
            existing_user = await user_repo.get_one_by(username=username)
            if existing_user is not None:
                raise ValueError("Username already exists")

            new_user = UserModel(
                username=username,
                password=_get_password_hash(password),
                money=money,
                is_admin=is_admin,
                is_active=True,
                has_certificate=False,
            )
            await user_repo.add(new_user)
            await uow.commit()
            return new_user.id

    async def verify_user(self, username: str, password: str) -> int:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user: UserModel | None = await user_repo.get_one_by(username=username)
            if user is None or not _verify_password(password, user.password):
                raise ValueError("Invalid username or password")
            if not user.is_active:
                raise ValueError("User account is inactive")
            return user.id

    async def delete_user(self, user_id: int) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_delete = await user_repo.get_by_id(user_id)
            if user_to_delete is None:
                raise ValueError("User not found")
            await user_repo.delete(user_to_delete)
            await uow.commit()

    async def update_user(
        self,
        user_id: int,
        update_data: UpdateUserRequest,
    ) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")

            attrs = (
                "username",
                "password",
                "money",
                "is_admin",
                "is_active",
                "has_certificate",
            )

            for attr in attrs:
                if getattr(update_data, attr) is not None:
                    if attr == "password":
                        setattr(
                            user_to_update,
                            attr,
                            _get_password_hash(getattr(update_data, attr)),
                        )
                    else:
                        setattr(user_to_update, attr, getattr(update_data, attr))

            await user_repo.update(user_to_update)
            await uow.commit()

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            return await user_repo.get_by_id(user_id)

    async def get_all_users(self) -> list[UserModel]:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            return await user_repo.get_all()

    async def change_money(self, user_id: int, amount: float) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "money", user_to_update.money + amount)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def change_certificate_status(
        self, user_id: int, has_certificate: bool
    ) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "has_certificate", has_certificate)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def change_active_status(self, user_id: int, is_active: bool) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "is_active", is_active)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def change_admin_status(self, user_id: int, is_admin: bool) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "is_admin", is_admin)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def del_if_inactive(self, user_id: int) -> None:
        async with self.__uow as uow:
            user_repo: GenericRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_check: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_check is None:
                raise ValueError("User not found")
            if not user_to_check.is_active:
                await user_repo.delete(user_to_check)
                await uow.commit()
