from fastapi import APIRouter

from app.api.routes import factura, health, ocr, upload

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(factura.router)
api_router.include_router(upload.router)
api_router.include_router(ocr.router)
