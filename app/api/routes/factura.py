import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.factura import Factura

router = APIRouter(prefix="/facturas", tags=["facturas"])


class FacturaCreate(BaseModel):
    numero: str = Field(..., max_length=50)
    proveedor: str = Field(..., max_length=255)
    monto_total: Decimal = Field(..., gt=0)
    moneda: str = Field(default="PEN", max_length=3)
    descripcion: str | None = Field(default=None)


class FacturaResponse(BaseModel):
    id: uuid.UUID
    numero: str
    proveedor: str
    monto_total: Decimal
    moneda: str
    descripcion: str | None
    estado: str

    model_config = {"from_attributes": True}


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(
    payload: FacturaCreate,
    db: AsyncSession = Depends(get_db),
) -> Factura:
    existing = await db.execute(
        select(Factura).where(Factura.numero == payload.numero)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una factura con el numero {payload.numero}",
        )

    factura = Factura(**payload.model_dump())
    db.add(factura)
    await db.flush()
    await db.refresh(factura)
    return factura


@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura(
    factura_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Factura:
    result = await db.execute(select(Factura).where(Factura.id == factura_id))
    factura = result.scalar_one_or_none()
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada",
        )
    return factura
