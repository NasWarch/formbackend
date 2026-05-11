"""Form and Submission models — core entities for the Form Backend API."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from app.core.database import Base


class Form(Base):
    """A form configuration owned by a user."""

    __tablename__ = "forms"
    __table_args__ = (
        UniqueConstraint("user_id", "slug", name="uq_form_user_slug"),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    submission_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="forms")
    submissions = relationship("Submission", back_populates="form", cascade="all, delete-orphan")


class Submission(Base):
    """A form submission containing form data."""

    __tablename__ = "submissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    form_id = Column(String, ForeignKey("forms.id"), nullable=False, index=True)
    data = Column(JSONB, nullable=False, default=dict)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    form = relationship("Form", back_populates="submissions")


@listens_for(Submission, "after_insert")
def increment_submission_count(mapper, connection, target):
    """Auto-increment form.submission_count when a new submission is created."""
    from sqlalchemy import update
    connection.execute(
        update(Form).where(Form.id == target.form_id).values(
            submission_count=Form.submission_count + 1
        )
    )
