from DataAccess.DataBase.models import User as UserModel
from DataAccess.DataBase.schemas import CreateCertificate
from fastapi import APIRouter, Depends, HTTPException, status
from Services.certificate import CertificateService
from sqlalchemy.exc import SQLAlchemyError

from API.dependencies import (
    get_certificate_service,
    get_current_admin_user,
    get_current_user,
)

public_router = APIRouter(prefix="/certificates", tags=["certificates"])
admin_router = APIRouter(
    prefix="/certificates",
    tags=["certificates"],
    dependencies=[Depends(get_current_admin_user)],
)


@public_router.get("/my")
async def get_my_certificates(
    current_user: UserModel = Depends(get_current_user),
    service: CertificateService = Depends(get_certificate_service),
):
    try:
        certificates = await service.get_user_certs(current_user.id)
        return certificates
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.get("/all")
async def get_all_certificates(
    service: CertificateService = Depends(get_certificate_service),
):
    try:
        certificates = await service.get_all_certs()
        return certificates
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_certificate(
    cert: CreateCertificate,
    service: CertificateService = Depends(get_certificate_service),
):
    try:
        await service.add_cert(cert, cert.user_id)
        return {"message": "Certificate added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.delete("/delete/{cert_id}", status_code=status.HTTP_201_CREATED)
async def delete_certificate(
    cert_id: int,
    user_id: int,
    service: CertificateService = Depends(get_certificate_service),
):
    try:
        await service.delete_cert(cert_id, user_id)
        return {"message": "Certificate deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.put("/update", status_code=status.HTTP_201_CREATED)
async def update_certificate(
    cert: CreateCertificate,
    service: CertificateService = Depends(get_certificate_service),
):
    try:
        await service.update_cert(cert)
        return {"message": "Certificate updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
