from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
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

router = APIRouter(prefix="/equipment", tags=["equipment"])


class EquipmentCreate(BaseModel):
    building_id: int
    name: str
    equipment_type: str
    serial_number: str | None = None
    installation_date: date | None = None
    last_control_date: date | None = None
    next_control_date: date | None = None
    status: str = "ok"
    notes: str | None = None


class EquipmentUpdate(BaseModel):
    name: str | None = None
    equipment_type: str | None = None
    serial_number: str | None = None
    installation_date: date | None = None
    last_control_date: date | None = None
    next_control_date: date | None = None
    status: str | None = None
    notes: str | None = None


class EquipmentResponse(BaseModel):
    id: int
    building_id: int
    building_name: str
    name: str
    equipment_type: str
    serial_number: str | None
    installation_date: str | None
    last_control_date: str | None
    next_control_date: str | None
    status: str
    notes: str | None
    created_at: str

    model_config = {"from_attributes": True}


class MaintenanceRecordBrief(BaseModel):
    id: int
    control_date: str
    next_control_date: str | None
    provider_name: str
    provider_phone: str | None
    result: str
    notes: str | None
    created_at: str

    model_config = {"from_attributes": True}


class EquipmentDetailResponse(BaseModel):
    id: int
    building_id: int
    building_name: str
    name: str
    equipment_type: str
    serial_number: str | None
    installation_date: str | None
    last_control_date: str | None
    next_control_date: str | None
    status: str
    notes: str | None
    created_at: str
    maintenance_history: list[MaintenanceRecordBrief] = []

    model_config = {"from_attributes": True}


async def _verify_building_ownership(building_id: int, user_id: int, db: AsyncSession) -> Building:
    """Verify the building belongs to the current user."""
    result = await db.execute(
        select(Building).where(Building.id == building_id, Building.user_id == user_id)
    )
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
    return building


async def _build_equipment_response(equipment: Equipment) -> EquipmentResponse:
    """Convert Equipment ORM object to response with building_name."""
    return EquipmentResponse(
        id=equipment.id,
        building_id=equipment.building_id,
        building_name=equipment.building.name if equipment.building else "",
        name=equipment.name,
        equipment_type=equipment.equipment_type,
        serial_number=equipment.serial_number,
        installation_date=equipment.installation_date.isoformat() if equipment.installation_date else None,
        last_control_date=equipment.last_control_date.isoformat() if equipment.last_control_date else None,
        next_control_date=equipment.next_control_date.isoformat() if equipment.next_control_date else None,
        status=equipment.status,
        notes=equipment.notes,
        created_at=equipment.created_at.isoformat() if equipment.created_at else "",
    )


@router.get("", response_model=list[EquipmentResponse])
async def list_equipment(
    building_id: int | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify building ownership if filtered
    if building_id is not None:
        await _verify_building_ownership(building_id, current_user.id, db)
        query = (
            select(Equipment)
            .where(Equipment.building_id == building_id)
            .options(selectinload(Equipment.building))
        )
    else:
        # Get all equipment for buildings owned by user
        query = (
            select(Equipment)
            .join(Building, Equipment.building_id == Building.id)
            .where(Building.user_id == current_user.id)
            .options(selectinload(Equipment.building))
        )

    result = await db.execute(query)
    equipment_list = result.scalars().all()

    return [await _build_equipment_response(e) for e in equipment_list]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EquipmentResponse)
async def create_equipment(
    body: EquipmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _verify_building_ownership(body.building_id, current_user.id, db)

    equipment = Equipment(
        building_id=body.building_id,
        name=body.name,
        equipment_type=body.equipment_type,
        serial_number=body.serial_number,
        installation_date=body.installation_date,
        last_control_date=body.last_control_date,
        next_control_date=body.next_control_date,
        status=body.status,
        notes=body.notes,
    )
    db.add(equipment)
    await db.commit()
    await db.refresh(equipment)

    # Reload with building relationship
    result = await db.execute(
        select(Equipment).where(Equipment.id == equipment.id).options(selectinload(Equipment.building))
    )
    equipment = result.scalar_one()
    return await _build_equipment_response(equipment)


@router.get("/{equipment_id}", response_model=EquipmentDetailResponse)
async def get_equipment(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Equipment)
        .join(Building, Equipment.building_id == Building.id)
        .where(Equipment.id == equipment_id, Building.user_id == current_user.id)
        .options(selectinload(Equipment.building), selectinload(Equipment.maintenance_records))
    )
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    records = [
        MaintenanceRecordBrief(
            id=r.id,
            control_date=r.control_date.isoformat() if r.control_date else "",
            next_control_date=r.next_control_date.isoformat() if r.next_control_date else None,
            provider_name=r.provider_name,
            provider_phone=r.provider_phone,
            result=r.result,
            notes=r.notes,
            created_at=r.created_at.isoformat() if r.created_at else "",
        )
        for r in sorted(equipment.maintenance_records, key=lambda x: x.control_date, reverse=True)
    ]

    return EquipmentDetailResponse(
        id=equipment.id,
        building_id=equipment.building_id,
        building_name=equipment.building.name if equipment.building else "",
        name=equipment.name,
        equipment_type=equipment.equipment_type,
        serial_number=equipment.serial_number,
        installation_date=equipment.installation_date.isoformat() if equipment.installation_date else None,
        last_control_date=equipment.last_control_date.isoformat() if equipment.last_control_date else None,
        next_control_date=equipment.next_control_date.isoformat() if equipment.next_control_date else None,
        status=equipment.status,
        notes=equipment.notes,
        created_at=equipment.created_at.isoformat() if equipment.created_at else "",
        maintenance_history=records,
    )


@router.put("/{equipment_id}", response_model=EquipmentResponse)
async def update_equipment(
    equipment_id: int,
    body: EquipmentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Equipment)
        .join(Building, Equipment.building_id == Building.id)
        .where(Equipment.id == equipment_id, Building.user_id == current_user.id)
        .options(selectinload(Equipment.building))
    )
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(equipment, key, value)

    await db.commit()
    await db.refresh(equipment)

    return await _build_equipment_response(equipment)


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Equipment)
        .join(Building, Equipment.building_id == Building.id)
        .where(Equipment.id == equipment_id, Building.user_id == current_user.id)
    )
    equipment = result.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")

    await db.delete(equipment)
    await db.commit()
    return None
