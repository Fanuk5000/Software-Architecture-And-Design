from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from Services.user import UpdateUserRequest, UserService
from sqlalchemy.exc import SQLAlchemyError

from API.dependencies import (
    create_access_token,
    get_current_admin_user,
    get_current_user,
    get_user_service,
)

admin_router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(get_current_admin_user)]
)
public_router = APIRouter(prefix="/users", tags=["users"])


@public_router.post("/register")
async def register_user(
    username: str, password: str, service: UserService = Depends(get_user_service)
) -> dict[str, str]:
    try:
        user_id = await service.register_user(
            username=username, password=password, money=0.0, is_admin=False
        )
        return {"message": f"User with ID {user_id} created successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@public_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(get_user_service),
):
    try:
        user_id = await service.login_user(form_data.username, form_data.password)

        access_token = create_access_token(data={"sub": str(user_id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@public_router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)) -> dict[str, Any]:
    return {
        "id": current_user.id,
        "username": current_user.username,
        "money": current_user.money,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
    }


@admin_router.delete("/{user_id}")
async def delete_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> dict[str, str]:
    try:
        await service.delete_user(user_id)
        return {"message": f"User with ID {user_id} deleted successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.put("/{user_id}")
async def update_user(
    user_id: int,
    update_data: UpdateUserRequest,
    service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await service.update_user(user_id, update_data)
        return {"message": f"User with ID {user_id} updated successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, service: UserService = Depends(get_user_service)
) -> dict[str, Any]:
    try:
        user = await service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": user.id,
            "username": user.username,
            "money": user.money,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.get("/")
async def get_all_users(
    service: UserService = Depends(get_user_service),
) -> list[dict[str, Any]]:
    try:
        users = await service.get_all_users()
        return [
            {
                "id": user.id,
                "username": user.username,
                "money": user.money,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            }
            for user in users
        ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/{user_id}/change_money")
async def change_user_money(
    user_id: int,
    amount: float,
    service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await service.change_money(user_id, amount)
        return {"message": f"User with ID {user_id} money changed by {amount}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/{user_id}/change_certificate")
async def change_user_certificate_status(
    user_id: int,
    has_certificate: bool,
    service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await service.change_certificate_status(user_id, has_certificate)
        status_str = "granted" if has_certificate else "revoked"
        return {"message": f"User with ID {user_id} certificate {status_str}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/{user_id}/change_active_status")
async def change_user_active_status(
    user_id: int,
    is_active: bool,
    service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await service.change_active_status(user_id, is_active)
        status_str = "activated" if is_active else "deactivated"
        return {"message": f"User with ID {user_id} {status_str}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/{user_id}/change_admin_status")
async def change_user_admin_status(
    user_id: int,
    is_admin: bool,
    service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await service.change_admin_status(user_id, is_admin)
        status_str = "granted" if is_admin else "revoked"
        return {"message": f"User with ID {user_id} admin rights {status_str}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/{user_id}/delete_if_inactive")
async def delete_user_if_inactive(
    user_id: int, service: UserService = Depends(get_user_service)
) -> dict[str, str]:
    try:
        await service.del_if_inactive(user_id)
        return {"message": f"User with ID {user_id} deleted if inactive"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=ve)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
