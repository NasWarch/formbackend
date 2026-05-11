from datetime import date, datetime, timezone
from sqlalchemy import String, Integer, Date, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipment.id"), nullable=False, index=True)
    control_date: Mapped[date] = mapped_column(Date, nullable=False)
    next_control_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    result: Mapped[str] = mapped_column(String(20), nullable=False)  # ok, issue, partial
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    document_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    equipment = relationship("Equipment", back_populates="maintenance_records")
