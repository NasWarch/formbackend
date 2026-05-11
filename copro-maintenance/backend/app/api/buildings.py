from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.building import Building
from app.models.equipment import Equipment

router = APIRouter(prefix="/buildings", tags=["buildings"])


class BuildingCreate(BaseModel):
    name: str
    address: str
    city: str
    postal_code: str
    nb_lots: int = 0


class BuildingUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    nb_lots: int | None = None


class BuildingResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    postal_code: str
    nb_lots: int
    equipment_count: int = 0
    created_at: str

    model_config = {"from_attributes": True}


class BuildingDetailResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    postal_code: str
    nb_lots: int
    created_at: str
    equipment: list["EquipmentBrief"] = []

    model_config = {"from_attributes": True}


class EquipmentBrief(BaseModel):
    id: int
    name: str
    equipment_type: str
    status: str
    next_control_date: str | None

    model_config = {"from_attributes": True}


@router.get("", response_model=list[BuildingResponse])
async def list_buildings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Building).where(Building.user_id == current_user.id)
    )
    buildings = result.scalars().all()

    # Get equipment counts in one query
    output = []
    for b in buildings:
        count_result = await db.execute(
            select(func.count(Equipment.id)).where(Equipment.building_id == b.id)
        )
        eq_count = count_result.scalar() or 0
        output.append(
            BuildingResponse(
                id=b.id,
                name=b.name,
                address=b.address,
                city=b.city,
                postal_code=b.postal_code,
                nb_lots=b.nb_lots,
                equipment_count=eq_count,
                created_at=b.created_at.isoformat() if b.created_at else "",
            )
        )
    return output


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BuildingResponse)
async def create_building(
    body: BuildingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    building = Building(
        user_id=current_user.id,
        name=body.name,
        address=body.address,
        city=body.city,
        postal_code=body.postal_code,
        nb_lots=body.nb_lots,
    )
    db.add(building)
    await db.commit()
    await db.refresh(building)

    return BuildingResponse(
        id=building.id,
        name=building.name,
        address=building.address,
        city=building.city,
        postal_code=building.postal_code,
        nb_lots=building.nb_lots,
        equipment_count=0,
        created_at=building.created_at.isoformat() if building.created_at else "",
    )


@router.get("/{building_id}", response_model=BuildingDetailResponse)
async def get_building(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Building)
        .where(Building.id == building_id, Building.user_id == current_user.id)
        .options(selectinload(Building.equipment))
    )
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")

    equipment_list = [
        EquipmentBrief(
            id=e.id,
            name=e.name,
            equipment_type=e.equipment_type,
            status=e.status,
            next_control_date=e.next_control_date.isoformat() if e.next_control_date else None,
        )
        for e in building.equipment
    ]

    return BuildingDetailResponse(
        id=building.id,
        name=building.name,
        address=building.address,
        city=building.city,
        postal_code=building.postal_code,
        nb_lots=building.nb_lots,
        created_at=building.created_at.isoformat() if building.created_at else "",
        equipment=equipment_list,
    )


@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: int,
    body: BuildingUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Building).where(
            Building.id == building_id, Building.user_id == current_user.id
        )
    )
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(building, key, value)

    await db.commit()
    await db.refresh(building)

    count_result = await db.execute(
        select(func.count(Equipment.id)).where(Equipment.building_id == building.id)
    )
    eq_count = count_result.scalar() or 0

    return BuildingResponse(
        id=building.id,
        name=building.name,
        address=building.address,
        city=building.city,
        postal_code=building.postal_code,
        nb_lots=building.nb_lots,
        equipment_count=eq_count,
        created_at=building.created_at.isoformat() if building.created_at else "",
    )


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Building).where(
            Building.id == building_id, Building.user_id == current_user.id
        )
    )
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")

    await db.delete(building)
    await db.commit()
    return None
