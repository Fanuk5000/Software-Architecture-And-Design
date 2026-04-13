from DataAccess.DataBase.models import User as UserModel
from DataAccess.repository import UserRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork


class UserService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.__uow = uow

    async def register_user(
        self, username: str, password: str, money: float, is_admin: bool
    ) -> int:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            existing_user = await user_repo.get_by_username(username)
            if existing_user is not None:
                raise ValueError("Username already exists")

            new_user = UserModel(
                username=username,
                password=password,
                money=money,
                is_admin=is_admin,
                is_active=True,
                has_certificate=False,
            )
            await user_repo.add(new_user)
            await uow.commit()
            return new_user.id

    async def login_user(self, username: str, password: str) -> int:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user: UserModel | None = await user_repo.get_by_username(username)
            if user is None or user.password != password:
                raise ValueError("Invalid username or password")
            if not user.is_active:
                raise ValueError("User account is inactive")
            return user.id

    async def delete_user(self, user_id: int) -> None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_delete = await user_repo.get_by_id(user_id)
            if user_to_delete is None:
                raise ValueError("User not found")
            await user_repo.delete(user_to_delete)
            await uow.commit()

    async def update_user(
        self, user_id: int, username: str | None = None, password: str | None = None
    ) -> None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            if username is not None:
                setattr(user_to_update, "username", username)
            if password is not None:
                setattr(user_to_update, "password", password)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def get_user(self, user_id: int) -> UserModel | None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            return await user_repo.get_by_id(user_id)

    async def get_all_users(self) -> list[UserModel]:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            return await user_repo.get_all()

    async def change_money(self, user_id: int, amount: float) -> None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
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
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "has_certificate", has_certificate)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def change_active_status(self, user_id: int, is_active: bool) -> None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "is_active", is_active)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def change_admin_status(self, user_id: int, is_admin: bool) -> None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_update: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_update is None:
                raise ValueError("User not found")
            setattr(user_to_update, "is_admin", is_admin)
            await user_repo.update(user_to_update)
            await uow.commit()

    async def del_if_inactive(self, user_id: int) -> None:
        async with self.__uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user_to_check: UserModel | None = await user_repo.get_by_id(user_id)
            if user_to_check is None:
                raise ValueError("User not found")
            if not user_to_check.is_active:
                await user_repo.delete(user_to_check)
                await uow.commit()
