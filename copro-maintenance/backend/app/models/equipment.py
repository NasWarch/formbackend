from datetime import date, datetime, timezone
from sqlalchemy import String, Integer, Date, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey("buildings.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    equipment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # ascenseur, chaudière, extincteur, porte, gaz, électricité, autre
    serial_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    installation_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_control_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_control_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ok", server_default="ok")  # ok, pending, overdue
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    building = relationship("Building", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="equipment", cascade="all, delete-orphan")
