from datetime import date, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.building import Building
from app.models.equipment import Equipment

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class DashboardSummary(BaseModel):
    total_buildings: int
    total_equipment: int
    equipment_ok: int
    equipment_pending: int
    equipment_overdue: int
    upcoming_controls: list["UpcomingControl"]


class UpcomingControl(BaseModel):
    equipment_id: int
    equipment_name: str
    equipment_type: str
    building_name: str
    next_control_date: str | None


@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Total buildings for user
    building_count_result = await db.execute(
        select(func.count(Building.id)).where(Building.user_id == current_user.id)
    )
    total_buildings = building_count_result.scalar() or 0

    # Equipment stats for user's buildings
    # Get all equipment for user's buildings
    eq_result = await db.execute(
        select(Equipment)
        .join(Building, Equipment.building_id == Building.id)
        .where(Building.user_id == current_user.id)
    )
    all_equipment = eq_result.scalars().all()

    total_equipment = len(all_equipment)
    equipment_ok = sum(1 for e in all_equipment if e.status == "ok")
    equipment_pending = sum(1 for e in all_equipment if e.status == "pending")
    equipment_overdue = sum(1 for e in all_equipment if e.status == "overdue")

    # Upcoming controls (next 30 days)
    today = date.today()
    cutoff = today + timedelta(days=30)
    upcoming = []
    for e in all_equipment:
        if e.next_control_date and today <= e.next_control_date <= cutoff:
            upcoming.append(
                UpcomingControl(
                    equipment_id=e.id,
                    equipment_name=e.name,
                    equipment_type=e.equipment_type,
                    building_name=e.building.name if e.building else "",
                    next_control_date=e.next_control_date.isoformat(),
                )
            )

    # Sort by next_control_date
    upcoming.sort(key=lambda x: x.next_control_date or "")

    return DashboardSummary(
        total_buildings=total_buildings,
        total_equipment=total_equipment,
        equipment_ok=equipment_ok,
        equipment_pending=equipment_pending,
        equipment_overdue=equipment_overdue,
        upcoming_controls=upcoming,
    )
