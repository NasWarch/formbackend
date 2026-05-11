from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.building import Building
from app.models.equipment import Equipment
from app.models.maintenance_record import MaintenanceRecord

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


class MaintenanceCreateRequest(BaseModel):
    equipment_id: int
    control_date: date
    next_control_date: date | None = None
    provider_name: str
    provider_phone: str | None = None
    result: str  # ok, issue, partial
    notes: str | None = None
    document_id: int | None = None


class MaintenanceRecordResponse(BaseModel):
    id: int
    equipment_id: int
    control_date: str
    next_control_date: str | None
    provider_name: str
    provider_phone: str | None
    result: str
    notes: str | None
    document_id: int | None
    created_at: str

    model_config = {"from_attributes": True}


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MaintenanceRecordResponse)
async def add_maintenance_record(
    body: MaintenanceCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify equipment belongs to user's building
    result = await db.execute(
        select(Equipment)
        .join(Building, Equipment.building_id == Building.id)
        .where(Equipment.id == body.equipment_id, Building.user_id == current_user.id)
    )
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    # Create maintenance record
    record = MaintenanceRecord(
        equipment_id=body.equipment_id,
        control_date=body.control_date,
        next_control_date=body.next_control_date,
        provider_name=body.provider_name,
        provider_phone=body.provider_phone,
        result=body.result,
        notes=body.notes,
        document_id=body.document_id,
    )
    db.add(record)

    # Update equipment's last_control_date and next_control_date
    equipment.last_control_date = body.control_date
    if body.next_control_date:
        equipment.next_control_date = body.next_control_date

    await db.commit()
    await db.refresh(record)

    return MaintenanceRecordResponse(
        id=record.id,
        equipment_id=record.equipment_id,
        control_date=record.control_date.isoformat() if record.control_date else "",
        next_control_date=record.next_control_date.isoformat() if record.next_control_date else None,
        provider_name=record.provider_name,
        provider_phone=record.provider_phone,
        result=record.result,
        notes=record.notes,
        document_id=record.document_id,
        created_at=record.created_at.isoformat() if record.created_at else "",
    )


# GET /api/equipment/{id}/records — mounted under equipment router but we also expose it here
records_router = APIRouter(tags=["maintenance-records"])


@records_router.get("/equipment/{equipment_id}/records", response_model=list[MaintenanceRecordResponse])
async def get_equipment_records(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify equipment belongs to user
    result = await db.execute(
        select(Equipment)
        .join(Building, Equipment.building_id == Building.id)
        .where(Equipment.id == equipment_id, Building.user_id == current_user.id)
    )
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    records_result = await db.execute(
        select(MaintenanceRecord)
        .where(MaintenanceRecord.equipment_id == equipment_id)
        .order_by(MaintenanceRecord.control_date.desc())
    )
    records = records_result.scalars().all()

    return [
        MaintenanceRecordResponse(
            id=r.id,
            equipment_id=r.equipment_id,
            control_date=r.control_date.isoformat() if r.control_date else "",
            next_control_date=r.next_control_date.isoformat() if r.next_control_date else None,
            provider_name=r.provider_name,
            provider_phone=r.provider_phone,
            result=r.result,
            notes=r.notes,
            document_id=r.document_id,
            created_at=r.created_at.isoformat() if r.created_at else "",
        )
        for r in records
    ]
